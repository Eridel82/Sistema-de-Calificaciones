import streamlit as st
from database.database import db

def check_authentication():
    """Verifica si el usuario está autenticado"""
    return 'user' in st.session_state and st.session_state.user is not None

def login_user(clave, password):
    """Autentica al usuario"""
    user = db.authenticate_user(clave, password)
    if user:
        st.session_state.user = user
        return True
    return False

def logout_user():
    """Cierra la sesión del usuario"""
    if 'user' in st.session_state:
        del st.session_state.user

def get_current_user():
    """Obtiene el usuario actual"""
    return st.session_state.get('user', None)

def require_auth():
    """Decorador para páginas que requieren autenticación"""
    if not check_authentication():
        st.error("Debes iniciar sesión para acceder a esta página")
        st.stop()