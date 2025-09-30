import sqlite3
import hashlib
import pandas as pd
from datetime import datetime
import random

class DatabaseManager:
    def __init__(self, db_path="database/calificaciones.db"):
        self.db_path = db_path
        self.init_database()
        
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Inicializa la base de datos con todas las tablas necesarias"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de profesores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profesores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido_paterno TEXT NOT NULL,
                apellido_materno TEXT NOT NULL,
                clave TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de materias
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS materias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                codigo TEXT UNIQUE NOT NULL,
                creditos INTEGER DEFAULT 6,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de estudiantes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estudiantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido_paterno TEXT NOT NULL,
                apellido_materno TEXT NOT NULL,
                clave TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de asignaciones profesor-materia
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profesor_materia (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profesor_id INTEGER,
                materia_id INTEGER,
                semestre TEXT NOT NULL,
                grupo TEXT NOT NULL,
                FOREIGN KEY (profesor_id) REFERENCES profesores (id),
                FOREIGN KEY (materia_id) REFERENCES materias (id),
                UNIQUE(profesor_id, materia_id, semestre, grupo)
            )
        ''')
        
        # Tabla de inscripciones estudiante-materia
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inscripciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                estudiante_id INTEGER,
                materia_id INTEGER,
                profesor_id INTEGER,
                semestre TEXT NOT NULL,
                grupo TEXT NOT NULL,
                FOREIGN KEY (estudiante_id) REFERENCES estudiantes (id),
                FOREIGN KEY (materia_id) REFERENCES materias (id),
                FOREIGN KEY (profesor_id) REFERENCES profesores (id),
                UNIQUE(estudiante_id, materia_id, semestre)
            )
        ''')
        
        # Tabla de calificaciones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS calificaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                estudiante_id INTEGER,
                materia_id INTEGER,
                profesor_id INTEGER,
                parcial_1 REAL DEFAULT NULL,
                parcial_2 REAL DEFAULT NULL,
                parcial_3 REAL DEFAULT NULL,
                ordinario REAL DEFAULT NULL,
                calificacion_final REAL DEFAULT NULL,
                semestre TEXT NOT NULL,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (estudiante_id) REFERENCES estudiantes (id),
                FOREIGN KEY (materia_id) REFERENCES materias (id),
                FOREIGN KEY (profesor_id) REFERENCES profesores (id),
                UNIQUE(estudiante_id, materia_id, profesor_id, semestre)
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def hash_password(self, password):
        """Hashea la contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def populate_sample_data(self):
        """Llena la base de datos con datos de muestra"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Verificar si ya hay datos
        cursor.execute("SELECT COUNT(*) FROM profesores")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return "Los datos ya existen en la base de datos"
        
        # Datos de profesores
        profesores = [
            ("María", "García", "López", "PROF001", "password123"),
            ("Juan", "Martínez", "Rodríguez", "PROF002", "password123"),
            ("Ana", "Hernández", "Sánchez", "PROF003", "password123"),
            ("Carlos", "López", "Pérez", "PROF004", "password123"),
            ("Laura", "González", "Ramírez", "PROF005", "password123")
        ]
        
        for prof in profesores:
            cursor.execute('''
                INSERT INTO profesores (nombre, apellido_paterno, apellido_materno, clave, password)
                VALUES (?, ?, ?, ?, ?)
            ''', (*prof[:4], self.hash_password(prof[4])))
        
        # Datos de materias
        materias = [
            ("Matemáticas I", "MAT001"),
            ("Física I", "FIS001"),
            ("Química General", "QUI001"),
            ("Programación I", "PRG001"),
            ("Cálculo Diferencial", "CAL001"),
            ("Álgebra Lineal", "ALG001"),
            ("Estadística", "EST001"),
            ("Base de Datos", "BDD001"),
            ("Ingeniería de Software", "ING001"),
            ("Redes de Computadoras", "RED001")
        ]
        
        for materia in materias:
            cursor.execute('''
                INSERT INTO materias (nombre, codigo) VALUES (?, ?)
            ''', materia)
        
        # Generar estudiantes
        nombres = ["José", "María", "Juan", "Ana", "Carlos", "Laura", "Pedro", "Carmen", "Luis", "Rosa",
                  "Miguel", "Isabel", "Antonio", "Pilar", "Francisco", "Dolores", "Manuel", "Teresa",
                  "David", "Cristina", "Alejandro", "Patricia", "Rafael", "Lucía", "Javier"]
        
        apellidos_p = ["García", "Martínez", "López", "Hernández", "González", "Pérez", "Sánchez",
                      "Ramírez", "Cruz", "Flores", "Gómez", "Díaz", "Ruiz", "Morales", "Jiménez"]
        
        apellidos_m = ["Rodríguez", "Fernández", "Torres", "Domínguez", "Vázquez", "Ramos", "Gil",
                      "Serrano", "Blanco", "Suárez", "Castro", "Ortega", "Rubio", "Molina", "Delgado"]
        
        estudiantes = []
        for i in range(100):
            nombre = random.choice(nombres)
            ap_pat = random.choice(apellidos_p)
            ap_mat = random.choice(apellidos_m)
            clave = f"EST{i+1:03d}"
            estudiantes.append((nombre, ap_pat, ap_mat, clave))
        
        cursor.executemany('''
            INSERT INTO estudiantes (nombre, apellido_paterno, apellido_materno, clave)
            VALUES (?, ?, ?, ?)
        ''', estudiantes)
        
        # Asignar materias a profesores
        cursor.execute("SELECT id FROM profesores")
        prof_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id FROM materias")
        mat_ids = [row[0] for row in cursor.fetchall()]
        
        # Cada profesor tendrá 2 materias
        asignaciones = []
        for i, prof_id in enumerate(prof_ids):
            # Asignar 2 materias por profesor
            materias_asignadas = random.sample(mat_ids, 2)
            for mat_id in materias_asignadas:
                asignaciones.append((prof_id, mat_id, "2025-2026A", "A"))
        
        cursor.executemany('''
            INSERT OR IGNORE INTO profesor_materia (profesor_id, materia_id, semestre, grupo)
            VALUES (?, ?, ?, ?)
        ''', asignaciones)
        
        # Inscribir estudiantes en materias (15-25 estudiantes por materia)
        cursor.execute("SELECT id FROM estudiantes")
        est_ids = [row[0] for row in cursor.fetchall()]
        
        inscripciones = []
        for mat_id in mat_ids:
            # Obtener profesor asignado a esta materia
            cursor.execute('''
                SELECT profesor_id FROM profesor_materia 
                WHERE materia_id = ? AND semestre = "2025-2026A"
            ''', (mat_id,))
            result = cursor.fetchone()
            if result:
                prof_id = result[0]
                # Seleccionar entre 15-25 estudiantes aleatoriamente
                num_estudiantes = random.randint(15, 25)
                estudiantes_seleccionados = random.sample(est_ids, num_estudiantes)
                
                for est_id in estudiantes_seleccionados:
                    inscripciones.append((est_id, mat_id, prof_id, "2025-2026A", "A"))
        
        cursor.executemany('''
            INSERT OR IGNORE INTO inscripciones (estudiante_id, materia_id, profesor_id, semestre, grupo)
            VALUES (?, ?, ?, ?, ?)
        ''', inscripciones)
        
        # Generar calificaciones de muestra
        cursor.execute('''
            SELECT i.estudiante_id, i.materia_id, i.profesor_id, i.semestre
            FROM inscripciones i
        ''')
        inscripciones_data = cursor.fetchall()
        
        calificaciones = []
        for est_id, mat_id, prof_id, semestre in inscripciones_data:
            # Generar calificaciones aleatorias (6.0 - 10.0)
            p1 = round(random.uniform(6.0, 10.0), 1)
            p2 = round(random.uniform(6.0, 10.0), 1)
            p3 = round(random.uniform(6.0, 10.0), 1)
            ordinario = round(random.uniform(6.0, 10.0), 1)
            
            # Calcular calificación final (50% parciales + 50% ordinario)
            promedio_parciales = (p1 + p2 + p3) / 3
            final = round((promedio_parciales * 0.5) + (ordinario * 0.5), 1)
            
            calificaciones.append((est_id, mat_id, prof_id, p1, p2, p3, ordinario, final, semestre))
        
        cursor.executemany('''
            INSERT OR IGNORE INTO calificaciones 
            (estudiante_id, materia_id, profesor_id, parcial_1, parcial_2, parcial_3, ordinario, calificacion_final, semestre)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', calificaciones)
        
        conn.commit()
        conn.close()
        
        return "Datos de muestra creados exitosamente"
    
    def authenticate_user(self, clave, password):
        """Autentica un usuario (profesor)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        hashed_password = self.hash_password(password)
        cursor.execute('''
            SELECT id, nombre, apellido_paterno, apellido_materno, clave
            FROM profesores 
            WHERE clave = ? AND password = ?
        ''', (clave, hashed_password))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'nombre': result[1],
                'apellido_paterno': result[2],
                'apellido_materno': result[3],
                'clave': result[4]
            }
        return None
    
    def get_profesor_materias(self, profesor_id):
        """Obtiene las materias asignadas a un profesor"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT m.id, m.nombre, m.codigo, pm.grupo, pm.semestre
            FROM materias m
            JOIN profesor_materia pm ON m.id = pm.materia_id
            WHERE pm.profesor_id = ?
        ''', (profesor_id,))
        
        result = cursor.fetchall()
        conn.close()
        
        return [{'id': row[0], 'nombre': row[1], 'codigo': row[2], 'grupo': row[3], 'semestre': row[4]} 
                for row in result]
    
    def get_estudiantes_materia(self, materia_id, profesor_id):
        """Obtiene los estudiantes inscritos en una materia específica"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT e.id, e.nombre, e.apellido_paterno, e.apellido_materno, e.clave,
                   c.parcial_1, c.parcial_2, c.parcial_3, c.ordinario, c.calificacion_final
            FROM estudiantes e
            JOIN inscripciones i ON e.id = i.estudiante_id
            LEFT JOIN calificaciones c ON e.id = c.estudiante_id AND c.materia_id = i.materia_id
            WHERE i.materia_id = ? AND i.profesor_id = ?
            ORDER BY e.apellido_paterno, e.apellido_materno, e.nombre
        ''', (materia_id, profesor_id))
        
        result = cursor.fetchall()
        conn.close()
        
        return [{'id': row[0], 'nombre': row[1], 'apellido_paterno': row[2], 
                'apellido_materno': row[3], 'clave': row[4],
                'parcial_1': row[5], 'parcial_2': row[6], 'parcial_3': row[7],
                'ordinario': row[8], 'calificacion_final': row[9]} for row in result]

# Crear instancia de la base de datos
db = DatabaseManager()