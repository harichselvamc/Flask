import os
import cv2
import numpy as np
from PIL import ImageEnhance
from PIL import ImageOps
from PIL import ImageChops

from typing import List
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, FileResponse
import uvicorn
from sklearn.cluster import KMeans
import os
from PIL import Image, ImageFilter
from scipy.ndimage import gaussian_filter
app = FastAPI()
if not os.path.exists("static"):
    os.makedirs("static")
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

@app.post("/effect")
async def apply_effect(files: List[UploadFile] = File(...)):
    output_directory = "static/effect"
    os.makedirs(output_directory, exist_ok=True)
    for i, file in enumerate(files):
        temp_path = os.path.join(output_directory, f"temp_{i}.png")
        with open(temp_path, "wb") as f:
            f.write(await file.read())
        image_gray = cv2.imread(temp_path, cv2.IMREAD_GRAYSCALE)
        gray_path = f"static/effect/out_gray_{i}.png"
        cv2.imwrite(gray_path, image_gray)
        apply_aqua_filter(temp_path, i)
        apply_colorize_filter(temp_path, i, red=150, green=50, blue=200)
        apply_comic_filter(temp_path, i)
        apply_darkness_filter(temp_path, i)
        apply_diffuse_filter(temp_path, i, degree=16)
        apply_emboss_filter(temp_path, i)
        apply_find_edge_filter(temp_path, i, angle=60)
        apply_glowing_edge_filter(temp_path, i)
        apply_ice_filter(temp_path, i)
        apply_inosculate_filter(temp_path, i)
        apply_lighting_filter(temp_path, i)
        apply_moire_fringe_filter(temp_path, i)
        apply_molten_filter(temp_path, i)
    processed_images = []
    for filename in os.listdir(output_directory):
        if filename.startswith("out") and filename.endswith(".png"):
            processed_images.append(filename)
    return {"message": "Images processed with effects successfully", "processed_images": processed_images}
def process_image(image_path, i):
    image = Image.open(image_path)
    if image.mode not in ["L", "RGB", "RGBA"]:
        image = image.convert("RGB")
        blurred_image = image.filter(ImageFilter.BLUR)
        sharpened_image = image.filter(ImageFilter.SHARPEN)
        inverted_image = ImageOps.invert(image)
        flipped_image = ImageOps.flip(image)
        rotated_image = image.rotate(45)
        gray_image.save(f"static/output/out_gray_{index}.png")
        blurred_image.save(f"static/output/out_blurred_{index}.png")
        sharpened_image.save(f"static/output/out_sharpened_{index}.png")
        inverted_image.save(f"static/output/out_inverted_{index}.png")
        flipped_image.save(f"static/output/out_flipped_{index}.png")
        rotated_image.save(f"static/output/out_rotated_{index}.png")
    else:
        print(f"Unsupported image mode: {image.mode}")

def convert_to_cartoon(image_path: str, index: int):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    gray_smooth = cv2.bilateralFilter(gray, 9, 250, 250)
    _, cartoon = cv2.threshold(gray_smooth, 100, 255, cv2.THRESH_BINARY)
    cartoon_path = f"static/cartoon/cartoon_{index}.png"
    cv2.imwrite(cartoon_path, cartoon)
def apply_aqua_filter(image_path: str, index: int):
    image = Image.open(image_path)
    enhanced_image = ImageEnhance.Color(image).enhance(0.5)
    enhanced_image.save(f"static/effect/out_aqua_{index}.png")
def apply_colorize_filter(image_path: str, index: int, red: int, green: int, blue: int):
    image = Image.open(image_path)
    colorized_image = ImageOps.colorize(image.convert("L"), (red, green, blue), (255, 255, 255))
    colorized_image.save(f"static/effect/out_colorize_{index}.png")
def apply_comic_filter(image_path: str, index: int):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(image, 9, 250, 250)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    cv2.imwrite(f"static/effect/out_comic_{index}.png", cartoon)
def apply_darkness_filter(image_path: str, index: int):
    image = Image.open(image_path)
    enhancer = ImageEnhance.Brightness(image)
    dark_image = enhancer.enhance(0.5)
    dark_image.save(f"static/effect/out_darkness_{index}.png")
def apply_diffuse_filter(image_path: str, index: int, degree: int):
    image = Image.open(image_path)
    image_gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    image_gray = Image.fromarray(image_gray)
    blurred_image = image_gray.filter(ImageFilter.GaussianBlur(degree))
    blurred_array = gaussian_filter(np.array(blurred_image), sigma=degree)
    diffused_image = Image.fromarray(blurred_array.astype('uint8'))
    diffused_image.save(f"static/effect/out_diffuse_{index}.png")
def apply_emboss_filter(image_path: str, index: int):
    image = Image.open(image_path)
    embossed_image = image.filter(ImageFilter.EMBOSS)
    embossed_image.save(f"static/effect/out_emboss_{index}.png")
def apply_find_edge_filter(image_path: str, index: int, angle: int):
    image = Image.open(image_path)
    edge_image = image.filter(ImageFilter.FIND_EDGES)
    rotated_image = edge_image.rotate(angle)
    rotated_image.save(f"static/effect/out_find_edge_{index}.png")
def apply_glowing_edge_filter(image_path: str, index: int):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (0, 0), 3)
    edges = cv2.Canny(blurred, 50, 150)
    glowing_edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    cv2.imwrite(f"static/effect/out_glowing_edge_{index}.png", glowing_edges)
def apply_ice_filter(image_path: str, index: int):
    image = Image.open(image_path)
    ice_image = ImageOps.colorize(image.convert("L"), "#2196F3", "#FFFFFF")
    ice_image.save(f"static/effect/out_ice_{index}.png")
def apply_inosculate_filter(image_path: str, index: int):
    image = Image.open(image_path)
    inosculated_image = ImageChops.invert(image)
    inosculated_image.save(f"static/effect/out_inosculate_{index}.png")
def apply_lighting_filter(image_path: str, index: int):
    image = Image.open(image_path)
    enhancer = ImageEnhance.Brightness(image)
    light_image = enhancer.enhance(1.5)
    light_image.save(f"static/effect/out_lighting_{index}.png")
def apply_moire_fringe_filter(image_path: str, index: int):
    image = Image.open(image_path)
    moire_fringe_image = image.filter(ImageFilter.MedianFilter(5))
    moire_fringe_image.save(f"static/effect/out_moire_fringe_{index}.png")
def apply_molten_filter(image_path: str, index: int):
    image = Image.open(image_path)
    molten_image = ImageOps.colorize(image.convert("L"), "#FF6F00", "#FFF59D")
    molten_image.save(f"static/effect/out_molten_{index}.png")
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
