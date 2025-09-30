🎓 Sistema de Gestión de Calificaciones - NovaUniversitas

Sistema completo de gestión de calificaciones desarrollado con Python y Streamlit para profesores universitarios.

📋 Características Principales
✅ Sistema de Autenticación Seguro: Login con hash SHA-256
✅ Gestión de Calificaciones: Registro y edición de parciales y ordinario
✅ Carga Masiva desde Excel: Importación de calificaciones con plantillas
✅ Reportes PDF Profesionales: 5 tipos de reportes con firmas
✅ Estadísticas Avanzadas: Análisis completo del rendimiento
✅ Base de Datos SQLite: Estructura robusta y eficiente
✅ Interfaz Intuitiva: Dashboard moderno con Streamlit
🏗️ Estructura del Proyecto
sistema_calificaciones/
├── app.py                      # Aplicación principal
├── requirements.txt            # Dependencias
├── README.md                  # Documentación
├── database/
│   ├── database.py            # Gestión de base de datos
│   └── calificaciones.db      # Base de datos SQLite (se crea automáticamente)
├── pages/
│   ├── login.py               # Página de inicio de sesión
│   ├── dashboard.py           # Dashboard principal
│   ├── calificaciones.py      # Gestión de calificaciones
│   ├── reportes.py            # Generación de reportes PDF
│   └── estadisticas.py        # Análisis estadístico
├── utils/
│   ├── auth.py                # Autenticación y sesiones
│   ├── pdf_generator.py       # Generación de PDFs
│   └── excel_handler.py       # Manejo de archivos Excel
├── templates/                 # Plantillas (futuro uso)
├── reports/                   # Reportes PDF generados
└── static/
    ├── css/                   # Estilos personalizados
    └── images/                # Imágenes del sistema

🚀 Instalación y Configuración
Prerrequisitos
Python 3.8 o superior
VS Code (recomendado)
Git
Pasos de Instalación
Clonar o descargar el proyecto
# Si usas Git
git clone <url-del-repositorio>
cd sistema_calificaciones

# O simplemente descargar y extraer los archivos

Crear entorno virtual
python -m venv venv

# Activar en Windows
venv\Scripts\activate

# Activar en macOS/Linux
source venv/bin/activate

Instalar dependencias
pip install -r requirements.txt

Ejecutar la aplicación
streamlit run app.py

Abrir en el navegador
La aplicación se abrirá automáticamente en http://localhost:8501
👥 Usuarios de Prueba

El sistema incluye 5 profesores de prueba:

Clave	Nombre	Contraseña
PROF001	María García López	password123
PROF002	Juan Martínez Rodríguez	password123
PROF003	Ana Hernández Sánchez	password123
PROF004	Carlos López Pérez	password123
PROF005	Laura González Ramírez	password123
📊 Datos de Muestra

El sistema incluye:

5 profesores con credenciales de acceso
10 materias distribuidas entre los profesores
100 estudiantes simulados con nombres realistas
Inscripciones de 15-25 estudiantes por materia
Calificaciones de muestra ya generadas
📅 Calendario Académico 2025-2026
Semestre A (2025-2026)
Inicio: 25 de agosto de 2025
Fin: 15 de diciembre de 2025
Exámenes Parciales
1er Parcial: 19-24 de septiembre de 2025
2do Parcial: 22-29 de octubre de 2025
3er Parcial: 26 nov - 03 dic de 2025
Exámenes Ordinarios
Ordinarios: 08-15 de diciembre de 2025
📄 Tipos de Reportes PDF
Reporte Parcial 1: Calificaciones del primer parcial
Reporte Parcial 2: Calificaciones del segundo parcial
Reporte Parcial 3: Calificaciones del tercer parcial
Reporte Ordinario: Calificaciones del examen ordinario
Reporte Final: Todas las calificaciones y promedio final

Todos los reportes incluyen:

Información completa del profesor
Datos de la materia y grupo
Espacios para firmas del profesor y coordinación
Espacios para firmas de estudiantes
Formato profesional con logo institucional
📈 Sistema de Calificaciones
Parciales: 3 exámenes parciales (50% de la calificación final)
Ordinario: 1 examen ordinario (50% de la calificación final)
Calificación Final: Promedio ponderado automático
Escala: 0.0 - 10.0
Aprobación: ≥ 6.0
🔧 Funcionalidades Principales
Dashboard
Resumen general de materias y estudiantes
Métricas de rendimiento
Acceso rápido a todas las funciones
Información del calendario académico
Gestión de Calificaciones
Visualización de calificaciones por materia
Edición individual de calificaciones
Carga masiva desde Excel
Descarga de plantillas
Cálculo automático de promedios
Reportes PDF
Generación de 5 tipos de reportes
Formato profesional con firmas
Descarga inmediata
Información completa del profesor y materia
Estadísticas
Análisis de rendimiento por materia
Gráficos interactivos con Plotly
Identificación de estudiantes en riesgo
Estudiantes destacados
Correlaciones entre evaluaciones
Recomendaciones automáticas
Carga desde Excel
Plantillas automáticas por materia
Validación de formato
Procesamiento masivo
Manejo de errores
Actualización automática de promedios
🛠️ Tecnologías Utilizadas
Backend: Python 3.8+
Frontend: Streamlit
Base de Datos: SQLite
Reportes: ReportLab
Gráficos: Plotly
Excel: Pandas + OpenPyXL
Autenticación: Hashlib (SHA-256)
📱 Uso del Sistema
Para Profesores

Iniciar Sesión

Usar clave de profesor y contraseña
El sistema recordará la sesión

Dashboard

Ver resumen de todas las materias
Acceder rápidamente a funciones
Consultar calendario académico

Gestionar Calificaciones

Seleccionar materia
Ver lista de estudiantes
Editar calificaciones individuales
Cargar desde Excel

Generar Reportes

Seleccionar tipo de reporte
Descargar PDF inmediatamente
Incluye firmas y formato oficial

Ver Estadísticas

Análisis completo del rendimiento
Gráficos interactivos
Identificar estudiantes en riesgo
🔒 Seguridad
Contraseñas hasheadas con SHA-256
Sesiones seguras con Streamlit
Validación de permisos por profesor
Protección contra inyección SQL
Validación de datos de entrada

Este sistema fue desarrollado siguiendo las mejores prácticas de desarrollo:

Código limpio y documentado
Estructura modular
Manejo de errores
Interfaz intuitiva
Escalabilidad
📝 Notas Importantes
La base de datos se crea automáticamente al ejecutar la aplicación
Los datos de muestra se cargan solo la primera vez
Los reportes PDF se guardan en la carpeta reports/
Las plantillas Excel se generan dinámicamente
El sistema calcula automáticamente las calificaciones finales
🎯 Objetivos Cumplidos

✅ Base de datos SQLite con estructura completa ✅ Interfaz Streamlit moderna e intuitiva
✅ Carga desde Excel con plantillas automáticas ✅ 5 tipos de reportes PDF con firmas profesionales ✅ Login seguro con hash SHA-256 ✅ Estadísticas avanzadas con gráficos interactivos ✅ Estructura modular organizada por carpetas ✅ Datos de muestra realistas (5 profesores, 10 materias, 100 estudiantes) ✅ Calendario académico integrado con fechas reales ✅ Sistema de calificaciones con parciales (50%) + ordinario (50%)
