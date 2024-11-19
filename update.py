import time
import urllib.parse

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import threading, logging, glob
import sys, os,  re, requests, binascii, datetime
from config import LOG_HANDLE, LOG_FILE, LOG_LEVEL
from logging.handlers import RotatingFileHandler

#  enable logging
top_log_handle = LOG_HANDLE
log = logging.getLogger(top_log_handle)

LOG_FILENAME = os.path.join(sys.path[0], f'log/{LOG_FILE}.txt')
try:
    log_level = getattr(logging, LOG_LEVEL)
except:
    log_level = getattr(logging, 'INFO')
log.setLevel(log_level)
log_handler = RotatingFileHandler(LOG_FILENAME, maxBytes=1024 * 1024, backupCount=20)
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
log_handler.setFormatter(log_formatter)
log.addHandler(log_handler)

# 0.1 initial version, start from fastapi-rfidusb 0.9

version = "0.1"

#  uvicorn.exe update:app

log.info("start")

app = FastAPI()
origins = ["*",]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"])


class ApiStartUpdate(BaseModel):
    url: str
    key: str
    from_version: float
    to_version: float


@app.post("/start")
def start(data: ApiStartUpdate):
    url = urllib.parse.unquote(data.url)
    url = urllib.parse.unquote(url)
    log.info(f"Start update from server: {url}")
    try:
        ret = requests.get(f"{url}?versions={data.from_version}-{data.to_version}", headers={'x-api-key': data.key})
    except Exception as e:
        log.error(f"requests.get error: {e}")
        return "nok"
    if ret.status_code == 200:
        try:
            res = ret.json()
            print(res)
            data = res["data"]
            if res["status"]:
                pass
                # stop the badgereader task
                # update the database
                # update the config file
                # git pull
                # start badgereader task

            else:
                log.error(f"get update data returned error: {data}")
        except Exception as e:
            log.error(f"ret.json() error: {e}")
            return "nok"
    return "ok"


