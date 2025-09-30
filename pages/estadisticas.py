import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.auth import require_auth, get_current_user
from database.database import db

def show_estadisticas_page():
    """Muestra la página de estadísticas"""
    require_auth()
    
    user = get_current_user()
    st.title("📊 Estadísticas y Análisis")
    
    # Obtener materias del profesor
    materias = db.get_profesor_materias(user['id'])
    
    if not materias:
        st.warning("No tienes materias asignadas.")
        return
    
    # Selector de materia
    materia_options = {f"{m['nombre']} ({m['codigo']})": m for m in materias}
    
    # Si hay una materia seleccionada desde el dashboard, usarla
    selected_materia_id = st.session_state.get('selected_materia', None)
    default_index = 0
    
    if selected_materia_id:
        for i, materia in enumerate(materias):
            if materia['id'] == selected_materia_id:
                default_index = i
                break
    
    selected_materia_name = st.selectbox(
        "Selecciona una materia:",
        options=list(materia_options.keys()),
        index=default_index
    )
    
    selected_materia = materia_options[selected_materia_name]
    
    # Limpiar la selección del session state
    if 'selected_materia' in st.session_state:
        del st.session_state.selected_materia
    
    st.subheader(f"Estadísticas de: {selected_materia['nombre']}")
    st.write(f"**Código:** {selected_materia['codigo']} | **Grupo:** {selected_materia['grupo']}")
    
    # Obtener datos de estudiantes
    estudiantes = db.get_estudiantes_materia(selected_materia['id'], user['id'])
    
    if not estudiantes:
        st.warning("No hay estudiantes inscritos en esta materia.")
        return
    
    # Tabs para diferentes tipos de estadísticas
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Resumen General", "📊 Distribuciones", "📉 Análisis Comparativo", "🎯 Rendimiento"])
    
    with tab1:
        show_general_summary(estudiantes)
    
    with tab2:
        show_distributions(estudiantes)
    
    with tab3:
        show_comparative_analysis(estudiantes)
    
    with tab4:
        show_performance_analysis(estudiantes)

def show_general_summary(estudiantes):
    """Muestra el resumen general de estadísticas"""
    st.subheader("📈 Resumen General")
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Estudiantes", len(estudiantes))
    
    # Calcular estadísticas generales
    calificaciones_finales = [est['calificacion_final'] for est in estudiantes if est['calificacion_final'] is not None]
    
    with col2:
        if calificaciones_finales:
            promedio = sum(calificaciones_finales) / len(calificaciones_finales)
            st.metric("Promedio General", f"{promedio:.2f}")
        else:
            st.metric("Promedio General", "N/A")
    
    with col3:
        aprobados = len([cal for cal in calificaciones_finales if cal >= 6.0])
        st.metric("Estudiantes Aprobados", aprobados)
    
    with col4:
        if len(estudiantes) > 0:
            porcentaje_aprobados = (aprobados / len(estudiantes)) * 100
            st.metric("% de Aprobación", f"{porcentaje_aprobados:.1f}%")
        else:
            st.metric("% de Aprobación", "N/A")
    
    # Estadísticas detalladas por evaluación
    st.subheader("📊 Estadísticas por Evaluación")
    
    evaluaciones = ['parcial_1', 'parcial_2', 'parcial_3', 'ordinario', 'calificacion_final']
    nombres_eval = ['Parcial 1', 'Parcial 2', 'Parcial 3', 'Ordinario', 'Calificación Final']
    
    stats_data = []
    for eval_key, eval_name in zip(evaluaciones, nombres_eval):
        calificaciones = [est[eval_key] for est in estudiantes if est[eval_key] is not None]
        
        if calificaciones:
            stats_data.append({
                'Evaluación': eval_name,
                'Estudiantes': len(calificaciones),
                'Promedio': round(sum(calificaciones) / len(calificaciones), 2),
                'Mínima': min(calificaciones),
                'Máxima': max(calificaciones),
                'Aprobados': len([cal for cal in calificaciones if cal >= 6.0]),
                '% Aprobación': round((len([cal for cal in calificaciones if cal >= 6.0]) / len(calificaciones)) * 100, 1)
            })
        else:
            stats_data.append({
                'Evaluación': eval_name,
                'Estudiantes': 0,
                'Promedio': 'N/A',
                'Mínima': 'N/A',
                'Máxima': 'N/A',
                'Aprobados': 0,
                '% Aprobación': 'N/A'
            })
    
    df_stats = pd.DataFrame(stats_data)
    st.dataframe(df_stats, use_container_width=True, hide_index=True)

