from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Configura estilos personalizados para el PDF"""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        self.header_style = ParagraphStyle(
            'CustomHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=12,
            alignment=TA_LEFT,
            textColor=colors.black
        )
        
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_LEFT
        )
    
    def create_header(self, profesor_info, materia_info, tipo_reporte):
        """Crea el encabezado del reporte"""
        elements = []
        
        # Título principal
        title = f"NOVAUNIVERSITAS - REPORTE DE CALIFICACIONES"
        elements.append(Paragraph(title, self.title_style))
        elements.append(Spacer(1, 20))
        
        # Información del profesor y materia
        info_data = [
            ['Profesor:', f"{profesor_info['nombre']} {profesor_info['apellido_paterno']} {profesor_info['apellido_materno']}"],
            ['Clave Profesor:', profesor_info['clave']],
            ['Materia:', materia_info['nombre']],
            ['Código Materia:', materia_info['codigo']],
            ['Tipo de Reporte:', tipo_reporte],
            ['Fecha de Generación:', datetime.now().strftime("%d/%m/%Y %H:%M")]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 30))
        
        return elements
    
    def create_grades_table(self, estudiantes_data, tipo_reporte):
        """Crea la tabla de calificaciones según el tipo de reporte"""
        if not estudiantes_data:
            return [Paragraph("No hay estudiantes registrados en esta materia.", self.normal_style)]
        
        elements = []
        
        # Definir columnas según el tipo de reporte
        if tipo_reporte == "Parcial 1":
            headers = ['No.', 'Clave', 'Nombre Completo', 'Parcial 1', 'Firma Estudiante']
            data = [headers]
            for i, est in enumerate(estudiantes_data, 1):
                nombre_completo = f"{est['apellido_paterno']} {est['apellido_materno']} {est['nombre']}"
                calificacion = est['parcial_1'] if est['parcial_1'] is not None else "N/A"
                data.append([str(i), est['clave'], nombre_completo, str(calificacion), ""])
            col_widths = [0.5*inch, 1*inch, 3*inch, 1*inch, 1.5*inch]
            
        elif tipo_reporte == "Parcial 2":
            headers = ['No.', 'Clave', 'Nombre Completo', 'Parcial 2', 'Firma Estudiante']
            data = [headers]
            for i, est in enumerate(estudiantes_data, 1):
                nombre_completo = f"{est['apellido_paterno']} {est['apellido_materno']} {est['nombre']}"
                calificacion = est['parcial_2'] if est['parcial_2'] is not None else "N/A"
                data.append([str(i), est['clave'], nombre_completo, str(calificacion), ""])
            col_widths = [0.5*inch, 1*inch, 3*inch, 1*inch, 1.5*inch]
            
        elif tipo_reporte == "Parcial 3":
            headers = ['No.', 'Clave', 'Nombre Completo', 'Parcial 3', 'Firma Estudiante']
            data = [headers]
            for i, est in enumerate(estudiantes_data, 1):
                nombre_completo = f"{est['apellido_paterno']} {est['apellido_materno']} {est['nombre']}"
                calificacion = est['parcial_3'] if est['parcial_3'] is not None else "N/A"
                data.append([str(i), est['clave'], nombre_completo, str(calificacion), ""])
            col_widths = [0.5*inch, 1*inch, 3*inch, 1*inch, 1.5*inch]
            
        elif tipo_reporte == "Ordinario":
            headers = ['No.', 'Clave', 'Nombre Completo', 'Ordinario', 'Firma Estudiante']
            data = [headers]
            for i, est in enumerate(estudiantes_data, 1):
                nombre_completo = f"{est['apellido_paterno']} {est['apellido_materno']} {est['nombre']}"
                calificacion = est['ordinario'] if est['ordinario'] is not None else "N/A"
                data.append([str(i), est['clave'], nombre_completo, str(calificacion), ""])
            col_widths = [0.5*inch, 1*inch, 3*inch, 1*inch, 1.5*inch]
            
        else:  # Calificación Final
            headers = ['No.', 'Clave', 'Nombre Completo', 'P1', 'P2', 'P3', 'Ord.', 'Final', 'Firma']
            data = [headers]
            for i, est in enumerate(estudiantes_data, 1):
                nombre_completo = f"{est['apellido_paterno']} {est['apellido_materno']} {est['nombre']}"
                p1 = est['parcial_1'] if est['parcial_1'] is not None else "N/A"
                p2 = est['parcial_2'] if est['parcial_2'] is not None else "N/A"
                p3 = est['parcial_3'] if est['parcial_3'] is not None else "N/A"
                ord_cal = est['ordinario'] if est['ordinario'] is not None else "N/A"
                final = est['calificacion_final'] if est['calificacion_final'] is not None else "N/A"
                data.append([str(i), est['clave'], nombre_completo, str(p1), str(p2), str(p3), str(ord_cal), str(final), ""])
            col_widths = [0.4*inch, 0.8*inch, 2.2*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.5*inch, 0.6*inch, 1*inch]
        
        # Crear tabla
        table = Table(data, colWidths=col_widths)
        table.setStyle(TableStyle([
            # Estilo del encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Estilo del contenido
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (2, 1), (2, -1), 'LEFT'),  # Nombres alineados a la izquierda
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.beige, colors.white]),
            
            # Bordes
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Altura de filas
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.beige, colors.white]),
        ]))
        
        elements.append(table)
        return elements
    
    def create_signature_section(self, profesor_info):
        """Crea la sección de firmas"""
        elements = []
        elements.append(Spacer(1, 40))
        
        # Crear tabla para firmas
        signature_data = [
            ['', ''],
            ['_' * 40, '_' * 40],
            [f"Profesor: {profesor_info['nombre']} {profesor_info['apellido_paterno']} {profesor_info['apellido_materno']}", 'Vo.Bo. Coordinación Académica'],
            [f"Clave: {profesor_info['clave']}", '']
        ]
        
        signature_table = Table(signature_data, colWidths=[3*inch, 3*inch])
        signature_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 2), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 2), (-1, -1), 9),
            ('TOPPADDING', (0, 1), (-1, 1), 10),
            ('BOTTOMPADDING', (0, 1), (-1, 1), 5),
        ]))
        
        elements.append(signature_table)
        return elements
    
    def generate_report(self, profesor_info, materia_info, estudiantes_data, tipo_reporte, output_path):
        """Genera el reporte PDF completo"""
        doc = SimpleDocTemplate(output_path, pagesize=A4, 
                              rightMargin=72, leftMargin=72, 
                              topMargin=72, bottomMargin=18)
        
        story = []
        
        # Agregar encabezado
        story.extend(self.create_header(profesor_info, materia_info, tipo_reporte))
        
        # Agregar tabla de calificaciones
        story.extend(self.create_grades_table(estudiantes_data, tipo_reporte))
        
        # Agregar sección de firmas
        story.extend(self.create_signature_section(profesor_info))
        
        # Construir PDF
        doc.build(story)
        
        return output_path

# Instancia global del generador de PDF
pdf_generator = PDFGenerator()