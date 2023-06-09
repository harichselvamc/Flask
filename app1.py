# import os
# import cv2
# from typing import List
# from fastapi import FastAPI, UploadFile, Request, File
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
# from fastapi.templating import Jinja2Templates
# import uvicorn
# import rembg

# app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

# # Define the home page
# @app.get("/", response_class=HTMLResponse)
# async def home(request: Request):
#     return templates.TemplateResponse("home.html", {"request": request})


# # Define the upload endpoint
# @app.post("/upload")
# async def upload(files: List[UploadFile] = File(...), text: str = None):
#     output_directory = "static/output"
#     os.makedirs(output_directory, exist_ok=True)

#     download_urls = []
#     instructions = []

#     for i, file in enumerate(files):
#         # Save the uploaded file temporarily
#         temp_path = os.path.join(output_directory, f"temp_{i}.png")
#         with open(temp_path, "wb") as f:
#             f.write(await file.read())

#         # Remove the background using rembg
#         output_path = os.path.join(output_directory, f"output_{i}.png")
#         with open(temp_path, "rb") as img_file, open(output_path, "wb") as output_file:
#             img_data = img_file.read()
#             output_data = rembg.remove(img_data)
#             output_file.write(output_data)

#         # Read the image using OpenCV
#         image = cv2.imread(output_path)

#         # Resize the image to 1080x1080
#         resized_image = cv2.resize(image, (1080, 1080))

#         # Get the name from the uploaded file
#         file_name = file.filename
#         file_name_without_extension, file_extension = os.path.splitext(file_name)

#         # Prepare the text to overlay on the image
#         if text:
#             overlay_text = text
#         else:
#             overlay_text = f"{file_name_without_extension}{file_extension}"

#         font = cv2.FONT_HERSHEY_SIMPLEX
#         font_scale = 2
#         font_thickness = 5
#         text_color = (0, 0, 238)

#         # Set the text size
#         (text_width, text_height), _ = cv2.getTextSize(
#             overlay_text, font, font_scale, font_thickness
#         )

#         # Calculate the position to place the text
#         x = int((resized_image.shape[1] - text_width) / 2)  # Centered horizontally
#         y = int((resized_image.shape[0] + text_height) - 30)  # Placed at the bottom

#         # Overlay the text on the image
#         cv2.putText(
#             resized_image,
#             overlay_text,
#             (x, y),
#             font,
#             font_scale,
#             text_color,
#             font_thickness,
#             cv2.LINE_AA,
#         )

#         # Save the resulting image
#         cv2.imwrite(output_path, resized_image)

#         # Remove the temporary file
#         os.remove(temp_path)

#         # Generate the download link URL for the output image
#         download_url = f"/static/output/output_{i}.png"
#         download_urls.append(download_url)

#         # Add instruction
#         instruction = f"Image {file_name} processed. Download: {download_url}"
#         instructions.append(instruction)

#     # Return the download URLs and instructions in the API response
#     return {"download_urls": download_urls, "instructions": instructions}


# @app.get("/download/{filename}")
# async def download(filename: str):
#     # Making the file path
#     file_path = os.path.join("static", "output", filename)

#     # Check if the file exists
#     if os.path.isfile(file_path):
#         # If the file exists, return it as a response
#         return FileResponse(file_path)

#     # If the file does not exist, return a 404 Not Found response
#     return {"detail": "File not found"}


# @app.get("/data")
# async def get_data():
#     overlayed_images = os.listdir("static/output")
#     return {"overlayed_images": overlayed_images}


# @app.get("/url")
# async def get_shareable_link(request: Request):
#     base_url = request.base_url
#     return {"shareable_link": base_url}


# @app.get("/images")
# async def get_images():
#     overlayed_images = os.listdir("static/output")
#     image_urls = [
#         f"http://localhost:12000/static/output/{image}" for image in overlayed_images
#     ]
#     return {"image_urls": image_urls}


# # Start the server
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=12000)
import os
from PIL import Image
from typing import List
from fastapi import FastAPI, UploadFile, Request, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import rembg

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Define the upload endpoint
@app.post("/upload")
async def upload(files: List[UploadFile] = File(...), text: str = None):
    output_directory = "static/output"
    os.makedirs(output_directory, exist_ok=True)

    download_urls = []
    instructions = []

    for i, file in enumerate(files):
        try:
            # Save the uploaded file temporarily
            temp_path = os.path.join(output_directory, f"temp_{i}.png")
            with open(temp_path, "wb") as f:
                f.write(await file.read())

            # Remove the background using rembg
            output_path = os.path.join(output_directory, f"output_{i}.png")
            with open(temp_path, "rb") as img_file, open(output_path, "wb") as output_file:
                img_data = img_file.read()
                output_data = rembg.remove(img_data)
                output_file.write(output_data)

            # Resize the image to 1080x1080 and add overlay text
            image = Image.open(output_path)
            image = image.resize((1080, 1080))
            image_with_text = add_text_overlay(image, file.filename, text)
            image_with_text.save(output_path)

            # Remove the temporary file
            os.remove(temp_path)

            # Generate the download link URL for the output image
            download_url = f"/static/output/output_{i}.png"
            download_urls.append(download_url)

            # Add instruction
            instruction = f"Image {file.filename} processed. Download: {download_url}"
            instructions.append(instruction)
        except Exception as e:
            # Log the error and continue with the next file
            error_message = f"Error processing file {file.filename}: {str(e)}"
            print(error_message)

    # Return the download URLs and instructions in the API response
    return {"download_urls": download_urls, "instructions": instructions}


def add_text_overlay(image, filename, text):
    from PIL import ImageDraw, ImageFont

    overlay_text = text or filename
    font = ImageFont.truetype("arial.ttf", 100)
    draw = ImageDraw.Draw(image)
    text_width, text_height = draw.textsize(overlay_text, font=font)
    x = int((image.width - text_width) / 2)
    y = image.height - text_height - 30
    draw.text((x, y), overlay_text, font=font, fill=(0, 0, 238))

    return image


@app.get("/download/{filename}")
async def download(filename: str):
    # Making the file path
    file_path = os.path.join("static", "output", filename)

    # Check if the file exists
    if os.path.isfile(file_path):
        # If the file exists, return it as a response
        return FileResponse(file_path)

    # If the file does not exist, return a 404 Not Found response
    return {"detail": "File not found"}


@app.get("/data")
async def get_data():
    overlayed_images = os.listdir("static/output")
    return {"overlayed_images": overlayed_images}


@app.get("/url")
async def get_shareable_link(request: Request):
    base_url = request.base_url
    return {"shareable_link": base_url}


@app.get("/images")
async def get_images():
    overlayed_images = os.listdir("static/output")
    image_urls = [
        f"http://localhost:12000/static/output/{image}" for image in overlayed_images
    ]
    return {"image_urls": image_urls}


# Start the server
if __name__ == "__main__":
    import sys

    if "--force-server" in sys.argv:
        uvicorn.run(app, host="0.0.0.0", port=12000)
    else:
        print("Use the --force-server flag to run the server forcefully.")
