# main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import httpx
import asyncio
import os
import vtracer
import aiofiles  # Import aiofiles for asynchronous file I/O

app = FastAPI()
async def download_image(url: str, local_path: str) -> None:
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            async with aiofiles.open(local_path, 'wb') as file:
                await file.write(response.content)
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Failed to download image from {url}")

def convert_image(input_path: str, output_path: str) -> None:
    vtracer.convert_image_to_svg_py(input_path, output_path)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/generate")
async def generate_svg(input: dict):
    print(input)
    input_path = "/tmp/input.png"
    output_path = "/tmp/output.svg"
    url_input = input.get('url_input')
    try:
        await download_image(url_input, input_path)
        convert_image(input_path, output_path) 
        await asyncio.sleep(9) # Introduce a 5-second delay
        async with aiofiles.open(output_path, 'r') as svg_file:
            svg_content = await svg_file.read()
        return JSONResponse(content={"svg": svg_content}, media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # finally:
        # os.remove('./output.svg')
