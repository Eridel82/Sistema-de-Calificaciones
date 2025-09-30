import streamlit as st
from utils.auth import login_user

def show_login_page():
    """Muestra la página de login"""
    st.title("🔐 Iniciar Sesión")
    st.subheader("Sistema de Gestión de Calificaciones - NovaUniversitas")
    
    # Crear columnas para centrar el formulario
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Formulario de login
        with st.form("login_form"):
            st.markdown("### Credenciales de Acceso")
            
            clave = st.text_input(
                "👤 Clave de Profesor",
                placeholder="Ej: PROF001",
                help="Ingrese su clave de profesor"
            )
            
            password = st.text_input(
                "🔒 Contraseña",
                type="password",
                placeholder="Ingrese su contraseña",
                help="Ingrese su contraseña"
            )
            
            # Botón de envío
            submit_button = st.form_submit_button(
                "🚀 Iniciar Sesión",
                use_container_width=True
            )
            
            # Procesar el login
            if submit_button:
                if clave and password:
                    with st.spinner("Verificando credenciales..."):
                        # Intentar autenticar al usuario
                        if login_user(clave, password):
                            st.success("¡Inicio de sesión exitoso!")
                            st.session_state.page = "dashboard"
                            st.rerun()
                        else:
                            st.error("❌ Clave de profesor o contraseña incorrectos")
                else:
                    st.error("⚠️ Por favor, complete todos los campos")
        
        # Mostrar información de usuarios de prueba
        with st.expander("👥 Usuarios de Prueba - Haz clic para ver"):
            st.markdown("""
            **Credenciales disponibles para pruebas:**
            
            | Clave | Contraseña | Profesor |
            |-------|------------|----------|
            | `PROF001` | `password123` | María García López |
            | `PROF002` | `password123` | Juan Martínez Rodríguez |
            | `PROF003` | `password123` | Ana Hernández Sánchez |
            | `PROF004` | `password123` | Carlos López Pérez |
            | `PROF005` | `password123` | Laura González Ramírez |
            
            💡 **Tip:** Copia y pega las credenciales para probar el sistema
            """)
        
        # Información adicional
        st.markdown("---")
        st.info("""
        🔒 **Sistema Seguro**
        - Las contraseñas están encriptadas
        - Sesión segura con autenticación
        - Acceso solo para profesores autorizados
        """)