from fastapi import FastAPI, Security, Depends, HTTPException
import io
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from starlette.responses import StreamingResponse, RedirectResponse, JSONResponse
from starlette.status import HTTP_403_FORBIDDEN
import logging
import pymysql

# Variables globales
API_KEY = "F><aw;v)9H4JRY=4#g@}YN68b$%6!j9F8g=V2^Kr^8s:([N7(]"
API_KEY_NAME = "access_token"
COOKIE_DOMAIN = "stevenkerautret.eu"


api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)


app = FastAPI()

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

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
def read_item(item_id: int, api_key: APIKey = Depends(get_api_key), access_token : str = None):
    return {"item_id": item_id}

@app.post("/vector_image")
def image_endpoint(*, vector):
    # Returns a cv2 image array from the document vector
    cv2img = my_function(vector)
    res, im_png = cv2.imencode(".png", cv2img)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")

def connect_db():
    return pymysql.connect(host='ryzen.ddns.net',user='timelapse', passwd='9_7b:r%HR-G%y@*U;>*3KDrU!-v,65U]Wq6H.xT5G}uiPAE}8k', db='timelapse')

@app.get("/th")
def get_th_data(first_date, last_date, api_key: APIKey = Depends(get_api_key), access_token : str = None):
    db = connect_db()
    cur = db.cursor()
    cur.execute("SELECT temperature, humidity, date FROM mesures WHERE date >'"+str(first_date)+"' AND date <'"+str(last_date)+"'")
    mesures = cur.fetchall() 
    cur.close()
    del cur
    db.close()
    return mesures

@app.get("/albums")
def get_albums(first_date, last_date, api_key: APIKey = Depends(get_api_key), access_token : str = None):
    db = connect_db()
    cur = db.cursor()
    cur.execute("SELECT id, description, date FROM albums WHERE date >'"+str(first_date)+"' AND date <'"+str(last_date)+"'")
    mesures = cur.fetchall() 
    cur.close()
    del cur
    db.close()
    return mesures

@app.get("/photos")
def get_albums(first_date, last_date, api_key: APIKey = Depends(get_api_key), access_token : str = None):
    db = connect_db()
    cur = db.cursor()
    cur.execute("SELECT id, description, date FROM albums WHERE date >'"+str(first_date)+"' AND date <'"+str(last_date)+"'")
    mesures = cur.fetchall() 
    cur.close()
    del cur
    db.close()
    return mesures
