# Timelapse

## FastAPI

1. Installation de dépendances:
```bash
sudo apt install python3-pip python3-picamera; python3 -m pip install --upgrade pip bcrypt
```

2. Installation de rust:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

rustup install nightly

rustup default nightly
```

3. Installation de FastAPI:
```bash
python3 -m pip install fastapi uvicorn
```

4. Ajout de uvicorn à la variable $PATH:
```bash
export PATH=/usr/local/bin:/usr/local/sbin:/home/pi/.local/bin:$PATH
```

5. Démarrage du serveur web:
```bash
cd Timelapse/app

uvicorn main:app --reload --host 192.168.1.21
```

6. Accès à la doc:
```bash
http://192.168.1.21:8000/docs
```

## Rclone

```bash
curl https://rclone.org/install.sh | sudo bash
```

```bash
*/5 * * * * rclone move /home/pi/camera/ timelapse:/home/timelapse/photos --delete-empty-src-dirs &
```

## Vidéo

```bash
ffmpeg -framerate 30 -pattern_type glob -i "*.jpg" -s:v 1920x1080 -c:v libx264 -crf 17 -pix_fmt yuv420p timelapse_${PWD##*/}.mp4
```

## Fastapi serveur

```dockerfile
version: '3.3'
services:
  traefik:
    image: traefik:latest
    container_name: traefik
    # Enables the web UI and tells Traefik to listen to docker
    command:
       ## API
       - --api.dashboard=true # <== Enabling the dashboard to view services, middlewares, routers, etc...
       ## Providers
       - --providers.docker=true # <== Enabling docker as the provider for traefik
       - --providers.docker.exposedbydefault=false # <== Don't expose every container to traefik, only expose enabled ones
       - --providers.file.filename=/dynamic.yaml # <== Referring to a dynamic configuration file
       - --providers.docker.network=web # <== Operate on the docker network named web
       ## Entrypoints Settings - https://docs.traefik.io/routing/entrypoints/#configuration ##
       - --entrypoints.web.address=:80 # <== Defining an entrypoint for port :80 named web
       - --entrypoints.web-secured.address=:443 # <== Defining an entrypoint for https on port :443 named web-secured
       ## Certificate Settings (Let's Encrypt) -  https://docs.traefik.io/https/acme/#configuration-examples ##
       - --certificatesresolvers.mytlschallenge.acme.tlschallenge=true # <== Enable TLS-ALPN-01 to generate and renew ACME certs
       - --certificatesresolvers.mytlschallenge.acme.email=steven.k8@protonmail.com # <== Setting email for certs
       - --certificatesresolvers.mytlschallenge.acme.storage=/letsencrypt/acme.json # <== Defining acme file to store cert information
    ports:
      # The HTTP port
      - "80:80"
      # The Web UI (enabled by --api.insecure=true)
      - "8080:8080"
      - "443:443" # <== https
    volumes:
      - "./traefik/letsencrypt:/letsencrypt"
      # So that Traefik can listen to the Docker events
      - /var/run/docker.sock:/var/run/docker.sock
      - ./traefik/dynamic.yaml:/dynamic.yaml # <== Volume for dynamic conf file
    networks:
      - web # <== Placing traefik on the network named web, to access containers on this network
    labels:
    #### Labels define the behavior and rules of the traefik proxy for this container ####
      - "traefik.enable=true" # <== Enable traefik on itself to view dashboard and assign subdomain to view it
      - traefik.http.routers.monitor.rule=Host(`monitor.stevenkerautret.eu`)
      - traefik.http.routers.monitor.tls=true
      - traefik.http.routers.monitor.service=api@internal
      - traefik.http.routers.monitor.tls.certresolver=mytlschallenge
    restart : always

fastapi:
    container_name: fastapi
    ports:
      - '6000:80'
    image: tiangolo/uvicorn-gunicorn-fastapi:python3.7
    volumes:
      - './app:/app'
    networks:
      - web
    labels:
      #### Labels define the behavior and rules of the traefik proxy for this container ####
      - "traefik.enable=true" # <== Enable traefik to proxy this container
      - "traefik.http.routers.fastapi-web.entrypoints=web" # <== Defining the entrypoint for http
      - "traefik.http.routers.fastapi-web.middlewares=redirect@file" # <== This is a middleware to redirect to https
      - "traefik.http.routers.fastapi-secured.entrypoints=web-secured" # <== Defining entrypoint for https
      - "traefik.http.routers.fastapi-secured.tls.certresolver=mytlschallenge" # <== Defining certsresolvers for https
      - "traefik.http.routers.fastapi-web.rule=Host(`fastapi.stevenkerautret.eu`)"
      - "traefik.http.routers.fastapi-secured.rule=Host(`fastapi.stevenkerautret.eu`)"

networks:
  web:
    external: true
  backend:
    external: false

```

```bash
pip3 install pymysql

pip3 install aiofiles
```


## Documentation de FastAPI

[FastAPI](https://fastapi.tiangolo.com/)

# Capteur DHT

## Dépendances

```bash
sudo apt install python-mysqldb


docker exec -it fastapi bash

python3 -m pip install PyMySQL
```

## Crontab

```bash
*/5 * * * * python3 /home/pi/Timelapse/logger-temp-hum.py &> /dev/null
```

