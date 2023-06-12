import os
import cv2
from PIL import ImageEnhance
from PIL import ImageOps
from PIL import ImageChops
from typing import List
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, FileResponse
from PIL import Image, ImageFilter
from scipy.ndimage import gaussian_filter
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import uvicorn
from sklearn.cluster import KMeans

app = FastAPI()


if not os.path.exists("static"):
    os.makedirs("static")
@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    output_directory = "static/output"
    os.makedirs(output_directory, exist_ok=True)
    for i, file in enumerate(files):
       
        temp_path = os.path.join(output_directory, f"temp_{i}.png")
        with open(temp_path, "wb") as f:
            f.write(await file.read())
        process_image(temp_path, i)
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
        
        apply_aqua_filter(temp_path, i+1)  # Increase the parameter on each iteration
        apply_colorize_filter(temp_path, i+1, red=150, green=50, blue=200)  # Increase the parameter on each iteration
        apply_comic_filter(temp_path, i+1)  # Increase the parameter on each iteration
        apply_darkness_filter(temp_path, i+1)  # Increase the parameter on each iteration
        apply_diffuse_filter(temp_path, i+1, degree=16)  # Increase the parameter on each iteration
        apply_emboss_filter(temp_path, i+1)  # Increase the parameter on each iteration
        apply_find_edge_filter(temp_path, i+1, angle=60)  # Increase the parameter on each iteration
        apply_glowing_edge_filter(temp_path, i+1)  # Increase the parameter on each iteration
        apply_ice_filter(temp_path, i+1)  # Increase the parameter on each iteration
        apply_inosculate_filter(temp_path, i+1)  # Increase the parameter on each iteration
        apply_lighting_filter(temp_path, i+1)  # Increase the parameter on each iteration
        apply_moire_fringe_filter(temp_path, i+1)  # Increase the parameter on each iteration
        apply_molten_filter(temp_path, i+1)  # Increase the parameter on each iteration

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

app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/output/{index}")
async def view_output_image(index: int):
    output_file_path = f"static/output/output_{index}.png"
    return FileResponse(output_file_path)
@app.get("/cartoon/{index}")
async def view_cartoon_image(index: int):
    cartoon_file_path = f"static/cartoon/cartoon_{index}.png"
    return FileResponse(cartoon_file_path)
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
def process_image(temp_path, index):
    img = cv2.imread(temp_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mask = np.zeros(img.shape[:2], np.uint8)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    rect = (1, 1, img.shape[1] - 1, img.shape[0] - 1)
    cv2.grabCut(img_rgb, mask, rect, bgd_model, fgd_model, 10, cv2.GC_INIT_WITH_RECT)
    mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    result = img * mask[:, :, np.newaxis]
    resized_result = cv2.resize(result, (1080, 1080))
    output_directory = "static/output"
    output_file_path = os.path.join(output_directory, f"output_{index}.png")
    cv2.imwrite(output_file_path, resized_result)
@app.post("/uploadcartoon")
async def upload_cartoon(files: List[UploadFile] = File(...)):
    output_directory = "static/cartoon"
    os.makedirs(output_directory, exist_ok=True)
    
    for i, file in enumerate(files):
        temp_path = os.path.join(output_directory, f"temp_{i}.png")
        with open(temp_path, "wb") as f:
            f.write(await file.read())
            
        for j in range(10):
            convert_to_cartoon(temp_path, i, j)

    processed_cartoons = []
    for j in range(10):
        cartoon_folder = os.path.join(output_directory, f"cartoon_{j}")
        cartoon_files = os.listdir(cartoon_folder)
        cartoon_files.sort()
        processed_cartoons.append(cartoon_files)
        
    return {"message": "Images converted to cartoons successfully", "processed_cartoons": processed_cartoons}

def convert_to_cartoon(temp_path: str, index: int, loop_index: int):
    img = cv2.imread(temp_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    line_size = 7
    blur_value = 7
    gray_blur = cv2.medianBlur(gray_img, blur_value)
    edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)
    
    filters = [
        ("aqua", lambda img: ImageEnhance.Color(img).enhance(0.5)),
        ("colorize", lambda img: ImageOps.colorize(img.convert("L"), (150, 50, 200), (255, 255, 255))),
        ("comic", lambda img: img.filter(ImageFilter.FIND_EDGES)),
        ("darkness", lambda img: ImageEnhance.Brightness(img).enhance(0.5)),
        ("diffuse", lambda img: img.filter(ImageFilter.GaussianBlur(16))),
        ("emboss", lambda img: img.filter(ImageFilter.EMBOSS)),
        ("find_edge", lambda img: img.filter(ImageFilter.FIND_EDGES)),
        
        ("ice", lambda img: ImageOps.colorize(img.convert("L"), "#2196F3", "#FFFFFF")),
        ("inosculate", lambda img: ImageChops.invert(img)),
        ("lighting", lambda img: ImageEnhance.Brightness(img).enhance(1.5)),
        ("moire_fringe", lambda img: img.filter(ImageFilter.MedianFilter(5))),
        ("molten", lambda img: ImageOps.colorize(img.convert("L"), "#FF6F00", "#FFF59D"))
    ]
    
    cartoon_folder = f"static/cartoon/cartoon_{loop_index}"
    os.makedirs(cartoon_folder, exist_ok=True)
    
    for filter_name, filter_function in filters:
        filtered_image = filter_function(Image.fromarray(img))
        filtered_image = np.array(filtered_image)
        filtered_cartoon = cv2.bitwise_and(filtered_image, filtered_image, mask=edges)
        
        output_file_path = f"{cartoon_folder}/{filter_name}_{index}.png"
        cv2.imwrite(output_file_path, filtered_cartoon)

app.mount("/static", StaticFiles(directory="static"), name="static")
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=12000)