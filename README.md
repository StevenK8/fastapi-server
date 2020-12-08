# Timelapse

1. Installation de docker:
```bash
`sudo curl -sSL https://get.docker.com/ | sh`
```

2. Build de l'image FastAPI:
```bash
docker build -t myimage .
```

3. Démarrage d'un conteneur basé sur cette image:
```bash
docker run -d --name mycontainer -p 80:80 myimage
```
