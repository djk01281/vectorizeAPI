# main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import httpx
import asyncio
import os
import vtracer
import requests

app = FastAPI()

async def download_image(url: str, local_path: str) -> None:
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_path, 'wb') as file:
            file.write(response.content)
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Failed to download image from {url}")

def convert_image(input_path: str, output_path: str) -> None:
    vtracer.convert_image_to_svg_py(input_path, output_path)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/generate")
async def generate_svg(input: dict):

    input_path = "/tmp/input.jpeg"
    output_path = "/tmp/output.svg"
    url_input = input.get('url_input')
    try:
        await download_image(url_input, input_path)
        convert_image(input_path, output_path)
        await asyncio.sleep(5)  # Introduce a 5-second delay
        with open(output_path, 'r') as svg_file:
            svg_content = svg_file.read()
        return JSONResponse(content={"svg": svg_content}, media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # finally:
        # os.remove('./output.svg')
