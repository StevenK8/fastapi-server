from typing import Optional
from datetime import date
from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import sys
import os
import time
import logging
import picamera
from datetime import datetime
from time import sleep

app = FastAPI()

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

now = datetime.now()

__output_folder_name__= '/home/pi/camera/'

__default_rotation__ = 0


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

#  Fonctions

# Fonctions associées à FastAPI

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/timelapse/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.get("/timelapse/start/")
def start_timelapse(length_in_seconds: int = 16, interval_in_seconds: int = 2, rotation: int = 0, iso : int = 0, shutter_speed : int = 0, autoWhiteBalance : bool = True):
    start_time = time.time()

    # Take pictures
    logging.info('Opening camera...')
    capture_images(length_in_seconds, interval_in_seconds, rotation, iso, shutter_speed, autoWhiteBalance)
    # logging.info('Writing timestamps...')

    # # Write timestamps to images
    # write_timestamps(72,32,__output_folder_name__)
    # logging.info('Captured images {} seconds to run'.format(str(time.time() - start_time)))

    return "Timelapse terminé"


@app.get("/timelapse/status/")
def is_timelapse():
    # process = subprocess.Popen(cmd.split(),
    #                            stdout=subprocess.PIPE,
    #                            stderr=subprocess.STDOUT)
    # returncode = process.wait()
    # print(returncode)
    return("Timelapse returned {}".format(proc==0))


@app.get("/timelapse/stop/")
def stop_timelapse():
    proc.kill()


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
    count = length_in_seconds / interval_in_seconds
    logging.info('Taking {} shots...'.format(count))
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
            if count <= 0:
                break