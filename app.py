import streamlit as st
import sys
import os

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.auth import check_authentication, logout_user, get_current_user
from database.database import db
from pages.login import show_login_page
from pages.dashboard import show_dashboard
from pages.calificaciones import show_calificaciones_page
from pages.reportes import show_reportes_page
from pages.estadisticas import show_estadisticas_page

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Calificaciones - NovaUniversitas",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        color: white;
        text-align: center;
        margin: 0;
    }
    
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 20px;
        border: none;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

def initialize_database():
    """Inicializa la base de datos con datos de muestra si es necesario"""
    if 'db_initialized' not in st.session_state:
        with st.spinner("Inicializando base de datos..."):
            try:
                message = db.populate_sample_data()
                st.session_state.db_initialized = True
                if "exitosamente" in message:
                    st.success("Base de datos inicializada correctamente")
                else:
                    st.info(message)
            except Exception as e:
                st.error(f"Error al inicializar la base de datos: {str(e)}")

def show_sidebar():
    """Muestra la barra lateral con navegación"""
    with st.sidebar:
        st.markdown("### 🎓 NovaUniversitas")
        st.markdown("**Sistema de Gestión de Calificaciones**")
        
        if check_authentication():
            user = get_current_user()
            st.markdown(f"**Bienvenido:** {user['nombre']} {user['apellido_paterno']}")
            st.markdown(f"**Clave:** {user['clave']}")
            
            st.markdown("---")
            
            # Menú de navegación
            st.markdown("### 📋 Menú Principal")
            
            if st.button("🏠 Dashboard", use_container_width=True):
                st.session_state.page = "dashboard"
                st.rerun()
            
            if st.button("📝 Calificaciones", use_container_width=True):
                st.session_state.page = "calificaciones"
                st.rerun()
            
            if st.button("📄 Reportes PDF", use_container_width=True):
                st.session_state.page = "reportes"
                st.rerun()
            
            if st.button("📊 Estadísticas", use_container_width=True):
                st.session_state.page = "estadisticas"
                st.rerun()
            
            st.markdown("---")
            
            # Información del sistema
            st.markdown("### ℹ️ Información")
            st.markdown("""
            **Funcionalidades:**
            - ✅ Gestión de calificaciones
            - ✅ Carga desde Excel
            - ✅ Reportes PDF
            - ✅ Estadísticas avanzadas
            - ✅ Sistema seguro
            """)
            
            st.markdown("---")
            
            # Botón de cerrar sesión
            if st.button("🚪 Cerrar Sesión", use_container_width=True, type="secondary"):
                logout_user()
                st.session_state.page = "login"
                st.rerun()
        
        else:
            st.markdown("### 🔐 Acceso Requerido")
            st.info("Inicia sesión para acceder al sistema")
            
            st.markdown("---")
            st.markdown("### 📞 Soporte")
            st.markdown("""
            **NovaUniversitas**
            
            📧 Email: soporte@novauniversitas.edu
            📞 Teléfono: (555) 123-4567
            🌐 Web: www.novauniversitas.edu
            """)

def main():
    """Función principal de la aplicación"""
    
    # Inicializar la base de datos
    initialize_database()
    
    # Inicializar el estado de la página si no existe
    if 'page' not in st.session_state:
        st.session_state.page = "login"
    
    # Mostrar barra lateral
    show_sidebar()
    
    # Mostrar contenido principal según la página actual
    if not check_authentication():
        show_login_page()
    else:
        # Header principal
        st.markdown("""
        <div class="main-header">
            <h1>🎓 Sistema de Gestión de Calificaciones - NovaUniversitas</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Navegación por páginas
        page = st.session_state.get('page', 'dashboard')
        
        if page == "dashboard":
            show_dashboard()
        elif page == "calificaciones":
            show_calificaciones_page()
        elif page == "reportes":
            show_reportes_page()
        elif page == "estadisticas":
            show_estadisticas_page()
        else:
            show_dashboard()

if __name__ == "__main__":
    main()