def show_distributions(estudiantes):
    """Muestra las distribuciones de calificaciones"""
    st.subheader("📊 Distribución de Calificaciones")
    
    # Crear datos para gráficos
    evaluaciones = ['parcial_1', 'parcial_2', 'parcial_3', 'ordinario', 'calificacion_final']
    nombres_eval = ['Parcial 1', 'Parcial 2', 'Parcial 3', 'Ordinario', 'Calificación Final']
    
    # Gráfico de histogramas
    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=nombres_eval,
        specs=[[{"type": "histogram"}, {"type": "histogram"}, {"type": "histogram"}],
               [{"type": "histogram"}, {"type": "histogram"}, None]]
    )
    
    positions = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2)]
    
    for i, (eval_key, eval_name) in enumerate(zip(evaluaciones, nombres_eval)):
        calificaciones = [est[eval_key] for est in estudiantes if est[eval_key] is not None]
        
        if calificaciones:
            row, col = positions[i]
            fig.add_trace(
                go.Histogram(
                    x=calificaciones,
                    nbinsx=10,
                    name=eval_name,
                    showlegend=False
                ),
                row=row, col=col
            )
    
    fig.update_layout(
        height=600,
        title_text="Distribución de Calificaciones por Evaluación",
        showlegend=False
    )
    
    fig.update_xaxes(title_text="Calificación", range=[0, 10])
    fig.update_yaxes(title_text="Frecuencia")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico de barras por rangos
    st.subheader("📈 Distribución por Rangos de Calificación")
    
    calificaciones_finales = [est['calificacion_final'] for est in estudiantes if est['calificacion_final'] is not None]
    
    if calificaciones_finales:
        rangos = {
            "Excelente (10.0)": 0,
            "Muy Bien (9.0-9.9)": 0,
            "Bien (8.0-8.9)": 0,
            "Regular (7.0-7.9)": 0,
            "Suficiente (6.0-6.9)": 0,
            "Reprobado (< 6.0)": 0
        }
        
        for cal in calificaciones_finales:
            if cal == 10.0:
                rangos["Excelente (10.0)"] += 1
            elif cal >= 9.0:
                rangos["Muy Bien (9.0-9.9)"] += 1
            elif cal >= 8.0:
                rangos["Bien (8.0-8.9)"] += 1
            elif cal >= 7.0:
                rangos["Regular (7.0-7.9)"] += 1
            elif cal >= 6.0:
                rangos["Suficiente (6.0-6.9)"] += 1
            else:
                rangos["Reprobado (< 6.0)"] += 1
        
        # Crear gráfico de barras
        fig_bar = px.bar(
            x=list(rangos.keys()),
            y=list(rangos.values()),
            title="Distribución por Rangos de Calificación Final",
            labels={'x': 'Rango de Calificación', 'y': 'Número de Estudiantes'},
            color=list(rangos.values()),
            color_continuous_scale='RdYlGn'
        )
        
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

