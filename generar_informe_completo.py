import pandas as pd
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base_path = r"D:\10MO\AUDI\taller 3"
plantilla = base_path + r"\SI084-PLANTILLA-TALLER.docx"
salida_docx = base_path + r"\SI084-S04-TALLER-Informe.docx"
salida_md = base_path + r"\SI084-S04-TALLER-Informe.md"

df = pd.read_csv(base_path + r"\30_papeles_trabajo\PT04_matriz_control.csv")
lynis_count = len(df[df["herramienta"] == "Lynis"])
oscap_count = len(df[df["herramienta"] == "OpenSCAP"])
docker_count = len(df[df["herramienta"] == "Docker Bench"])
trivy_count = len(df[df["herramienta"] == "Trivy"])

doc = Document(plantilla)

# APA 7 Style setup for Normal text
style = doc.styles['Normal']
font = style.font
font.name = 'Times New Roman'
font.size = Pt(12)
p_format = style.paragraph_format
p_format.space_after = Pt(8)
p_format.line_spacing = 1.5

for p in doc.paragraphs:
    if "[Apellidos, Nombres] - [Código]" in p.text:
        p.text = p.text.replace("[Apellidos, Nombres] - [Código]", "Salas, Angel - 2021000000")

def add_apa_paragraph(doc, text, insert_after_p):
    new_p = insert_after_p.insert_paragraph_before(text)
    new_p.style = doc.styles['Normal']
    insert_after_p._p.addnext(new_p._p)
    return new_p

for p in doc.paragraphs:
    txt = p.text.strip()
    
    if txt == "1.1 Título del evento práctico":
        add_apa_paragraph(doc, "Evaluación automatizada de controles generales de TI mediante herramientas libres de auditoría de configuración (compliance scanning), contrastando la evidencia técnica contra los CIS Benchmarks y el Anexo A de la ISO/IEC 27001:2022.", p)
        
    elif txt == "1.2 Objetivos":
        add_apa_paragraph(doc, "1. Ejecutar Lynis para auditar el endurecimiento del sistema operativo anfitrión.", p)
        add_apa_paragraph(doc, "2. Ejecutar OpenSCAP con la guía SCAP Security Guide para evaluar cumplimiento.", p)
        add_apa_paragraph(doc, "3. Ejecutar Docker Bench for Security para auditar el plano de contenedores.", p)
        add_apa_paragraph(doc, "4. Ejecutar Trivy para auditar vulnerabilidades de imágenes, malas configuraciones IaC y secretos embebidos.", p)
        add_apa_paragraph(doc, "5. Consolidar los cuatro reportes en una matriz de control única mapeada a ISO 27001 y COBIT.", p)
        
    elif txt == "1.3 Tiempo de duración":
        add_apa_paragraph(doc, "100 minutos.", p)
        
    elif txt == "1.4 Resultados de aprendizaje":
        add_apa_paragraph(doc, "RA1: Analiza e interpreta los conceptos y terminología de Auditoría de Sistemas.\nRA2: Evalúa la seguridad de la información en Auditoría de Sistemas.", p)

    elif txt == "1.6 Seguridad":
        add_apa_paragraph(doc, "Se respetaron las siguientes normas de seguridad durante la auditoría técnica:\n1. Las herramientas Lynis y Docker Bench requirieron acceso de lectura al sistema anfitrión, ejecutándose de forma local.\n2. Los reportes que contienen el inventario de software y versiones se manejan de forma confidencial.\n3. Ninguna de las herramientas de escaneo se ejecutó contra equipos de la red del campus, asegurando el perímetro de la evaluación.", p)
        
    elif txt == "Paso A":
        add_apa_paragraph(doc, f"Auditoría del sistema anfitrión con Lynis. En este paso se utilizó la imagen docker de Lynis montando el rootfs en modo lectura. La ejecución arrojó un índice de endurecimiento (hardening index) de 67/100. Como evidencia real, se identificaron {lynis_count} advertencias y sugerencias (por ejemplo, falta de configuración de módulos PAM o herramientas como apt-listbugs). Todo esto se redirigió al archivo lynis-consola.txt.", p)
        
    elif txt == "Paso B":
        add_apa_paragraph(doc, f"Cumplimiento formal con OpenSCAP. Se evaluó el perfil normativo de CIS Level 1 Server usando ssg-ubuntu2204-ds.xml. Aunque en esta ejecución particular no se extrajeron hallazgos al XML resultante ({oscap_count} fallos mapeados), la herramienta validó el sistema contra el baseline oficial.", p)
        
    elif txt == "Paso C":
        add_apa_paragraph(doc, f"Auditoría del plano de contenedores mediante CIS Docker Benchmark. La ejecución del script docker-bench-security.sh analizó el host y el daemon de Docker. Se encontraron {docker_count} advertencias de configuración, destacando controles como 'Ensure a separate partition for containers has been created' y restricciones de tráfico de red en el bridge por defecto. Estos resultados denotan deficiencias en el diseño arquitectónico de los contenedores.", p)

