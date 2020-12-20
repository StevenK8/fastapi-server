# Timelapse

## Raspberry Pi

1. Installation de pip:
```bash
sudo apt install python3-pip

python3 -m pip install --upgrade pip bcrypt
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
uvicorn main:app --reload --host 192.168.1.IP
```

6. Accès à la doc:
```bash
http://192.168.1.IP:8000/docs
```

## Documentation de FastAPI

[FastAPI](https://fastapi.tiangolo.com/)