def show_comparative_analysis(estudiantes):
    """Muestra análisis comparativo entre evaluaciones"""
    st.subheader("📉 Análisis Comparativo")
    
    # Crear DataFrame para análisis
    data_for_comparison = []
    for est in estudiantes:
        if all(est[key] is not None for key in ['parcial_1', 'parcial_2', 'parcial_3', 'ordinario']):
            data_for_comparison.append({
                'Estudiante': f"{est['apellido_paterno']} {est['nombre']}",
                'Parcial 1': est['parcial_1'],
                'Parcial 2': est['parcial_2'],
                'Parcial 3': est['parcial_3'],
                'Ordinario': est['ordinario'],
                'Final': est['calificacion_final']
            })
    
    if not data_for_comparison:
        st.warning("No hay suficientes datos para realizar el análisis comparativo.")
        return
    
    df_comparison = pd.DataFrame(data_for_comparison)
    
    # Gráfico de líneas para mostrar evolución
    st.subheader("📈 Evolución de Calificaciones por Estudiante")
    
    # Seleccionar algunos estudiantes para mostrar (máximo 10)
    estudiantes_muestra = df_comparison.head(10)
    
    fig_lines = go.Figure()
    
    for _, row in estudiantes_muestra.iterrows():
        fig_lines.add_trace(go.Scatter(
            x=['Parcial 1', 'Parcial 2', 'Parcial 3', 'Ordinario'],
            y=[row['Parcial 1'], row['Parcial 2'], row['Parcial 3'], row['Ordinario']],
            mode='lines+markers',
            name=row['Estudiante'],
            line=dict(width=2),
            marker=dict(size=6)
        ))
    
    fig_lines.update_layout(
        title="Evolución de Calificaciones (Primeros 10 estudiantes)",
        xaxis_title="Evaluación",
        yaxis_title="Calificación",
        yaxis=dict(range=[0, 10]),
        height=500
    )
    
    st.plotly_chart(fig_lines, use_container_width=True)
    
    # Gráfico de caja (box plot) para comparar distribuciones
    st.subheader("📦 Comparación de Distribuciones")
    
    # Preparar datos para box plot
    box_data = []
    evaluaciones = ['Parcial 1', 'Parcial 2', 'Parcial 3', 'Ordinario']
    
    for eval_name in evaluaciones:
        for _, row in df_comparison.iterrows():
            box_data.append({
                'Evaluación': eval_name,
                'Calificación': row[eval_name]
            })
    
    df_box = pd.DataFrame(box_data)
    
    fig_box = px.box(
        df_box,
        x='Evaluación',
        y='Calificación',
        title="Distribución de Calificaciones por Evaluación",
        points="outliers"
    )
    
    fig_box.update_layout(height=400)
    st.plotly_chart(fig_box, use_container_width=True)
    
    # Correlaciones entre evaluaciones
    st.subheader("🔗 Correlaciones entre Evaluaciones")
    
    correlation_data = df_comparison[['Parcial 1', 'Parcial 2', 'Parcial 3', 'Ordinario', 'Final']].corr()
    
    fig_corr = px.imshow(
        correlation_data,
        title="Matriz de Correlación entre Evaluaciones",
        color_continuous_scale='RdBu',
        aspect="auto"
    )
    
    st.plotly_chart(fig_corr, use_container_width=True)

