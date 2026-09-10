import pandas as pd
from docx import Document
from docx.shared import Pt
import sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base_path = r"D:\10MO\AUDI\taller 3"
salida_docx = base_path + r"\SI084-S04-TALLER-Informe.docx"
salida_md = base_path + r"\SI084-S04-TALLER-Informe.md"

doc = Document(salida_docx)

def add_apa_paragraph(doc, text, insert_after_p):
    new_p = insert_after_p.insert_paragraph_before(text)
    new_p.style = doc.styles['Normal']
    insert_after_p._p.addnext(new_p._p)
    return new_p

for p in doc.paragraphs:
    txt = p.text.strip()
    
    if "5. Cuestionario" in txt:
        add_apa_paragraph(doc, "Pregunta de transferencia: ¿Qué riesgo correría una organización real si esto se hiciera mal?", p)
        add_apa_paragraph(doc, "Respuesta: Si una organización omite la automatización y gestión de la configuración segura (mediante compliance scanning, SBOM, etc.), se expondría a riesgos críticos de ciberseguridad. Al no tener visibilidad sobre vulnerabilidades de dependencias ni deficiencias de configuración en sus contenedores (como el montaje del socket de Docker), un atacante podría explotar fácilmente las fallas y escalar privilegios desde la aplicación hacia el sistema operativo anfitrión. Esto no solo facilitaría el compromiso total de la infraestructura, sino que conllevaría a graves sanciones legales por incumplimiento de normativas internacionales como ISO/IEC 27001 o la pérdida de certificaciones, impactando directamente en la continuidad del negocio y la reputación de la empresa.", p)

    elif "6. Referencias bibliográficas" in txt:
        add_apa_paragraph(doc, "Aqua Security. (s.f.). Trivy Documentation. https://trivy.dev/", p)
        add_apa_paragraph(doc, "Center for Internet Security. (s.f.). CIS Benchmarks. https://www.cisecurity.org/cis-benchmarks", p)
        add_apa_paragraph(doc, "CISOfy. (s.f.). Lynis — Security auditing tool. https://cisofy.com/lynis/", p)
        add_apa_paragraph(doc, "ISACA. (2018). COBIT 2019 Framework: Governance and Management Objectives. https://www.isaca.org/resources/cobit", p)
        add_apa_paragraph(doc, "ISO. (2022). ISO/IEC 27001:2022 Information security, cybersecurity and privacy protection — Information security management systems — Requirements. https://www.iso.org/standard/27001", p)
        add_apa_paragraph(doc, "OpenSCAP Project. (s.f.). OpenSCAP Project. https://www.open-scap.org/", p)

    elif "7. Anexos" in txt:
        add_apa_paragraph(doc, "Anexo A: Reporte completo de configuración extraído (docker-bench.log, lynis-consola.txt).", p)
        add_apa_paragraph(doc, "Anexo B: Matriz consolidada de hallazgos (PT04_matriz_control.csv).", p)
        add_apa_paragraph(doc, "Anexo C: Inventario de componentes (sbom_juiceshop.json).", p)

doc.save(salida_docx)

# Update the MD file by appending these sections
md_appendix = """
## 5. Cuestionario
**Pregunta de transferencia: ¿Qué riesgo correría una organización real si esto se hiciera mal?**
Respuesta: Si una organización omite la automatización y gestión de la configuración segura (mediante compliance scanning, SBOM, etc.), se expondría a riesgos críticos de ciberseguridad. Al no tener visibilidad sobre vulnerabilidades de dependencias ni deficiencias de configuración en sus contenedores (como el montaje del socket de Docker), un atacante podría explotar fácilmente las fallas y escalar privilegios desde la aplicación hacia el sistema operativo anfitrión. Esto no solo facilitaría el compromiso total de la infraestructura, sino que conllevaría a graves sanciones legales por incumplimiento de normativas internacionales como ISO/IEC 27001 o la pérdida de certificaciones, impactando directamente en la continuidad del negocio y la reputación de la empresa.

## 6. Referencias bibliográficas
- Aqua Security. (s.f.). Trivy Documentation. https://trivy.dev/
- Center for Internet Security. (s.f.). CIS Benchmarks. https://www.cisecurity.org/cis-benchmarks
- CISOfy. (s.f.). Lynis — Security auditing tool. https://cisofy.com/lynis/
- ISACA. (2018). COBIT 2019 Framework: Governance and Management Objectives. https://www.isaca.org/resources/cobit
- ISO. (2022). ISO/IEC 27001:2022 Information security, cybersecurity and privacy protection — Information security management systems — Requirements. https://www.iso.org/standard/27001
- OpenSCAP Project. (s.f.). OpenSCAP Project. https://www.open-scap.org/

## 7. Anexos
- Anexo A: Reporte completo de configuración extraído (docker-bench.log, lynis-consola.txt).
- Anexo B: Matriz consolidada de hallazgos (PT04_matriz_control.csv).
- Anexo C: Inventario de componentes (sbom_juiceshop.json).
"""

with open(salida_md, "a", encoding="utf-8") as f:
    f.write(md_appendix)

print("Anexos agregados")
