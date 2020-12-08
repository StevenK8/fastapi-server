# Timelapse

1. Installation de FastAPI:
```bash
pip3 install fastapi[all]
```

2. Ajout de uvicorn à la variable $PATH:
```bash
export PATH=/usr/local/bin:/usr/local/sbin:/home/pi/.local/bin:$PATH
```

3. Démarrage du serveur web:
```bash
uvicorn main:app --reload --host 192.168.1.IP
```

4. Accès à la doc:
##http://192.168.1.IP:8000/docs
