import os
import cv2
import numpy as np
from typing import List
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, FileResponse
import uvicorn
from sklearn.cluster import KMeans

app = FastAPI()

# Define the upload endpoint
@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    output_directory = "static/output"
    os.makedirs(output_directory, exist_ok=True)

    for i, file in enumerate(files):
        # Save the uploaded file temporarily
        temp_path = os.path.join(output_directory, f"temp_{i}.png")
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        # Process the image
        process_image(temp_path, i)

    # Get a list of processed image file paths
    processed_images = []
    for filename in os.listdir(output_directory):
        if filename.startswith("out") and filename.endswith(".png"):
            processed_images.append(filename)

    return {"message": "Images processed successfully", "processed_images": processed_images}


# Define the uploadcartoon endpoint
@app.post("/uploadcartoon")
async def upload_cartoon(files: List[UploadFile] = File(...)):
    output_directory = "static/cartoon"
    os.makedirs(output_directory, exist_ok=True)

    for i, file in enumerate(files):
        # Save the uploaded file temporarily
        temp_path = os.path.join(output_directory, f"temp_{i}.png")
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        # Process the image
        convert_to_cartoon(temp_path, i)

    # Get a list of processed cartoon image file paths
    processed_cartoons = []
    for filename in os.listdir(output_directory):
        if filename.startswith("cartoon") and filename.endswith(".png"):
            processed_cartoons.append(filename)

    return {"message": "Images converted to cartoons successfully", "processed_cartoons": processed_cartoons}


# Serve the static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Define the endpoint to view the output image
@app.get("/output/{index}")
async def view_output_image(index: int):
    output_file_path = f"static/output/output_{index}.png"
    return FileResponse(output_file_path)


# Define the endpoint to view the cartoon image
@app.get("/cartoon/{index}")
async def view_cartoon_image(index: int):
    cartoon_file_path = f"static/cartoon/cartoon_{index}.png"
    return FileResponse(cartoon_file_path)


# Define the endpoint to get all the image previews
@app.get("/img")
async def get_image_previews():
    previews = []

    output_directory = "static/output"
    for filename in os.listdir(output_directory):
        if filename.startswith("output_") and filename.endswith(".png"):
            output_file_path = os.path.join(output_directory, filename)
            previews.append(output_file_path)

    def stream():
        for preview_path in previews:
            with open(preview_path, "rb") as f:
                yield f.read()

    return StreamingResponse(stream(), media_type="image/png")


# Utility function to process the image
def process_image(temp_path, index):
    # Read the image using OpenCV
    img = cv2.imread(temp_path)

    # Convert image to RGB format
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Create a mask with white background
    mask = np.zeros(img.shape[:2], np.uint8)

    # Define the background and foreground models
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)

    # Define the bounding rectangle for the foreground object
    rect = (1, 1, img.shape[1] - 1, img.shape[0] - 1)

    # Apply GrabCut algorithm to extract foreground
    cv2.grabCut(img_rgb, mask, rect, bgd_model, fgd_model, 10, cv2.GC_INIT_WITH_RECT)

    # Create a mask with only the foreground region
    mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    # Apply the mask to the original image
    result = img * mask[:, :, np.newaxis]

    # Resize the image to 1080x1080
    resized_result = cv2.resize(result, (1080, 1080))

    # Save the resulting image
    output_directory = "static/output"
    output_file_path = os.path.join(output_directory, f"output_{index}.png")
    cv2.imwrite(output_file_path, resized_result)


# Utility function to convert image to cartoon
def convert_to_cartoon(temp_path, index):
    # Read the image using OpenCV
    img = cv2.imread(temp_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Convert image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Generate edge mask
    line_size = 7
    blur_value = 7
    gray_blur = cv2.medianBlur(gray_img, blur_value)
    edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)

    # Color quantization with KMeans clustering
    k = 7
    data = img.reshape(-1, 3)
    kmeans = KMeans(n_clusters=k, random_state=42).fit(data)
    img_reduced = kmeans.cluster_centers_[kmeans.labels_]
    img_reduced = img_reduced.reshape(img.shape)
    img_reduced = img_reduced.astype(np.uint8)

    # Apply bilateral filter
    d = 7
    sigma_color = 200
    sigma_space = 200
    blurred = cv2.bilateralFilter(img_reduced, d=d, sigmaColor=sigma_color, sigmaSpace=sigma_space)

    # Apply the edge mask to the blurred image
    cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)

    # Save the resulting cartoon image
    output_directory = "static/cartoon"
    output_file_path = os.path.join(output_directory, f"cartoon_{index}.png")
    cv2.imwrite(output_file_path, cartoon)


# Start the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=12000)
