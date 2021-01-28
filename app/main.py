from typing import Optional
from datetime import date
from fastapi import FastAPI, Security, Depends, HTTPException, BackgroundTasks
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
import adafruit_dht
import board
import json
import subprocess
import sys
import os
import time
import logging
import picamera
from datetime import datetime
from time import sleep

# Variables globales
API_KEY = "!$j;,=QzViep^\ZP~9_pWg[[{8p*3d9ZP9NxxB5XFDNpB5Btv~"
API_KEY_NAME = "access_token"
COOKIE_DOMAIN = "ryzen.ddns.net"


api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)

app = FastAPI()

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

__output_folder_name__= '/home/pi/camera/'

__default_rotation__ = 0

dhtDevice = adafruit_dht.DHT22(board.D18)

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

class Data():
    isRunning : bool = False
    stopTimelapse : bool = False

#  Fonctions

# Fonctions associées à FastAPI

async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
):

    if api_key_query == API_KEY:
        return api_key_query
    elif api_key_header == API_KEY:
        return api_key_header
    elif api_key_cookie == API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

@app.get("/")
def read_root():
    return {"Hello": "World"}



@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/timelapse/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.get("/timelapse/start/", tags=["timelapse"])
async def start_timelapse(background_tasks: BackgroundTasks, api_key: APIKey = Depends(get_api_key), access_token : str = None, length_in_seconds: int = 1, interval_in_seconds: int = 1, rotation: int = 0, iso : int = 0, shutter_speed : int = 0, autoWhiteBalance : bool = True):
    start_time = time.time()
    # Take pictures
    stopTimelapse = False
    background_tasks.add_task(capture_images ,length_in_seconds, interval_in_seconds, rotation, iso, shutter_speed, autoWhiteBalance)
    return "Timelapse démarré"


@app.get("/timelapse/status/", tags=["timelapse"])
def is_timelapse(api_key: APIKey = Depends(get_api_key), access_token : str = None):
    return Data.isRunning


@app.get("/timelapse/stop/", tags=["timelapse"])
def stop_timelapse(api_key: APIKey = Depends(get_api_key), access_token : str = None):
    Data.stopTimelapse = True
    return "Timelapse arrété"

@app.get("/dht/value/", tags=["dht"])
def get_th_value(api_key: APIKey = Depends(get_api_key), access_token : str = None):
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        return(
            "Température: {:.1f}°C    Humidité: {}% ".format(
                temperature_c, humidity
            )
        )
 
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        return(error.args[0])
        time.sleep(2.0)
    except Exception as error:
        dhtDevice.exit()
        raise error

# Fonctions de Timelapse

def camera_options(camera, iso, rotation, shutter_speed, autoWhiteBalance):
    camera.iso = iso
    camera.rotation = rotation
    camera.shutter_speed = shutter_speed

    if(shutter_speed != 0):
        # Sleep to allow the shutter speed to take effect correctly.
        sleep(1)
        camera.exposure_mode = 'off'

    if(not autoWhiteBalance):
        camera.awb_mode = 'off'

    return camera

def capture_images(length_in_seconds, interval_in_seconds, rotation, iso, shutter_speed, autoWhiteBalance):
    Data.isRunning = True
    count = length_in_seconds / interval_in_seconds
    logging.info('Taking {} shots...'.format(count))
    now = datetime.now()
    dateTimelapse = now.strftime("%d-%m-%Y_%H:%M:%S")
    path = __output_folder_name__+dateTimelapse
    if not os.path.exists(path):
        os.makedirs(path)
    print(path)

    with picamera.PiCamera() as camera:
        camera.start_preview()
        camera_options(camera, iso, rotation, shutter_speed, autoWhiteBalance)
        time.sleep(2)
        for filename in camera.capture_continuous(__output_folder_name__+dateTimelapse+'/img{counter:06d}.jpg'):
            time.sleep(interval_in_seconds) # wait <interval_in_seconds> seconds
            count -= 1
            if count <= 0 or Data.stopTimelapse:
                Data.stopTimelapse = False
                break

    Data.isRunning = False