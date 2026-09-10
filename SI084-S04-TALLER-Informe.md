# UNIVERSIDAD PRIVADA DE TACNA
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
Durante la ejecución real de las herramientas en el entorno WSL Ubuntu (recién formateado), se hallaron un total de **483 vulnerabilidades y problemas de configuración**.
De los cuales **421** son de riesgo ALTO/CRÍTICO y **62** son de riesgo MEDIO.

### 2.1 Resumen por Herramienta
- **Lynis:** 38 hallazgos (Problemas de configuración OS)
- **OpenSCAP:** 0 hallazgos (Compliance CIS)
- **Docker Bench for Security:** 25 hallazgos (Configuración de contenedores)
- **Trivy:** 420 hallazgos (Vulnerabilidades en imágenes)

### 2.2 Matriz de Hallazgos (Evidencia Real)
Consulte el archivo CSV generado en `30_papeles_trabajo/PT04_matriz_control.csv` o el documento Word (`SI084-S04-TALLER-Informe.docx`) para ver los 483 hallazgos completos.

### 2.3 Problemas Superados
- **WSL Corrupto:** El sistema original Windows Subsystem for Linux de la máquina no pudo montar la partición C:\ ni arrancar `/bin/sh` debido a un error de formato de ejecución ("Exec format error"). Se procedió a desregistrar la distribución y realizar una instalación limpia.
- **Instalación de herramientas:** Las herramientas de auditoría se instalaron directamente en el subsistema para auditar tanto el nivel de sistema operativo como los contenedores Docker que se instalaron como prerequisito.
