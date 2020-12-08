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
uvicorn main:app --reload
```
