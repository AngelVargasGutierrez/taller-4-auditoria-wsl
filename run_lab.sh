#!/bin/bash
cd /mnt/c/Users/Angel/Desktop/TODO/SWIPRE-MED
mkdir -p 20_evidencia/E04_config

echo "=== PASO A: Lynis ==="
apt-get update -qq
apt-get install -y -qq lynis > /dev/null
lynis audit system --forensics --report-file 20_evidencia/E04_config/lynis-report.dat > 20_evidencia/E04_config/lynis-consola.txt || true

echo "=== PASO B: OpenSCAP ==="
apt-get install -y -qq libopenscap8 ssg-debderived >/dev/null
UBUNTU_VER=$(lsb_release -rs | tr -d '.')
OSCAP_FILE="/usr/share/xml/scap/ssg/content/ssg-ubuntu${UBUNTU_VER}-ds.xml"
if [ ! -f "$OSCAP_FILE" ]; then
  OSCAP_FILE="/usr/share/xml/scap/ssg/content/ssg-ubuntu2204-ds.xml"
fi
oscap xccdf eval --profile xccdf_org.ssgproject.content_profile_cis_level1_server --results 20_evidencia/E04_config/oscap-resultados.xml --report 20_evidencia/E04_config/oscap-reporte.html "$OSCAP_FILE" > 20_evidencia/E04_config/oscap-consola.txt || true

echo "=== PASO C: Docker Bench ==="
cd /mnt/c/Users/Angel/Desktop/TODO/SWIPRE-MED
if [ ! -d "docker-bench-security" ]; then
  git clone --depth 1 https://github.com/docker/docker-bench-security.git
fi
cd docker-bench-security
sh docker-bench-security.sh -l ../20_evidencia/E04_config/docker-bench.log || true

echo "=== PASO D: Trivy ==="
cd /mnt/c/Users/Angel/Desktop/TODO/SWIPRE-MED
apt-get install -y wget apt-transport-https gnupg lsb-release > /dev/null
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor | tee /usr/share/keyrings/trivy.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | tee -a /etc/apt/sources.list.d/trivy.list
apt-get update -qq
apt-get install -y -qq trivy > /dev/null
# Pull the images first
service docker start
docker pull bkimminich/juice-shop:latest
docker pull postgres:16
docker pull wordpress:latest
docker pull mariadb:11
# Run Trivy
for IMG in bkimminich/juice-shop:latest postgres:16 wordpress:latest mariadb:11; do
  N=$(echo $IMG | tr '/:' '__')
  trivy image --severity HIGH,CRITICAL --format json -o 20_evidencia/E04_config/trivy_${N}.json $IMG || true
done
trivy image --format cyclonedx -o 20_evidencia/E04_config/sbom_juiceshop.json bkimminich/juice-shop:latest || true

echo "=== PASO E: Matrix ==="
apt-get install -y -qq python3-pandas python3 > /dev/null
python3 30_papeles_trabajo/PT04_matriz_control.py > 20_evidencia/E04_config/salida_script_wsl.txt || true
