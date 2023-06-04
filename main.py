import uvicorn
import cv2
import os
from typing import List
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse

app = FastAPI()

def resize_image(image, size):
    width, height = size.split('x')
    width = int(width)
    height = int(height)
    return cv2.resize(image, (width, height))

@app.post('/overlay-text')
async def overlay_text(files: List[UploadFile] = File(...), image_size: str = '1080x1080'):
    # If no files are uploaded
    if len(files) == 0:
        return {'error': 'No files uploaded'}

    output_directory = os.path.join(os.getcwd(), 'output')
    os.makedirs(output_directory, exist_ok=True)  # Directory allocation

    download_urls = []  # List of URLs
    for i, file in enumerate(files):
        temp_path = f'temp_{i}.png'
        with open(temp_path, 'wb') as temp_file:
            temp_file.write(await file.read())  # Saving the file to a temporary location

        # Loading the image
        image = cv2.imread(temp_path)

        if image is None: # If the image fails to load
            os.remove(temp_path)
            return {'error': f'Failed to load image {i}'}

        # Resize the image
        image = resize_image(image, image_size)

        # Extracting the file name from the uploaded file
        file_name = file.filename
        file_name_without_extension, file_extension = os.path.splitext(file_name)

        # Prepare the text to overlay on the image
        text = f'{file_name_without_extension}{file_extension}'
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2
        font_thickness = 5
        text_color = (0, 0, 238)

        # Set the text size
        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, font_thickness)

        # Calculate the position to place the text
        x = int((image.shape[1] - text_width) / 2) # Centered horizontally
        y = int((image.shape[0] + text_height) - 30)  # Centered vertically

        # Overlay the text on the image
        cv2.putText(image, text, (x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA)

        # Set the output file path
        output_file_path = os.path.join(output_directory, f'output_{i}.png')

        # Save the resulting image
        cv2.imwrite(output_file_path, image)

        # Remove the temporary file
        os.remove(temp_path)

        # Generate the download link URL for the output image
        download_url = f'/download/output_{i}.png'
        download_urls.append(download_url)

    # Return the download URLs in the API response
    return {'download_urls': download_urls}

@app.get('/download/{filename}')
async def download(filename: str):
    # Making the file path
    file_path = os.path.join(os.getcwd(), 'output', filename)

    # Check if the file exists
    if os.path.isfile(file_path):
        # Returning the file as a downloadable response
        return FileResponse(file_path, filename=filename)

    # If the file doesn't exist, this will return a 404 Not Found error
    return {'error': 'File not found'}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
