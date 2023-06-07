# import os
# import cv2
# import numpy as np
# from typing import List
# from fastapi import FastAPI, UploadFile, Request, File
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import HTMLResponse, FileResponse
# from fastapi.templating import Jinja2Templates
# import uvicorn
# from rembg import remove

# app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

# def create_static_folder():
#     base_directory = os.getcwd()
#     static_directory = os.path.join(base_directory, "static")
#     overlayed_images_directory = os.path.join(static_directory, "overlayed_images")

#     print("Base Directory:", base_directory)
#     print("Static Directory:", static_directory)
#     print("Overlayed Images Directory:", overlayed_images_directory)

#     if not os.path.exists(static_directory):
#         os.makedirs(static_directory)
#         print("Static Directory Created.")

#     if not os.path.exists(overlayed_images_directory):
#         os.makedirs(overlayed_images_directory)
#         print("Overlayed Images Directory Created.")


# def get_next_file_number():
#     overlayed_images = os.listdir("static/overlayed_images")
#     file_numbers = [
#         int(file.split("_")[1].split(".")[0])
#         for file in overlayed_images
#         if file.startswith("output_")
#     ]
#     if file_numbers:
#         return max(file_numbers) + 1
#     else:
#         return 0


# @app.get("/", response_class=HTMLResponse)
# async def home(request: Request):
#     return templates.TemplateResponse("home.html", {"request": request})


# @app.post("/upload")
# async def upload(files: List[UploadFile] = File(...), text: str = None):
#     output_directory = "static/overlayed_images"
#     os.makedirs(output_directory, exist_ok=True)

#     download_urls = []
#     instructions = []

#     next_file_number = get_next_file_number()

#     for i, file in enumerate(files):
     
#         temp_path = os.path.join(output_directory, f"temp_{i}.png")
#         with open(temp_path, "wb") as f:
#             f.write(await file.read())

      
#         with open(temp_path, "rb") as image_file:
#             image_data = image_file.read()
#             output_data = remove(image_data)

#         image_array = np.frombuffer(output_data, np.uint8)

#         image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

#         image = cv2.resize(image, (1080, 1080))

       
#         file_name = file.filename
#         file_name_without_extension, file_extension = os.path.splitext(file_name)

#         if text:
#             overlay_text = text
#         else:
#             overlay_text = f"{file_name_without_extension}{file_extension}"

#         font = cv2.FONT_HERSHEY_SIMPLEX
#         font_scale = 2
#         font_thickness = 5
#         text_color = (0, 0, 238)

#         (text_width, text_height), _ = cv2.getTextSize(
#             overlay_text, font, font_scale, font_thickness
#         )

#         x = int((image.shape[1] - text_width) / 2)  
#         y = image.shape[0] - int(text_height) - 30  

#         cv2.putText(
#             image, overlay_text, (x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA
#         )

     
#         output_file_path = os.path.join(output_directory, f"output_{next_file_number}.png")
#         cv2.imwrite(output_file_path, image)

#         download_url = f"/static/overlayed_images/output_{next_file_number}.png"
#         download_urls.append(download_url)

#         instruction = f"Image {file_name} processed. Download: {download_url}"
#         instructions.append(instruction)

#         next_file_number += 1

#     return {"download_urls": download_urls, "instructions": instructions}



# create_static_folder()


# @app.get("/download/{filename}")
# async def download(filename: str):

#     file_path = os.path.join("static", "overlayed_images", filename)

#     if os.path.isfile(file_path):
    
#         return FileResponse(file_path)

#     return {"detail": "File not found"}


# @app.get("/data")
# async def get_data():
#     overlayed_images = os.listdir("static/overlayed_images")
#     return {"overlayed_images": overlayed_images}


# @app.get("/url")
# async def get_shareable_link(request: Request):
#     base_url = request.base_url
#     return {"shareable_link": base_url}