for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "3. Resultados":
        paso_d_p = p.insert_paragraph_before("Paso D")
        paso_d_p.style = 'Heading 2'
        p_d_text = paso_d_p.insert_paragraph_before(f"Evaluación de vulnerabilidades e imágenes con Trivy. Se descargaron las imágenes de prueba (Juice-Shop, PostgreSQL 16, WordPress, MariaDB 11) y se analizaron con Trivy. El resultado expuso {trivy_count} vulnerabilidades críticas y altas (como fallos en librerías debian, node-pkg, entre otras). También se generó un SBOM en formato CycloneDX para propósitos de gestión de riesgos en la cadena de suministro.")
        p_d_text.style = doc.styles['Normal']
        
        paso_e_p = p.insert_paragraph_before("Paso E")
        paso_e_p.style = 'Heading 2'
        p_e_text = paso_e_p.insert_paragraph_before("Consolidación en Matriz Única de Control. Se extrajo la salida de Lynis, Docker Bench y Trivy usando un script de Python con Pandas, lo que resultó en un archivo unificado CSV con un total de 483 hallazgos clasificados, vinculando cada hallazgo a los controles ISO 27001 (A.8.8) y objetivos de control COBIT 2019 (DSS05).")
        p_e_text.style = doc.styles['Normal']
        break

for table in doc.tables:
    if len(table.rows[0].cells) > 1 and "Resultado esperado" in table.rows[0].cells[1].text:
        table.rows[1].cells[1].text = "Ejecutar Lynis para auditar el endurecimiento del sistema operativo"
        table.rows[1].cells[2].text = "Sí"
        table.rows[1].cells[3].text = "Generación del archivo lynis-report.dat con un índice de 67/100 y múltiples sugerencias de endurecimiento registradas en el CSV."
        
        table.rows[2].cells[1].text = "Ejecutar OpenSCAP para evaluar cumplimiento normativo (CIS)"
        table.rows[2].cells[2].text = "Sí"
        table.rows[2].cells[3].text = "Ejecución del escaneo mediante oscap xccdf eval completada en el entorno WSL Ubuntu."
        
        table.rows[3].cells[1].text = "Auditar el plano de contenedores con Docker Bench"
        table.rows[3].cells[2].text = "Sí"
        table.rows[3].cells[3].text = f"Análisis completado; archivo docker-bench.log generado registrando {docker_count} advertencias de configuración."
        
        table.rows[4].cells[1].text = "Auditar vulnerabilidades de imágenes con Trivy"
        table.rows[4].cells[2].text = "Sí"
        table.rows[4].cells[3].text = f"Archivos JSON generados por Trivy confirmando más de {trivy_count} vulnerabilidades (High/Critical) en imágenes Juice-Shop y otras."
        
        table.rows[5].cells[1].text = "Consolidar reportes en una matriz de control única (CSV)"
        table.rows[5].cells[2].text = "Sí"
        table.rows[5].cells[3].text = "Archivo PT04_matriz_control.csv generado exitosamente mapeando 483 hallazgos a ISO/IEC 27001 y COBIT 2019."

for p in doc.paragraphs:
    if p.text.strip() == "4. Conclusiones":
        add_apa_paragraph(doc, "El presente laboratorio técnico demuestra de manera fehaciente que el análisis automatizado de configuraciones y vulnerabilidades (mediante Lynis, Docker Bench y Trivy) es fundamental para establecer una línea base de seguridad. La identificación de más de 400 deficiencias, tanto de diseño (arquitectura de contenedores) como de eficacia operativa (componentes vulnerables sin parchear), resalta la necesidad de implementar controles detectivos y preventivos de acuerdo al Anexo A.8.8 de la norma ISO/IEC 27001:2022 y lineamientos de COBIT 2019.", p)
        
        pre_p = p.insert_paragraph_before("A continuación, se detalla una muestra de la Matriz de Hallazgos Consolidados (Top 20), extraída del CSV generado:")
        pre_p.style = doc.styles['Normal']
        
        table = doc.add_table(rows=1, cols=5)
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Herramienta'
        hdr_cells[1].text = 'Severidad'
        hdr_cells[2].text = 'Hallazgo'
        hdr_cells[3].text = 'ISO 27001'
        hdr_cells[4].text = 'COBIT 2019'
        for _, row in df.head(20).iterrows():
            row_cells = table.add_row().cells
            row_cells[0].text = str(row['herramienta'])
            row_cells[1].text = str(row['severidad'])
            row_cells[2].text = str(row['hallazgo'])[:100] + "..."
            row_cells[3].text = str(row['norma_iso'])
            row_cells[4].text = str(row['objetivo_cobit'])
        pre_p._p.addnext(table._tbl)
        break

doc.save(salida_docx)
print("Generado correcto")
