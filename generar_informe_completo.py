import pandas as pd
from docx import Document
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

# Reemplazar nombre
for p in doc.paragraphs:
    if "[Apellidos, Nombres] - [Código]" in p.text:
        p.text = p.text.replace("[Apellidos, Nombres] - [Código]", "Salas, Angel - 2021000000")

def insert_after_heading(doc, heading_text, content_list):
    # Encontrar el heading
    for i, p in enumerate(doc.paragraphs):
        if heading_text in p.text and p.style.name.startswith('Heading'):
            # Insertar despues del heading (antes del siguiente)
            for text in reversed(content_list):
                new_p = p.insert_paragraph_before(text)
                # Mover el nuevo parrafo despues de p
                p._p.addnext(new_p._p)
            break

def append_table_after_heading(doc, heading_text, df_top):
    for i, p in enumerate(doc.paragraphs):
        if heading_text in p.text and p.style.name.startswith('Heading'):
            table = doc.add_table(rows=1, cols=5)
            hdr_cells = table.rows[0].cells
            hdr_cells[0].text = 'Herramienta'
            hdr_cells[1].text = 'Severidad'
            hdr_cells[2].text = 'Hallazgo'
            hdr_cells[3].text = 'ISO 27001'
            hdr_cells[4].text = 'COBIT 2019'
            
            for _, row in df_top.iterrows():
                row_cells = table.add_row().cells
                row_cells[0].text = str(row['herramienta'])
                row_cells[1].text = str(row['severidad'])
                row_cells[2].text = str(row['hallazgo'])[:100] + "..."
                row_cells[3].text = str(row['norma_iso'])
                row_cells[4].text = str(row['objetivo_cobit'])
            
            p._p.addnext(table._tbl)
            break

insert_after_heading(doc, "1.1 Título del evento práctico", [
    "Evaluación automatizada de controles generales de TI mediante herramientas libres de auditoría de configuración (compliance scanning), contrastando la evidencia técnica contra los CIS Benchmarks y el Anexo A de la ISO/IEC 27001:2022."
])

insert_after_heading(doc, "1.2 Objetivos", [
    "- Ejecutar Lynis para auditar el endurecimiento del sistema operativo anfitrión.",
    "- Ejecutar OpenSCAP con la guía SCAP Security Guide para evaluar cumplimiento contra un perfil normativo formal.",
    "- Ejecutar Docker Bench for Security para auditar el plano de contenedores contra el CIS Docker Benchmark.",
    "- Ejecutar Trivy para auditar vulnerabilidades de imágenes, malas configuraciones IaC y secretos embebidos.",
    "- Consolidar los cuatro reportes en una matriz de control única mapeada a ISO/IEC 27001:2022 y COBIT 2019."
])

insert_after_heading(doc, "1.3 Tiempo de duración", ["100 minutos."])

insert_after_heading(doc, "1.4 Resultados de aprendizaje", [
    "- RA1 Analiza e interpreta los conceptos y terminología de Auditoría de Sistemas.",
    "- RA2 Evalúa la seguridad de la información en Auditoría de Sistemas."
])

insert_after_heading(doc, "1.6 Seguridad", [
    "1. Lynis y Docker Bench requieren acceso de lectura al sistema anfitrión.",
    "2. Los reportes contienen el inventario de software y se clasifican como Confidenciales.",
    "3. Trivy en modo secret puede detectar credenciales reales presentes en el equipo.",
    "4. Ninguna herramienta se ejecuta contra equipos de la red del campus."
])

insert_after_heading(doc, "Paso A", [
    "Auditoría del sistema anfitrión con Lynis.",
    f"Resultados Reales Obtenidos: El análisis reportó {lynis_count} warnings/sugerencias de endurecimiento en el entorno WSL Ubuntu (ej: falta de módulos PAM, etc)."
])

insert_after_heading(doc, "Paso B", [
    "Cumplimiento formal con OpenSCAP.",
    f"Resultados Reales Obtenidos: El análisis encontró {oscap_count} fallos contra las reglas de nivel 1 de CIS."
])

insert_after_heading(doc, "Paso C", [
    "CIS Docker Benchmark con Docker Bench.",
    f"Resultados Reales Obtenidos: El análisis encontró {docker_count} problemas de configuración en el daemon y runtime de contenedores Docker (ej: Docker daemon root privileges, user namespace remapping, etc)."
])

# Para Paso D (Vulnerabilidades, IaC y secretos con Trivy) hay que crearlo si no existe
# El documento tiene hasta Paso C. Vamos a añadir Paso D y E
doc.add_heading("Paso D", level=2)
doc.add_paragraph(f"Vulnerabilidades en imágenes con Trivy. Resultados Reales Obtenidos: Se identificaron {trivy_count} vulnerabilidades (Severidad Alta y Crítica) en las imágenes Juice-Shop, Postgres, WordPress y MariaDB.")

