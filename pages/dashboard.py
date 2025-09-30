import streamlit as st
from utils.auth import require_auth, get_current_user
from database.database import db

def show_dashboard():
    """Muestra el dashboard principal del profesor"""
    require_auth()
    
    user = get_current_user()
    
    st.title(f"📊 Dashboard - Profesor {user['nombre']} {user['apellido_paterno']}")
    
    # Obtener materias del profesor
    materias = db.get_profesor_materias(user['id'])
    
    if not materias:
        st.warning("No tienes materias asignadas en este semestre.")
        return
    
    # Métricas generales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Materias Asignadas", len(materias))
    
    # Calcular estadísticas generales
    total_estudiantes = 0
    total_calificaciones = 0
    
    for materia in materias:
        estudiantes = db.get_estudiantes_materia(materia['id'], user['id'])
        total_estudiantes += len(estudiantes)
        for est in estudiantes:
            if est['calificacion_final'] is not None:
                total_calificaciones += 1
    
    with col2:
        st.metric("Total Estudiantes", total_estudiantes)
    
    with col3:
        st.metric("Calificaciones Finales", total_calificaciones)
    
    with col4:
        porcentaje_completado = (total_calificaciones / total_estudiantes * 100) if total_estudiantes > 0 else 0
        st.metric("% Completado", f"{porcentaje_completado:.1f}%")
    
    st.markdown("---")
    
    # Resumen por materia
    st.subheader("📚 Resumen por Materia")
    
    for materia in materias:
        with st.expander(f"{materia['nombre']} ({materia['codigo']}) - Grupo {materia['grupo']}"):
            estudiantes = db.get_estudiantes_materia(materia['id'], user['id'])
            
            if estudiantes:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Estudiantes Inscritos", len(estudiantes))
                
                # Calcular estadísticas de la materia
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
                
                # Mostrar distribución de calificaciones
                if calificaciones_finales:
                    st.markdown("**Distribución de Calificaciones:**")
                    
                    # Crear rangos de calificaciones
                    rangos = {
                        "10.0": 0,
                        "9.0-9.9": 0,
                        "8.0-8.9": 0,
                        "7.0-7.9": 0,
                        "6.0-6.9": 0,
                        "< 6.0": 0
                    }
                    
                    for cal in calificaciones_finales:
                        if cal == 10.0:
                            rangos["10.0"] += 1
                        elif cal >= 9.0:
                            rangos["9.0-9.9"] += 1
                        elif cal >= 8.0:
                            rangos["8.0-8.9"] += 1
                        elif cal >= 7.0:
                            rangos["7.0-7.9"] += 1
                        elif cal >= 6.0:
                            rangos["6.0-6.9"] += 1
                        else:
                            rangos["< 6.0"] += 1
                    
                    # Mostrar en columnas
                    cols = st.columns(6)
                    for i, (rango, cantidad) in enumerate(rangos.items()):
                        with cols[i]:
                            st.metric(rango, cantidad)
                
                # Botones de acción rápida
                st.markdown("**Acciones Rápidas:**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button(f"📝 Gestionar Calificaciones", key=f"manage_{materia['id']}"):
                        st.session_state.selected_materia = materia['id']
                        st.session_state.page = "calificaciones"
                        st.rerun()
                
                with col2:
                    if st.button(f"📊 Ver Estadísticas", key=f"stats_{materia['id']}"):
                        st.session_state.selected_materia = materia['id']
                        st.session_state.page = "estadisticas"
                        st.rerun()
                
                with col3:
                    if st.button(f"📄 Generar Reportes", key=f"reports_{materia['id']}"):
                        st.session_state.selected_materia = materia['id']
                        st.session_state.page = "reportes"
                        st.rerun()
            else:
                st.info("No hay estudiantes inscritos en esta materia.")
    
    # Información del calendario académico
    st.markdown("---")
    st.subheader("📅 Calendario Académico 2025-2026A")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Fechas Importantes:**
        - **Inicio de semestre:** 25 de agosto de 2025
        - **Fin de semestre:** 15 de diciembre de 2025
        """)
    
    with col2:
        st.markdown("""
        **Exámenes Parciales:**
        - **1er Parcial:** 19-24 de septiembre de 2025
        - **2do Parcial:** 22-29 de octubre de 2025
        - **3er Parcial:** 26 nov - 03 dic de 2025
        """)
    
    st.markdown("""
    **Exámenes Ordinarios:** 08-15 de diciembre de 2025
    
    *Nota: La fecha límite de entrega de calificaciones es el tercer día hábil posterior al examen.*
    """)

if __name__ == "__main__":
    show_dashboard()