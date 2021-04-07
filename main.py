from fastapi import FastAPI, Security, Depends, HTTPException
import io, os, zipfile
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from starlette.responses import StreamingResponse, RedirectResponse, JSONResponse, FileResponse, Response
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
def get_albums(api_key: APIKey = Depends(get_api_key), access_token : str = None):
    db = connect_db()
    cur = db.cursor()
    cur.execute("SELECT id, description, date FROM albums")
    mesures = cur.fetchall() 
    cur.close()
    del cur
    db.close()
    return mesures

@app.get("/firstphoto")
def get_albums(id_album, api_key: APIKey = Depends(get_api_key), access_token : str = None):
    db = connect_db()
    cur = db.cursor()
    cur.execute("SELECT nom, measuredate FROM photos WHERE id_album like "+str(id_album)+" ORDER BY nom LIMIT 1")
    photos = cur.fetchone() 
    cur.close()
    del cur
    db.close()

    print(photos[0])

    path = "/photos/remote/"

    return FileResponse(path+photos[0], media_type="image/jpeg")


@app.get("/photos")
def get_albums(id_album, api_key: APIKey = Depends(get_api_key), access_token : str = None):
    db = connect_db()
    cur = db.cursor()
    cur.execute("SELECT nom, measuredate  FROM photos WHERE id_album like "+str(id_album))
    photos = cur.fetchall() 
    cur.close()
    del cur
    db.close()

    path = "/photos/remote/"
    zip_filename=photos[0][0].split("/")[0]+".zip"
    s = io.BytesIO()
    zf = zipfile.ZipFile(s, "w")

    photoTab = []
    
    for p in photos:
        file_path = os.path.join(path, p[0])
        # if os.path.exists(file_path):
        zf.write(file_path, p[0].split("/")[1])
        # photoTab.append(FileResponse(file_path, media_type="image/jpeg", filename=p[0].split("/")[1]))

        # photoTab.append(FileResponse("/photos/remote/"+p[0], media_type="image/jpeg"))
    zf.close()

    resp = Response(s.getvalue(), media_type="application/x-zip-compressed", headers={
        'Content-Disposition': f'attachment;filename={zip_filename}'
    })

    return resp
