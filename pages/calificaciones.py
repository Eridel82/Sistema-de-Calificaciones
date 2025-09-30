import streamlit as st
import pandas as pd
from utils.auth import require_auth, get_current_user
from utils.excel_handler import excel_handler
from database.database import db
import sqlite3

def show_calificaciones_page():
    """Muestra la página de gestión de calificaciones"""
    require_auth()
    
    user = get_current_user()
    st.title("📝 Gestión de Calificaciones")
    
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
    
    st.subheader(f"Materia: {selected_materia['nombre']}")
    st.write(f"**Código:** {selected_materia['codigo']} | **Grupo:** {selected_materia['grupo']} | **Semestre:** {selected_materia['semestre']}")
    
    # Tabs para diferentes funcionalidades
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Ver Calificaciones", "📤 Cargar desde Excel", "📥 Descargar Plantilla", "✏️ Editar Individual"])
    
    with tab1:
        show_grades_table(selected_materia, user['id'])
    
    with tab2:
        show_excel_upload(selected_materia, user['id'])
    
    with tab3:
        show_template_download(selected_materia, user['id'])
    
    with tab4:
        show_individual_edit(selected_materia, user['id'])

def show_grades_table(materia, profesor_id):
    """Muestra la tabla de calificaciones"""
    st.subheader("📊 Calificaciones Actuales")
    
    estudiantes = db.get_estudiantes_materia(materia['id'], profesor_id)
    
    if not estudiantes:
        st.info("No hay estudiantes inscritos en esta materia.")
        return
    
    # Crear DataFrame para mostrar
    data = []
    for est in estudiantes:
        data.append({
            'Clave': est['clave'],
            'Nombre': est['nombre'],
            'Apellido Paterno': est['apellido_paterno'],
            'Apellido Materno': est['apellido_materno'],
            'Parcial 1': est['parcial_1'] if est['parcial_1'] is not None else '-',
            'Parcial 2': est['parcial_2'] if est['parcial_2'] is not None else '-',
            'Parcial 3': est['parcial_3'] if est['parcial_3'] is not None else '-',
            'Ordinario': est['ordinario'] if est['ordinario'] is not None else '-',
            'Final': est['calificacion_final'] if est['calificacion_final'] is not None else '-'
        })
    
    df = pd.DataFrame(data)
    
    # Mostrar estadísticas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Estudiantes", len(estudiantes))
    
    with col2:
        calificaciones_finales = [est['calificacion_final'] for est in estudiantes if est['calificacion_final'] is not None]
        if calificaciones_finales:
            promedio = sum(calificaciones_finales) / len(calificaciones_finales)
            st.metric("Promedio General", f"{promedio:.2f}")
        else:
            st.metric("Promedio General", "N/A")
    
    with col3:
        aprobados = len([cal for cal in calificaciones_finales if cal >= 6.0])
        st.metric("Aprobados", aprobados)
    
    with col4:
        reprobados = len([cal for cal in calificaciones_finales if cal < 6.0])
        st.metric("Reprobados", reprobados)
    
    # Mostrar tabla
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Botón para exportar
    if st.button("📥 Exportar a Excel"):
        df_export, filename = excel_handler.export_grades_to_excel(materia['id'], profesor_id, materia['nombre'])
        if df_export is not None:
            csv = df_export.to_csv(index=False)
            st.download_button(
                label="Descargar archivo Excel",
                data=csv,
                file_name=filename.replace('.xlsx', '.csv'),
                mime='text/csv'
            )

def show_excel_upload(materia, profesor_id):
    """Muestra la sección de carga desde Excel"""
    st.subheader("📤 Cargar Calificaciones desde Excel")
    
    st.info("""
    **Instrucciones:**
    1. Descarga la plantilla desde la pestaña "Descargar Plantilla"
    2. Llena las calificaciones en el archivo Excel
    3. Sube el archivo completado aquí
    
    **Formato requerido:**
    - Las calificaciones deben estar entre 0 y 10
    - Puedes dejar celdas vacías para calificaciones no capturadas
    - No modifiques las columnas de clave_estudiante y nombre_completo
    """)
    
    uploaded_file = st.file_uploader(
        "Selecciona el archivo Excel con las calificaciones",
        type=['xlsx', 'xls'],
        help="Archivo Excel con el formato de la plantilla"
    )
    
    if uploaded_file is not None:
        try:
            # Mostrar preview del archivo
            df_preview = pd.read_excel(uploaded_file)
            st.subheader("Vista previa del archivo:")
            st.dataframe(df_preview.head(), use_container_width=True)
            
            if st.button("🚀 Procesar y Actualizar Calificaciones", type="primary"):
                with st.spinner("Procesando archivo..."):
                    success, message = excel_handler.process_excel_upload(uploaded_file, materia['id'], profesor_id)
                    
                    if success:
                        st.success(message)
                        st.balloons()
                        # Recargar la página para mostrar los cambios
                        st.rerun()
                    else:
                        st.error(message)
                        
        except Exception as e:
            st.error(f"Error al leer el archivo: {str(e)}")

