from typing import List
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse, FileResponse
from PIL import Image, ImageDraw, ImageFont
import os
import json
import cv2

app = FastAPI()

UPLOAD_DIRECTORY = "uploads/"
OVERLAYED_DIRECTORY = "overlayed_images/"

@app.get("/", response_class=HTMLResponse)
async def root():
    instructions = """
    <h1>Welcome to the Image Overlay API</h1>
<p>Instructions:</p>
<ol>
    <li>Use the Postman tool or any HTTP client to interact with the API.</li>
    <li>Send a <strong>POST</strong> request to <code>/upload</code> endpoint to upload an image and specify the following optional parameters:</li>
    <ul>
        <li><strong>file</strong>: The image file to upload.</li>
        <li><strong>text</strong>: Text to overlay on the image.</li>
        <li><strong>size</strong>: Size of the resized image (square).</li>
        <li><strong>width</strong>: Width of the resized image.</li>
        <li><strong>height</strong>: Height of the resized image.</li>
        <li><strong>position</strong>: Position of the overlayed text ("top left", "top right", "bottom left", or "bottom right").</li>
    </ul>
    <li>Retrieve the uploaded data using a <strong>GET</strong> request to <code>/data</code> endpoint.</li>
    <li>Download the overlayed image using a <strong>GET</strong> request to <code>/download</code> endpoint.</li>
</ol>
Here are the Postman commands to interact with the API:

<br>
<strong>Upload an Image:</strong><br>
Endpoint: <code>POST http://localhost:8000/upload</code><br>
Body:Select <strong>form-data</strong> as the body type.
Add the following key-value pairs:
<br>
<strong>file</strong>: Select the image file to upload.
<br>
<strong>text</strong>: (Optional) Add text to overlay on the image.
<br>
<strong>size</strong>: (Optional) Specify the size of the resized image.
<br>
<strong>width</strong>: (Optional) Specify the width of the resized image.
<br>
<strong>height</strong>: (Optional) Specify the height of the resized image.
<br>
<strong>position</strong>: (Optional) Specify the position of the overlayed text ("top left", "top right", "bottom left", or "bottom right").
<br>
<br>
<strong>Retrieve Uploaded Data:</strong><br>

Endpoint: <code>GET http://localhost:8000/data</code>
<br>

<strong>Download Overlayed Image:</strong><br>
Endpoint: <code>GET http://localhost:8000/download</code>
<br>
<h3>make sure host link suitable for your machine </h3>
    """
    return instructions

def get_overlayed_images() -> List[str]:
    overlayed_images = []
    for root, dirs, files in os.walk(OVERLAYED_DIRECTORY):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
                overlayed_images.append(os.path.join(root, file))
    return overlayed_images

def get_image_dimensions(image_path):
    image = Image.open(image_path)
    width, height = image.size
    return width, height

@app.post("/upload")
async def upload_image(
    request: Request,
    file: UploadFile = File(...),
    text: str = Form("", convert_empty_to_none=True),
    size: int = Form(None, convert_empty_to_none=True),
    width: int = Form(None, convert_empty_to_none=True),
    height: int = Form(None, convert_empty_to_none=True),
    position: str = Form("top", regex=r"^(top|bottom)\s+(left|right)?$"),
):
  
    if not os.path.exists(OVERLAYED_DIRECTORY):
        os.makedirs(OVERLAYED_DIRECTORY)

    
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_path, "wb") as image_file:
        content = await file.read()
        image_file.write(content)


    image = Image.open(file_path)


    if text:
       
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", size or 24)
        text_width, text_height = draw.textsize(text, font=font)
        if position.startswith("top"):
            text_position = (10, 10)
        else:
            text_position = (10, image.height - text_height - 10)
        draw.text(text_position, text, fill="white", font=font)
        file_name, file_ext = os.path.splitext(file.filename)
        file_name = text.replace(" ", "_")
        modified_file_name = f"{file_name}{file_ext}"
    elif size:

        image = image.resize((size, size))
        file_name, file_ext = os.path.splitext(file.filename)
        file_name = file_name.replace(" ", "_")
        modified_file_name = f"{file_name}_overlay{size}{file_ext}"
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", size or 24)
        text_width, text_height = draw.textsize(modified_file_name, font=font)
        if position.startswith("top"):
            text_position = (10, 10)
        else:
            text_position = (10, image.height - text_height - 10)
        draw.text(text_position, modified_file_name, fill="white", font=font)
    elif width and height:
      
        image = image.resize((width, height))
        file_name, file_ext = os.path.splitext(file.filename)
        file_name = file_name.replace(" ", "_")
        modified_file_name = f"{file_name}_overlay{width}_{height}{file_ext}"
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 24)
        text_width, text_height = draw.textsize(modified_file_name, font=font)
        if position.startswith("top"):
            text_position = (10, 10)
        else:
            text_position = (10, image.height - text_height - 10)
        draw.text(text_position, modified_file_name, fill="white", font=font)
    else:
     
        modified_file_name = file.filename

 
    modified_file_path = os.path.join(OVERLAYED_DIRECTORY, modified_file_name)
    image.save(modified_file_path)

 
    response = {
        "file_name": modified_file_name,
        "text": text,
        "size": size,
        "width": width,
        "height": height,
        "position": position,
        "download_link": f"http://localhost:8000/download", 
    }


    json_file_path = os.path.join(OVERLAYED_DIRECTORY, "data.json")
    with open(json_file_path, "w") as json_file:
        json.dump(response, json_file)

    return JSONResponse(content=response)

@app.get("/data")
async def get_data():
    json_file_path = os.path.join(OVERLAYED_DIRECTORY, "data.json")
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)
    return data

@app.get("/download")
async def download():
    
    json_file_path = os.path.join(OVERLAYED_DIRECTORY, "data.json")
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)
    file_name = data.get("file_name")

    if file_name:

        file_path = os.path.join(OVERLAYED_DIRECTORY, file_name)

     
        if os.path.isfile(file_path):
            
            return FileResponse(file_path, filename=file_name)

    return JSONResponse(content={"error": "File not found"})
