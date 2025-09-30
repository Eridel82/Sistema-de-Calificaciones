import pandas as pd
import streamlit as st
from database.database import db
import sqlite3

class ExcelHandler:
    def __init__(self):
        pass
    
    def create_template(self, materia_id, profesor_id):
        """Crea una plantilla de Excel para cargar calificaciones"""
        try:
            # Obtener estudiantes de la materia
            estudiantes = db.get_estudiantes_materia(materia_id, profesor_id)
            
            if not estudiantes:
                return None
            
            # Crear DataFrame con la estructura requerida
            data = []
            for est in estudiantes:
                data.append({
                    'clave_estudiante': est['clave'],
                    'nombre_completo': f"{est['apellido_paterno']} {est['apellido_materno']} {est['nombre']}",
                    'parcial_1': est['parcial_1'] if est['parcial_1'] is not None else '',
                    'parcial_2': est['parcial_2'] if est['parcial_2'] is not None else '',
                    'parcial_3': est['parcial_3'] if est['parcial_3'] is not None else '',
                    'ordinario': est['ordinario'] if est['ordinario'] is not None else ''
                })
            
            df = pd.DataFrame(data)
            return df
            
        except Exception as e:
            st.error(f"Error al crear plantilla: {str(e)}")
            return None
    
    def validate_excel_format(self, df):
        """Valida que el archivo Excel tenga el formato correcto"""
        required_columns = ['clave_estudiante', 'nombre_completo', 'parcial_1', 'parcial_2', 'parcial_3', 'ordinario']
        
        # Verificar que todas las columnas requeridas estén presentes
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return False, f"Faltan las siguientes columnas: {', '.join(missing_columns)}"
        
        # Verificar que las calificaciones estén en el rango válido (0-10) o vacías
        grade_columns = ['parcial_1', 'parcial_2', 'parcial_3', 'ordinario']
        for col in grade_columns:
            for idx, value in df[col].items():
                if pd.notna(value) and value != '':
                    try:
                        grade = float(value)
                        if grade < 0 or grade > 10:
                            return False, f"Calificación inválida en fila {idx+2}, columna {col}: {grade}. Debe estar entre 0 y 10."
                    except ValueError:
                        return False, f"Valor no numérico en fila {idx+2}, columna {col}: {value}"
        
        return True, "Formato válido"
    
    def process_excel_upload(self, uploaded_file, materia_id, profesor_id):
        """Procesa el archivo Excel subido y actualiza las calificaciones"""
        try:
            # Leer el archivo Excel
            df = pd.read_excel(uploaded_file)
            
            # Validar formato
            is_valid, message = self.validate_excel_format(df)
            if not is_valid:
                return False, message
            
            # Obtener conexión a la base de datos
            conn = db.get_connection()
            cursor = conn.cursor()
            
            updated_count = 0
            errors = []
            
            for idx, row in df.iterrows():
                try:
                    clave_estudiante = row['clave_estudiante']
                    
                    # Verificar que el estudiante existe y está inscrito en la materia
                    cursor.execute('''
                        SELECT e.id FROM estudiantes e
                        JOIN inscripciones i ON e.id = i.estudiante_id
                        WHERE e.clave = ? AND i.materia_id = ? AND i.profesor_id = ?
                    ''', (clave_estudiante, materia_id, profesor_id))
                    
                    result = cursor.fetchone()
                    if not result:
                        errors.append(f"Estudiante {clave_estudiante} no encontrado o no inscrito en esta materia")
                        continue
                    
                    estudiante_id = result[0]
                    
                    # Preparar calificaciones (convertir valores vacíos a None)
                    parcial_1 = float(row['parcial_1']) if pd.notna(row['parcial_1']) and row['parcial_1'] != '' else None
                    parcial_2 = float(row['parcial_2']) if pd.notna(row['parcial_2']) and row['parcial_2'] != '' else None
                    parcial_3 = float(row['parcial_3']) if pd.notna(row['parcial_3']) and row['parcial_3'] != '' else None
                    ordinario = float(row['ordinario']) if pd.notna(row['ordinario']) and row['ordinario'] != '' else None
                    
                    # Calcular calificación final si todas las calificaciones están presentes
                    calificacion_final = None
                    if all(cal is not None for cal in [parcial_1, parcial_2, parcial_3, ordinario]):
                        promedio_parciales = (parcial_1 + parcial_2 + parcial_3) / 3
                        calificacion_final = round((promedio_parciales * 0.5) + (ordinario * 0.5), 1)
                    
                    # Actualizar o insertar calificaciones
                    cursor.execute('''
                        INSERT OR REPLACE INTO calificaciones 
                        (estudiante_id, materia_id, profesor_id, parcial_1, parcial_2, parcial_3, 
                         ordinario, calificacion_final, semestre, fecha_actualizacion)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, "2025-2026A", CURRENT_TIMESTAMP)
                    ''', (estudiante_id, materia_id, profesor_id, parcial_1, parcial_2, parcial_3, 
                          ordinario, calificacion_final))
                    
                    updated_count += 1
                    
                except Exception as e:
                    errors.append(f"Error en fila {idx+2}: {str(e)}")
            
            conn.commit()
            conn.close()
            
            if errors:
                error_message = f"Se actualizaron {updated_count} registros. Errores encontrados:\n" + "\n".join(errors)
                return True, error_message
            else:
                return True, f"Se actualizaron exitosamente {updated_count} registros de calificaciones."
                
        except Exception as e:
            return False, f"Error al procesar archivo: {str(e)}"
    
    def export_grades_to_excel(self, materia_id, profesor_id, materia_nombre):
        """Exporta las calificaciones actuales a un archivo Excel"""
        try:
            estudiantes = db.get_estudiantes_materia(materia_id, profesor_id)
            
            if not estudiantes:
                return None
            
            # Crear DataFrame con todas las calificaciones
            data = []
            for est in estudiantes:
                data.append({
                    'Clave': est['clave'],
                    'Nombre Completo': f"{est['apellido_paterno']} {est['apellido_materno']} {est['nombre']}",
                    'Parcial 1': est['parcial_1'] if est['parcial_1'] is not None else '',
                    'Parcial 2': est['parcial_2'] if est['parcial_2'] is not None else '',
                    'Parcial 3': est['parcial_3'] if est['parcial_3'] is not None else '',
                    'Ordinario': est['ordinario'] if est['ordinario'] is not None else '',
                    'Calificación Final': est['calificacion_final'] if est['calificacion_final'] is not None else ''
                })
            
            df = pd.DataFrame(data)
            
            # Crear archivo Excel en memoria
            output_filename = f"calificaciones_{materia_nombre.replace(' ', '_')}.xlsx"
            return df, output_filename
            
        except Exception as e:
            st.error(f"Error al exportar calificaciones: {str(e)}")
            return None, None

# Instancia global del manejador de Excel
excel_handler = ExcelHandler()