def show_template_download(materia, profesor_id):
    """Muestra la sección de descarga de plantilla"""
    st.subheader("📥 Descargar Plantilla de Excel")
    
    st.info("""
    **La plantilla incluye:**
    - Lista de todos los estudiantes inscritos en la materia
    - Columnas para cada parcial y ordinario
    - Calificaciones actuales (si las hay)
    - Formato correcto para la carga masiva
    """)
    
    if st.button("📋 Generar Plantilla", type="primary"):
        with st.spinner("Generando plantilla..."):
            df_template = excel_handler.create_template(materia['id'], profesor_id)
            
            if df_template is not None:
                # Convertir a CSV para descarga
                csv = df_template.to_csv(index=False)
                filename = f"plantilla_calificaciones_{materia['codigo']}.csv"
                
                st.success("¡Plantilla generada exitosamente!")
                st.download_button(
                    label="📥 Descargar Plantilla",
                    data=csv,
                    file_name=filename,
                    mime='text/csv',
                    help="Descarga la plantilla y ábrela en Excel para llenar las calificaciones"
                )
                
                # Mostrar preview de la plantilla
                st.subheader("Vista previa de la plantilla:")
                st.dataframe(df_template.head(10), use_container_width=True)
                
            else:
                st.error("No se pudo generar la plantilla. Verifica que haya estudiantes inscritos.")

def show_individual_edit(materia, profesor_id):
    """Muestra la sección de edición individual"""
    st.subheader("✏️ Editar Calificaciones Individuales")
    
    estudiantes = db.get_estudiantes_materia(materia['id'], profesor_id)
    
    if not estudiantes:
        st.info("No hay estudiantes inscritos en esta materia.")
        return
    
    # Selector de estudiante
    estudiante_options = {f"{est['clave']} - {est['apellido_paterno']} {est['apellido_materno']} {est['nombre']}": est for est in estudiantes}
    
    selected_estudiante_name = st.selectbox(
        "Selecciona un estudiante:",
        options=list(estudiante_options.keys())
    )
    
    selected_estudiante = estudiante_options[selected_estudiante_name]
    
    # Formulario de edición
    with st.form("edit_grades_form"):
        st.write(f"**Editando calificaciones de:** {selected_estudiante['nombre']} {selected_estudiante['apellido_paterno']} {selected_estudiante['apellido_materno']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            parcial_1 = st.number_input(
                "Parcial 1",
                min_value=0.0,
                max_value=10.0,
                value=float(selected_estudiante['parcial_1']) if selected_estudiante['parcial_1'] is not None else 0.0,
                step=0.1,
                format="%.1f"
            )
            
            parcial_2 = st.number_input(
                "Parcial 2",
                min_value=0.0,
                max_value=10.0,
                value=float(selected_estudiante['parcial_2']) if selected_estudiante['parcial_2'] is not None else 0.0,
                step=0.1,
                format="%.1f"
            )
        
        with col2:
            parcial_3 = st.number_input(
                "Parcial 3",
                min_value=0.0,
                max_value=10.0,
                value=float(selected_estudiante['parcial_3']) if selected_estudiante['parcial_3'] is not None else 0.0,
                step=0.1,
                format="%.1f"
            )
            
            ordinario = st.number_input(
                "Ordinario",
                min_value=0.0,
                max_value=10.0,
                value=float(selected_estudiante['ordinario']) if selected_estudiante['ordinario'] is not None else 0.0,
                step=0.1,
                format="%.1f"
            )
        
        # Calcular calificación final automáticamente
        promedio_parciales = (parcial_1 + parcial_2 + parcial_3) / 3
        calificacion_final = (promedio_parciales * 0.5) + (ordinario * 0.5)
        
        st.info(f"**Calificación Final Calculada:** {calificacion_final:.1f}")
        
        if st.form_submit_button("💾 Guardar Calificaciones", type="primary"):
            try:
                conn = db.get_connection()
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO calificaciones 
                    (estudiante_id, materia_id, profesor_id, parcial_1, parcial_2, parcial_3, 
                     ordinario, calificacion_final, semestre, fecha_actualizacion)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, "2025-2026A", CURRENT_TIMESTAMP)
                ''', (selected_estudiante['id'], materia['id'], profesor_id, 
                      parcial_1, parcial_2, parcial_3, ordinario, round(calificacion_final, 1)))
                
                conn.commit()
                conn.close()
                
                st.success("¡Calificaciones guardadas exitosamente!")
                st.rerun()
                
            except Exception as e:
                st.error(f"Error al guardar calificaciones: {str(e)}")

if __name__ == "__main__":
    show_calificaciones_page()