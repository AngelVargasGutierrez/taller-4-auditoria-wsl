import pandas as pd, json, re, glob
import os

filas = []
base_path = r"c:\Users\Angel\Desktop\TODO\SWIPRE-MED"

# --- Lynis ---
try:
    with open(base_path + r"\20_evidencia\E04_config\lynis-report.dat", encoding="utf-8") as f:
        for l in f:
            if l.startswith("warning[]=") or l.startswith("suggestion[]="):
                tipo = "warning" if l.startswith("warning") else "suggestion"
                filas.append(dict(herramienta="Lynis", severidad="Alta" if tipo=="warning" else "Media",
                                  hallazgo=l.split("=",1)[1].strip()[:160]))
except Exception as e: print("Lynis err", e)

# --- OpenSCAP ---
try:
    with open(base_path + r"\20_evidencia\E04_config\oscap-resultados.xml", encoding="utf-8") as f:
        c = f.read()
        for r in re.findall(r'<rule-result.*?idref="(.*?)".*?<result>(.*?)</result>', c, re.S):
            if r[1].strip() in ["fail", "error"]:
                filas.append(dict(herramienta="OpenSCAP", severidad="Alta", hallazgo=r[0]))
except Exception as e: print("OSCAP err", e)

# --- Docker Bench ---
try:
    with open(base_path + r"\20_evidencia\E04_config\docker-bench.log", encoding="utf-8") as f:
        for l in f:
            if "[WARN]" in l:
                filas.append(dict(herramienta="Docker Bench", severidad="Media", hallazgo=re.sub(r'\x1b\[[0-9;]*m', '', l).replace("[WARN]","").strip()[:160]))
except Exception as e: print("Docker err", e)

# --- Trivy ---
try:
    for arch in glob.glob(base_path + r"\20_evidencia\E04_config\trivy_*.json"):
        with open(arch, encoding="utf-8") as f:
            d = json.load(f)
            for r in d.get("Results", []):
                for v in r.get("Vulnerabilities", []):
                    filas.append(dict(herramienta="Trivy", severidad=v.get("Severity","Alta"),
                                      hallazgo=f"{v.get('VulnerabilityID')}: {v.get('Title','')}"))
except Exception as e: print("Trivy err", e)

df = pd.DataFrame(filas)
if df.empty:
    print("No se encontraron hallazgos")
else:
    df["norma_iso"] = "A.8.8"
    df["objetivo_cobit"] = "DSS05.07"
    df.loc[df["herramienta"]=="Lynis", "objetivo_cobit"] = "DSS05.04"
    df.to_csv(base_path + r"\30_papeles_trabajo\PT04_matriz_control.csv", index=False)
    print(df)
