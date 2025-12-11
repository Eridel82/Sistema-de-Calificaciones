import streamlit as st
import os
from utils.auth import require_auth, get_current_user
from utils.pdf_generator import PDFGenerator
from database.database import db

# Crear instancia del generador de PDF con el logo
# El logo debe estar en la carpeta raíz o especifica la ruta completa
pdf_generator = PDFGenerator(logo_path='logo.png')

def show_reportes_page():
    """Muestra la página de generación de reportes"""
    require_auth()
    
    user = get_current_user()
    st.title("📄 Generación de Reportes PDF")
    
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
    
    st.subheader(f"Reportes para: {selected_materia['nombre']}")
    st.write(f"**Código:** {selected_materia['codigo']} | **Grupo:** {selected_materia['grupo']}")
    
    # Obtener estudiantes para verificar que hay datos
    estudiantes = db.get_estudiantes_materia(selected_materia['id'], user['id'])
    
    if not estudiantes:
        st.warning("No hay estudiantes inscritos en esta materia.")
        return
    
    # Información sobre los reportes
    st.info("""
    **Tipos de Reportes Disponibles:**
    - **Parcial 1, 2, 3:** Reportes individuales de cada parcial con espacio para firmas
    - **Ordinario:** Reporte del examen ordinario
    - **Calificación Final:** Reporte completo con todas las calificaciones
    
    Todos los reportes incluyen información del profesor, materia y espacios para firmas.
    """)
    
    # Crear columnas para los botones de reportes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📝 Reportes Parciales")
        
        if st.button("📊 Generar Reporte Parcial 1", use_container_width=True):
            generate_report(user, selected_materia, estudiantes, "Parcial 1")
        
        if st.button("📊 Generar Reporte Parcial 2", use_container_width=True):
            generate_report(user, selected_materia, estudiantes, "Parcial 2")
        
        if st.button("📊 Generar Reporte Parcial 3", use_container_width=True):
            generate_report(user, selected_materia, estudiantes, "Parcial 3")
    
    with col2:
        st.subheader("🎯 Reporte Ordinario")
        
        if st.button("📊 Generar Reporte Ordinario", use_container_width=True):
            generate_report(user, selected_materia, estudiantes, "Ordinario")
    
    with col3:
        st.subheader("🏆 Reporte Final")
        
        if st.button("📊 Generar Reporte Final", use_container_width=True):
            generate_report(user, selected_materia, estudiantes, "Calificación Final")
    
    # Mostrar estadísticas de la materia
    st.markdown("---")
    st.subheader("📈 Estadísticas de la Materia")
    
    show_materia_statistics(estudiantes)
    
    # Información sobre fechas del calendario académico
    st.markdown("---")
    st.subheader("📅 Fechas Importantes del Calendario")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Exámenes Parciales 2025-2026A:**
        - **1er Parcial:** 19-24 de septiembre de 2025
        - **2do Parcial:** 22-29 de octubre de 2025
        - **3er Parcial:** 26 nov - 03 dic de 2025
        """)
    
    with col2:
        st.markdown("""
        **Exámenes Ordinarios:**
        - **Ordinarios:** 08-15 de diciembre de 2025
        
        **Fecha límite de entrega:** 
        Tercer día hábil posterior al examen
        """)

def generate_report(profesor_info, materia_info, estudiantes_data, tipo_reporte):
    """Genera un reporte PDF específico"""
    try:
        with st.spinner(f"Generando reporte {tipo_reporte}..."):
            # Crear directorio de reportes si no existe
            reports_dir = "reports"
            os.makedirs(reports_dir, exist_ok=True)
            
            # Generar nombre del archivo
            filename = f"{tipo_reporte.replace(' ', '_').lower()}_{materia_info['codigo']}_{profesor_info['clave']}.pdf"
            output_path = os.path.join(reports_dir, filename)
            
            # Generar el PDF
            pdf_path = pdf_generator.generate_report(
                profesor_info, 
                materia_info, 
                estudiantes_data, 
                tipo_reporte, 
                output_path
            )
            
            st.success(f"¡Reporte {tipo_reporte} generado exitosamente!")
            
            # Leer el archivo PDF para descarga
            with open(pdf_path, "rb") as pdf_file:
                pdf_data = pdf_file.read()
            
            st.download_button(
                label=f"📥 Descargar Reporte {tipo_reporte}",
                data=pdf_data,
                file_name=filename,
                mime="application/pdf",
                type="primary"
            )
            
            # Mostrar información del archivo generado
            st.info(f"**Archivo generado:** {filename}")
            
    except Exception as e:
        st.error(f"Error al generar el reporte: {str(e)}")

def show_materia_statistics(estudiantes):
    """Muestra estadísticas detalladas de la materia"""
    
    # Métricas generales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Estudiantes", len(estudiantes))
    
    # Calcular estadísticas
    calificaciones_finales = [est['calificacion_final'] for est in estudiantes if est['calificacion_final'] is not None]
    
    with col2:
        if calificaciones_finales:
            promedio = sum(calificaciones_finales) / len(calificaciones_finales)
            st.metric("Promedio General", f"{promedio:.2f}")
        else:
            st.metric("Promedio General", "N/A")
    
    with col3:
        aprobados = len([cal for cal in calificaciones_finales if cal >= 6.0])
        st.metric("Aprobados", aprobados)
    
    with col4:
        if len(estudiantes) > 0:
            porcentaje_aprobados = (aprobados / len(estudiantes)) * 100
            st.metric("% Aprobación", f"{porcentaje_aprobados:.1f}%")
        else:
            st.metric("% Aprobación", "N/A")
    
    # Distribución por parciales
    if calificaciones_finales:
        st.subheader("📊 Distribución de Calificaciones Finales")
        
        # Crear rangos
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
        
        # Mostrar en columnas
        cols = st.columns(3)
        for i, (rango, cantidad) in enumerate(rangos.items()):
            with cols[i % 3]:
                porcentaje = (cantidad / len(calificaciones_finales)) * 100 if calificaciones_finales else 0
                st.metric(rango, f"{cantidad} ({porcentaje:.1f}%)")
    
    # Estadísticas por parcial
    st.subheader("📈 Promedios por Evaluación")
    
    col1, col2, col3, col4 = st.columns(4)
    
    evaluaciones = ['parcial_1', 'parcial_2', 'parcial_3', 'ordinario']
    nombres_eval = ['Parcial 1', 'Parcial 2', 'Parcial 3', 'Ordinario']
    
    for i, (eval_key, eval_name) in enumerate(zip(evaluaciones, nombres_eval)):
        calificaciones_eval = [est[eval_key] for est in estudiantes if est[eval_key] is not None]
        
        with [col1, col2, col3, col4][i]:
            if calificaciones_eval:
                promedio_eval = sum(calificaciones_eval) / len(calificaciones_eval)
                st.metric(eval_name, f"{promedio_eval:.2f}")
            else:
                st.metric(eval_name, "N/A")

if __name__ == "__main__":
    show_reportes_page()