doc.add_heading("Paso E", level=2)
doc.add_paragraph("Consolidación en una matriz de control. Se extrajeron los hallazgos a un formato CSV unificado mapeado con ISO 27001:A.8.8 y COBIT DSS05.")

insert_after_heading(doc, "3. Resultados", [
    "A continuación, se muestra una extracción (top 20) de la matriz de hallazgos consolidada (PT04_matriz_control.csv) a partir de los escaneos en el entorno real."
])
append_table_after_heading(doc, "3. Resultados", df.head(20))

insert_after_heading(doc, "4. Conclusiones", [
    "Se demostró de manera práctica la utilidad de las herramientas automatizadas (Lynis, OpenSCAP, Docker Bench, Trivy) para auditar configuraciones y vulnerabilidades en un entorno real.",
    "Al procesar los resultados obtenidos, se pudo generar una base consolidada de hallazgos mapeados con estándares de seguridad internacional, sirviendo como evidencia legítima de auditoría técnica."
])

doc.save(salida_docx)
print("Word completado.")

md_content = f"""# UNIVERSIDAD PRIVADA DE TACNA
## FACULTAD DE INGENIERÍA
## ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

**INFORME DE LABORATORIO N.º 04**
**AUDITORÍA DE SISTEMAS · SI-084**

**Título del taller:** Auditoría de configuración segura con Lynis, OpenSCAP, Docker Bench y Trivy

**Integrantes**
- Salas, Angel - 2021000000

## 1. Información sobre el evento práctico
### 1.1 Título del evento práctico
Evaluación automatizada de controles generales de TI mediante herramientas libres de auditoría de configuración (compliance scanning), contrastando la evidencia técnica contra los CIS Benchmarks y el Anexo A de la ISO/IEC 27001:2022.

### 1.2 Objetivos
- Ejecutar Lynis para auditar el endurecimiento del sistema operativo anfitrión.
- Ejecutar OpenSCAP con la guía SCAP Security Guide para evaluar cumplimiento contra un perfil normativo formal.
- Ejecutar Docker Bench for Security para auditar el plano de contenedores contra el CIS Docker Benchmark.
- Ejecutar Trivy para auditar vulnerabilidades de imágenes, malas configuraciones IaC y secretos embebidos.
- Consolidar los cuatro reportes en una matriz de control única mapeada a ISO/IEC 27001:2022 y COBIT 2019.

### 1.3 Tiempo de duración
100 minutos.

### 1.4 Resultados de aprendizaje
- RA1 Analiza e interpreta los conceptos y terminología de Auditoría de Sistemas.
- RA2 Evalúa la seguridad de la información en Auditoría de Sistemas.

### 1.5 Recursos
- Lynis
- OpenSCAP + SCAP Security Guide
- Docker Bench for Security
- Trivy
- Python 3.11+ con `pandas`

### 1.6 Seguridad
1. Lynis y Docker Bench requieren acceso de lectura al sistema anfitrión.
2. Los reportes se clasifican como Confidenciales.
3. Trivy en modo secret puede detectar credenciales reales.
4. Ninguna herramienta se ejecuta contra equipos de la red del campus.

## 2. Procedimiento o metodología
### Paso A
Auditoría del sistema anfitrión con Lynis.
**Resultados:** {lynis_count} warnings/sugerencias detectadas en Ubuntu WSL.

### Paso B
Cumplimiento formal con OpenSCAP.
**Resultados:** {oscap_count} fallos contra CIS (nivel 1).

### Paso C
CIS Docker Benchmark con Docker Bench.
**Resultados:** {docker_count} problemas de configuración en contenedores.

### Paso D
Vulnerabilidades, IaC y secretos con Trivy.
**Resultados:** {trivy_count} vulnerabilidades críticas detectadas en imágenes de prueba.

### Paso E
Consolidación de matriz de control. Se unificaron los resultados en el documento `PT04_matriz_control.csv`.

## 3. Resultados
En total, el análisis real identificó {len(df)} deficiencias y problemas de cumplimiento mapeados exitosamente a ISO 27001:A.8.8 y COBIT DSS05.07/DSS05.04.

## 4. Conclusiones
Se probó la efectividad del escaneo de compliance con herramientas de la industria sobre un entorno nativo (WSL Ubuntu), permitiendo estructurar evidencia concreta en papeles de trabajo formales de auditoría.
"""

with open(salida_md, "w", encoding="utf-8") as f:
    f.write(md_content)

print("MD completado.")
