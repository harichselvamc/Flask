import os
import cv2
from typing import List
from fastapi import FastAPI, UploadFile, Request, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

output_directory = "static/output"
os.makedirs(output_directory, exist_ok=True)


def create_index_html():
    index_html_path = os.path.join("templates", "index.html")
    if not os.path.exists(index_html_path):
        with open(index_html_path, "w") as f:
            f.write(
                """
                <html>
                <head>
                    <title>Image Overlay App</title>
                </head>
                <body>
                    <h1>Image Overlay App</h1>
                    <form action="/upload" method="post" enctype="multipart/form-data">
                        <div>
                            <label for="files">Upload Image(s)</label>
                            <input type="file" id="files" name="files" accept="image/*" multiple>
                        </div>
                        <div>
                            <label for="text">Text Overlay</label>
                            <input type="text" id="text" name="text">
                        </div>
                        <div>
                            <input type="submit" value="Upload">
                        </div>
                    </form>
                    <h2>Instructions:</h2>
                    {% for instruction in instructions %}
                        <p>{{ instruction }}</p>
                    {% endfor %}
                </body>
                </html>
                """
            )


create_index_html()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    overlayed_images = os.listdir(output_directory)
    instructions = [
        f"Image {image} processed. Download: <a href='/download/{image}'>{image}</a>"
        for image in overlayed_images
    ]
    return templates.TemplateResponse("index.html", {"request": request, "instructions": instructions})


@app.get("/home", response_class=HTMLResponse)
async def show_home(request: Request):
    overlayed_images = os.listdir(output_directory)
    instructions = [
        f"Image {image} processed. Download: <a href='/download/{image}'>{image}</a>"
        for image in overlayed_images
    ]
    return templates.TemplateResponse("index.html", {"request": request, "instructions": instructions})


@app.post("/upload")
async def upload(files: List[UploadFile] = File(...), text: str = None):
    download_urls = []
    instructions = []

    for i, file in enumerate(files):
        # Save the uploaded file temporarily
        temp_path = os.path.join(output_directory, f"temp_{i}.png")
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        # Read the image using OpenCV
        image = cv2.imread(temp_path)

        # Get the name from the uploaded file
        file_name = file.filename
        file_name_without_extension, file_extension = os.path.splitext(file_name)

        # Prepare the text to overlay on the image
        if text:
            overlay_text = text
        else:
            overlay_text = f"{file_name_without_extension}{file_extension}"

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2
        font_thickness = 5
        text_color = (0, 0, 238)

        # Set the text size
        (text_width, text_height), _ = cv2.getTextSize(
            overlay_text, font, font_scale, font_thickness
        )

        # Calculate the position to place the text
        x = int((image.shape[1] - text_width) / 2)  # Centered horizontally
        y = int((image.shape[0] + text_height) - 30)  # Centered vertically

        # Overlay the text on the image
        cv2.putText(
            image, overlay_text, (x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA
        )

        # Set the output file path
        output_file_path = os.path.join(output_directory, f"output_{i}.png")

        # Save the resulting image
        cv2.imwrite(output_file_path, image)

        # Remove the temporary file
        os.remove(temp_path)

        # Generate the download link URL for the output image
        download_url = f"/static/output/output_{i}.png"
        download_urls.append(download_url)

        # Add instruction
        instruction = f"Image {file_name} processed. Download: <a href='{download_url}'>{file_name}</a>"
        instructions.append(instruction)

    # Return the download URLs and instructions in the API response
    return {"download_urls": download_urls, "instructions": instructions}


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
async def get_overlayed_image_data():
    overlayed_images = os.listdir(output_directory)
    image_data = []
    for image in overlayed_images:
        file_path = os.path.join(output_directory, image)
        size = os.path.getsize(file_path)
        image_data.append({
            "filename": image,
            "size": size
        })
    return {"images": image_data}


# Start the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=12000)