def show_performance_analysis(estudiantes):
    """Muestra análisis de rendimiento"""
    st.subheader("🎯 Análisis de Rendimiento")
    
    # Análisis de estudiantes en riesgo
    st.subheader("⚠️ Estudiantes en Riesgo")
    
    estudiantes_riesgo = []
    for est in estudiantes:
        # Criterios de riesgo: promedio de parciales < 6.0 o calificación final < 6.0
        parciales = [est['parcial_1'], est['parcial_2'], est['parcial_3']]
        parciales_validos = [p for p in parciales if p is not None]
        
        if parciales_validos:
            promedio_parciales = sum(parciales_validos) / len(parciales_validos)
            
            en_riesgo = False
            razon = []
            
            if promedio_parciales < 6.0:
                en_riesgo = True
                razon.append(f"Promedio parciales: {promedio_parciales:.1f}")
            
            if est['calificacion_final'] is not None and est['calificacion_final'] < 6.0:
                en_riesgo = True
                razon.append(f"Calificación final: {est['calificacion_final']:.1f}")
            
            if en_riesgo:
                estudiantes_riesgo.append({
                    'Clave': est['clave'],
                    'Nombre': f"{est['apellido_paterno']} {est['apellido_materno']} {est['nombre']}",
                    'Promedio Parciales': f"{promedio_parciales:.1f}",
                    'Calificación Final': est['calificacion_final'] if est['calificacion_final'] is not None else 'N/A',
                    'Razón': '; '.join(razon)
                })
    
    if estudiantes_riesgo:
        df_riesgo = pd.DataFrame(estudiantes_riesgo)
        st.dataframe(df_riesgo, use_container_width=True, hide_index=True)
        st.warning(f"Se identificaron {len(estudiantes_riesgo)} estudiantes en riesgo de reprobar.")
    else:
        st.success("No se identificaron estudiantes en riesgo inmediato.")
    
    # Análisis de mejores estudiantes
    st.subheader("🏆 Estudiantes Destacados")
    
    estudiantes_destacados = []
    for est in estudiantes:
        if est['calificacion_final'] is not None and est['calificacion_final'] >= 9.0:
            estudiantes_destacados.append({
                'Clave': est['clave'],
                'Nombre': f"{est['apellido_paterno']} {est['apellido_materno']} {est['nombre']}",
                'Parcial 1': est['parcial_1'] if est['parcial_1'] is not None else 'N/A',
                'Parcial 2': est['parcial_2'] if est['parcial_2'] is not None else 'N/A',
                'Parcial 3': est['parcial_3'] if est['parcial_3'] is not None else 'N/A',
                'Ordinario': est['ordinario'] if est['ordinario'] is not None else 'N/A',
                'Calificación Final': est['calificacion_final']
            })
    
    if estudiantes_destacados:
        # Ordenar por calificación final descendente
        estudiantes_destacados.sort(key=lambda x: x['Calificación Final'], reverse=True)
        df_destacados = pd.DataFrame(estudiantes_destacados)
        st.dataframe(df_destacados, use_container_width=True, hide_index=True)
        st.success(f"¡{len(estudiantes_destacados)} estudiantes han obtenido calificaciones excelentes (≥9.0)!")
    else:
        st.info("No hay estudiantes con calificaciones excelentes (≥9.0) aún.")
    
    # Recomendaciones
    st.subheader("💡 Recomendaciones")
    
    calificaciones_finales = [est['calificacion_final'] for est in estudiantes if est['calificacion_final'] is not None]
    
    if calificaciones_finales:
        promedio_general = sum(calificaciones_finales) / len(calificaciones_finales)
        porcentaje_aprobados = (len([cal for cal in calificaciones_finales if cal >= 6.0]) / len(calificaciones_finales)) * 100
        
        recomendaciones = []
        
        if promedio_general < 7.0:
            recomendaciones.append("📚 Considerar reforzar los temas más difíciles con sesiones adicionales")
        
        if porcentaje_aprobados < 70:
            recomendaciones.append("⚠️ El porcentaje de aprobación es bajo, revisar metodología de enseñanza")
        
        if len(estudiantes_riesgo) > len(estudiantes) * 0.3:
            recomendaciones.append("🆘 Más del 30% de estudiantes están en riesgo, implementar estrategias de apoyo")
        
        if not estudiantes_destacados:
            recomendaciones.append("🎯 Implementar actividades para motivar la excelencia académica")
        
        if promedio_general >= 8.0 and porcentaje_aprobados >= 80:
            recomendaciones.append("🎉 ¡Excelente rendimiento del grupo! Continuar con la metodología actual")
        
        if recomendaciones:
            for rec in recomendaciones:
                st.info(rec)
        else:
            st.success("El rendimiento del grupo está dentro de los parámetros normales.")

if __name__ == "__main__":
    show_estadisticas_page()