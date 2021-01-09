from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


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


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.route("/starttimelapse")
def start_timelapse(t: int = 30000, tl: int = 2000):
	subprocess.run("raspistill -t".split()+str(t)+" -tl "+str(tl)+" -o image%04d.jpg".split())
	return "Démarrage du timelapse : une photo toutes les "+str(tl)+"s pendant "+str(t)+"s"
