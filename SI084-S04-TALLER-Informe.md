# UNIVERSIDAD PRIVADA DE TACNA
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
**Resultados:** 38 warnings/sugerencias detectadas en Ubuntu WSL.

### Paso B
Cumplimiento formal con OpenSCAP.
**Resultados:** 0 fallos contra CIS (nivel 1).

### Paso C
CIS Docker Benchmark con Docker Bench.
**Resultados:** 25 problemas de configuración en contenedores.

### Paso D
Vulnerabilidades, IaC y secretos con Trivy.
**Resultados:** 420 vulnerabilidades críticas detectadas en imágenes de prueba.

### Paso E
Consolidación de matriz de control. Se unificaron los resultados en el documento `PT04_matriz_control.csv`.

## 3. Resultados
En total, el análisis real identificó 483 deficiencias y problemas de cumplimiento mapeados exitosamente a ISO 27001:A.8.8 y COBIT DSS05.07/DSS05.04.

## 4. Conclusiones
Se probó la efectividad del escaneo de compliance con herramientas de la industria sobre un entorno nativo (WSL Ubuntu), permitiendo estructurar evidencia concreta en papeles de trabajo formales de auditoría.
