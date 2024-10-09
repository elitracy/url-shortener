from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import hashlib
import base64
import time

app = FastAPI()
BASE_URL: str = "http://localhost:8000"

class ShortenRequest(BaseModel):
    url: str

MAX_URL_LEN = 7

# Two tables for fast look up and to prevent multiple hashing for identical urls
url_short_table = {} # short_url -> url
url_long_table = {} # url -> short_url

def encode_url(url: str):
    """
    1. convert url to sha256 (HEX)
    2. slice sha256 to N characters
     - check for collision
     - if collision exists go to next slice
     - iterate till no more collisions or unable to store hash
    3. convert slice to base64
    """

    if url in url_long_table:
        return url_long_table[url]

    # convert url to sha256
    url_hash = hashlib.sha256(url.encode() + time.time().hex().encode())
    
    # use slices of sha256 hash when collisions are detected
    for i in range(0, url_hash.digest_size, MAX_URL_LEN):
        hash_slice = url_hash.digest()[i:i+MAX_URL_LEN] 
        url_code = base64.urlsafe_b64encode(hash_slice).decode('utf-8').rstrip('=')

        short_url = f"{BASE_URL}/r/{url_code[:MAX_URL_LEN]}"

        if short_url not in url_short_table:
            return url_code[:MAX_URL_LEN] 

    return None

def store_url(url: str, short_url: str):
    url_short_table[short_url] = url 
    url_long_table[url] = short_url

@app.post("/url/shorten")
async def url_shorten(request: ShortenRequest):
    """
    Given a URL, generate a short version of the URL that can be later resolved to the originally
    specified URL.

    Returns a url safe, base64, 7 character url
    """

    url_code = encode_url(request.url)
    if not url_code:
        raise HTTPException(status_code=400, detail={"Unable to safely shorten url"})

    short_url = f"{BASE_URL}/r/{url_code}"
    store_url(request.url, short_url)

    return {"short_url": short_url}


class ResolveRequest(BaseModel):
    short_url: str 


@app.get("/r/{url_code}")
async def url_resolve(url_code: str):
    """
    Return a redirect response for a valid shortened URL string.
    If the short URL is unknown, return an HTTP 404 response.
    """

    short_url = f"{BASE_URL}/r/{url_code}"
    if short_url not in url_short_table:
        raise HTTPException(status_code=404, detail="URL not found")

    return RedirectResponse(url_short_table[short_url]) 


@app.get("/")
async def index():
    return "Your URL Shortener is running!"