# @app.get("/images")
# async def get_images():
#     overlayed_images = os.listdir("static/overlayed_images")
#     image_urls = [
#         f"http://localhost:12000/static/overlayed_images/{image}" for image in overlayed_images
#     ]
#     return {"image_urls": image_urls}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=12000)
import os
import cv2
import numpy as np
from typing import List
from fastapi import FastAPI, UploadFile, Request, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from rembg import remove

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def create_static_folder():
    base_directory = os.getcwd()
    static_directory = os.path.join(base_directory, "static")
    overlayed_images_directory = os.path.join(static_directory, "overlayed_images")

    print("Base Directory:", base_directory)
    print("Static Directory:", static_directory)
    print("Overlayed Images Directory:", overlayed_images_directory)

    if not os.path.exists(static_directory):
        os.makedirs(static_directory)
        print("Static Directory Created.")

    if not os.path.exists(overlayed_images_directory):
        os.makedirs(overlayed_images_directory)
        print("Overlayed Images Directory Created.")

def create_home_html():
    templates_directory = os.path.join(os.getcwd(), "templates")
    home_html_path = os.path.join(templates_directory, "home.html")

    if not os.path.exists(home_html_path):
        with open(home_html_path, "w") as f:
            f.write(
                """
                <html>
                <head>
                    <title>Upload Images</title>
                </head>
                <body>
                    <h1>Upload Images</h1>
                    <form action="/upload" enctype="multipart/form-data" method="post">
                        <input name="files" type="file" multiple>
                        <input type="text" name="text" placeholder="Overlay Text">
                        <input type="submit">
                    </form>
                </body>
                </html>
                """
            )
        print("home.html created.")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/upload")
async def upload(files: List[UploadFile] = File(...), text: str = None):
    output_directory = "static/overlayed_images"
    os.makedirs(output_directory, exist_ok=True)

    download_urls = []
    instructions = []

    next_file_number = get_next_file_number()

    for i, file in enumerate(files):
        temp_path = os.path.join(output_directory, f"temp_{i}.png")
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        with open(temp_path, "rb") as image_file:
            image_data = image_file.read()
            output_data = remove(image_data)

        image_array = np.frombuffer(output_data, np.uint8)

        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        image = cv2.resize(image, (1080, 1080))

        file_name = file.filename
        file_name_without_extension, file_extension = os.path.splitext(file_name)

        if text:
            overlay_text = text
        else:
            overlay_text = f"{file_name_without_extension}{file_extension}"

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2
        font_thickness = 5
        text_color = (0, 0, 238)

        (text_width, text_height), _ = cv2.getTextSize(
            overlay_text, font, font_scale, font_thickness
        )

        x = int((image.shape[1] - text_width) / 2)
        y = image.shape[0] - int(text_height) - 30

        cv2.putText(
            image, overlay_text, (x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA
        )

        output_file_path = os.path.join(output_directory, f"output_{next_file_number}.png")
        cv2.imwrite(output_file_path, image)

        download_url = f"/static/overlayed_images/output_{next_file_number}.png"
        download_urls.append(download_url)

        instruction = f"Image {file_name} processed. Download: {download_url}"
        instructions.append(instruction)

        next_file_number += 1

    return {"download_urls": download_urls, "instructions": instructions}

def get_next_file_number():
    overlayed_images = os.listdir("static/overlayed_images")
    file_numbers = [
        int(file.split("_")[1].split(".")[0])
        for file in overlayed_images
        if file.startswith("output_")
    ]
    if file_numbers:
        return max(file_numbers) + 1
    else:
        return 0

create_static_folder()
create_home_html()

@app.get("/download/{filename}")
async def download(filename: str):
    file_path = os.path.join("static", "overlayed_images", filename)

    if os.path.isfile(file_path):
        return FileResponse(file_path)

    return {"detail": "File not found"}

@app.get("/data")
async def get_data():
    overlayed_images = os.listdir("static/overlayed_images")
    return {"overlayed_images": overlayed_images}

@app.get("/url")
async def get_shareable_link(request: Request):
    base_url = request.base_url
    return {"shareable_link": base_url}

@app.get("/images")
async def get_images():
    overlayed_images = os.listdir("static/overlayed_images")
    image_urls = [
        f"http://localhost:12000/static/overlayed_images/{image}" for image in overlayed_images
    ]
    return {"image_urls": image_urls}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=12000)
