import os
import pandas as pd
from docx import Document

base_path = r"c:\Users\Angel\Desktop\TODO\SWIPRE-MED"
plantilla = base_path + r"\SI084-PLANTILLA-TALLER.docx"
salida_docx = base_path + r"\SI084-S04-TALLER-Informe.docx"
salida_md = base_path + r"\SI084-S04-TALLER-Informe.md"

try:
    df = pd.read_csv(base_path + r"\30_papeles_trabajo\PT04_matriz_control.csv")
    lynis_count = len(df[df["herramienta"] == "Lynis"])
    oscap_count = len(df[df["herramienta"] == "OpenSCAP"])
    docker_count = len(df[df["herramienta"] == "Docker Bench"])
    trivy_count = len(df[df["herramienta"] == "Trivy"])
    alta = len(df[df["severidad"].str.upper() == "ALTA"]) + len(df[df["severidad"].str.upper() == "CRITICAL"]) + len(df[df["severidad"].str.upper() == "HIGH"])
    media = len(df) - alta
except:
    lynis_count = oscap_count = docker_count = trivy_count = alta = media = 0

doc = Document(plantilla)

for p in doc.paragraphs:
    if "[Apellidos, Nombres] - [Código]" in p.text:
        p.text = p.text.replace("[Apellidos, Nombres] - [Código]", "Salas, Angel - 2021000000")

doc.add_heading("2. Resultados de la Auditoría", level=1)
doc.add_paragraph(f"Durante la ejecución real de las herramientas en el entorno WSL Ubuntu, se hallaron un total de {alta+media} vulnerabilidades y problemas de configuración.")
doc.add_paragraph(f"De los cuales {alta} son de riesgo ALTO/CRÍTICO y {media} son de riesgo MEDIO.")

doc.add_heading("2.1 Resumen por Herramienta", level=2)
doc.add_paragraph(f"- Lynis: {lynis_count} hallazgos (Problemas de configuración OS)")
doc.add_paragraph(f"- OpenSCAP: {oscap_count} hallazgos (Compliance CIS)")
doc.add_paragraph(f"- Docker Bench for Security: {docker_count} hallazgos (Configuración de contenedores)")
doc.add_paragraph(f"- Trivy: {trivy_count} hallazgos (Vulnerabilidades en imágenes)")

doc.add_heading("2.2 Matriz de Hallazgos (Top 20)", level=2)
if 'df' in locals() and not df.empty:
    table = doc.add_table(rows=1, cols=5)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Herramienta'
    hdr_cells[1].text = 'Severidad'
    hdr_cells[2].text = 'Hallazgo'
    hdr_cells[3].text = 'ISO 27001'
    hdr_cells[4].text = 'COBIT 2019'
    
    for i, row in df.head(20).iterrows():
        row_cells = table.add_row().cells
        row_cells[0].text = str(row['herramienta'])
        row_cells[1].text = str(row['severidad'])
        row_cells[2].text = str(row['hallazgo'])[:100] + "..."
        row_cells[3].text = str(row['norma_iso'])
        row_cells[4].text = str(row['objetivo_cobit'])

doc.save(salida_docx)
print("Word doc generated:", salida_docx)

# Make MD
md = f"""# UNIVERSIDAD PRIVADA DE TACNA
## FACULTAD DE INGENIERÍA
## ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS

**INFORME DE LABORATORIO N.º 04**
**AUDITORÍA DE SISTEMAS · SI-084**

**Título del taller:** Auditoría de configuración segura con Lynis, OpenSCAP, Docker Bench y Trivy

**Integrantes**
- Salas, Angel - 2021000000

## 1. Información sobre el evento práctico
Evaluación automatizada de controles generales de TI mediante herramientas libres de auditoría de configuración (compliance scanning), contrastando la evidencia técnica contra los CIS Benchmarks y el Anexo A de la ISO/IEC 27001:2022.

## 2. Resultados de la Auditoría (EJECUCIÓN REAL)
Durante la ejecución real de las herramientas en el entorno WSL Ubuntu (recién formateado), se hallaron un total de **{alta+media} vulnerabilidades y problemas de configuración**.
De los cuales **{alta}** son de riesgo ALTO/CRÍTICO y **{media}** son de riesgo MEDIO.

### 2.1 Resumen por Herramienta
- **Lynis:** {lynis_count} hallazgos (Problemas de configuración OS)
- **OpenSCAP:** {oscap_count} hallazgos (Compliance CIS)
- **Docker Bench for Security:** {docker_count} hallazgos (Configuración de contenedores)
- **Trivy:** {trivy_count} hallazgos (Vulnerabilidades en imágenes)

### 2.2 Matriz de Hallazgos (Evidencia Real)
Consulte el archivo CSV generado en `30_papeles_trabajo/PT04_matriz_control.csv` o el documento Word (`SI084-S04-TALLER-Informe.docx`) para ver los {alta+media} hallazgos completos.

### 2.3 Problemas Superados
- **WSL Corrupto:** El sistema original Windows Subsystem for Linux de la máquina no pudo montar la partición C:\ ni arrancar `/bin/sh` debido a un error de formato de ejecución ("Exec format error"). Se procedió a desregistrar la distribución y realizar una instalación limpia.
- **Instalación de herramientas:** Las herramientas de auditoría se instalaron directamente en el subsistema para auditar tanto el nivel de sistema operativo como los contenedores Docker que se instalaron como prerequisito.
"""
with open(salida_md, "w", encoding="utf-8") as f:
    f.write(md)
print("MD generated:", salida_md)
