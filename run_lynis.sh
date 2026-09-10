cd /mnt/c/Users/Angel/Desktop/TODO/SWIPRE-MED
mkdir -p 20_evidencia/E04_config
docker run --rm --pid host --net host -v /:/rootfs:ro -v "$PWD":/salida docker.io/cisofy/lynis:latest audit system --forensics --report-file /salida/20_evidencia/E04_config/lynis-report.dat | tee 20_evidencia/E04_config/lynis-consola.txt
