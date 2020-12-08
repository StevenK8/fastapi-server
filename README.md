# Timelapse

Build your FastAPI image:
docker build -t myimage .

Run a container based on your image:
docker run -d --name mycontainer -p 80:80 myimage
