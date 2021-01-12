from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
import subprocess

app = FastAPI()

proc = subprocess


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/timelapse/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.route("/timelapse/start/")
def start_timelapse(t: int = 30000, tl: int = 2000):
    cmd = "raspistill -t"+str(t)+"-tl"+str(tl)+"-o image%04d.jpg"
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    return "Démarrage du timelapse : une photo toutes les "+str(tl)+"s pendant "+str(t)+"s"


@app.get("/timelapse/status/")
def is_timelapse():
    # cmd = "ps aux | grep raspistill | wc -l"

    # process = subprocess.Popen(cmd.split(),
    #                            stdout=subprocess.PIPE,
    #                            stderr=subprocess.STDOUT)
    # returncode = process.wait()
    # print(returncode)
    return("Timelapse returned {}".format(proc==0))


@app.get("/timelapse/stop/")
def stop_timelapse():
    proc.kill()
