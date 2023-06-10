# # # # # # # # # # # # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # # # # # # # # # # # import cv2
# # # # # # # # # # # # # # # # # # # # # # # # # # import numpy as np
# # # # # # # # # # # # # # # # # # # # # # # # # # from typing import List
# # # # # # # # # # # # # # # # # # # # # # # # # # from fastapi import FastAPI, UploadFile, Request, File
# # # # # # # # # # # # # # # # # # # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # # # # # # # # # # # # # # # # # # from fastapi.responses import HTMLResponse, FileResponse
# # # # # # # # # # # # # # # # # # # # # # # # # # from fastapi.templating import Jinja2Templates
# # # # # # # # # # # # # # # # # # # # # # # # # # import uvicorn
# # # # # # # # # # # # # # # # # # # # # # # # # # from rembg import remove

# # # # # # # # # # # # # # # # # # # # # # # # # # app = FastAPI()
# # # # # # # # # # # # # # # # # # # # # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")
# # # # # # # # # # # # # # # # # # # # # # # # # # templates = Jinja2Templates(directory="templates")

# # # # # # # # # # # # # # # # # # # # # # # # # # def create_static_folder():
# # # # # # # # # # # # # # # # # # # # # # # # # #     base_directory = os.getcwd()
# # # # # # # # # # # # # # # # # # # # # # # # # #     static_directory = os.path.join(base_directory, "static")
# # # # # # # # # # # # # # # # # # # # # # # # # #     overlayed_images_directory = os.path.join(static_directory, "overlayed_images")

# # # # # # # # # # # # # # # # # # # # # # # # # #     print("Base Directory:", base_directory)
# # # # # # # # # # # # # # # # # # # # # # # # # #     print("Static Directory:", static_directory)
# # # # # # # # # # # # # # # # # # # # # # # # # #     print("Overlayed Images Directory:", overlayed_images_directory)

# # # # # # # # # # # # # # # # # # # # # # # # # #     if not os.path.exists(static_directory):
# # # # # # # # # # # # # # # # # # # # # # # # # #         os.makedirs(static_directory)
# # # # # # # # # # # # # # # # # # # # # # # # # #         print("Static Directory Created.")

# # # # # # # # # # # # # # # # # # # # # # # # # #     if not os.path.exists(overlayed_images_directory):
# # # # # # # # # # # # # # # # # # # # # # # # # #         os.makedirs(overlayed_images_directory)
# # # # # # # # # # # # # # # # # # # # # # # # # #         print("Overlayed Images Directory Created.")


# # # # # # # # # # # # # # # # # # # # # # # # # # def get_next_file_number():
# # # # # # # # # # # # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/overlayed_images")
# # # # # # # # # # # # # # # # # # # # # # # # # #     file_numbers = [
# # # # # # # # # # # # # # # # # # # # # # # # # #         int(file.split("_")[1].split(".")[0])
# # # # # # # # # # # # # # # # # # # # # # # # # #         for file in overlayed_images
# # # # # # # # # # # # # # # # # # # # # # # # # #         if file.startswith("output_")
# # # # # # # # # # # # # # # # # # # # # # # # # #     ]
# # # # # # # # # # # # # # # # # # # # # # # # # #     if file_numbers:
# # # # # # # # # # # # # # # # # # # # # # # # # #         return max(file_numbers) + 1
# # # # # # # # # # # # # # # # # # # # # # # # # #     else:
# # # # # # # # # # # # # # # # # # # # # # # # # #         return 0


# # # # # # # # # # # # # # # # # # # # # # # # # # @app.get("/", response_class=HTMLResponse)
# # # # # # # # # # # # # # # # # # # # # # # # # # async def home(request: Request):
# # # # # # # # # # # # # # # # # # # # # # # # # #     return templates.TemplateResponse("home.html", {"request": request})


# # # # # # # # # # # # # # # # # # # # # # # # # # @app.post("/upload")
# # # # # # # # # # # # # # # # # # # # # # # # # # async def upload(files: List[UploadFile] = File(...), text: str = None):
# # # # # # # # # # # # # # # # # # # # # # # # # #     output_directory = "static/overlayed_images"
# # # # # # # # # # # # # # # # # # # # # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # # # # # # # # # # # # # # # # # # # # #     download_urls = []
# # # # # # # # # # # # # # # # # # # # # # # # # #     instructions = []

# # # # # # # # # # # # # # # # # # # # # # # # # #     next_file_number = get_next_file_number()

# # # # # # # # # # # # # # # # # # # # # # # # # #     for i, file in enumerate(files):
     
# # # # # # # # # # # # # # # # # # # # # # # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # # # # # # # # # # # # # # # # # # # # # #         with open(temp_path, "wb") as f:
# # # # # # # # # # # # # # # # # # # # # # # # # #             f.write(await file.read())

      
# # # # # # # # # # # # # # # # # # # # # # # # # #         with open(temp_path, "rb") as image_file:
# # # # # # # # # # # # # # # # # # # # # # # # # #             image_data = image_file.read()
# # # # # # # # # # # # # # # # # # # # # # # # # #             output_data = remove(image_data)

# # # # # # # # # # # # # # # # # # # # # # # # # #         image_array = np.frombuffer(output_data, np.uint8)

# # # # # # # # # # # # # # # # # # # # # # # # # #         image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

# # # # # # # # # # # # # # # # # # # # # # # # # #         image = cv2.resize(image, (1080, 1080))

       
# # # # # # # # # # # # # # # # # # # # # # # # # #         file_name = file.filename
# # # # # # # # # # # # # # # # # # # # # # # # # #         file_name_without_extension, file_extension = os.path.splitext(file_name)

# # # # # # # # # # # # # # # # # # # # # # # # # #         if text:
# # # # # # # # # # # # # # # # # # # # # # # # # #             overlay_text = text
# # # # # # # # # # # # # # # # # # # # # # # # # #         else:
# # # # # # # # # # # # # # # # # # # # # # # # # #             overlay_text = f"{file_name_without_extension}{file_extension}"

# # # # # # # # # # # # # # # # # # # # # # # # # #         font = cv2.FONT_HERSHEY_SIMPLEX
# # # # # # # # # # # # # # # # # # # # # # # # # #         font_scale = 2
# # # # # # # # # # # # # # # # # # # # # # # # # #         font_thickness = 5
# # # # # # # # # # # # # # # # # # # # # # # # # #         text_color = (0, 0, 238)

# # # # # # # # # # # # # # # # # # # # # # # # # #         (text_width, text_height), _ = cv2.getTextSize(
# # # # # # # # # # # # # # # # # # # # # # # # # #             overlay_text, font, font_scale, font_thickness
# # # # # # # # # # # # # # # # # # # # # # # # # #         )

# # # # # # # # # # # # # # # # # # # # # # # # # #         x = int((image.shape[1] - text_width) / 2)  
# # # # # # # # # # # # # # # # # # # # # # # # # #         y = image.shape[0] - int(text_height) - 30  

# # # # # # # # # # # # # # # # # # # # # # # # # #         cv2.putText(
# # # # # # # # # # # # # # # # # # # # # # # # # #             image, overlay_text, (x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA
# # # # # # # # # # # # # # # # # # # # # # # # # #         )

     
# # # # # # # # # # # # # # # # # # # # # # # # # #         output_file_path = os.path.join(output_directory, f"output_{next_file_number}.png")
# # # # # # # # # # # # # # # # # # # # # # # # # #         cv2.imwrite(output_file_path, image)

# # # # # # # # # # # # # # # # # # # # # # # # # #         download_url = f"/static/overlayed_images/output_{next_file_number}.png"
# # # # # # # # # # # # # # # # # # # # # # # # # #         download_urls.append(download_url)

# # # # # # # # # # # # # # # # # # # # # # # # # #         instruction = f"Image {file_name} processed. Download: {download_url}"
# # # # # # # # # # # # # # # # # # # # # # # # # #         instructions.append(instruction)

# # # # # # # # # # # # # # # # # # # # # # # # # #         next_file_number += 1

# # # # # # # # # # # # # # # # # # # # # # # # # #     return {"download_urls": download_urls, "instructions": instructions}



# # # # # # # # # # # # # # # # # # # # # # # # # # create_static_folder()


# # # # # # # # # # # # # # # # # # # # # # # # # # @app.get("/download/{filename}")
# # # # # # # # # # # # # # # # # # # # # # # # # # async def download(filename: str):

# # # # # # # # # # # # # # # # # # # # # # # # # #     file_path = os.path.join("static", "overlayed_images", filename)

# # # # # # # # # # # # # # # # # # # # # # # # # #     if os.path.isfile(file_path):
    
# # # # # # # # # # # # # # # # # # # # # # # # # #         return FileResponse(file_path)

# # # # # # # # # # # # # # # # # # # # # # # # # #     return {"detail": "File not found"}


# # # # # # # # # # # # # # # # # # # # # # # # # # @app.get("/data")
# # # # # # # # # # # # # # # # # # # # # # # # # # async def get_data():
# # # # # # # # # # # # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/overlayed_images")
# # # # # # # # # # # # # # # # # # # # # # # # # #     return {"overlayed_images": overlayed_images}


# # # # # # # # # # # # # # # # # # # # # # # # # # @app.get("/url")
# # # # # # # # # # # # # # # # # # # # # # # # # # async def get_shareable_link(request: Request):
# # # # # # # # # # # # # # # # # # # # # # # # # #     base_url = request.base_url
# # # # # # # # # # # # # # # # # # # # # # # # # #     return {"shareable_link": base_url}


# # # # # # # # # # # # # # # # # # # # # # # # # # @app.get("/images")
# # # # # # # # # # # # # # # # # # # # # # # # # # async def get_images():
# # # # # # # # # # # # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/overlayed_images")
# # # # # # # # # # # # # # # # # # # # # # # # # #     image_urls = [
# # # # # # # # # # # # # # # # # # # # # # # # # #         f"http://localhost:12000/static/overlayed_images/{image}" for image in overlayed_images
# # # # # # # # # # # # # # # # # # # # # # # # # #     ]
# # # # # # # # # # # # # # # # # # # # # # # # # #     return {"image_urls": image_urls}


# # # # # # # # # # # # # # # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # # # # # # # # # # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)

# # # # # # # # # # # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # # # # # # # # # # import cv2
# # # # # # # # # # # # # # # # # # # # # # # # # import numpy as np
# # # # # # # # # # # # # # # # # # # # # # # # # from typing import List
# # # # # # # # # # # # # # # # # # # # # # # # # from fastapi import FastAPI, UploadFile, Request, File
# # # # # # # # # # # # # # # # # # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # # # # # # # # # # # # # # # # # from fastapi.responses import HTMLResponse, FileResponse
# # # # # # # # # # # # # # # # # # # # # # # # # from fastapi.templating import Jinja2Templates
# # # # # # # # # # # # # # # # # # # # # # # # # import uvicorn
# # # # # # # # # # # # # # # # # # # # # # # # # from rembg import remove

# # # # # # # # # # # # # # # # # # # # # # # # # app = FastAPI()
# # # # # # # # # # # # # # # # # # # # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")
# # # # # # # # # # # # # # # # # # # # # # # # # templates = Jinja2Templates(directory="templates")

# # # # # # # # # # # # # # # # # # # # # # # # # def create_static_folder():
# # # # # # # # # # # # # # # # # # # # # # # # #     base_directory = os.getcwd()
# # # # # # # # # # # # # # # # # # # # # # # # #     static_directory = os.path.join(base_directory, "static")
# # # # # # # # # # # # # # # # # # # # # # # # #     overlayed_images_directory = os.path.join(static_directory, "overlayed_images")

# # # # # # # # # # # # # # # # # # # # # # # # #     print("Base Directory:", base_directory)
# # # # # # # # # # # # # # # # # # # # # # # # #     print("Static Directory:", static_directory)
# # # # # # # # # # # # # # # # # # # # # # # # #     print("Overlayed Images Directory:", overlayed_images_directory)

# # # # # # # # # # # # # # # # # # # # # # # # #     if not os.path.exists(static_directory):
# # # # # # # # # # # # # # # # # # # # # # # # #         os.makedirs(static_directory)
# # # # # # # # # # # # # # # # # # # # # # # # #         print("Static Directory Created.")

# # # # # # # # # # # # # # # # # # # # # # # # #     if not os.path.exists(overlayed_images_directory):
# # # # # # # # # # # # # # # # # # # # # # # # #         os.makedirs(overlayed_images_directory)
# # # # # # # # # # # # # # # # # # # # # # # # #         print("Overlayed Images Directory Created.")

# # # # # # # # # # # # # # # # # # # # # # # # # def create_home_html():
# # # # # # # # # # # # # # # # # # # # # # # # #     templates_directory = os.path.join(os.getcwd(), "templates")
# # # # # # # # # # # # # # # # # # # # # # # # #     home_html_path = os.path.join(templates_directory, "home.html")

# # # # # # # # # # # # # # # # # # # # # # # # #     if not os.path.exists(home_html_path):
# # # # # # # # # # # # # # # # # # # # # # # # #         with open(home_html_path, "w") as f:
# # # # # # # # # # # # # # # # # # # # # # # # #             f.write(
# # # # # # # # # # # # # # # # # # # # # # # # #                 """
# # # # # # # # # # # # # # # # # # # # # # # # #                 <html>
# # # # # # # # # # # # # # # # # # # # # # # # #                 <head>
# # # # # # # # # # # # # # # # # # # # # # # # #                     <title>Upload Images</title>
# # # # # # # # # # # # # # # # # # # # # # # # #                 </head>
# # # # # # # # # # # # # # # # # # # # # # # # #                 <body>
# # # # # # # # # # # # # # # # # # # # # # # # #                     <h1>Upload Images</h1>
# # # # # # # # # # # # # # # # # # # # # # # # #                     <form action="/upload" enctype="multipart/form-data" method="post">
# # # # # # # # # # # # # # # # # # # # # # # # #                         <input name="files" type="file" multiple>
# # # # # # # # # # # # # # # # # # # # # # # # #                         <input type="text" name="text" placeholder="Overlay Text">
# # # # # # # # # # # # # # # # # # # # # # # # #                         <input type="submit">
# # # # # # # # # # # # # # # # # # # # # # # # #                     </form>
# # # # # # # # # # # # # # # # # # # # # # # # #                 </body>
# # # # # # # # # # # # # # # # # # # # # # # # #                 </html>
# # # # # # # # # # # # # # # # # # # # # # # # #                 """
# # # # # # # # # # # # # # # # # # # # # # # # #             )
# # # # # # # # # # # # # # # # # # # # # # # # #         print("home.html created.")

# # # # # # # # # # # # # # # # # # # # # # # # # @app.get("/", response_class=HTMLResponse)
# # # # # # # # # # # # # # # # # # # # # # # # # async def home(request: Request):
# # # # # # # # # # # # # # # # # # # # # # # # #     return templates.TemplateResponse("home.html", {"request": request})

# # # # # # # # # # # # # # # # # # # # # # # # # @app.post("/upload")
# # # # # # # # # # # # # # # # # # # # # # # # # async def upload(files: List[UploadFile] = File(...), text: str = None):
# # # # # # # # # # # # # # # # # # # # # # # # #     output_directory = "static/overlayed_images"
# # # # # # # # # # # # # # # # # # # # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # # # # # # # # # # # # # # # # # # # #     download_urls = []
# # # # # # # # # # # # # # # # # # # # # # # # #     instructions = []

# # # # # # # # # # # # # # # # # # # # # # # # #     next_file_number = get_next_file_number()

# # # # # # # # # # # # # # # # # # # # # # # # #     for i, file in enumerate(files):
# # # # # # # # # # # # # # # # # # # # # # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # # # # # # # # # # # # # # # # # # # # #         with open(temp_path, "wb") as f:
# # # # # # # # # # # # # # # # # # # # # # # # #             f.write(await file.read())

# # # # # # # # # # # # # # # # # # # # # # # # #         with open(temp_path, "rb") as image_file:
# # # # # # # # # # # # # # # # # # # # # # # # #             image_data = image_file.read()
# # # # # # # # # # # # # # # # # # # # # # # # #             output_data = remove(image_data)

# # # # # # # # # # # # # # # # # # # # # # # # #         image_array = np.frombuffer(output_data, np.uint8)

# # # # # # # # # # # # # # # # # # # # # # # # #         image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

# # # # # # # # # # # # # # # # # # # # # # # # #         image = cv2.resize(image, (1080, 1080))

# # # # # # # # # # # # # # # # # # # # # # # # #         file_name = file.filename
# # # # # # # # # # # # # # # # # # # # # # # # #         file_name_without_extension, file_extension = os.path.splitext(file_name)

# # # # # # # # # # # # # # # # # # # # # # # # #         if text:
# # # # # # # # # # # # # # # # # # # # # # # # #             overlay_text = text
# # # # # # # # # # # # # # # # # # # # # # # # #         else:
# # # # # # # # # # # # # # # # # # # # # # # # #             overlay_text = f"{file_name_without_extension}{file_extension}"

# # # # # # # # # # # # # # # # # # # # # # # # #         font = cv2.FONT_HERSHEY_SIMPLEX
# # # # # # # # # # # # # # # # # # # # # # # # #         font_scale = 2
# # # # # # # # # # # # # # # # # # # # # # # # #         font_thickness = 5
# # # # # # # # # # # # # # # # # # # # # # # # #         text_color = (0, 0, 238)

# # # # # # # # # # # # # # # # # # # # # # # # #         (text_width, text_height), _ = cv2.getTextSize(
# # # # # # # # # # # # # # # # # # # # # # # # #             overlay_text, font, font_scale, font_thickness
# # # # # # # # # # # # # # # # # # # # # # # # #         )

# # # # # # # # # # # # # # # # # # # # # # # # #         x = int((image.shape[1] - text_width) / 2)
# # # # # # # # # # # # # # # # # # # # # # # # #         y = image.shape[0] - int(text_height) - 30

# # # # # # # # # # # # # # # # # # # # # # # # #         cv2.putText(
# # # # # # # # # # # # # # # # # # # # # # # # #             image, overlay_text, (x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA
# # # # # # # # # # # # # # # # # # # # # # # # #         )

# # # # # # # # # # # # # # # # # # # # # # # # #         output_file_path = os.path.join(output_directory, f"output_{next_file_number}.png")
# # # # # # # # # # # # # # # # # # # # # # # # #         cv2.imwrite(output_file_path, image)

# # # # # # # # # # # # # # # # # # # # # # # # #         download_url = f"/static/overlayed_images/output_{next_file_number}.png"
# # # # # # # # # # # # # # # # # # # # # # # # #         download_urls.append(download_url)

# # # # # # # # # # # # # # # # # # # # # # # # #         instruction = f"Image {file_name} processed. Download: {download_url}"
# # # # # # # # # # # # # # # # # # # # # # # # #         instructions.append(instruction)

# # # # # # # # # # # # # # # # # # # # # # # # #         next_file_number += 1

# # # # # # # # # # # # # # # # # # # # # # # # #     return {"download_urls": download_urls, "instructions": instructions}

# # # # # # # # # # # # # # # # # # # # # # # # # def get_next_file_number():
# # # # # # # # # # # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/overlayed_images")
# # # # # # # # # # # # # # # # # # # # # # # # #     file_numbers = [
# # # # # # # # # # # # # # # # # # # # # # # # #         int(file.split("_")[1].split(".")[0])
# # # # # # # # # # # # # # # # # # # # # # # # #         for file in overlayed_images
# # # # # # # # # # # # # # # # # # # # # # # # #         if file.startswith("output_")
# # # # # # # # # # # # # # # # # # # # # # # # #     ]
# # # # # # # # # # # # # # # # # # # # # # # # #     if file_numbers:
# # # # # # # # # # # # # # # # # # # # # # # # #         return max(file_numbers) + 1
# # # # # # # # # # # # # # # # # # # # # # # # #     else:
# # # # # # # # # # # # # # # # # # # # # # # # #         return 0

# # # # # # # # # # # # # # # # # # # # # # # # # create_static_folder()
# # # # # # # # # # # # # # # # # # # # # # # # # create_home_html()

# # # # # # # # # # # # # # # # # # # # # # # # # @app.get("/download/{filename}")
# # # # # # # # # # # # # # # # # # # # # # # # # async def download(filename: str):
# # # # # # # # # # # # # # # # # # # # # # # # #     file_path = os.path.join("static", "overlayed_images", filename)

# # # # # # # # # # # # # # # # # # # # # # # # #     if os.path.isfile(file_path):
# # # # # # # # # # # # # # # # # # # # # # # # #         return FileResponse(file_path)

# # # # # # # # # # # # # # # # # # # # # # # # #     return {"detail": "File not found"}

# # # # # # # # # # # # # # # # # # # # # # # # # @app.get("/data")
# # # # # # # # # # # # # # # # # # # # # # # # # async def get_data():
# # # # # # # # # # # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/overlayed_images")
# # # # # # # # # # # # # # # # # # # # # # # # #     return {"overlayed_images": overlayed_images}

# # # # # # # # # # # # # # # # # # # # # # # # # @app.get("/url")
# # # # # # # # # # # # # # # # # # # # # # # # # async def get_shareable_link(request: Request):
# # # # # # # # # # # # # # # # # # # # # # # # #     base_url = request.base_url
# # # # # # # # # # # # # # # # # # # # # # # # #     return {"shareable_link": base_url}

# # # # # # # # # # # # # # # # # # # # # # # # # @app.get("/images")
# # # # # # # # # # # # # # # # # # # # # # # # # async def get_images():
# # # # # # # # # # # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/overlayed_images")
# # # # # # # # # # # # # # # # # # # # # # # # #     image_urls = [
# # # # # # # # # # # # # # # # # # # # # # # # #         f"http://localhost:12000/static/overlayed_images/{image}" for image in overlayed_images
# # # # # # # # # # # # # # # # # # # # # # # # #     ]
# # # # # # # # # # # # # # # # # # # # # # # # #     return {"image_urls": image_urls}

# # # # # # # # # # # # # # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # # # # # # # # # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)

# # # # # # # # # # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # # # # # # # # # import cv2
# # # # # # # # # # # # # # # # # # # # # # # # import numpy as np
# # # # # # # # # # # # # # # # # # # # # # # # from typing import List
# # # # # # # # # # # # # # # # # # # # # # # # from fastapi import FastAPI, UploadFile, Request, File, BackgroundTasks
# # # # # # # # # # # # # # # # # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # # # # # # # # # # # # # # # # from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse
# # # # # # # # # # # # # # # # # # # # # # # # from fastapi.templating import Jinja2Templates
# # # # # # # # # # # # # # # # # # # # # # # # import uvicorn
# # # # # # # # # # # # # # # # # # # # # # # # from rembg import remove
# # # # # # # # # # # # # # # # # # # # # # # # from multiprocessing import Process

# # # # # # # # # # # # # # # # # # # # # # # # app = FastAPI()
# # # # # # # # # # # # # # # # # # # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")
# # # # # # # # # # # # # # # # # # # # # # # # templates = Jinja2Templates(directory="templates")

# # # # # # # # # # # # # # # # # # # # # # # # def create_static_folder():
# # # # # # # # # # # # # # # # # # # # # # # #     base_directory = os.getcwd()
# # # # # # # # # # # # # # # # # # # # # # # #     static_directory = os.path.join(base_directory, "static")
# # # # # # # # # # # # # # # # # # # # # # # #     overlayed_images_directory = os.path.join(static_directory, "overlayed_images")

# # # # # # # # # # # # # # # # # # # # # # # #     print("Base Directory:", base_directory)
# # # # # # # # # # # # # # # # # # # # # # # #     print("Static Directory:", static_directory)
# # # # # # # # # # # # # # # # # # # # # # # #     print("Overlayed Images Directory:", overlayed_images_directory)

# # # # # # # # # # # # # # # # # # # # # # # #     if not os.path.exists(static_directory):
# # # # # # # # # # # # # # # # # # # # # # # #         os.makedirs(static_directory)
# # # # # # # # # # # # # # # # # # # # # # # #         print("Static Directory Created.")

# # # # # # # # # # # # # # # # # # # # # # # #     if not os.path.exists(overlayed_images_directory):
# # # # # # # # # # # # # # # # # # # # # # # #         os.makedirs(overlayed_images_directory)
# # # # # # # # # # # # # # # # # # # # # # # #         print("Overlayed Images Directory Created.")

# # # # # # # # # # # # # # # # # # # # # # # # def create_home_html():
# # # # # # # # # # # # # # # # # # # # # # # #     templates_directory = os.path.join(os.getcwd(), "templates")
# # # # # # # # # # # # # # # # # # # # # # # #     home_html_path = os.path.join(templates_directory, "home.html")

# # # # # # # # # # # # # # # # # # # # # # # #     if not os.path.exists(home_html_path):
# # # # # # # # # # # # # # # # # # # # # # # #         with open(home_html_path, "w") as f:
# # # # # # # # # # # # # # # # # # # # # # # #             f.write(
# # # # # # # # # # # # # # # # # # # # # # # #                 """
# # # # # # # # # # # # # # # # # # # # # # # #                 <html>
# # # # # # # # # # # # # # # # # # # # # # # #                 <head>
# # # # # # # # # # # # # # # # # # # # # # # #                     <title>Upload Images</title>
# # # # # # # # # # # # # # # # # # # # # # # #                 </head>
# # # # # # # # # # # # # # # # # # # # # # # #                 <body>
# # # # # # # # # # # # # # # # # # # # # # # #                     <h1>Upload Images</h1>
# # # # # # # # # # # # # # # # # # # # # # # #                     <form action="/upload" enctype="multipart/form-data" method="post">
# # # # # # # # # # # # # # # # # # # # # # # #                         <input name="files" type="file" multiple>
# # # # # # # # # # # # # # # # # # # # # # # #                         <input type="text" name="text" placeholder="Overlay Text">
# # # # # # # # # # # # # # # # # # # # # # # #                         <input type="submit">
# # # # # # # # # # # # # # # # # # # # # # # #                     </form>
# # # # # # # # # # # # # # # # # # # # # # # #                 </body>
# # # # # # # # # # # # # # # # # # # # # # # #                 </html>
# # # # # # # # # # # # # # # # # # # # # # # #                 """
# # # # # # # # # # # # # # # # # # # # # # # #             )
# # # # # # # # # # # # # # # # # # # # # # # #         print("home.html created.")

# # # # # # # # # # # # # # # # # # # # # # # # @app.get("/", response_class=HTMLResponse)
# # # # # # # # # # # # # # # # # # # # # # # # async def home(request: Request):
# # # # # # # # # # # # # # # # # # # # # # # #     return templates.TemplateResponse("home.html", {"request": request})

# # # # # # # # # # # # # # # # # # # # # # # # def process_image(file: UploadFile, text: str):
# # # # # # # # # # # # # # # # # # # # # # # #     output_directory = "static/overlayed_images"
# # # # # # # # # # # # # # # # # # # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # # # # # # # # # # # # # # # # # # #     with open(f"{output_directory}/{file.filename}", "wb") as f:
# # # # # # # # # # # # # # # # # # # # # # # #         f.write(file.file.read())

# # # # # # # # # # # # # # # # # # # # # # # #     with open(f"{output_directory}/{file.filename}", "rb") as image_file:
# # # # # # # # # # # # # # # # # # # # # # # #         image_data = image_file.read()
# # # # # # # # # # # # # # # # # # # # # # # #         output_data = remove(image_data)

# # # # # # # # # # # # # # # # # # # # # # # #     image_array = np.frombuffer(output_data, np.uint8)

# # # # # # # # # # # # # # # # # # # # # # # #     image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

# # # # # # # # # # # # # # # # # # # # # # # #     image = cv2.resize(image, (1080, 1080))

# # # # # # # # # # # # # # # # # # # # # # # #     file_name_without_extension, file_extension = os.path.splitext(file.filename)

# # # # # # # # # # # # # # # # # # # # # # # #     if text:
# # # # # # # # # # # # # # # # # # # # # # # #         overlay_text = text
# # # # # # # # # # # # # # # # # # # # # # # #     else:
# # # # # # # # # # # # # # # # # # # # # # # #         overlay_text = f"{file_name_without_extension}{file_extension}"

# # # # # # # # # # # # # # # # # # # # # # # #     font = cv2.FONT_HERSHEY_SIMPLEX
# # # # # # # # # # # # # # # # # # # # # # # #     font_scale = 2
# # # # # # # # # # # # # # # # # # # # # # # #     font_thickness = 5
# # # # # # # # # # # # # # # # # # # # # # # #     text_color = (0, 0, 238)

# # # # # # # # # # # # # # # # # # # # # # # #     (text_width, text_height), _ = cv2.getTextSize(
# # # # # # # # # # # # # # # # # # # # # # # #         overlay_text, font, font_scale, font_thickness
# # # # # # # # # # # # # # # # # # # # # # # #     )

# # # # # # # # # # # # # # # # # # # # # # # #     x = int((image.shape[1] - text_width) / 2)
# # # # # # # # # # # # # # # # # # # # # # # #     y = image.shape[0] - int(text_height) - 30

# # # # # # # # # # # # # # # # # # # # # # # #     cv2.putText(
# # # # # # # # # # # # # # # # # # # # # # # #         image, overlay_text, (x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA
# # # # # # # # # # # # # # # # # # # # # # # #     )

# # # # # # # # # # # # # # # # # # # # # # # #     output_file_path = os.path.join(output_directory, file.filename)
# # # # # # # # # # # # # # # # # # # # # # # #     cv2.imwrite(output_file_path, image)

# # # # # # # # # # # # # # # # # # # # # # # # @app.post("/upload")
# # # # # # # # # # # # # # # # # # # # # # # # async def upload(files: List[UploadFile] = File(...), text: str = None, background_tasks: BackgroundTasks = None):
# # # # # # # # # # # # # # # # # # # # # # # #     instructions = []

# # # # # # # # # # # # # # # # # # # # # # # #     for file in files:
# # # # # # # # # # # # # # # # # # # # # # # #         p = Process(target=process_image, args=(file, text))
# # # # # # # # # # # # # # # # # # # # # # # #         p.start()
# # # # # # # # # # # # # # # # # # # # # # # #         p.join()

# # # # # # # # # # # # # # # # # # # # # # # #         instruction = f"Image {file.filename} processing has started."
# # # # # # # # # # # # # # # # # # # # # # # #         instructions.append(instruction)

# # # # # # # # # # # # # # # # # # # # # # # #     return {"instructions": instructions}

# # # # # # # # # # # # # # # # # # # # # # # # @app.get("/download/{filename}")
# # # # # # # # # # # # # # # # # # # # # # # # async def download(filename: str):
# # # # # # # # # # # # # # # # # # # # # # # #     file_path = os.path.join("static", "overlayed_images", filename)

# # # # # # # # # # # # # # # # # # # # # # # #     if os.path.isfile(file_path):
# # # # # # # # # # # # # # # # # # # # # # # #         return FileResponse(file_path)

# # # # # # # # # # # # # # # # # # # # # # # #     return {"detail": "File not found"}

# # # # # # # # # # # # # # # # # # # # # # # # @app.get("/data")
# # # # # # # # # # # # # # # # # # # # # # # # async def get_data():
# # # # # # # # # # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/overlayed_images")
# # # # # # # # # # # # # # # # # # # # # # # #     return {"overlayed_images": overlayed_images}

# # # # # # # # # # # # # # # # # # # # # # # # @app.get("/url")
# # # # # # # # # # # # # # # # # # # # # # # # async def get_shareable_link(request: Request):
# # # # # # # # # # # # # # # # # # # # # # # #     base_url = request.base_url
# # # # # # # # # # # # # # # # # # # # # # # #     return {"shareable_link": base_url}

# # # # # # # # # # # # # # # # # # # # # # # # @app.get("/images")
# # # # # # # # # # # # # # # # # # # # # # # # async def get_images():
# # # # # # # # # # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/overlayed_images")
# # # # # # # # # # # # # # # # # # # # # # # #     image_urls = [
# # # # # # # # # # # # # # # # # # # # # # # #         f"http://localhost:12000/static/overlayed_images/{image}" for image in overlayed_images
# # # # # # # # # # # # # # # # # # # # # # # #     ]
# # # # # # # # # # # # # # # # # # # # # # # #     return {"image_urls": image_urls}

# # # # # # # # # # # # # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # # # # # # # # # # # # #     create_static_folder()
# # # # # # # # # # # # # # # # # # # # # # # #     create_home_html()
# # # # # # # # # # # # # # # # # # # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000, timeout_keep_alive=900)

# # # # # # # # # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # # # # # # # # import cv2
# # # # # # # # # # # # # # # # # # # # # # # import numpy as np
# # # # # # # # # # # # # # # # # # # # # # # from typing import List
# # # # # # # # # # # # # # # # # # # # # # # from fastapi import FastAPI, UploadFile, Request, File
# # # # # # # # # # # # # # # # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # # # # # # # # # # # # # # # from fastapi.responses import HTMLResponse, FileResponse
# # # # # # # # # # # # # # # # # # # # # # # from fastapi.templating import Jinja2Templates
# # # # # # # # # # # # # # # # # # # # # # # import uvicorn
# # # # # # # # # # # # # # # # # # # # # # # from rembg import remove
# # # # # # # # # # # # # # # # # # # # # # # import multiprocessing
# # # # # # # # # # # # # # # # # # # # # # # import asyncio
# # # # # # # # # # # # # # # # # # # # # # # import time


# # # # # # # # # # # # # # # # # # # # # # # app = FastAPI()
# # # # # # # # # # # # # # # # # # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")
# # # # # # # # # # # # # # # # # # # # # # # templates = Jinja2Templates(directory="templates")

# # # # # # # # # # # # # # # # # # # # # # # def create_static_folder():
# # # # # # # # # # # # # # # # # # # # # # #     base_directory = os.getcwd()
# # # # # # # # # # # # # # # # # # # # # # #     static_directory = os.path.join(base_directory, "static")
# # # # # # # # # # # # # # # # # # # # # # #     overlayed_images_directory = os.path.join(static_directory, "overlayed_images")

# # # # # # # # # # # # # # # # # # # # # # #     print("Base Directory:", base_directory)
# # # # # # # # # # # # # # # # # # # # # # #     print("Static Directory:", static_directory)
# # # # # # # # # # # # # # # # # # # # # # #     print("Overlayed Images Directory:", overlayed_images_directory)

# # # # # # # # # # # # # # # # # # # # # # #     if not os.path.exists(static_directory):
# # # # # # # # # # # # # # # # # # # # # # #         os.makedirs(static_directory)
# # # # # # # # # # # # # # # # # # # # # # #         print("Static Directory Created.")

# # # # # # # # # # # # # # # # # # # # # # #     if not os.path.exists(overlayed_images_directory):
# # # # # # # # # # # # # # # # # # # # # # #         os.makedirs(overlayed_images_directory)
# # # # # # # # # # # # # # # # # # # # # # #         print("Overlayed Images Directory Created.")

# # # # # # # # # # # # # # # # # # # # # # # def create_home_html():
# # # # # # # # # # # # # # # # # # # # # # #     templates_directory = os.path.join(os.getcwd(), "templates")
# # # # # # # # # # # # # # # # # # # # # # #     home_html_path = os.path.join(templates_directory, "home.html")

# # # # # # # # # # # # # # # # # # # # # # #     if not os.path.exists(home_html_path):
# # # # # # # # # # # # # # # # # # # # # # #         with open(home_html_path, "w") as f:
# # # # # # # # # # # # # # # # # # # # # # #             f.write(
# # # # # # # # # # # # # # # # # # # # # # #                 """
# # # # # # # # # # # # # # # # # # # # # # #                 <html>
# # # # # # # # # # # # # # # # # # # # # # #                 <head>
# # # # # # # # # # # # # # # # # # # # # # #                     <title>Upload Images</title>
# # # # # # # # # # # # # # # # # # # # # # #                 </head>
# # # # # # # # # # # # # # # # # # # # # # #                 <body>
# # # # # # # # # # # # # # # # # # # # # # #                     <h1>Upload Images</h1>
# # # # # # # # # # # # # # # # # # # # # # #                     <form action="/upload" enctype="multipart/form-data" method="post">
# # # # # # # # # # # # # # # # # # # # # # #                         <input name="files" type="file" multiple>
# # # # # # # # # # # # # # # # # # # # # # #                         <input type="text" name="text" placeholder="Overlay Text">
# # # # # # # # # # # # # # # # # # # # # # #                         <input type="submit">
# # # # # # # # # # # # # # # # # # # # # # #                     </form>
# # # # # # # # # # # # # # # # # # # # # # #                 </body>
# # # # # # # # # # # # # # # # # # # # # # #                 </html>
# # # # # # # # # # # # # # # # # # # # # # #                 """
# # # # # # # # # # # # # # # # # # # # # # #             )
# # # # # # # # # # # # # # # # # # # # # # #         print("home.html created.")

# # # # # # # # # # # # # # # # # # # # # # # @app.get("/", response_class=HTMLResponse)
# # # # # # # # # # # # # # # # # # # # # # # async def home(request: Request):
# # # # # # # # # # # # # # # # # # # # # # #     return templates.TemplateResponse("home.html", {"request": request})

# # # # # # # # # # # # # # # # # # # # # # # async def process_image(file, text, output_directory, next_file_number):
# # # # # # # # # # # # # # # # # # # # # # #     temp_path = os.path.join(output_directory, f"temp_{file.filename}")
# # # # # # # # # # # # # # # # # # # # # # #     with open(temp_path, "wb") as f:
# # # # # # # # # # # # # # # # # # # # # # #         f.write(await file.read())

# # # # # # # # # # # # # # # # # # # # # # #     with open(temp_path, "rb") as image_file:
# # # # # # # # # # # # # # # # # # # # # # #         image_data = image_file.read()
# # # # # # # # # # # # # # # # # # # # # # #         output_data = remove(image_data)

# # # # # # # # # # # # # # # # # # # # # # #     image_array = np.frombuffer(output_data, np.uint8)

# # # # # # # # # # # # # # # # # # # # # # #     image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

# # # # # # # # # # # # # # # # # # # # # # #     image = cv2.resize(image, (1080, 1080))

# # # # # # # # # # # # # # # # # # # # # # #     file_name = file.filename
# # # # # # # # # # # # # # # # # # # # # # #     file_name_without_extension, file_extension = os.path.splitext(file_name)

# # # # # # # # # # # # # # # # # # # # # # #     if text:
# # # # # # # # # # # # # # # # # # # # # # #         overlay_text = text
# # # # # # # # # # # # # # # # # # # # # # #     else:
# # # # # # # # # # # # # # # # # # # # # # #         overlay_text = f"{file_name_without_extension}{file_extension}"

# # # # # # # # # # # # # # # # # # # # # # #     font = cv2.FONT_HERSHEY_SIMPLEX
# # # # # # # # # # # # # # # # # # # # # # #     font_scale = 2
# # # # # # # # # # # # # # # # # # # # # # #     font_thickness = 5
# # # # # # # # # # # # # # # # # # # # # # #     text_color = (0, 0, 238)

# # # # # # # # # # # # # # # # # # # # # # #     (text_width, text_height), _ = cv2.getTextSize(
# # # # # # # # # # # # # # # # # # # # # # #         overlay_text, font, font_scale, font_thickness
# # # # # # # # # # # # # # # # # # # # # # #     )

# # # # # # # # # # # # # # # # # # # # # # #     x = int((image.shape[1] - text_width) / 2)
# # # # # # # # # # # # # # # # # # # # # # #     y = image.shape[0] - int(text_height) - 30

# # # # # # # # # # # # # # # # # # # # # # #     cv2.putText(
# # # # # # # # # # # # # # # # # # # # # # #         image, overlay_text, (x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA
# # # # # # # # # # # # # # # # # # # # # # #     )

# # # # # # # # # # # # # # # # # # # # # # #     output_file_path = os.path.join(output_directory, f"output_{next_file_number}.png")
# # # # # # # # # # # # # # # # # # # # # # #     cv2.imwrite(output_file_path, image)

# # # # # # # # # # # # # # # # # # # # # # #     download_url = f"/static/overlayed_images/output_{next_file_number}.png"

# # # # # # # # # # # # # # # # # # # # # # #     return file.filename, download_url

# # # # # # # # # # # # # # # # # # # # # # # @app.post("/upload")
# # # # # # # # # # # # # # # # # # # # # # # async def upload(files: List[UploadFile] = File(...), text: str = None):
# # # # # # # # # # # # # # # # # # # # # # #     output_directory = "static/overlayed_images"
# # # # # # # # # # # # # # # # # # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # # # # # # # # # # # # # # # # # #     next_file_number = get_next_file_number()

# # # # # # # # # # # # # # # # # # # # # # #     tasks = []
# # # # # # # # # # # # # # # # # # # # # # #     for file in files:
# # # # # # # # # # # # # # # # # # # # # # #         tasks.append(process_image(file, text, output_directory, next_file_number))
# # # # # # # # # # # # # # # # # # # # # # #         next_file_number += 1

# # # # # # # # # # # # # # # # # # # # # # #     results = await asyncio.gather(*tasks)

# # # # # # # # # # # # # # # # # # # # # # #     download_urls = [result[1] for result in results]
# # # # # # # # # # # # # # # # # # # # # # #     instructions = [f"Image {result[0]} processed. Download: {result[1]}" for result in results]

# # # # # # # # # # # # # # # # # # # # # # #     return {"download_urls": download_urls, "instructions": instructions}

# # # # # # # # # # # # # # # # # # # # # # # def get_next_file_number():
# # # # # # # # # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/overlayed_images")
# # # # # # # # # # # # # # # # # # # # # # #     file_numbers = [
# # # # # # # # # # # # # # # # # # # # # # #         int(file.split("_")[1].split(".")[0])
# # # # # # # # # # # # # # # # # # # # # # #         for file in overlayed_images
# # # # # # # # # # # # # # # # # # # # # # #         if file.startswith("output_")
# # # # # # # # # # # # # # # # # # # # # # #     ]
# # # # # # # # # # # # # # # # # # # # # # #     if file_numbers:
# # # # # # # # # # # # # # # # # # # # # # #         return max(file_numbers) + 1
# # # # # # # # # # # # # # # # # # # # # # #     else:
# # # # # # # # # # # # # # # # # # # # # # #         return 0

# # # # # # # # # # # # # # # # # # # # # # # create_static_folder()
# # # # # # # # # # # # # # # # # # # # # # # create_home_html()

# # # # # # # # # # # # # # # # # # # # # # # @app.get("/download/{filename}")
# # # # # # # # # # # # # # # # # # # # # # # async def download(filename: str):
# # # # # # # # # # # # # # # # # # # # # # #     file_path = os.path.join("static", "overlayed_images", filename)

# # # # # # # # # # # # # # # # # # # # # # #     if os.path.isfile(file_path):
# # # # # # # # # # # # # # # # # # # # # # #         return FileResponse(file_path)

# # # # # # # # # # # # # # # # # # # # # # #     return {"detail": "File not found"}

# # # # # # # # # # # # # # # # # # # # # # # @app.get("/data")
# # # # # # # # # # # # # # # # # # # # # # # async def get_data():
# # # # # # # # # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/overlayed_images")
# # # # # # # # # # # # # # # # # # # # # # #     return {"overlayed_images": overlayed_images}

# # # # # # # # # # # # # # # # # # # # # # # @app.get("/url")
# # # # # # # # # # # # # # # # # # # # # # # async def get_shareable_link(request: Request):
# # # # # # # # # # # # # # # # # # # # # # #     base_url = request.base_url
# # # # # # # # # # # # # # # # # # # # # # #     return {"shareable_link": base_url}

# # # # # # # # # # # # # # # # # # # # # # # @app.get("/images")
# # # # # # # # # # # # # # # # # # # # # # # async def get_images():
# # # # # # # # # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/overlayed_images")
# # # # # # # # # # # # # # # # # # # # # # #     image_urls = [
# # # # # # # # # # # # # # # # # # # # # # #         f"http://localhost:12000/static/overlayed_images/{image}" for image in overlayed_images
# # # # # # # # # # # # # # # # # # # # # # #     ]
# # # # # # # # # # # # # # # # # # # # # # #     return {"image_urls": image_urls}

# # # # # # # # # # # # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # # # # # # # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)
# # # # # # # # # # # # # # # # # # # # # # #     time.sleep(900)  # Wait for 15 minutes
# # # # # # # # # # # # # # # # # # # # # # #     uvicorn.stop()



# # # # # # # # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # # # # # # # from PIL import Image
# # # # # # # # # # # # # # # # # # # # # # from typing import List
# # # # # # # # # # # # # # # # # # # # # # from fastapi import FastAPI, UploadFile, Request, File
# # # # # # # # # # # # # # # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # # # # # # # # # # # # # # from fastapi.responses import FileResponse, JSONResponse
# # # # # # # # # # # # # # # # # # # # # # from fastapi.templating import Jinja2Templates
# # # # # # # # # # # # # # # # # # # # # # import rembg

# # # # # # # # # # # # # # # # # # # # # # app = FastAPI()
# # # # # # # # # # # # # # # # # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")
# # # # # # # # # # # # # # # # # # # # # # templates = Jinja2Templates(directory="templates")

# # # # # # # # # # # # # # # # # # # # # # # Define the upload endpoint
# # # # # # # # # # # # # # # # # # # # # # @app.post("/upload")
# # # # # # # # # # # # # # # # # # # # # # async def upload(files: List[UploadFile] = File(...), text: str = None):
# # # # # # # # # # # # # # # # # # # # # #     output_directory = "static/output"
# # # # # # # # # # # # # # # # # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # # # # # # # # # # # # # # # # #     download_urls = []
# # # # # # # # # # # # # # # # # # # # # #     instructions = []

# # # # # # # # # # # # # # # # # # # # # #     for i, file in enumerate(files):
# # # # # # # # # # # # # # # # # # # # # #         try:
# # # # # # # # # # # # # # # # # # # # # #             # Save the uploaded file temporarily
# # # # # # # # # # # # # # # # # # # # # #             temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # # # # # # # # # # # # # # # # # #             with open(temp_path, "wb") as f:
# # # # # # # # # # # # # # # # # # # # # #                 f.write(await file.read())

# # # # # # # # # # # # # # # # # # # # # #             # Remove the background using rembg
# # # # # # # # # # # # # # # # # # # # # #             output_path = os.path.join(output_directory, f"output_{i}.png")
# # # # # # # # # # # # # # # # # # # # # #             with open(temp_path, "rb") as img_file, open(output_path, "wb") as output_file:
# # # # # # # # # # # # # # # # # # # # # #                 img_data = img_file.read()
# # # # # # # # # # # # # # # # # # # # # #                 output_data = rembg.remove(img_data)
# # # # # # # # # # # # # # # # # # # # # #                 output_file.write(output_data)

# # # # # # # # # # # # # # # # # # # # # #             # Resize the image to 1080x1080 and add overlay text
# # # # # # # # # # # # # # # # # # # # # #             image = Image.open(output_path)
# # # # # # # # # # # # # # # # # # # # # #             image = image.resize((1080, 1080))
# # # # # # # # # # # # # # # # # # # # # #             image_with_text = add_text_overlay(image, file.filename, text)
# # # # # # # # # # # # # # # # # # # # # #             image_with_text.save(output_path)

# # # # # # # # # # # # # # # # # # # # # #             # Remove the temporary file
# # # # # # # # # # # # # # # # # # # # # #             os.remove(temp_path)

# # # # # # # # # # # # # # # # # # # # # #             # Generate the download link URL for the output image
# # # # # # # # # # # # # # # # # # # # # #             download_url = f"/static/output/output_{i}.png"
# # # # # # # # # # # # # # # # # # # # # #             download_urls.append(download_url)

# # # # # # # # # # # # # # # # # # # # # #             # Add instruction
# # # # # # # # # # # # # # # # # # # # # #             instruction = f"Image {file.filename} processed. Download: {download_url}"
# # # # # # # # # # # # # # # # # # # # # #             instructions.append(instruction)
# # # # # # # # # # # # # # # # # # # # # #         except Exception as e:
# # # # # # # # # # # # # # # # # # # # # #             # Log the error and continue with the next file
# # # # # # # # # # # # # # # # # # # # # #             error_message = f"Error processing file {file.filename}: {str(e)}"
# # # # # # # # # # # # # # # # # # # # # #             print(error_message)

# # # # # # # # # # # # # # # # # # # # # #     # Return the download URLs and instructions in the API response
# # # # # # # # # # # # # # # # # # # # # #     return {"download_urls": download_urls, "instructions": instructions}


# # # # # # # # # # # # # # # # # # # # # # def add_text_overlay(image, filename, text):
# # # # # # # # # # # # # # # # # # # # # #     from PIL import ImageDraw, ImageFont

# # # # # # # # # # # # # # # # # # # # # #     overlay_text = text or filename
# # # # # # # # # # # # # # # # # # # # # #     font = ImageFont.truetype("arial.ttf", 100)
# # # # # # # # # # # # # # # # # # # # # #     draw = ImageDraw.Draw(image)
# # # # # # # # # # # # # # # # # # # # # #     text_width, text_height = draw.textsize(overlay_text, font=font)
# # # # # # # # # # # # # # # # # # # # # #     x = int((image.width - text_width) / 2)
# # # # # # # # # # # # # # # # # # # # # #     y = image.height - text_height - 30
# # # # # # # # # # # # # # # # # # # # # #     draw.text((x, y), overlay_text, font=font, fill=(0, 0, 238))

# # # # # # # # # # # # # # # # # # # # # #     return image


# # # # # # # # # # # # # # # # # # # # # # @app.get("/download/{filename}")
# # # # # # # # # # # # # # # # # # # # # # async def download(filename: str):
# # # # # # # # # # # # # # # # # # # # # #     # Making the file path
# # # # # # # # # # # # # # # # # # # # # #     file_path = os.path.join("static", "output", filename)

# # # # # # # # # # # # # # # # # # # # # #     # Check if the file exists
# # # # # # # # # # # # # # # # # # # # # #     if os.path.isfile(file_path):
# # # # # # # # # # # # # # # # # # # # # #         # If the file exists, return it as a response
# # # # # # # # # # # # # # # # # # # # # #         return FileResponse(file_path)

# # # # # # # # # # # # # # # # # # # # # #     # If the file does not exist, return a 404 Not Found response
# # # # # # # # # # # # # # # # # # # # # #     return {"detail": "File not found"}


# # # # # # # # # # # # # # # # # # # # # # @app.get("/data")
# # # # # # # # # # # # # # # # # # # # # # async def get_data():
# # # # # # # # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/output")
# # # # # # # # # # # # # # # # # # # # # #     return {"overlayed_images": overlayed_images}


# # # # # # # # # # # # # # # # # # # # # # @app.get("/url")
# # # # # # # # # # # # # # # # # # # # # # async def get_shareable_link(request: Request):
# # # # # # # # # # # # # # # # # # # # # #     base_url = request.base_url
# # # # # # # # # # # # # # # # # # # # # #     return {"shareable_link": base_url}


# # # # # # # # # # # # # # # # # # # # # # @app.get("/images")
# # # # # # # # # # # # # # # # # # # # # # async def get_images():
# # # # # # # # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/output")
# # # # # # # # # # # # # # # # # # # # # #     image_urls = [
# # # # # # # # # # # # # # # # # # # # # #         f"/static/output/{image}" for image in overlayed_images
# # # # # # # # # # # # # # # # # # # # # #     ]
# # # # # # # # # # # # # # # # # # # # # #     return {"image_urls": image_urls}

# # # # # # # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # # # # # # import cv2
# # # # # # # # # # # # # # # # # # # # # from typing import List
# # # # # # # # # # # # # # # # # # # # # from fastapi import FastAPI, UploadFile, Request, File
# # # # # # # # # # # # # # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # # # # # # # # # # # # # from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
# # # # # # # # # # # # # # # # # # # # # from fastapi.templating import Jinja2Templates
# # # # # # # # # # # # # # # # # # # # # import uvicorn

# # # # # # # # # # # # # # # # # # # # # app = FastAPI()
# # # # # # # # # # # # # # # # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")
# # # # # # # # # # # # # # # # # # # # # templates = Jinja2Templates(directory="templates")

# # # # # # # # # # # # # # # # # # # # # # Define the home page
# # # # # # # # # # # # # # # # # # # # # @app.get("/", response_class=HTMLResponse)
# # # # # # # # # # # # # # # # # # # # # async def home(request: Request):
# # # # # # # # # # # # # # # # # # # # #     return templates.TemplateResponse("home.html", {"request": request})


# # # # # # # # # # # # # # # # # # # # # # Define the upload endpoint
# # # # # # # # # # # # # # # # # # # # # @app.post("/upload")
# # # # # # # # # # # # # # # # # # # # # async def upload(files: List[UploadFile] = File(...), text: str = None):
# # # # # # # # # # # # # # # # # # # # #     output_directory = "static/output"
# # # # # # # # # # # # # # # # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # # # # # # # # # # # # # # # #     download_urls = []
# # # # # # # # # # # # # # # # # # # # #     instructions = []

# # # # # # # # # # # # # # # # # # # # #     for i, file in enumerate(files):
# # # # # # # # # # # # # # # # # # # # #         # Save the uploaded file temporarily
# # # # # # # # # # # # # # # # # # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # # # # # # # # # # # # # # # # #         with open(temp_path, "wb") as f:
# # # # # # # # # # # # # # # # # # # # #             f.write(await file.read())

# # # # # # # # # # # # # # # # # # # # #         # Read the image using OpenCV
# # # # # # # # # # # # # # # # # # # # #         image = cv2.imread(temp_path)

# # # # # # # # # # # # # # # # # # # # #         # Get the name from the uploaded file
# # # # # # # # # # # # # # # # # # # # #         file_name = file.filename
# # # # # # # # # # # # # # # # # # # # #         file_name_without_extension, file_extension = os.path.splitext(file_name)

# # # # # # # # # # # # # # # # # # # # #         # Prepare the text to overlay on the image
# # # # # # # # # # # # # # # # # # # # #         if text:
# # # # # # # # # # # # # # # # # # # # #             overlay_text = text
# # # # # # # # # # # # # # # # # # # # #         else:
# # # # # # # # # # # # # # # # # # # # #             overlay_text = f"{file_name_without_extension}{file_extension}"

# # # # # # # # # # # # # # # # # # # # #         font = cv2.FONT_HERSHEY_SIMPLEX
# # # # # # # # # # # # # # # # # # # # #         font_scale = 2
# # # # # # # # # # # # # # # # # # # # #         font_thickness = 5
# # # # # # # # # # # # # # # # # # # # #         text_color = (0, 0, 238)

# # # # # # # # # # # # # # # # # # # # #         # Set the text size
# # # # # # # # # # # # # # # # # # # # #         (text_width, text_height), _ = cv2.getTextSize(
# # # # # # # # # # # # # # # # # # # # #             overlay_text, font, font_scale, font_thickness
# # # # # # # # # # # # # # # # # # # # #         )

# # # # # # # # # # # # # # # # # # # # #         # Calculate the position to place the text
# # # # # # # # # # # # # # # # # # # # #         x = int((image.shape[1] - text_width) / 2)  # Centered horizontally
# # # # # # # # # # # # # # # # # # # # #         y = int((image.shape[0] + text_height) - 30)  # Centered vertically

# # # # # # # # # # # # # # # # # # # # #         # Overlay the text on the image
# # # # # # # # # # # # # # # # # # # # #         cv2.putText(
# # # # # # # # # # # # # # # # # # # # #             image, overlay_text, (x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA
# # # # # # # # # # # # # # # # # # # # #         )

# # # # # # # # # # # # # # # # # # # # #         # Set the output file path
# # # # # # # # # # # # # # # # # # # # #         output_file_path = os.path.join(output_directory, f"output_{i}.png")

# # # # # # # # # # # # # # # # # # # # #         # Save the resulting image
# # # # # # # # # # # # # # # # # # # # #         cv2.imwrite(output_file_path, image)

# # # # # # # # # # # # # # # # # # # # #         # Remove the temporary file
# # # # # # # # # # # # # # # # # # # # #         os.remove(temp_path)

# # # # # # # # # # # # # # # # # # # # #         # Generate the download link URL for the output image
# # # # # # # # # # # # # # # # # # # # #         download_url = f"/static/output/output_{i}.png"
# # # # # # # # # # # # # # # # # # # # #         download_urls.append(download_url)

# # # # # # # # # # # # # # # # # # # # #         # Add instruction
# # # # # # # # # # # # # # # # # # # # #         instruction = f"Image {file_name} processed. Download: {download_url}"
# # # # # # # # # # # # # # # # # # # # #         instructions.append(instruction)

# # # # # # # # # # # # # # # # # # # # #     # Return the download URLs and instructions in the API response
# # # # # # # # # # # # # # # # # # # # #     return {"download_urls": download_urls, "instructions": instructions}


# # # # # # # # # # # # # # # # # # # # # @app.get("/download/{filename}")
# # # # # # # # # # # # # # # # # # # # # async def download(filename: str):
# # # # # # # # # # # # # # # # # # # # #     # Making the file path
# # # # # # # # # # # # # # # # # # # # #     file_path = os.path.join("static", "output", filename)

# # # # # # # # # # # # # # # # # # # # #     # Check if the file exists
# # # # # # # # # # # # # # # # # # # # #     if os.path.isfile(file_path):
# # # # # # # # # # # # # # # # # # # # #         # If the file exists, return it as a response
# # # # # # # # # # # # # # # # # # # # #         return FileResponse(file_path)

# # # # # # # # # # # # # # # # # # # # #     # If the file does not exist, return a 404 Not Found response
# # # # # # # # # # # # # # # # # # # # #     return {"detail": "File not found"}


# # # # # # # # # # # # # # # # # # # # # @app.get("/data")
# # # # # # # # # # # # # # # # # # # # # async def get_data():
# # # # # # # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/output")
# # # # # # # # # # # # # # # # # # # # #     return {"overlayed_images": overlayed_images}


# # # # # # # # # # # # # # # # # # # # # @app.get("/url")
# # # # # # # # # # # # # # # # # # # # # async def get_shareable_link(request: Request):
# # # # # # # # # # # # # # # # # # # # #     base_url = request.base_url
# # # # # # # # # # # # # # # # # # # # #     return {"shareable_link": base_url}


# # # # # # # # # # # # # # # # # # # # # @app.get("/images")
# # # # # # # # # # # # # # # # # # # # # async def get_images():
# # # # # # # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/output")
# # # # # # # # # # # # # # # # # # # # #     image_urls = [
# # # # # # # # # # # # # # # # # # # # #         f"http://localhost:12000/static/output/{image}" for image in overlayed_images
# # # # # # # # # # # # # # # # # # # # #     ]
# # # # # # # # # # # # # # # # # # # # #     return {"image_urls": image_urls}


# # # # # # # # # # # # # # # # # # # # # # Start the server
# # # # # # # # # # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # # # # # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)


# # # # # # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # # # # # import cv2
# # # # # # # # # # # # # # # # # # # # from typing import List
# # # # # # # # # # # # # # # # # # # # from fastapi import FastAPI, UploadFile, Request, File
# # # # # # # # # # # # # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # # # # # # # # # # # # from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
# # # # # # # # # # # # # # # # # # # # from fastapi.templating import Jinja2Templates
# # # # # # # # # # # # # # # # # # # # import uvicorn
# # # # # # # # # # # # # # # # # # # # import numpy as np
# # # # # # # # # # # # # # # # # # # # from rembg import remove

# # # # # # # # # # # # # # # # # # # # app = FastAPI()
# # # # # # # # # # # # # # # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")
# # # # # # # # # # # # # # # # # # # # templates = Jinja2Templates(directory="templates")

# # # # # # # # # # # # # # # # # # # # # Define the home page
# # # # # # # # # # # # # # # # # # # # @app.get("/", response_class=HTMLResponse)
# # # # # # # # # # # # # # # # # # # # async def home(request: Request):
# # # # # # # # # # # # # # # # # # # #     return templates.TemplateResponse("home.html", {"request": request})


# # # # # # # # # # # # # # # # # # # # # Define the upload endpoint
# # # # # # # # # # # # # # # # # # # # @app.post("/upload")
# # # # # # # # # # # # # # # # # # # # async def upload(files: List[UploadFile] = File(...), text: str = None):
# # # # # # # # # # # # # # # # # # # #     output_directory = "static/output"
# # # # # # # # # # # # # # # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # # # # # # # # # # # # # # #     download_urls = []
# # # # # # # # # # # # # # # # # # # #     instructions = []

# # # # # # # # # # # # # # # # # # # #     for i, file in enumerate(files):
# # # # # # # # # # # # # # # # # # # #         # Save the uploaded file temporarily
# # # # # # # # # # # # # # # # # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # # # # # # # # # # # # # # # #         with open(temp_path, "wb") as f:
# # # # # # # # # # # # # # # # # # # #             f.write(await file.read())

# # # # # # # # # # # # # # # # # # # #         # Remove the background of the image using rembg module
# # # # # # # # # # # # # # # # # # # #         with open(temp_path, "rb") as image_file:
# # # # # # # # # # # # # # # # # # # #             image_data = image_file.read()
# # # # # # # # # # # # # # # # # # # #             output_data = remove(image_data)

# # # # # # # # # # # # # # # # # # # #         # Convert the image data to a NumPy array
# # # # # # # # # # # # # # # # # # # #         image_array = np.frombuffer(output_data, np.uint8)

# # # # # # # # # # # # # # # # # # # #         # Decode the image array
# # # # # # # # # # # # # # # # # # # #         image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

# # # # # # # # # # # # # # # # # # # #         # Get the name from the uploaded file
# # # # # # # # # # # # # # # # # # # #         file_name = file.filename
# # # # # # # # # # # # # # # # # # # #         file_name_without_extension, file_extension = os.path.splitext(file_name)

# # # # # # # # # # # # # # # # # # # #         # Prepare the text to overlay on the image
# # # # # # # # # # # # # # # # # # # #         if text:
# # # # # # # # # # # # # # # # # # # #             overlay_text = text
# # # # # # # # # # # # # # # # # # # #         else:
# # # # # # # # # # # # # # # # # # # #             overlay_text = f"{file_name_without_extension}{file_extension}"

# # # # # # # # # # # # # # # # # # # #         font = cv2.FONT_HERSHEY_SIMPLEX
# # # # # # # # # # # # # # # # # # # #         font_scale = 2
# # # # # # # # # # # # # # # # # # # #         font_thickness = 5
# # # # # # # # # # # # # # # # # # # #         text_color = (0, 0, 238)

# # # # # # # # # # # # # # # # # # # #         # Set the text size
# # # # # # # # # # # # # # # # # # # #         (text_width, text_height), _ = cv2.getTextSize(
# # # # # # # # # # # # # # # # # # # #             overlay_text, font, font_scale, font_thickness
# # # # # # # # # # # # # # # # # # # #         )

# # # # # # # # # # # # # # # # # # # #         # Calculate the position to place the text
# # # # # # # # # # # # # # # # # # # #         x = int((text_width - image.shape[1]) / 2)  # Centered horizontally
# # # # # # # # # # # # # # # # # # # #         y = int((image.shape[0] + text_height) - 30)  # Centered vertically

# # # # # # # # # # # # # # # # # # # #         # Overlay the text on the image
# # # # # # # # # # # # # # # # # # # #         cv2.putText(
# # # # # # # # # # # # # # # # # # # #             image, overlay_text, (x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA
# # # # # # # # # # # # # # # # # # # #         )

# # # # # # # # # # # # # # # # # # # #         # Set the output file path
# # # # # # # # # # # # # # # # # # # #         output_file_path = os.path.join(output_directory, f"output_{i}.png")

# # # # # # # # # # # # # # # # # # # #         # Save the resulting image
# # # # # # # # # # # # # # # # # # # #         cv2.imwrite(output_file_path, image)

# # # # # # # # # # # # # # # # # # # #         # Remove the temporary file
# # # # # # # # # # # # # # # # # # # #         os.remove(temp_path)

# # # # # # # # # # # # # # # # # # # #         # Generate the download link URL for the output image
# # # # # # # # # # # # # # # # # # # #         download_url = f"/static/output/output_{i}.png"
# # # # # # # # # # # # # # # # # # # #         download_urls.append(download_url)

# # # # # # # # # # # # # # # # # # # #         # Add instruction
# # # # # # # # # # # # # # # # # # # #         instruction = f"Image {file_name} processed. Download: {download_url}"
# # # # # # # # # # # # # # # # # # # #         instructions.append(instruction)

# # # # # # # # # # # # # # # # # # # #     # Return the download URLs and instructions in the API response
# # # # # # # # # # # # # # # # # # # #     return {"download_urls": download_urls, "instructions": instructions}


# # # # # # # # # # # # # # # # # # # # @app.get("/download/{filename}")
# # # # # # # # # # # # # # # # # # # # async def download(filename: str):
# # # # # # # # # # # # # # # # # # # #     # Making the file path
# # # # # # # # # # # # # # # # # # # #     file_path = os.path.join("static", "output", filename)

# # # # # # # # # # # # # # # # # # # #     # Check if the file exists
# # # # # # # # # # # # # # # # # # # #     if os.path.isfile(file_path):
# # # # # # # # # # # # # # # # # # # #         # If the file exists, return it as a response
# # # # # # # # # # # # # # # # # # # #         return FileResponse(file_path)

# # # # # # # # # # # # # # # # # # # #     # If the file does not exist, return a 404 Not Found response
# # # # # # # # # # # # # # # # # # # #     return {"detail": "File not found"}


# # # # # # # # # # # # # # # # # # # # @app.get("/data")
# # # # # # # # # # # # # # # # # # # # async def get_data():
# # # # # # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/output")
# # # # # # # # # # # # # # # # # # # #     return {"overlayed_images": overlayed_images}


# # # # # # # # # # # # # # # # # # # # @app.get("/url")
# # # # # # # # # # # # # # # # # # # # async def get_shareable_link(request: Request):
# # # # # # # # # # # # # # # # # # # #     base_url = request.base_url
# # # # # # # # # # # # # # # # # # # #     return {"shareable_link": base_url}


# # # # # # # # # # # # # # # # # # # # @app.get("/images")
# # # # # # # # # # # # # # # # # # # # async def get_images():
# # # # # # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/output")
# # # # # # # # # # # # # # # # # # # #     image_urls = [
# # # # # # # # # # # # # # # # # # # #         f"http://localhost:12000/static/output/{image}" for image in overlayed_images
# # # # # # # # # # # # # # # # # # # #     ]
# # # # # # # # # # # # # # # # # # # #     return {"image_urls": image_urls}


# # # # # # # # # # # # # # # # # # # # # Start the server
# # # # # # # # # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # # # # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)


# # # # # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # # # # import cv2
# # # # # # # # # # # # # # # # # # # from typing import List
# # # # # # # # # # # # # # # # # # # from fastapi import FastAPI, UploadFile, Request, File
# # # # # # # # # # # # # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # # # # # # # # # # # from fastapi.responses import FileResponse, JSONResponse
# # # # # # # # # # # # # # # # # # # from fastapi.templating import Jinja2Templates
# # # # # # # # # # # # # # # # # # # import uvicorn

# # # # # # # # # # # # # # # # # # # app = FastAPI()
# # # # # # # # # # # # # # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")
# # # # # # # # # # # # # # # # # # # templates = Jinja2Templates(directory="templates")

# # # # # # # # # # # # # # # # # # # # Define the upload endpoint
# # # # # # # # # # # # # # # # # # # @app.post("/upload")
# # # # # # # # # # # # # # # # # # # async def upload(files: List[UploadFile] = File(...), text: str = None):
# # # # # # # # # # # # # # # # # # #     output_directory = "static/output"
# # # # # # # # # # # # # # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # # # # # # # # # # # # # #     download_urls = []
# # # # # # # # # # # # # # # # # # #     instructions = []

# # # # # # # # # # # # # # # # # # #     for i, file in enumerate(files):
# # # # # # # # # # # # # # # # # # #         # Save the uploaded file temporarily
# # # # # # # # # # # # # # # # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # # # # # # # # # # # # # # #         with open(temp_path, "wb") as f:
# # # # # # # # # # # # # # # # # # #             f.write(await file.read())

# # # # # # # # # # # # # # # # # # #         # Read the image using OpenCV
# # # # # # # # # # # # # # # # # # #         image = cv2.imread(temp_path)

# # # # # # # # # # # # # # # # # # #         # Resize the image to 1080x1080
# # # # # # # # # # # # # # # # # # #         image = cv2.resize(image, (1080, 1080))

# # # # # # # # # # # # # # # # # # #         # Remove the background using Rembg (requires Rembg library installed)
# # # # # # # # # # # # # # # # # # #         try:
# # # # # # # # # # # # # # # # # # #             import rembg
# # # # # # # # # # # # # # # # # # #             image = rembg.remove(image)
# # # # # # # # # # # # # # # # # # #         except ImportError:
# # # # # # # # # # # # # # # # # # #             return JSONResponse(
# # # # # # # # # # # # # # # # # # #                 {"error": "Rembg library not found. Please install it to remove the background."},
# # # # # # # # # # # # # # # # # # #                 status_code=500,
# # # # # # # # # # # # # # # # # # #             )

# # # # # # # # # # # # # # # # # # #         # Prepare the text to overlay on the image
# # # # # # # # # # # # # # # # # # #         if text:
# # # # # # # # # # # # # # # # # # #             overlay_text = text
# # # # # # # # # # # # # # # # # # #         else:
# # # # # # # # # # # # # # # # # # #             file_name = file.filename
# # # # # # # # # # # # # # # # # # #             file_name_without_extension, file_extension = os.path.splitext(file_name)
# # # # # # # # # # # # # # # # # # #             overlay_text = f"{file_name_without_extension}{file_extension}"

# # # # # # # # # # # # # # # # # # #         font = cv2.FONT_HERSHEY_SIMPLEX
# # # # # # # # # # # # # # # # # # #         font_scale = 2
# # # # # # # # # # # # # # # # # # #         font_thickness = 5
# # # # # # # # # # # # # # # # # # #         text_color = (0, 0, 238)

# # # # # # # # # # # # # # # # # # #         # Set the text size
# # # # # # # # # # # # # # # # # # #         (text_width, text_height), _ = cv2.getTextSize(
# # # # # # # # # # # # # # # # # # #             overlay_text, font, font_scale, font_thickness
# # # # # # # # # # # # # # # # # # #         )

# # # # # # # # # # # # # # # # # # #         # Calculate the position to place the text
# # # # # # # # # # # # # # # # # # #         x = int((image.shape[1] - text_width) / 2)  # Centered horizontally
# # # # # # # # # # # # # # # # # # #         y = int((image.shape[0] + text_height) - 30)  # Placed at the bottom

# # # # # # # # # # # # # # # # # # #         # Overlay the text on the image
# # # # # # # # # # # # # # # # # # #         cv2.putText(
# # # # # # # # # # # # # # # # # # #             image, overlay_text, (x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA
# # # # # # # # # # # # # # # # # # #         )

# # # # # # # # # # # # # # # # # # #         # Set the output file path
# # # # # # # # # # # # # # # # # # #         output_file_path = os.path.join(output_directory, f"output_{i}.png")

# # # # # # # # # # # # # # # # # # #         # Save the resulting image
# # # # # # # # # # # # # # # # # # #         cv2.imwrite(output_file_path, image)

# # # # # # # # # # # # # # # # # # #         # Remove the temporary file
# # # # # # # # # # # # # # # # # # #         os.remove(temp_path)

# # # # # # # # # # # # # # # # # # #         # Generate the download link URL for the output image
# # # # # # # # # # # # # # # # # # #         download_url = f"/static/output/output_{i}.png"
# # # # # # # # # # # # # # # # # # #         download_urls.append(download_url)

# # # # # # # # # # # # # # # # # # #         # Add instruction
# # # # # # # # # # # # # # # # # # #         instruction = f"Image {file.filename} processed. Download: {download_url}"
# # # # # # # # # # # # # # # # # # #         instructions.append(instruction)

# # # # # # # # # # # # # # # # # # #     # Return the download URLs and instructions in the API response
# # # # # # # # # # # # # # # # # # #     return {"download_urls": download_urls, "instructions": instructions}


# # # # # # # # # # # # # # # # # # # @app.get("/download/{filename}")
# # # # # # # # # # # # # # # # # # # async def download(filename: str):
# # # # # # # # # # # # # # # # # # #     # Making the file path
# # # # # # # # # # # # # # # # # # #     file_path = os.path.join("static", "output", filename)

# # # # # # # # # # # # # # # # # # #     # Check if the file exists
# # # # # # # # # # # # # # # # # # #     if os.path.isfile(file_path):
# # # # # # # # # # # # # # # # # # #         # If the file exists, return it as a response
# # # # # # # # # # # # # # # # # # #         return FileResponse(file_path)

# # # # # # # # # # # # # # # # # # #     # If the file does not exist, return a 404 Not Found response
# # # # # # # # # # # # # # # # # # #     return {"detail": "File not found"}


# # # # # # # # # # # # # # # # # # # @app.get("/data")
# # # # # # # # # # # # # # # # # # # async def get_data():
# # # # # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/output")
# # # # # # # # # # # # # # # # # # #     return {"overlayed_images": overlayed_images}


# # # # # # # # # # # # # # # # # # # @app.get("/url")
# # # # # # # # # # # # # # # # # # # async def get_shareable_link(request: Request):
# # # # # # # # # # # # # # # # # # #     base_url = request.base_url
# # # # # # # # # # # # # # # # # # #     return {"shareable_link": base_url}


# # # # # # # # # # # # # # # # # # # @app.get("/images")
# # # # # # # # # # # # # # # # # # # async def get_images():
# # # # # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/output")
# # # # # # # # # # # # # # # # # # #     image_urls = [
# # # # # # # # # # # # # # # # # # #         f"http://localhost:12000/static/output/{image}" for image in overlayed_images
# # # # # # # # # # # # # # # # # # #     ]
# # # # # # # # # # # # # # # # # # #     return {"image_urls": image_urls}


# # # # # # # # # # # # # # # # # # # # Start the server
# # # # # # # # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # # # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)
# # # # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # # # import cv2
# # # # # # # # # # # # # # # # # # import numpy as np
# # # # # # # # # # # # # # # # # # from typing import List
# # # # # # # # # # # # # # # # # # from fastapi import FastAPI, UploadFile, Request, File
# # # # # # # # # # # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # # # # # # # # # # from fastapi.responses import FileResponse, JSONResponse
# # # # # # # # # # # # # # # # # # from fastapi.templating import Jinja2Templates
# # # # # # # # # # # # # # # # # # import uvicorn
# # # # # # # # # # # # # # # # # # from PIL import Image

# # # # # # # # # # # # # # # # # # app = FastAPI()
# # # # # # # # # # # # # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")
# # # # # # # # # # # # # # # # # # templates = Jinja2Templates(directory="templates")

# # # # # # # # # # # # # # # # # # # Define the upload endpoint
# # # # # # # # # # # # # # # # # # @app.post("/upload")
# # # # # # # # # # # # # # # # # # async def upload(files: List[UploadFile] = File(...), text: str = None):
# # # # # # # # # # # # # # # # # #     output_directory = "static/output"
# # # # # # # # # # # # # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # # # # # # # # # # # # #     download_urls = []
# # # # # # # # # # # # # # # # # #     instructions = []

# # # # # # # # # # # # # # # # # #     for i, file in enumerate(files):
# # # # # # # # # # # # # # # # # #         # Save the uploaded file temporarily
# # # # # # # # # # # # # # # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # # # # # # # # # # # # # #         with open(temp_path, "wb") as f:
# # # # # # # # # # # # # # # # # #             f.write(await file.read())

# # # # # # # # # # # # # # # # # #         # Read the image using OpenCV
# # # # # # # # # # # # # # # # # #         img = cv2.imread(temp_path)

# # # # # # # # # # # # # # # # # #         # Remove the background using the provided code
# # # # # # # # # # # # # # # # # #         original = img.copy()

# # # # # # # # # # # # # # # # # #         l = int(max(5, 6))
# # # # # # # # # # # # # # # # # #         u = int(min(6, 6))

# # # # # # # # # # # # # # # # # #         ed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# # # # # # # # # # # # # # # # # #         edges = cv2.GaussianBlur(img, (21, 51), 3)
# # # # # # # # # # # # # # # # # #         edges = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)
# # # # # # # # # # # # # # # # # #         edges = cv2.Canny(edges, l, u)

# # # # # # # # # # # # # # # # # #         _, thresh = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# # # # # # # # # # # # # # # # # #         kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
# # # # # # # # # # # # # # # # # #         mask = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=4)

# # # # # # # # # # # # # # # # # #         data = mask.tolist()
# # # # # # # # # # # # # # # # # #         sys.setrecursionlimit(10**8)
# # # # # # # # # # # # # # # # # #         for i in range(len(data)):
# # # # # # # # # # # # # # # # # #             for j in range(len(data[i])):
# # # # # # # # # # # # # # # # # #                 if data[i][j] != 255:
# # # # # # # # # # # # # # # # # #                     data[i][j] = -1
# # # # # # # # # # # # # # # # # #                 else:
# # # # # # # # # # # # # # # # # #                     break
# # # # # # # # # # # # # # # # # #             for j in range(len(data[i])-1, -1, -1):
# # # # # # # # # # # # # # # # # #                 if data[i][j] != 255:
# # # # # # # # # # # # # # # # # #                     data[i][j] = -1
# # # # # # # # # # # # # # # # # #                 else:
# # # # # # # # # # # # # # # # # #                     break
# # # # # # # # # # # # # # # # # #         image = np.array(data)
# # # # # # # # # # # # # # # # # #         image[image != -1] = 255
# # # # # # # # # # # # # # # # # #         image[image == -1] = 0

# # # # # # # # # # # # # # # # # #         mask = np.array(image, np.uint8)

# # # # # # # # # # # # # # # # # #         result = cv2.bitwise_and(original, original, mask=mask)
# # # # # # # # # # # # # # # # # #         result[mask == 0] = 255
# # # # # # # # # # # # # # # # # #         cv2.imwrite('bg.png', result)

# # # # # # # # # # # # # # # # # #         img = Image.open('bg.png')
# # # # # # # # # # # # # # # # # #         img.convert("RGBA")
# # # # # # # # # # # # # # # # # #         datas = img.getdata()

# # # # # # # # # # # # # # # # # #         newData = []
# # # # # # # # # # # # # # # # # #         for item in datas:
# # # # # # # # # # # # # # # # # #             if item[0] == 255 and item[1] == 255 and item[2] == 255:
# # # # # # # # # # # # # # # # # #                 newData.append((255, 255, 255, 0))
# # # # # # # # # # # # # # # # # #             else:
# # # # # # # # # # # # # # # # # #                 newData.append(item)

# # # # # # # # # # # # # # # # # #         img.putdata(newData)
# # # # # # # # # # # # # # # # # #         img_path = os.path.join(output_directory, f"output_{i}.png")
# # # # # # # # # # # # # # # # # #         img.save(img_path, "PNG")

# # # # # # # # # # # # # # # # # #         # Prepare the text to overlay on the image
# # # # # # # # # # # # # # # # # #         if text:
# # # # # # # # # # # # # # # # # #             overlay_text = text
# # # # # # # # # # # # # # # # # #         else:
# # # # # # # # # # # # # # # # # #             file_name = file.filename
# # # # # # # # # # # # # # # # # #             file_name_without_extension, file_extension = os.path.splitext(file_name)
# # # # # # # # # # # # # # # # # #             overlay_text = f"{file_name_without_extension}{file_extension}"

# # # # # # # # # # # # # # # # # #         font = cv2.FONT_HERSHEY_SIMPLEX
# # # # # # # # # # # # # # # # # #         font_scale = 2
# # # # # # # # # # # # # # # # # #         font_thickness = 5
# # # # # # # # # # # # # # # # # #         text_color = (0, 0, 238)

# # # # # # # # # # # # # # # # # #         # Set the text size
# # # # # # # # # # # # # # # # # #         (text_width, text_height), _ = cv2.getTextSize(
# # # # # # # # # # # # # # # # # #             overlay_text, font, font_scale, font_thickness
# # # # # # # # # # # # # # # # # #         )

# # # # # # # # # # # # # # # # # #         # Calculate the position to place the text
# # # # # # # # # # # # # # # # # #         x = int((img.shape[1] - text_width) / 2)  # Centered horizontally
# # # # # # # # # # # # # # # # # #         y = int((img.shape[0] + text_height) - 30)  # Placed at the bottom

# # # # # # # # # # # # # # # # # #         # Overlay the text on the image
# # # # # # # # # # # # # # # # # #         cv2.putText(
# # # # # # # # # # # # # # # # # #             img, overlay_text, (x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA
# # # # # # # # # # # # # # # # # #         )

# # # # # # # # # # # # # # # # # #         # Set the output file path
# # # # # # # # # # # # # # # # # #         output_file_path = os.path.join(output_directory, f"output_{i}.png")

# # # # # # # # # # # # # # # # # #         # Save the resulting image
# # # # # # # # # # # # # # # # # #         cv2.imwrite(output_file_path, img)

# # # # # # # # # # # # # # # # # #         # Generate the download link URL for the output image
# # # # # # # # # # # # # # # # # #         download_url = f"/static/output/output_{i}.png"
# # # # # # # # # # # # # # # # # #         download_urls.append(download_url)

# # # # # # # # # # # # # # # # # #         # Add instruction
# # # # # # # # # # # # # # # # # #         instruction = f"Image {file.filename} processed. Download: {download_url}"
# # # # # # # # # # # # # # # # # #         instructions.append(instruction)

# # # # # # # # # # # # # # # # # #     # Return the download URLs and instructions in the API response
# # # # # # # # # # # # # # # # # #     return {"download_urls": download_urls, "instructions": instructions}


# # # # # # # # # # # # # # # # # # @app.get("/download/{filename}")
# # # # # # # # # # # # # # # # # # async def download(filename: str):
# # # # # # # # # # # # # # # # # #     # Making the file path
# # # # # # # # # # # # # # # # # #     file_path = os.path.join("static", "output", filename)

# # # # # # # # # # # # # # # # # #     # Check if the file exists
# # # # # # # # # # # # # # # # # #     if os.path.isfile(file_path):
# # # # # # # # # # # # # # # # # #         # If the file exists, return it as a response
# # # # # # # # # # # # # # # # # #         return FileResponse(file_path)

# # # # # # # # # # # # # # # # # #     # If the file does not exist, return a 404 Not Found response
# # # # # # # # # # # # # # # # # #     return {"detail": "File not found"}


# # # # # # # # # # # # # # # # # # @app.get("/data")
# # # # # # # # # # # # # # # # # # async def get_data():
# # # # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/output")
# # # # # # # # # # # # # # # # # #     return {"overlayed_images": overlayed_images}


# # # # # # # # # # # # # # # # # # @app.get("/url")
# # # # # # # # # # # # # # # # # # async def get_shareable_link(request: Request):
# # # # # # # # # # # # # # # # # #     base_url = request.base_url
# # # # # # # # # # # # # # # # # #     return {"shareable_link": base_url}


# # # # # # # # # # # # # # # # # # @app.get("/images")
# # # # # # # # # # # # # # # # # # async def get_images():
# # # # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/output")
# # # # # # # # # # # # # # # # # #     image_urls = [
# # # # # # # # # # # # # # # # # #         f"http://localhost:12000/static/output/{image}" for image in overlayed_images
# # # # # # # # # # # # # # # # # #     ]
# # # # # # # # # # # # # # # # # #     return {"image_urls": image_urls}


# # # # # # # # # # # # # # # # # # # Start the server
# # # # # # # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)
# # # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # # import cv2
# # # # # # # # # # # # # # # # # import numpy as np
# # # # # # # # # # # # # # # # # from typing import List
# # # # # # # # # # # # # # # # # from fastapi import FastAPI, UploadFile, Request, File
# # # # # # # # # # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # # # # # # # # # from fastapi.responses import FileResponse, JSONResponse
# # # # # # # # # # # # # # # # # from fastapi.templating import Jinja2Templates
# # # # # # # # # # # # # # # # # import uvicorn
# # # # # # # # # # # # # # # # # from PIL import Image

# # # # # # # # # # # # # # # # # app = FastAPI()
# # # # # # # # # # # # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")
# # # # # # # # # # # # # # # # # templates = Jinja2Templates(directory="templates")

# # # # # # # # # # # # # # # # # # Define the upload endpoint
# # # # # # # # # # # # # # # # # @app.post("/upload")
# # # # # # # # # # # # # # # # # async def upload(files: List[UploadFile] = File(...), text: str = None):
# # # # # # # # # # # # # # # # #     output_directory = "static/output"
# # # # # # # # # # # # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # # # # # # # # # # # #     download_urls = []
# # # # # # # # # # # # # # # # #     instructions = []

# # # # # # # # # # # # # # # # #     for i, file in enumerate(files):
# # # # # # # # # # # # # # # # #         # Save the uploaded file temporarily
# # # # # # # # # # # # # # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # # # # # # # # # # # # #         with open(temp_path, "wb") as f:
# # # # # # # # # # # # # # # # #             contents = await file.read()  # Read the file contents
# # # # # # # # # # # # # # # # #             f.write(contents)

# # # # # # # # # # # # # # # # #         # Read the image using OpenCV
# # # # # # # # # # # # # # # # #         img = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_UNCHANGED)

# # # # # # # # # # # # # # # # #         # Remove the background using the provided code
# # # # # # # # # # # # # # # # #         original = img.copy()

# # # # # # # # # # # # # # # # #         l = int(max(5, 6))
# # # # # # # # # # # # # # # # #         u = int(min(6, 6))

# # # # # # # # # # # # # # # # #         ed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# # # # # # # # # # # # # # # # #         edges = cv2.GaussianBlur(img, (21, 51), 3)
# # # # # # # # # # # # # # # # #         edges = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)
# # # # # # # # # # # # # # # # #         edges = cv2.Canny(edges, l, u)

# # # # # # # # # # # # # # # # #         _, thresh = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# # # # # # # # # # # # # # # # #         kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
# # # # # # # # # # # # # # # # #         mask = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=4)

# # # # # # # # # # # # # # # # #         data = mask.tolist()
# # # # # # # # # # # # # # # # #         sys.setrecursionlimit(10**8)
# # # # # # # # # # # # # # # # #         for i in range(len(data)):
# # # # # # # # # # # # # # # # #             for j in range(len(data[i])):
# # # # # # # # # # # # # # # # #                 if data[i][j] != 255:
# # # # # # # # # # # # # # # # #                     data[i][j] = -1
# # # # # # # # # # # # # # # # #                 else:
# # # # # # # # # # # # # # # # #                     break
# # # # # # # # # # # # # # # # #             for j in range(len(data[i])-1, -1, -1):
# # # # # # # # # # # # # # # # #                 if data[i][j] != 255:
# # # # # # # # # # # # # # # # #                     data[i][j] = -1
# # # # # # # # # # # # # # # # #                 else:
# # # # # # # # # # # # # # # # #                     break
# # # # # # # # # # # # # # # # #         image = np.array(data)
# # # # # # # # # # # # # # # # #         image[image != -1] = 255
# # # # # # # # # # # # # # # # #         image[image == -1] = 0

# # # # # # # # # # # # # # # # #         mask = np.array(image, np.uint8)

# # # # # # # # # # # # # # # # #         result = cv2.bitwise_and(original, original, mask=mask)
# # # # # # # # # # # # # # # # #         result[mask == 0] = 255
# # # # # # # # # # # # # # # # #         cv2.imwrite('bg.png', result)

# # # # # # # # # # # # # # # # #         img = Image.open('bg.png')
# # # # # # # # # # # # # # # # #         img.convert("RGBA")
# # # # # # # # # # # # # # # # #         datas = img.getdata()

# # # # # # # # # # # # # # # # #         newData = []
# # # # # # # # # # # # # # # # #         for item in datas:
# # # # # # # # # # # # # # # # #             if item[0] == 255 and item[1] == 255 and item[2] == 255:
# # # # # # # # # # # # # # # # #                 newData.append((255, 255, 255, 0))
# # # # # # # # # # # # # # # # #             else:
# # # # # # # # # # # # # # # # #                 newData.append(item)

# # # # # # # # # # # # # # # # #         img.putdata(newData)
# # # # # # # # # # # # # # # # #         img_path = os.path.join(output_directory, f"output_{i}.png")
# # # # # # # # # # # # # # # # #         img.save(img_path, "PNG")

# # # # # # # # # # # # # # # # #         # Prepare the text to overlay on the image
# # # # # # # # # # # # # # # # #         if text:
# # # # # # # # # # # # # # # # #             overlay_text = text
# # # # # # # # # # # # # # # # #         else:
# # # # # # # # # # # # # # # # #             file_name = file.filename
# # # # # # # # # # # # # # # # #             file_name_without_extension, file_extension = os.path.splitext(file_name)
# # # # # # # # # # # # # # # # #             overlay_text = f"{file_name_without_extension}{file_extension}"

# # # # # # # # # # # # # # # # #         font = cv2.FONT_HERSHEY_SIMPLEX
# # # # # # # # # # # # # # # # #         font_scale = 2
# # # # # # # # # # # # # # # # #         font_thickness = 5
# # # # # # # # # # # # # # # # #         text_color = (0, 0, 238)

# # # # # # # # # # # # # # # # #         # Set the text size
# # # # # # # # # # # # # # # # #         (text_width, text_height), _ = cv2.getTextSize(
# # # # # # # # # # # # # # # # #             overlay_text, font, font_scale, font_thickness
# # # # # # # # # # # # # # # # #         )

# # # # # # # # # # # # # # # # #         # Calculate the position to place the text
# # # # # # # # # # # # # # # # #         x = int((img.shape[1] - text_width) / 2)  # Centered horizontally
# # # # # # # # # # # # # # # # #         y = int((img.shape[0] + text_height) - 30)  # Placed at the bottom

# # # # # # # # # # # # # # # # #         # Overlay the text on the image
# # # # # # # # # # # # # # # # #         cv2.putText(
# # # # # # # # # # # # # # # # #             img, overlay_text, (x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA
# # # # # # # # # # # # # # # # #         )

# # # # # # # # # # # # # # # # #         # Set the output file path
# # # # # # # # # # # # # # # # #         output_file_path = os.path.join(output_directory, f"output_{i}.png")

# # # # # # # # # # # # # # # # #         # Save the resulting image
# # # # # # # # # # # # # # # # #         cv2.imwrite(output_file_path, img)

# # # # # # # # # # # # # # # # #         # Generate the download link URL for the output image
# # # # # # # # # # # # # # # # #         download_url = f"/static/output/output_{i}.png"
# # # # # # # # # # # # # # # # #         download_urls.append(download_url)

# # # # # # # # # # # # # # # # #         # Add instruction
# # # # # # # # # # # # # # # # #         instruction = f"Image {file.filename} processed. Download: {download_url}"
# # # # # # # # # # # # # # # # #         instructions.append(instruction)

# # # # # # # # # # # # # # # # #     # Return the download URLs and instructions in the API response
# # # # # # # # # # # # # # # # #     return {"download_urls": download_urls, "instructions": instructions}


# # # # # # # # # # # # # # # # # @app.get("/download/{filename}")
# # # # # # # # # # # # # # # # # async def download(filename: str):
# # # # # # # # # # # # # # # # #     # Making the file path
# # # # # # # # # # # # # # # # #     file_path = os.path.join("static", "output", filename)

# # # # # # # # # # # # # # # # #     # Check if the file exists
# # # # # # # # # # # # # # # # #     if os.path.isfile(file_path):
# # # # # # # # # # # # # # # # #         # If the file exists, return it as a response
# # # # # # # # # # # # # # # # #         return FileResponse(file_path)

# # # # # # # # # # # # # # # # #     # If the file does not exist, return a 404 Not Found response
# # # # # # # # # # # # # # # # #     return {"detail": "File not found"}


# # # # # # # # # # # # # # # # # @app.get("/data")
# # # # # # # # # # # # # # # # # async def get_data():
# # # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/output")
# # # # # # # # # # # # # # # # #     return {"overlayed_images": overlayed_images}


# # # # # # # # # # # # # # # # # @app.get("/url")
# # # # # # # # # # # # # # # # # async def get_shareable_link(request: Request):
# # # # # # # # # # # # # # # # #     base_url = request.base_url
# # # # # # # # # # # # # # # # #     return {"shareable_link": base_url}


# # # # # # # # # # # # # # # # # @app.get("/images")
# # # # # # # # # # # # # # # # # async def get_images():
# # # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/output")
# # # # # # # # # # # # # # # # #     image_urls = [
# # # # # # # # # # # # # # # # #         f"http://localhost:12000/static/output/{image}" for image in overlayed_images
# # # # # # # # # # # # # # # # #     ]
# # # # # # # # # # # # # # # # #     return {"image_urls": image_urls}


# # # # # # # # # # # # # # # # # # Start the server
# # # # # # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)
# # # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # # import cv2
# # # # # # # # # # # # # # # # # import numpy as np
# # # # # # # # # # # # # # # # # from typing import List
# # # # # # # # # # # # # # # # # from fastapi import FastAPI, UploadFile, Request, File
# # # # # # # # # # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # # # # # # # # # from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
# # # # # # # # # # # # # # # # # from fastapi.templating import Jinja2Templates
# # # # # # # # # # # # # # # # # import uvicorn
# # # # # # # # # # # # # # # # # from PIL import Image

# # # # # # # # # # # # # # # # # app = FastAPI()
# # # # # # # # # # # # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")
# # # # # # # # # # # # # # # # # templates = Jinja2Templates(directory="templates")

# # # # # # # # # # # # # # # # # # Define the upload endpoint
# # # # # # # # # # # # # # # # # @app.post("/upload")
# # # # # # # # # # # # # # # # # async def upload(files: List[UploadFile] = File(...), text: str = None):
# # # # # # # # # # # # # # # # #     output_directory = "static/output"
# # # # # # # # # # # # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # # # # # # # # # # # #     download_urls = []
# # # # # # # # # # # # # # # # #     instructions = []

# # # # # # # # # # # # # # # # #     for i, file in enumerate(files):
# # # # # # # # # # # # # # # # #         # Save the uploaded file temporarily
# # # # # # # # # # # # # # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # # # # # # # # # # # # #         with open(temp_path, "wb") as f:
# # # # # # # # # # # # # # # # #             f.write(await file.read())

# # # # # # # # # # # # # # # # #         # Read the image using OpenCV
# # # # # # # # # # # # # # # # #         img = cv2.imread(temp_path)

# # # # # # # # # # # # # # # # #         # Resize the image to 1080x1080
# # # # # # # # # # # # # # # # #         img = cv2.resize(img, (1080, 1080))

# # # # # # # # # # # # # # # # #         # Remove the background using the provided code
# # # # # # # # # # # # # # # # #         original = img.copy()

# # # # # # # # # # # # # # # # #         l = int(max(5, 6))
# # # # # # # # # # # # # # # # #         u = int(min(6, 6))

# # # # # # # # # # # # # # # # #         ed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# # # # # # # # # # # # # # # # #         edges = cv2.GaussianBlur(img, (21, 51), 3)
# # # # # # # # # # # # # # # # #         edges = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)
# # # # # # # # # # # # # # # # #         edges = cv2.Canny(edges, l, u)

# # # # # # # # # # # # # # # # #         _, thresh = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# # # # # # # # # # # # # # # # #         kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
# # # # # # # # # # # # # # # # #         mask = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=4)

# # # # # # # # # # # # # # # # #         data = mask.tolist()
# # # # # # # # # # # # # # # # #         for i in range(len(data)):
# # # # # # # # # # # # # # # # #             for j in range(len(data[i])):
# # # # # # # # # # # # # # # # #                 if data[i][j] != 255:
# # # # # # # # # # # # # # # # #                     data[i][j] = -1
# # # # # # # # # # # # # # # # #                 else:
# # # # # # # # # # # # # # # # #                     break
# # # # # # # # # # # # # # # # #             for j in range(len(data[i])-1, -1, -1):
# # # # # # # # # # # # # # # # #                 if data[i][j] != 255:
# # # # # # # # # # # # # # # # #                     data[i][j] = -1
# # # # # # # # # # # # # # # # #                 else:
# # # # # # # # # # # # # # # # #                     break
# # # # # # # # # # # # # # # # #         image = np.array(data)
# # # # # # # # # # # # # # # # #         image[image != -1] = 255
# # # # # # # # # # # # # # # # #         image[image == -1] = 0

# # # # # # # # # # # # # # # # #         mask = np.array(image, np.uint8)

# # # # # # # # # # # # # # # # #         result = cv2.bitwise_and(original, original, mask=mask)
# # # # # # # # # # # # # # # # #         result[mask == 0] = 255
# # # # # # # # # # # # # # # # #         cv2.imwrite('bg.png', result)

# # # # # # # # # # # # # # # # #         img = Image.open('bg.png')
# # # # # # # # # # # # # # # # #         img.convert("RGBA")
# # # # # # # # # # # # # # # # #         datas = img.getdata()

# # # # # # # # # # # # # # # # #         newData = []
# # # # # # # # # # # # # # # # #         for item in datas:
# # # # # # # # # # # # # # # # #             if item[0] == 255 and item[1] == 255 and item[2] == 255:
# # # # # # # # # # # # # # # # #                 newData.append((255, 255, 255, 0))
# # # # # # # # # # # # # # # # #             else:
# # # # # # # # # # # # # # # # #                 newData.append(item)

# # # # # # # # # # # # # # # # #         img.putdata(newData)
# # # # # # # # # # # # # # # # #         img_path = os.path.join(output_directory, f"output_{i}.png")
# # # # # # # # # # # # # # # # #         img.save(img_path, "PNG")

# # # # # # # # # # # # # # # # #         # Prepare the text to overlay on the image
# # # # # # # # # # # # # # # # #         if text:
# # # # # # # # # # # # # # # # #             overlay_text = text
# # # # # # # # # # # # # # # # #         else:
# # # # # # # # # # # # # # # # #             file_name = file.filename
# # # # # # # # # # # # # # # # #             file_name_without_extension, file_extension = os.path.splitext(file_name)
# # # # # # # # # # # # # # # # #             overlay_text = f"{file_name_without_extension}{file_extension}"

# # # # # # # # # # # # # # # # #         font = cv2.FONT_HERSHEY_SIMPLEX
# # # # # # # # # # # # # # # # #         font_scale = 2
# # # # # # # # # # # # # # # # #         font_thickness = 5
# # # # # # # # # # # # # # # # #         text_color = (0, 0, 238)

# # # # # # # # # # # # # # # # #         # Set the text size
# # # # # # # # # # # # # # # # #         text_width, text_height = cv2.getTextSize(
# # # # # # # # # # # # # # # # #             overlay_text, font, font_scale, font_thickness
# # # # # # # # # # # # # # # # #         )[0]

# # # # # # # # # # # # # # # # #         # Calculate the position to place the text
# # # # # # # # # # # # # # # # #         img_width, img_height = img.size
# # # # # # # # # # # # # # # # #         x = int((img_width - text_width) / 2)  # Centered horizontally
# # # # # # # # # # # # # # # # #         y = int((img_height + text_height) - 30)  # Placed at the bottom

# # # # # # # # # # # # # # # # #         # Overlay the text on the image
# # # # # # # # # # # # # # # # #         cv2.putText(
# # # # # # # # # # # # # # # # #             np.array(img), overlay_text, (x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA
# # # # # # # # # # # # # # # # #         )

# # # # # # # # # # # # # # # # #         # Set the output file path
# # # # # # # # # # # # # # # # #         output_file_path = os.path.join(output_directory, f"output_{i}.png")

# # # # # # # # # # # # # # # # #         # Save the resulting image
# # # # # # # # # # # # # # # # #         img.save(output_file_path, "PNG")

# # # # # # # # # # # # # # # # #         # Generate the download link URL for the output image
# # # # # # # # # # # # # # # # #         download_url = f"/static/output/output_{i}.png"
# # # # # # # # # # # # # # # # #         download_urls.append(download_url)

# # # # # # # # # # # # # # # # #         # Add instruction
# # # # # # # # # # # # # # # # #         instruction = f"Image {file.filename} processed. Download: {download_url}"
# # # # # # # # # # # # # # # # #         instructions.append(instruction)

# # # # # # # # # # # # # # # # #     # Return the download URLs and instructions in the API response
# # # # # # # # # # # # # # # # #     return {"download_urls": download_urls, "instructions": instructions}


# # # # # # # # # # # # # # # # # # Define the download endpoint
# # # # # # # # # # # # # # # # # @app.get("/download/{filename}")
# # # # # # # # # # # # # # # # # async def download(filename: str):
# # # # # # # # # # # # # # # # #     # Making the file path
# # # # # # # # # # # # # # # # #     file_path = os.path.join("static", "output", filename)

# # # # # # # # # # # # # # # # #     # Check if the file exists
# # # # # # # # # # # # # # # # #     if os.path.isfile(file_path):
# # # # # # # # # # # # # # # # #         # If the file exists, return it as a response
# # # # # # # # # # # # # # # # #         return FileResponse(file_path)

# # # # # # # # # # # # # # # # #     # If the file does not exist, return a 404 Not Found response
# # # # # # # # # # # # # # # # #     return JSONResponse({"detail": "File not found"}, status_code=404)


# # # # # # # # # # # # # # # # # # Define the data endpoint
# # # # # # # # # # # # # # # # # @app.get("/data")
# # # # # # # # # # # # # # # # # async def get_data():
# # # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/output")
# # # # # # # # # # # # # # # # #     return {"overlayed_images": overlayed_images}


# # # # # # # # # # # # # # # # # # Define the shareable link endpoint
# # # # # # # # # # # # # # # # # @app.get("/url")
# # # # # # # # # # # # # # # # # async def get_shareable_link(request: Request):
# # # # # # # # # # # # # # # # #     base_url = request.base_url
# # # # # # # # # # # # # # # # #     return {"shareable_link": base_url}


# # # # # # # # # # # # # # # # # # Define the images endpoint
# # # # # # # # # # # # # # # # # @app.get("/images")
# # # # # # # # # # # # # # # # # async def get_images():
# # # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/output")
# # # # # # # # # # # # # # # # #     image_urls = [
# # # # # # # # # # # # # # # # #         f"http://localhost:12000/static/output/{image}" for image in overlayed_images
# # # # # # # # # # # # # # # # #     ]
# # # # # # # # # # # # # # # # #     return {"image_urls": image_urls}


# # # # # # # # # # # # # # # # # # Define the preview endpoint
# # # # # # # # # # # # # # # # # @app.get("/preview/{filename}")
# # # # # # # # # # # # # # # # # async def preview(filename: str):
# # # # # # # # # # # # # # # # #     # Making the file path
# # # # # # # # # # # # # # # # #     file_path = os.path.join("static", "output", filename)

# # # # # # # # # # # # # # # # #     # Check if the file exists
# # # # # # # # # # # # # # # # #     if os.path.isfile(file_path):
# # # # # # # # # # # # # # # # #         # If the file exists, return it as a response
# # # # # # # # # # # # # # # # #         return FileResponse(file_path)

# # # # # # # # # # # # # # # # #     # If the file does not exist, return a 404 Not Found response
# # # # # # # # # # # # # # # # #     return JSONResponse({"detail": "File not found"}, status_code=404)


# # # # # # # # # # # # # # # # # # Start the server
# # # # # # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)
# # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # import cv2
# # # # # # # # # # # # # # # # import numpy as np
# # # # # # # # # # # # # # # # from typing import List
# # # # # # # # # # # # # # # # from fastapi import FastAPI, UploadFile, Request, File
# # # # # # # # # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # # # # # # # # from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
# # # # # # # # # # # # # # # # from fastapi.templating import Jinja2Templates
# # # # # # # # # # # # # # # # import uvicorn
# # # # # # # # # # # # # # # # from PIL import Image, ImageDraw, ImageFont

# # # # # # # # # # # # # # # # app = FastAPI()
# # # # # # # # # # # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")
# # # # # # # # # # # # # # # # templates = Jinja2Templates(directory="templates")

# # # # # # # # # # # # # # # # # Define the upload endpoint
# # # # # # # # # # # # # # # # @app.post("/upload")
# # # # # # # # # # # # # # # # async def upload(files: List[UploadFile] = File(...), text: str = None):
# # # # # # # # # # # # # # # #     output_directory = "static/output"
# # # # # # # # # # # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # # # # # # # # # # #     download_urls = []
# # # # # # # # # # # # # # # #     instructions = []

# # # # # # # # # # # # # # # #     for i, file in enumerate(files):
# # # # # # # # # # # # # # # #         # Save the uploaded file temporarily
# # # # # # # # # # # # # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # # # # # # # # # # # #         with open(temp_path, "wb") as f:
# # # # # # # # # # # # # # # #             f.write(await file.read())

# # # # # # # # # # # # # # # #         # Read the image using OpenCV
# # # # # # # # # # # # # # # #         img = cv2.imread(temp_path)

# # # # # # # # # # # # # # # #         # Remove the background using the provided code
# # # # # # # # # # # # # # # #         original = img.copy()

# # # # # # # # # # # # # # # #         l = int(max(5, 6))
# # # # # # # # # # # # # # # #         u = int(min(6, 6))

# # # # # # # # # # # # # # # #         ed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# # # # # # # # # # # # # # # #         edges = cv2.GaussianBlur(img, (21, 51), 3)
# # # # # # # # # # # # # # # #         edges = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)
# # # # # # # # # # # # # # # #         edges = cv2.Canny(edges, l, u)

# # # # # # # # # # # # # # # #         _, thresh = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# # # # # # # # # # # # # # # #         kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
# # # # # # # # # # # # # # # #         mask = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=4)

# # # # # # # # # # # # # # # #         data = mask.tolist()
# # # # # # # # # # # # # # # #         for i in range(len(data)):
# # # # # # # # # # # # # # # #             for j in range(len(data[i])):
# # # # # # # # # # # # # # # #                 if data[i][j] != 255:
# # # # # # # # # # # # # # # #                     data[i][j] = -1
# # # # # # # # # # # # # # # #                 else:
# # # # # # # # # # # # # # # #                     break
# # # # # # # # # # # # # # # #             for j in range(len(data[i])-1, -1, -1):
# # # # # # # # # # # # # # # #                 if data[i][j] != 255:
# # # # # # # # # # # # # # # #                     data[i][j] = -1
# # # # # # # # # # # # # # # #                 else:
# # # # # # # # # # # # # # # #                     break
# # # # # # # # # # # # # # # #         image = np.array(data)
# # # # # # # # # # # # # # # #         image[image != -1] = 255
# # # # # # # # # # # # # # # #         image[image == -1] = 0

# # # # # # # # # # # # # # # #         mask = np.array(image, np.uint8)

# # # # # # # # # # # # # # # #         result = cv2.bitwise_and(original, original, mask=mask)
# # # # # # # # # # # # # # # #         result[mask == 0] = 255

# # # # # # # # # # # # # # # #         # Create a transparent background image
# # # # # # # # # # # # # # # #         transparent_img = np.zeros_like(result, dtype=np.uint8)
# # # # # # # # # # # # # # # #         transparent_img[:, :] = (255, 255, 255, 0)

# # # # # # # # # # # # # # # #         # Resize the image to 1080x1080
# # # # # # # # # # # # # # # #         resized_result = cv2.resize(result, (1080, 1080))
# # # # # # # # # # # # # # # #         resized_transparent_img = cv2.resize(transparent_img, (1080, 1080))

# # # # # # # # # # # # # # # #         # Overlay the image on the transparent background
# # # # # # # # # # # # # # # #         alpha = 0.5  # Opacity of the overlay image
# # # # # # # # # # # # # # # #         overlay = cv2.addWeighted(resized_result, alpha, resized_transparent_img, 1 - alpha, 0)

# # # # # # # # # # # # # # # #         # Convert the image to PIL format
# # # # # # # # # # # # # # # #         pil_img = Image.fromarray(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))

# # # # # # # # # # # # # # # #         # Draw text on the image
# # # # # # # # # # # # # # # #         draw = ImageDraw.Draw(pil_img)
# # # # # # # # # # # # # # # #         text_font = ImageFont.truetype("arial.ttf", 10)
# # # # # # # # # # # # # # # #         text_color = (0, 0, 238)
# # # # # # # # # # # # # # # #         text_position = (10, 1060)  # Bottom left corner
# # # # # # # # # # # # # # # #         draw.text(text_position, text, font=text_font, fill=text_color)

# # # # # # # # # # # # # # # #         # Save the resulting image
# # # # # # # # # # # # # # # #         output_file_path = os.path.join(output_directory, f"output_{i}.png")
# # # # # # # # # # # # # # # #         pil_img.save(output_file_path, "PNG")

# # # # # # # # # # # # # # # #         # Generate the download link URL for the output image
# # # # # # # # # # # # # # # #         download_url = f"/static/output/output_{i}.png"
# # # # # # # # # # # # # # # #         download_urls.append(download_url)

# # # # # # # # # # # # # # # #         # Add instruction
# # # # # # # # # # # # # # # #         instruction = f"Image {file.filename} processed. Download: {download_url}"
# # # # # # # # # # # # # # # #         instructions.append(instruction)

# # # # # # # # # # # # # # # #     # Return the download URLs and instructions in the API response
# # # # # # # # # # # # # # # #     return {"download_urls": download_urls, "instructions": instructions}


# # # # # # # # # # # # # # # # # Define the download endpoint
# # # # # # # # # # # # # # # # @app.get("/download/{filename}")
# # # # # # # # # # # # # # # # async def download(filename: str):
# # # # # # # # # # # # # # # #     # Making the file path
# # # # # # # # # # # # # # # #     file_path = os.path.join("static", "output", filename)

# # # # # # # # # # # # # # # #     # Check if the file exists
# # # # # # # # # # # # # # # #     if os.path.isfile(file_path):
# # # # # # # # # # # # # # # #         # If the file exists, return it as a response
# # # # # # # # # # # # # # # #         return FileResponse(file_path)

# # # # # # # # # # # # # # # #     # If the file does not exist, return a 404 Not Found response
# # # # # # # # # # # # # # # #     return JSONResponse({"detail": "File not found"}, status_code=404)


# # # # # # # # # # # # # # # # # Define the data endpoint
# # # # # # # # # # # # # # # # @app.get("/data")
# # # # # # # # # # # # # # # # async def get_data():
# # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/output")
# # # # # # # # # # # # # # # #     return {"overlayed_images": overlayed_images}


# # # # # # # # # # # # # # # # # Define the shareable link endpoint
# # # # # # # # # # # # # # # # @app.get("/url")
# # # # # # # # # # # # # # # # async def get_shareable_link(request: Request):
# # # # # # # # # # # # # # # #     base_url = request.base_url
# # # # # # # # # # # # # # # #     return {"shareable_link": base_url}


# # # # # # # # # # # # # # # # # Define the images endpoint
# # # # # # # # # # # # # # # # @app.get("/images")
# # # # # # # # # # # # # # # # async def get_images():
# # # # # # # # # # # # # # # #     overlayed_images = os.listdir("static/output")
# # # # # # # # # # # # # # # #     image_urls = [
# # # # # # # # # # # # # # # #         f"http://localhost:12000/static/output/{image}" for image in overlayed_images
# # # # # # # # # # # # # # # #     ]
# # # # # # # # # # # # # # # #     return {"image_urls": image_urls}


# # # # # # # # # # # # # # # # # Define the preview endpoint
# # # # # # # # # # # # # # # # @app.get("/preview/{filename}")
# # # # # # # # # # # # # # # # async def preview(filename: str):
# # # # # # # # # # # # # # # #     # Making the file path
# # # # # # # # # # # # # # # #     file_path = os.path.join("static", "output", filename)

# # # # # # # # # # # # # # # #     # Check if the file exists
# # # # # # # # # # # # # # # #     if os.path.isfile(file_path):
# # # # # # # # # # # # # # # #         # If the file exists, return it as a response
# # # # # # # # # # # # # # # #         return FileResponse(file_path)

# # # # # # # # # # # # # # # #     # If the file does not exist, return a 404 Not Found response
# # # # # # # # # # # # # # # #     return JSONResponse({"detail": "File not found"}, status_code=404)


# # # # # # # # # # # # # # # # # Start the server
# # # # # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)
# # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # import cv2
# # # # # # # # # # # # # # # import numpy as np
# # # # # # # # # # # # # # # from typing import List
# # # # # # # # # # # # # # # from fastapi import FastAPI, UploadFile, File
# # # # # # # # # # # # # # # from fastapi.responses import FileResponse
# # # # # # # # # # # # # # # from PIL import Image, ImageDraw, ImageFont
# # # # # # # # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # # # # # # # import uvicorn

# # # # # # # # # # # # # # # app = FastAPI()

# # # # # # # # # # # # # # # # Define the upload endpoint
# # # # # # # # # # # # # # # @app.post("/upload")
# # # # # # # # # # # # # # # async def upload(files: List[UploadFile] = File(...)):
# # # # # # # # # # # # # # #     output_directory = "static/output"
# # # # # # # # # # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # # # # # # # # # #     for i, file in enumerate(files):
# # # # # # # # # # # # # # #         # Save the uploaded file temporarily
# # # # # # # # # # # # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # # # # # # # # # # #         with open(temp_path, "wb") as f:
# # # # # # # # # # # # # # #             f.write(await file.read())

# # # # # # # # # # # # # # #         # Read the image using PIL
# # # # # # # # # # # # # # #         pil_img = Image.open(temp_path)

# # # # # # # # # # # # # # #         # Convert the PIL image to numpy array
# # # # # # # # # # # # # # #         img = np.array(pil_img)

# # # # # # # # # # # # # # #         # Remove the background using the provided code
# # # # # # # # # # # # # # #         # Replace the following lines with your background removal code
# # # # # # # # # # # # # # #         result = img  # Placeholder for the result
# # # # # # # # # # # # # # #         transparent_img = np.zeros_like(result, dtype=np.uint8)
# # # # # # # # # # # # # # #         print("Transparent Image Shape:", transparent_img.shape)  # Debug print

# # # # # # # # # # # # # # #         # Resize the image to 1080x1080
# # # # # # # # # # # # # # #         resized_result = cv2.resize(result, (1080, 1080))
# # # # # # # # # # # # # # #         resized_transparent_img = cv2.resize(transparent_img, (1080, 1080))

# # # # # # # # # # # # # # #         # Overlay the image on the transparent background
# # # # # # # # # # # # # # #         alpha = 0.5  # Opacity of the overlay image
# # # # # # # # # # # # # # #         overlay = cv2.addWeighted(resized_result, alpha, resized_transparent_img, 1 - alpha, 0)

# # # # # # # # # # # # # # #         # Overlay the image name as text
# # # # # # # # # # # # # # #         image_name = file.filename
# # # # # # # # # # # # # # #         font_path = "static/fonts/arial.ttf"  # Path to the font file
# # # # # # # # # # # # # # #         font_size = 20
# # # # # # # # # # # # # # #         font = ImageFont.truetype(font_path, font_size)
# # # # # # # # # # # # # # #         pil_overlay = Image.fromarray(overlay)
# # # # # # # # # # # # # # #         draw = ImageDraw.Draw(pil_overlay)
# # # # # # # # # # # # # # #         text_width, text_height = draw.textsize(image_name, font=font)
# # # # # # # # # # # # # # #         text_position = (10, 10)
# # # # # # # # # # # # # # #         draw.text(text_position, image_name, font=font, fill=(255, 255, 255, 128))

# # # # # # # # # # # # # # #         # Convert the overlay back to numpy array
# # # # # # # # # # # # # # #         overlay = np.array(pil_overlay)

# # # # # # # # # # # # # # #         # Save the resulting image
# # # # # # # # # # # # # # #         output_file_path = os.path.join(output_directory, f"output_{i}.png")
# # # # # # # # # # # # # # #         cv2.imwrite(output_file_path, overlay)

# # # # # # # # # # # # # # #     return {"message": "Images processed successfully"}

# # # # # # # # # # # # # # # # Serve the static files
# # # # # # # # # # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")

# # # # # # # # # # # # # # # # Define the endpoint to view the output image
# # # # # # # # # # # # # # # @app.get("/output/{index}")
# # # # # # # # # # # # # # # async def view_output_image(index: int):
# # # # # # # # # # # # # # #     output_file_path = f"static/output/output_{index}.png"
# # # # # # # # # # # # # # #     return FileResponse(output_file_path)

# # # # # # # # # # # # # # # # Start the server
# # # # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)
# # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # import cv2
# # # # # # # # # # # # # # import numpy as np
# # # # # # # # # # # # # # from typing import List
# # # # # # # # # # # # # # from fastapi import FastAPI, UploadFile, File
# # # # # # # # # # # # # # from fastapi.responses import FileResponse
# # # # # # # # # # # # # # from PIL import Image, ImageDraw, ImageFont
# # # # # # # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # # # # # # import uvicorn

# # # # # # # # # # # # # # app = FastAPI()

# # # # # # # # # # # # # # # Define the upload endpoint
# # # # # # # # # # # # # # @app.post("/upload")
# # # # # # # # # # # # # # async def upload(files: List[UploadFile] = File(...)):
# # # # # # # # # # # # # #     output_directory = "static/output"
# # # # # # # # # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # # # # # # # # #     for i, file in enumerate(files):
# # # # # # # # # # # # # #         # Save the uploaded file temporarily
# # # # # # # # # # # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # # # # # # # # # #         with open(temp_path, "wb") as f:
# # # # # # # # # # # # # #             f.write(await file.read())

# # # # # # # # # # # # # #         # Read the image using PIL
# # # # # # # # # # # # # #         pil_img = Image.open(temp_path)

# # # # # # # # # # # # # #         # Convert the PIL image to numpy array
# # # # # # # # # # # # # #         img = np.array(pil_img)

# # # # # # # # # # # # # #         # Remove the background using the provided code
# # # # # # # # # # # # # #         # Replace the following lines with your background removal code
# # # # # # # # # # # # # #         result = img  # Placeholder for the result
# # # # # # # # # # # # # #         transparent_img = np.zeros_like(result, dtype=np.uint8)
# # # # # # # # # # # # # #         print("Transparent Image Shape:", transparent_img.shape)  # Debug print

# # # # # # # # # # # # # #         # Resize the image to 1080x1080
# # # # # # # # # # # # # #         resized_result = cv2.resize(result, (1080, 1080))
# # # # # # # # # # # # # #         resized_transparent_img = cv2.resize(transparent_img, (1080, 1080))

# # # # # # # # # # # # # #         # Overlay the image on the transparent background
# # # # # # # # # # # # # #         alpha = 0.5  # Opacity of the overlay image
# # # # # # # # # # # # # #         overlay = cv2.addWeighted(resized_result, alpha, resized_transparent_img, 1 - alpha, 0)

# # # # # # # # # # # # # #         # Convert the overlay image to PIL Image
# # # # # # # # # # # # # #         pil_overlay = Image.fromarray(overlay)

# # # # # # # # # # # # # #         # Add text overlay
# # # # # # # # # # # # # #         draw = ImageDraw.Draw(pil_overlay)
# # # # # # # # # # # # # #         font_path = "static/fonts/arial.ttf"  # Path to the font file
# # # # # # # # # # # # # #         font_size = 20
# # # # # # # # # # # # # #         font = ImageFont.truetype(font_path, font_size)
# # # # # # # # # # # # # #         text = file.filename  # Get the filename as the text
# # # # # # # # # # # # # #         text_position = (10, 10)
# # # # # # # # # # # # # #         text_color = (255, 255, 255)  # White color
# # # # # # # # # # # # # #         draw.text(text_position, text, font=font, fill=text_color)

# # # # # # # # # # # # # #         # Convert the PIL overlay back to numpy array
# # # # # # # # # # # # # #         overlay_with_text = np.array(pil_overlay)

# # # # # # # # # # # # # #         # Save the resulting image
# # # # # # # # # # # # # #         output_file_path = os.path.join(output_directory, f"output_{i}.png")
# # # # # # # # # # # # # #         cv2.imwrite(output_file_path, overlay_with_text)

# # # # # # # # # # # # # #     return {"message": "Images processed successfully"}

# # # # # # # # # # # # # # # Serve the static files
# # # # # # # # # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")

# # # # # # # # # # # # # # # Define the endpoint to view the output image
# # # # # # # # # # # # # # @app.get("/output/{index}")
# # # # # # # # # # # # # # async def view_output_image(index: int):
# # # # # # # # # # # # # #     output_file_path = f"static/output/output_{index}.png"
# # # # # # # # # # # # # #     return FileResponse(output_file_path)

# # # # # # # # # # # # # # # Start the server
# # # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)


# # # # # # # # # # # # # import os
# # # # # # # # # # # # # import cv2
# # # # # # # # # # # # # import numpy as np
# # # # # # # # # # # # # from typing import List
# # # # # # # # # # # # # from fastapi import FastAPI, UploadFile, File
# # # # # # # # # # # # # from fastapi.responses import Response
# # # # # # # # # # # # # from PIL import Image, ImageDraw, ImageFont
# # # # # # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # # # # # import uvicorn
# # # # # # # # # # # # # from fastapi.responses import FileResponse

# # # # # # # # # # # # # app = FastAPI()

# # # # # # # # # # # # # # Define the upload endpoint
# # # # # # # # # # # # # @app.post("/upload")
# # # # # # # # # # # # # async def upload(files: List[UploadFile] = File(...)):
# # # # # # # # # # # # #     output_directory = "static/output"
# # # # # # # # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # # # # # # # #     for i, file in enumerate(files):
# # # # # # # # # # # # #         # Save the uploaded file temporarily
# # # # # # # # # # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # # # # # # # # #         with open(temp_path, "wb") as f:
# # # # # # # # # # # # #             f.write(await file.read())

# # # # # # # # # # # # #         # Read the image using PIL
# # # # # # # # # # # # #         pil_img = Image.open(temp_path)

# # # # # # # # # # # # #         # Convert the PIL image to numpy array
# # # # # # # # # # # # #         img = np.array(pil_img)

# # # # # # # # # # # # #         # Remove the background using the provided code
# # # # # # # # # # # # #         # Replace the following lines with your background removal code
# # # # # # # # # # # # #         result = img  # Placeholder for the result
# # # # # # # # # # # # #         transparent_img = np.zeros_like(result, dtype=np.uint8)
# # # # # # # # # # # # #         print("Transparent Image Shape:", transparent_img.shape)  # Debug print

# # # # # # # # # # # # #         # Resize the image to 1080x1080
# # # # # # # # # # # # #         resized_result = cv2.resize(result, (1080, 1080))
# # # # # # # # # # # # #         resized_transparent_img = cv2.resize(transparent_img, (1080, 1080))

# # # # # # # # # # # # #         # Overlay the image on the transparent background
# # # # # # # # # # # # #         alpha = 0.5  # Opacity of the overlay image
# # # # # # # # # # # # #         overlay = cv2.addWeighted(resized_result, alpha, resized_transparent_img, 1 - alpha, 0)

# # # # # # # # # # # # #         # Convert the overlay image to PIL Image
# # # # # # # # # # # # #         pil_overlay = Image.fromarray(overlay)

# # # # # # # # # # # # #         # Add text overlay
# # # # # # # # # # # # #         draw = ImageDraw.Draw(pil_overlay)
# # # # # # # # # # # # #         font_path = "static/fonts/arial.ttf"  # Path to the font file
# # # # # # # # # # # # #         font_size = 20
# # # # # # # # # # # # #         font = ImageFont.truetype(font_path, font_size)
# # # # # # # # # # # # #         text = file.filename  # Get the filename as the text
# # # # # # # # # # # # #         text_position = (10, 10)
# # # # # # # # # # # # #         text_color = (255, 255, 255)  # White color
# # # # # # # # # # # # #         draw.text(text_position, text, font=font, fill=text_color)

# # # # # # # # # # # # #         # Convert the PIL overlay back to numpy array
# # # # # # # # # # # # #         overlay_with_text = np.array(pil_overlay)

# # # # # # # # # # # # #         # Save the resulting image
# # # # # # # # # # # # #         output_file_path = os.path.join(output_directory, f"output_{i}.png")
# # # # # # # # # # # # #         cv2.imwrite(output_file_path, overlay_with_text)

# # # # # # # # # # # # #     return {"message": "Images processed successfully"}


# # # # # # # # # # # # # # Serve the static files
# # # # # # # # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")


# # # # # # # # # # # # # # Define the endpoint to view the output image
# # # # # # # # # # # # # @app.get("/output/{index}")
# # # # # # # # # # # # # async def view_output_image(index: int):
# # # # # # # # # # # # #     output_file_path = f"static/output/output_{index}.png"
# # # # # # # # # # # # #     return FileResponse(output_file_path)


# # # # # # # # # # # # # # Define the endpoint to preview the output image in Postman
# # # # # # # # # # # # # @app.post("/preview")
# # # # # # # # # # # # # async def preview_image(file: UploadFile = File(...)):
# # # # # # # # # # # # #     # Read the uploaded image using PIL
# # # # # # # # # # # # #     pil_img = Image.open(file.file)

# # # # # # # # # # # # #     # Convert the PIL image to numpy array
# # # # # # # # # # # # #     img = np.array(pil_img)

# # # # # # # # # # # # #     # Remove the background using the provided code
# # # # # # # # # # # # #     # Replace the following lines with your background removal code
# # # # # # # # # # # # #     result = img  # Placeholder for the result
# # # # # # # # # # # # #     transparent_img = np.zeros_like(result, dtype=np.uint8)
# # # # # # # # # # # # #     print("Transparent Image Shape:", transparent_img.shape)  # Debug print

# # # # # # # # # # # # #     # Resize the image to 1080x1080
# # # # # # # # # # # # #     resized_result = cv2.resize(result, (1080, 1080))
# # # # # # # # # # # # #     resized_transparent_img = cv2.resize(transparent_img, (1080, 1080))

# # # # # # # # # # # # #     # Overlay the image on the transparent background
# # # # # # # # # # # # #     alpha = 0.5  # Opacity of the overlay image
# # # # # # # # # # # # #     overlay = cv2.addWeighted(resized_result, alpha, resized_transparent_img, 1 - alpha, 0)

# # # # # # # # # # # # #     # Convert the overlay image to PIL Image
# # # # # # # # # # # # #     pil_overlay = Image.fromarray(overlay)

# # # # # # # # # # # # #     # Add text overlay
# # # # # # # # # # # # #     draw = ImageDraw.Draw(pil_overlay)
# # # # # # # # # # # # #     font_path = "static/fonts/arial.ttf"  # Path to the font file
# # # # # # # # # # # # #     font_size = 20
# # # # # # # # # # # # #     font = ImageFont.truetype(font_path, font_size)
# # # # # # # # # # # # #     text = file.filename  # Get the filename as the text
# # # # # # # # # # # # #     text_position = (10, 10)
# # # # # # # # # # # # #     text_color = (255, 255, 255)  # White color
# # # # # # # # # # # # #     draw.text(text_position, text, font=font, fill=text_color)

# # # # # # # # # # # # #     # Convert the PIL overlay back to numpy array
# # # # # # # # # # # # #     overlay_with_text = np.array(pil_overlay)

# # # # # # # # # # # # #     # Encode the processed image as base64
# # # # # # # # # # # # #     _, buffer = cv2.imencode(".png", overlay_with_text)
# # # # # # # # # # # # #     image_data = buffer.tobytes()

# # # # # # # # # # # # #     return Response(content=image_data, media_type="image/png")


# # # # # # # # # # # # # # Start the server
# # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)
# # # # # # # # # # # # # import os
# # # # # # # # # # # # # import cv2
# # # # # # # # # # # # # import base64
# # # # # # # # # # # # # import numpy as np
# # # # # # # # # # # # # from typing import List
# # # # # # # # # # # # # from fastapi import FastAPI, UploadFile, File
# # # # # # # # # # # # # from fastapi.responses import Response
# # # # # # # # # # # # # from PIL import Image, ImageDraw, ImageFont
# # # # # # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # # # # # import uvicorn
# # # # # # # # # # # # # from fastapi.responses import FileResponse

# # # # # # # # # # # # # app = FastAPI()

# # # # # # # # # # # # # # Define the upload endpoint
# # # # # # # # # # # # # @app.post("/upload")
# # # # # # # # # # # # # async def upload(files: List[UploadFile] = File(...)):
# # # # # # # # # # # # #     output_directory = "static/output"
# # # # # # # # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # # # # # # # #     for i, file in enumerate(files):
# # # # # # # # # # # # #         # Save the uploaded file temporarily
# # # # # # # # # # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # # # # # # # # #         with open(temp_path, "wb") as f:
# # # # # # # # # # # # #             f.write(await file.read())

# # # # # # # # # # # # #         # Process the image
# # # # # # # # # # # # #         process_image(temp_path, i)

# # # # # # # # # # # # #     return {"message": "Images processed successfully"}


# # # # # # # # # # # # # # Serve the static files
# # # # # # # # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")


# # # # # # # # # # # # # # Define the endpoint to view the output image
# # # # # # # # # # # # # @app.get("/output/{index}")
# # # # # # # # # # # # # async def view_output_image(index: int):
# # # # # # # # # # # # #     output_file_path = f"static/output/output_{index}.png"
# # # # # # # # # # # # #     return FileResponse(output_file_path)


# # # # # # # # # # # # # # Define the endpoint to preview all the output images in Postman
# # # # # # # # # # # # # @app.post("/preview")
# # # # # # # # # # # # # async def preview_images(files: List[UploadFile] = File(...)):
# # # # # # # # # # # # #     previews = []

# # # # # # # # # # # # #     for i, file in enumerate(files):
# # # # # # # # # # # # #         # Save the uploaded file temporarily
# # # # # # # # # # # # #         temp_path = os.path.join("static", f"temp_{i}.png")
# # # # # # # # # # # # #         with open(temp_path, "wb") as f:
# # # # # # # # # # # # #             f.write(await file.read())

# # # # # # # # # # # # #         # Process the image and generate the preview
# # # # # # # # # # # # #         process_image(temp_path, i)

# # # # # # # # # # # # #         # Read the preview image as base64-encoded string
# # # # # # # # # # # # #         output_file_path = f"static/output/output_{i}.png"
# # # # # # # # # # # # #         with open(output_file_path, "rb") as f:
# # # # # # # # # # # # #             image_data = base64.b64encode(f.read()).decode("utf-8")
# # # # # # # # # # # # #             previews.append(image_data)

# # # # # # # # # # # # #     return {"previews": previews}


# # # # # # # # # # # # # # Utility function to process the image
# # # # # # # # # # # # # def process_image(temp_path, index):
# # # # # # # # # # # # #     # Read the image using PIL
# # # # # # # # # # # # #     pil_img = Image.open(temp_path)

# # # # # # # # # # # # #     # Convert the PIL image to numpy array
# # # # # # # # # # # # #     img = np.array(pil_img)

# # # # # # # # # # # # #     # Remove the background using the provided code
# # # # # # # # # # # # #     # Replace the following lines with your background removal code
# # # # # # # # # # # # #     result = img  # Placeholder for the result
# # # # # # # # # # # # #     transparent_img = np.zeros_like(result, dtype=np.uint8)

# # # # # # # # # # # # #     # Resize the image to 1080x1080
# # # # # # # # # # # # #     resized_result = cv2.resize(result, (1080, 1080))
# # # # # # # # # # # # #     resized_transparent_img = cv2.resize(transparent_img, (1080, 1080))

# # # # # # # # # # # # #     # Overlay the image on the transparent background
# # # # # # # # # # # # #     alpha = 0.5  # Opacity of the overlay image
# # # # # # # # # # # # #     overlay = cv2.addWeighted(resized_result, alpha, resized_transparent_img, 1 - alpha, 0)

# # # # # # # # # # # # #     # Convert the overlay image to PIL Image
# # # # # # # # # # # # #     pil_overlay = Image.fromarray(overlay)

# # # # # # # # # # # # #     # Add text overlay
# # # # # # # # # # # # #     draw = ImageDraw.Draw(pil_overlay)
# # # # # # # # # # # # #     font_path = "static/fonts/arial.ttf"  # Path to the font file
# # # # # # # # # # # # #     font_size = 20
# # # # # # # # # # # # #     font = ImageFont.truetype(font_path, font_size)
# # # # # # # # # # # # #     text = os.path.basename(temp_path)  # Get the filename as the text
# # # # # # # # # # # # #     text_position = (10, 10)
# # # # # # # # # # # # #     text_color = (255, 255, 255)  # White color
# # # # # # # # # # # # #     draw.text(text_position, text, font=font, fill=text_color)

# # # # # # # # # # # # #     # Convert the PIL overlay back to numpy array
# # # # # # # # # # # # #     overlay_with_text = np.array(pil_overlay)

# # # # # # # # # # # # #     # Save the resulting image
# # # # # # # # # # # # #     output_directory = "static/output"
# # # # # # # # # # # # #     output_file_path = os.path.join(output_directory, f"output_{index}.png")
# # # # # # # # # # # # #     cv2.imwrite(output_file_path, overlay_with_text)


# # # # # # # # # # # # # # Start the server
# # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)
# # # # # # # # # # # # import os
# # # # # # # # # # # # import cv2
# # # # # # # # # # # # import numpy as np
# # # # # # # # # # # # from typing import List
# # # # # # # # # # # # from fastapi import FastAPI, UploadFile, File
# # # # # # # # # # # # from PIL import Image, ImageDraw, ImageFont
# # # # # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # # # # from fastapi.responses import FileResponse
# # # # # # # # # # # # import uvicorn

# # # # # # # # # # # # app = FastAPI()

# # # # # # # # # # # # # Define the upload endpoint
# # # # # # # # # # # # @app.post("/upload")
# # # # # # # # # # # # async def upload(files: List[UploadFile] = File(...)):
# # # # # # # # # # # #     output_directory = "static/output"
# # # # # # # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # # # # # # #     for i, file in enumerate(files):
# # # # # # # # # # # #         # Save the uploaded file temporarily
# # # # # # # # # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # # # # # # # #         with open(temp_path, "wb") as f:
# # # # # # # # # # # #             f.write(await file.read())

# # # # # # # # # # # #         # Process the image
# # # # # # # # # # # #         process_image(temp_path, i)

# # # # # # # # # # # #     return {"message": "Images processed successfully"}


# # # # # # # # # # # # # Serve the static files
# # # # # # # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")


# # # # # # # # # # # # # Define the endpoint to view the output image
# # # # # # # # # # # # @app.get("/output/{index}")
# # # # # # # # # # # # async def view_output_image(index: int):
# # # # # # # # # # # #     output_file_path = f"static/output/output_{index}.png"
# # # # # # # # # # # #     return FileResponse(output_file_path)


# # # # # # # # # # # # # Define the endpoint to preview all the output images in Postman
# # # # # # # # # # # # @app.post("/preview")
# # # # # # # # # # # # async def preview_images(files: List[UploadFile] = File(...)):
# # # # # # # # # # # #     previews = []

# # # # # # # # # # # #     for i, file in enumerate(files):
# # # # # # # # # # # #         # Save the uploaded file temporarily
# # # # # # # # # # # #         temp_path = os.path.join("static", f"temp_{i}.png")
# # # # # # # # # # # #         with open(temp_path, "wb") as f:
# # # # # # # # # # # #             f.write(await file.read())

# # # # # # # # # # # #         # Process the image and generate the preview
# # # # # # # # # # # #         process_image(temp_path, i)

# # # # # # # # # # # #         # Add the preview image path to the response
# # # # # # # # # # # #         output_file_path = f"static/output/output_{i}.png"
# # # # # # # # # # # #         previews.append(output_file_path)

# # # # # # # # # # # #     return {"previews": previews}


# # # # # # # # # # # # # Utility function to process the image
# # # # # # # # # # # # def process_image(temp_path, index):
# # # # # # # # # # # #     # Read the image using PIL
# # # # # # # # # # # #     pil_img = Image.open(temp_path)

# # # # # # # # # # # #     # Convert the PIL image to numpy array
# # # # # # # # # # # #     img = np.array(pil_img)

# # # # # # # # # # # #     # Remove the background using the provided code
# # # # # # # # # # # #     # Replace the following lines with your background removal code
# # # # # # # # # # # #     result = img  # Placeholder for the result
# # # # # # # # # # # #     transparent_img = np.zeros_like(result, dtype=np.uint8)

# # # # # # # # # # # #     # Resize the image to 1080x1080
# # # # # # # # # # # #     resized_result = cv2.resize(result, (1080, 1080))
# # # # # # # # # # # #     resized_transparent_img = cv2.resize(transparent_img, (1080, 1080))

# # # # # # # # # # # #     # Overlay the image on the transparent background
# # # # # # # # # # # #     alpha = 0.5  # Opacity of the overlay image
# # # # # # # # # # # #     overlay = cv2.addWeighted(resized_result, alpha, resized_transparent_img, 1 - alpha, 0)

# # # # # # # # # # # #     # Convert the overlay image to PIL Image
# # # # # # # # # # # #     pil_overlay = Image.fromarray(overlay)

# # # # # # # # # # # #     # Add text overlay
# # # # # # # # # # # #     draw = ImageDraw.Draw(pil_overlay)
# # # # # # # # # # # #     font_path = "static/fonts/arial.ttf"  # Path to the font file
# # # # # # # # # # # #     font_size = 20
# # # # # # # # # # # #     font = ImageFont.truetype(font_path, font_size)
# # # # # # # # # # # #     text = os.path.basename(temp_path)  # Get the filename as the text
# # # # # # # # # # # #     text_position = (10, 10)
# # # # # # # # # # # #     text_color = (255, 255, 255)  # White color
# # # # # # # # # # # #     draw.text(text_position, text, font=font, fill=text_color)

# # # # # # # # # # # #     # Convert the PIL overlay back to numpy array
# # # # # # # # # # # #     overlay_with_text = np.array(pil_overlay)

# # # # # # # # # # # #     # Save the resulting image
# # # # # # # # # # # #     output_directory = "static/output"
# # # # # # # # # # # #     output_file_path = os.path.join(output_directory, f"output_{index}.png")
# # # # # # # # # # # #     cv2.imwrite(output_file_path, overlay_with_text)


# # # # # # # # # # # # # Start the server
# # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)



# # # # # # # # # # # import os
# # # # # # # # # # # import cv2
# # # # # # # # # # # import base64
# # # # # # # # # # # import numpy as np
# # # # # # # # # # # from typing import List
# # # # # # # # # # # from fastapi import FastAPI, UploadFile, File
# # # # # # # # # # # from PIL import Image, ImageDraw, ImageFont
# # # # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # # # from fastapi.responses import StreamingResponse
# # # # # # # # # # # import uvicorn

# # # # # # # # # # # app = FastAPI()

# # # # # # # # # # # # Define the upload endpoint
# # # # # # # # # # # @app.post("/upload")
# # # # # # # # # # # async def upload(files: List[UploadFile] = File(...)):
# # # # # # # # # # #     output_directory = "static/output"
# # # # # # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # # # # # #     for i, file in enumerate(files):
# # # # # # # # # # #         # Save the uploaded file temporarily
# # # # # # # # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # # # # # # #         with open(temp_path, "wb") as f:
# # # # # # # # # # #             f.write(await file.read())

# # # # # # # # # # #         # Process the image
# # # # # # # # # # #         process_image(temp_path, i)

# # # # # # # # # # #     return {"message": "Images processed successfully"}


# # # # # # # # # # # # Serve the static files
# # # # # # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")


# # # # # # # # # # # # Define the endpoint to view the output image
# # # # # # # # # # # @app.get("/output/{index}")
# # # # # # # # # # # async def view_output_image(index: int):
# # # # # # # # # # #     output_file_path = f"static/output/output_{index}.png"
# # # # # # # # # # #     return FileResponse(output_file_path)


# # # # # # # # # # # # Define the endpoint to get all the image previews
# # # # # # # # # # # @app.get("/img")
# # # # # # # # # # # async def get_image_previews():
# # # # # # # # # # #     previews = []

# # # # # # # # # # #     output_directory = "static/output"
# # # # # # # # # # #     for filename in os.listdir(output_directory):
# # # # # # # # # # #         if filename.startswith("output_") and filename.endswith(".png"):
# # # # # # # # # # #             output_file_path = os.path.join(output_directory, filename)
# # # # # # # # # # #             previews.append(output_file_path)

# # # # # # # # # # #     def stream():
# # # # # # # # # # #         for preview_path in previews:
# # # # # # # # # # #             with open(preview_path, "rb") as f:
# # # # # # # # # # #                 yield f.read()

# # # # # # # # # # #     return StreamingResponse(stream(), media_type="image/png")


# # # # # # # # # # # # Utility function to process the image
# # # # # # # # # # # def process_image(temp_path, index):
# # # # # # # # # # #     # Read the image using PIL
# # # # # # # # # # #     pil_img = Image.open(temp_path)

# # # # # # # # # # #     # Convert the PIL image to numpy array
# # # # # # # # # # #     img = np.array(pil_img)

# # # # # # # # # # #     # Remove the background using the provided code
# # # # # # # # # # #     # Replace the following lines with your background removal code
# # # # # # # # # # #     result = img  # Placeholder for the result
# # # # # # # # # # #     transparent_img = np.zeros_like(result, dtype=np.uint8)

# # # # # # # # # # #     # Resize the image to 1080x1080
# # # # # # # # # # #     resized_result = cv2.resize(result, (1080, 1080))
# # # # # # # # # # #     resized_transparent_img = cv2.resize(transparent_img, (1080, 1080))

# # # # # # # # # # #     # Overlay the image on the transparent background
# # # # # # # # # # #     alpha = 0.5  # Opacity of the overlay image
# # # # # # # # # # #     overlay = cv2.addWeighted(resized_result, alpha, resized_transparent_img, 1 - alpha, 0)

# # # # # # # # # # #     # Convert the overlay image to PIL Image
# # # # # # # # # # #     pil_overlay = Image.fromarray(overlay)

# # # # # # # # # # #     # Add text overlay
# # # # # # # # # # #     draw = ImageDraw.Draw(pil_overlay)
# # # # # # # # # # #     font_path = "static/fonts/arial.ttf"  # Path to the font file
# # # # # # # # # # #     font_size = 20
# # # # # # # # # # #     font = ImageFont.truetype(font_path, font_size)
# # # # # # # # # # #     text = os.path.basename(temp_path)  # Get the filename as the text
# # # # # # # # # # #     text_position = (10, 10)
# # # # # # # # # # #     text_color = (255, 255, 255)  # White color
# # # # # # # # # # #     draw.text(text_position, text, font=font, fill=text_color)

# # # # # # # # # # #     # Convert the PIL overlay back to numpy array
# # # # # # # # # # #     overlay_with_text = np.array(pil_overlay)

# # # # # # # # # # #     # Save the resulting image
# # # # # # # # # # #     output_directory = "static/output"
# # # # # # # # # # #     output_file_path = os.path.join(output_directory, f"output_{index}.png")
# # # # # # # # # # #     cv2.imwrite(output_file_path, overlay_with_text)


# # # # # # # # # # # # Start the server
# # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)
# # # # # # # # # # import os
# # # # # # # # # # import cv2
# # # # # # # # # # import numpy as np
# # # # # # # # # # from typing import List
# # # # # # # # # # from fastapi import FastAPI, UploadFile, File
# # # # # # # # # # from PIL import Image, ImageDraw, ImageFont
# # # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # # from fastapi.responses import StreamingResponse
# # # # # # # # # # import uvicorn

# # # # # # # # # # app = FastAPI()

# # # # # # # # # # # Define the upload endpoint
# # # # # # # # # # @app.post("/upload")
# # # # # # # # # # async def upload(files: List[UploadFile] = File(...)):
# # # # # # # # # #     output_directory = "static/output"
# # # # # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # # # # #     for i, file in enumerate(files):
# # # # # # # # # #         # Save the uploaded file temporarily
# # # # # # # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # # # # # #         with open(temp_path, "wb") as f:
# # # # # # # # # #             f.write(await file.read())

# # # # # # # # # #         # Process the image
# # # # # # # # # #         process_image(temp_path, i)

# # # # # # # # # #     return {"message": "Images processed successfully"}


# # # # # # # # # # # Serve the static files
# # # # # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")


# # # # # # # # # # # Define the endpoint to view the output image
# # # # # # # # # # @app.get("/output/{index}")
# # # # # # # # # # async def view_output_image(index: int):
# # # # # # # # # #     output_file_path = f"static/output/output_{index}.png"
# # # # # # # # # #     return FileResponse(output_file_path)


# # # # # # # # # # # Define the endpoint to get all the image previews
# # # # # # # # # # @app.get("/img")
# # # # # # # # # # async def get_image_previews():
# # # # # # # # # #     previews = []

# # # # # # # # # #     output_directory = "static/output"
# # # # # # # # # #     for filename in os.listdir(output_directory):
# # # # # # # # # #         if filename.startswith("output_") and filename.endswith(".png"):
# # # # # # # # # #             output_file_path = os.path.join(output_directory, filename)
# # # # # # # # # #             previews.append(output_file_path)

# # # # # # # # # #     def stream():
# # # # # # # # # #         for preview_path in previews:
# # # # # # # # # #             with open(preview_path, "rb") as f:
# # # # # # # # # #                 yield f.read()

# # # # # # # # # #     return StreamingResponse(stream(), media_type="image/png")


# # # # # # # # # # # Utility function to process the image
# # # # # # # # # # def process_image(temp_path, index):
# # # # # # # # # #     # Read the image using PIL
# # # # # # # # # #     pil_img = Image.open(temp_path)

# # # # # # # # # #     # Convert the PIL image to numpy array
# # # # # # # # # #     img = np.array(pil_img)

# # # # # # # # # #     # Remove the background and make it green
# # # # # # # # # #     green_background = np.zeros_like(img, dtype=np.uint8)
# # # # # # # # # #     green_background[:, :] = (0, 255, 0)  # Green color

# # # # # # # # # #     # Mask the original image on the green background
# # # # # # # # # #     mask = np.all(img == [255, 255, 255], axis=2)  # White pixels mask
# # # # # # # # # #     result = np.where(mask[:, :, np.newaxis], img, green_background)

# # # # # # # # # #     # Save the resulting image
# # # # # # # # # #     output_directory = "static/output"
# # # # # # # # # #     output_file_path = os.path.join(output_directory, f"output_{index}.png")
# # # # # # # # # #     cv2.imwrite(output_file_path, result)


# # # # # # # # # # # Start the server
# # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)

# # # # # # # # # import os
# # # # # # # # # import cv2
# # # # # # # # # import numpy as np
# # # # # # # # # from typing import List
# # # # # # # # # from fastapi import FastAPI, UploadFile, File
# # # # # # # # # from PIL import Image, ImageDraw, ImageFont
# # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # from fastapi.responses import StreamingResponse
# # # # # # # # # import uvicorn

# # # # # # # # # app = FastAPI()

# # # # # # # # # # Define the upload endpoint
# # # # # # # # # @app.post("/upload")
# # # # # # # # # async def upload(files: List[UploadFile] = File(...)):
# # # # # # # # #     output_directory = "static/output"
# # # # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # # # #     for i, file in enumerate(files):
# # # # # # # # #         # Save the uploaded file temporarily
# # # # # # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # # # # #         with open(temp_path, "wb") as f:
# # # # # # # # #             f.write(await file.read())

# # # # # # # # #         # Process the image
# # # # # # # # #         process_image(temp_path, i)

# # # # # # # # #     return {"message": "Images processed successfully"}


# # # # # # # # # # Serve the static files
# # # # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")


# # # # # # # # # # Define the endpoint to view the output image
# # # # # # # # # @app.get("/output/{index}")
# # # # # # # # # async def view_output_image(index: int):
# # # # # # # # #     output_file_path = f"static/output/output_{index}.png"
# # # # # # # # #     return FileResponse(output_file_path)


# # # # # # # # # # Define the endpoint to get all the image previews
# # # # # # # # # @app.get("/img")
# # # # # # # # # async def get_image_previews():
# # # # # # # # #     previews = []

# # # # # # # # #     output_directory = "static/output"
# # # # # # # # #     for filename in os.listdir(output_directory):
# # # # # # # # #         if filename.startswith("output_") and filename.endswith(".png"):
# # # # # # # # #             output_file_path = os.path.join(output_directory, filename)
# # # # # # # # #             previews.append(output_file_path)

# # # # # # # # #     def stream():
# # # # # # # # #         for preview_path in previews:
# # # # # # # # #             with open(preview_path, "rb") as f:
# # # # # # # # #                 yield f.read()

# # # # # # # # #     return StreamingResponse(stream(), media_type="image/png")


# # # # # # # # # # Utility function to process the image
# # # # # # # # # def process_image(temp_path, index):
# # # # # # # # #     # Read the image using PIL
# # # # # # # # #     pil_img = Image.open(temp_path)

# # # # # # # # #     # Convert the PIL image to numpy array
# # # # # # # # #     img = np.array(pil_img)

# # # # # # # # #     # Remove the background using the provided code
# # # # # # # # #     # Replace the following lines with your background removal code
# # # # # # # # #     result = img  # Placeholder for the result

# # # # # # # # #     # Resize the image to 1080x1080
# # # # # # # # #     resized_result = cv2.resize(result, (1080, 1080))

# # # # # # # # #     # Save the resulting image
# # # # # # # # #     output_directory = "static/output"
# # # # # # # # #     output_file_path = os.path.join(output_directory, f"out{index}.png")
# # # # # # # # #     cv2.imwrite(output_file_path, resized_result)


# # # # # # # # # # Start the server
# # # # # # # # # if __name__ == "__main__":
# # # # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)
# # # # # # # # # import os
# # # # # # # # # import cv2
# # # # # # # # # import numpy as np
# # # # # # # # # from typing import List
# # # # # # # # # from fastapi import FastAPI, UploadFile, File
# # # # # # # # # from PIL import Image, ImageDraw, ImageFont
# # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # from fastapi.responses import StreamingResponse
# # # # # # # # # import uvicorn

# # # # # # # # # app = FastAPI()

# # # # # # # # # # Define the upload endpoint
# # # # # # # # # @app.post("/upload")
# # # # # # # # # async def upload(files: List[UploadFile] = File(...)):
# # # # # # # # #     output_directory = "static/output"
# # # # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # # # #     for i, file in enumerate(files):
# # # # # # # # #         # Save the uploaded file temporarily
# # # # # # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # # # # #         with open(temp_path, "wb") as f:
# # # # # # # # #             f.write(await file.read())

# # # # # # # # #         # Process the image
# # # # # # # # #         process_image(temp_path, i)

# # # # # # # # #     return {"message": "Images processed successfully"}


# # # # # # # # # # Serve the static files
# # # # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")


# # # # # # # # # # Define the endpoint to view the output image
# # # # # # # # # @app.get("/output/{index}")
# # # # # # # # # async def view_output_image(index: int):
# # # # # # # # #     output_file_path = f"static/output/output_{index}.png"
# # # # # # # # #     return FileResponse(output_file_path)


# # # # # # # # # # Define the endpoint to get all the image previews
# # # # # # # # # @app.get("/img")
# # # # # # # # # async def get_image_previews():
# # # # # # # # #     previews = []

# # # # # # # # #     output_directory = "static/output"
# # # # # # # # #     for filename in os.listdir(output_directory):
# # # # # # # # #         if filename.startswith("output_") and filename.endswith(".png"):
# # # # # # # # #             output_file_path = os.path.join(output_directory, filename)
# # # # # # # # #             previews.append(output_file_path)

# # # # # # # # #     def stream():
# # # # # # # # #         for preview_path in previews:
# # # # # # # # #             with open(preview_path, "rb") as f:
# # # # # # # # #                 yield f.read()

# # # # # # # # #     return StreamingResponse(stream(), media_type="image/png")


# # # # # # # # # # Utility function to process the image
# # # # # # # # # def process_image(temp_path, index):
# # # # # # # # #     # Read the image using OpenCV
# # # # # # # # #     img = cv2.imread(temp_path)

# # # # # # # # #     # Convert the image to grayscale
# # # # # # # # #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # # # # # # # #     # Perform background removal using thresholding
# # # # # # # # #     _, thresholded = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

# # # # # # # # #     # Find contours of the foreground objects
# # # # # # # # #     contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # # # # # # # #     # Create a mask for the foreground objects
# # # # # # # # #     mask = np.zeros_like(thresholded)
# # # # # # # # #     cv2.drawContours(mask, contours, -1, (255), thickness=cv2.FILLED)

# # # # # # # # #     # Apply the mask to the original image
# # # # # # # # #     result = cv2.bitwise_and(img, img, mask=mask)

# # # # # # # # #     # Resize the image to 1080x1080
# # # # # # # # #     resized_result = cv2.resize(result, (1080, 1080))

# # # # # # # # #     # Save the resulting image
# # # # # # # # #     output_directory = "static/output"
# # # # # # # # #     output_file_path = os.path.join(output_directory, f"out{index}.png")
# # # # # # # # #     cv2.imwrite(output_file_path, resized_result)


# # # # # # # # # # Start the server
# # # # # # # # # if __name__ == "__main__":
# # # # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)



# # # # # # # # import os
# # # # # # # # import cv2
# # # # # # # # import numpy as np
# # # # # # # # from typing import List
# # # # # # # # from fastapi import FastAPI, UploadFile, File
# # # # # # # # from PIL import Image, ImageDraw, ImageFont
# # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # from fastapi.responses import StreamingResponse, FileResponse
# # # # # # # # import uvicorn

# # # # # # # # app = FastAPI()

# # # # # # # # # Define the upload endpoint
# # # # # # # # @app.post("/upload")
# # # # # # # # async def upload(files: List[UploadFile] = File(...)):
# # # # # # # #     output_directory = "static/output"
# # # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # # #     for i, file in enumerate(files):
# # # # # # # #         # Save the uploaded file temporarily
# # # # # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # # # #         with open(temp_path, "wb") as f:
# # # # # # # #             f.write(await file.read())

# # # # # # # #         # Process the image
# # # # # # # #         process_image(temp_path, i)

# # # # # # # #     # Get a list of processed image file paths
# # # # # # # #     processed_images = []
# # # # # # # #     for filename in os.listdir(output_directory):
# # # # # # # #         if filename.startswith("out") and filename.endswith(".png"):
# # # # # # # #             processed_images.append(filename)

# # # # # # # #     return {"message": "Images processed successfully", "processed_images": processed_images}


# # # # # # # # # Serve the static files
# # # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")


# # # # # # # # # Define the endpoint to view the output image
# # # # # # # # @app.get("/output/{index}")
# # # # # # # # async def view_output_image(index: int):
# # # # # # # #     output_file_path = f"static/output/output_{index}.png"
# # # # # # # #     return FileResponse(output_file_path)


# # # # # # # # # Define the endpoint to get all the image previews
# # # # # # # # @app.get("/img")
# # # # # # # # async def get_image_previews():
# # # # # # # #     previews = []

# # # # # # # #     output_directory = "static/output"
# # # # # # # #     for filename in os.listdir(output_directory):
# # # # # # # #         if filename.startswith("output_") and filename.endswith(".png"):
# # # # # # # #             output_file_path = os.path.join(output_directory, filename)
# # # # # # # #             previews.append(output_file_path)

# # # # # # # #     def stream():
# # # # # # # #         for preview_path in previews:
# # # # # # # #             with open(preview_path, "rb") as f:
# # # # # # # #                 yield f.read()

# # # # # # # #     return StreamingResponse(stream(), media_type="image/png")


# # # # # # # # # Utility function to process the image
# # # # # # # # def process_image(temp_path, index):
# # # # # # # #     # Read the image using OpenCV
# # # # # # # #     img = cv2.imread(temp_path)

# # # # # # # #     # Convert the image to grayscale
# # # # # # # #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # # # # # # #     # Perform background removal using thresholding
# # # # # # # #     _, thresholded = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

# # # # # # # #     # Find contours of the foreground objects
# # # # # # # #     contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # # # # # # #     # Create a mask for the foreground objects
# # # # # # # #     mask = np.zeros_like(thresholded)
# # # # # # # #     cv2.drawContours(mask, contours, -1, (255), thickness=cv2.FILLED)

# # # # # # # #     # Apply the mask to the original image
# # # # # # # #     result = cv2.bitwise_and(img, img, mask=mask)

# # # # # # # #     # Resize the image to 1080x1080
# # # # # # # #     resized_result = cv2.resize(result, (1080, 1080))

# # # # # # # #     # Save the resulting image
# # # # # # # #     output_directory = "static/output"
# # # # # # # #     output_file_path = os.path.join(output_directory, f"out{index}.png")
# # # # # # # #     cv2.imwrite(output_file_path, resized_result)


# # # # # # # # # Start the server
# # # # # # # # if __name__ == "__main__":
# # # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)
# # # # # # # import os
# # # # # # # import cv2
# # # # # # # import numpy as np
# # # # # # # import torch
# # # # # # # from torchvision import transforms
# # # # # # # from typing import List
# # # # # # # from fastapi import FastAPI, UploadFile, File
# # # # # # # from PIL import Image
# # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # from fastapi.responses import StreamingResponse, FileResponse
# # # # # # # import uvicorn

# # # # # # # app = FastAPI()

# # # # # # # # Load the pre-trained DeepLabv3 model
# # # # # # # model = torch.hub.load('pytorch/vision:v0.9.0', 'deeplabv3_resnet101', pretrained=True)
# # # # # # # model.eval()

# # # # # # # # Define the image transformation
# # # # # # # transform = transforms.Compose([
# # # # # # #     transforms.Resize((1080, 1080)),
# # # # # # #     transforms.ToTensor(),
# # # # # # #     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
# # # # # # # ])

# # # # # # # # Define the upload endpoint
# # # # # # # @app.post("/upload")
# # # # # # # async def upload(files: List[UploadFile] = File(...)):
# # # # # # #     output_directory = "static/output"
# # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # #     for i, file in enumerate(files):
# # # # # # #         # Save the uploaded file temporarily
# # # # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # # #         with open(temp_path, "wb") as f:
# # # # # # #             f.write(await file.read())

# # # # # # #         # Process the image
# # # # # # #         process_image(temp_path, i)

# # # # # # #     # Get a list of processed image file paths
# # # # # # #     processed_images = []
# # # # # # #     for filename in os.listdir(output_directory):
# # # # # # #         if filename.startswith("out") and filename.endswith(".png"):
# # # # # # #             processed_images.append(filename)

# # # # # # #     return {"message": "Images processed successfully", "processed_images": processed_images}


# # # # # # # # Serve the static files
# # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")


# # # # # # # # Define the endpoint to view the output image
# # # # # # # @app.get("/output/{index}")
# # # # # # # async def view_output_image(index: int):
# # # # # # #     output_file_path = f"static/output/output_{index}.png"
# # # # # # #     return FileResponse(output_file_path)


# # # # # # # # Define the endpoint to get all the image previews
# # # # # # # @app.get("/img")
# # # # # # # async def get_image_previews():
# # # # # # #     previews = []

# # # # # # #     output_directory = "static/output"
# # # # # # #     for filename in os.listdir(output_directory):
# # # # # # #         if filename.startswith("output_") and filename.endswith(".png"):
# # # # # # #             output_file_path = os.path.join(output_directory, filename)
# # # # # # #             previews.append(output_file_path)

# # # # # # #     def stream():
# # # # # # #         for preview_path in previews:
# # # # # # #             with open(preview_path, "rb") as f:
# # # # # # #                 yield f.read()

# # # # # # #     return StreamingResponse(stream(), media_type="image/png")


# # # # # # # # Utility function to process the image
# # # # # # # def process_image(temp_path, index):
# # # # # # #     # Read the image using PIL
# # # # # # #     pil_img = Image.open(temp_path).convert("RGB")

# # # # # # #     # Apply the transformation
# # # # # # #     img = transform(pil_img).unsqueeze(0)

# # # # # # #     # Perform background removal using the pre-trained model
# # # # # # #     with torch.no_grad():
# # # # # # #         output = model(img)[0]
# # # # # # #         mask = output.argmax(0)

# # # # # # #     # Convert the mask to a numpy array
# # # # # # #     mask = mask.byte().cpu().numpy()

# # # # # # #     # Apply the mask to the original image
# # # # # # #     img = np.array(pil_img)
# # # # # # #     result = np.zeros_like(img)
# # # # # # #     result[mask == 1] = img[mask == 1]

# # # # # # #     # Save the resulting image
# # # # # # #     output_directory = "static/output"
# # # # # # #     output_file_path = os.path.join(output_directory, f"out{index}.png")
# # # # # # #     cv2.imwrite(output_file_path, result)


# # # # # # # # Start the server
# # # # # # # if __name__ == "__main__":
# # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)
# # # # # # # import os
# # # # # # # import cv2
# # # # # # # import numpy as np
# # # # # # # from typing import List
# # # # # # # from fastapi import FastAPI, UploadFile, File
# # # # # # # from PIL import Image, ImageDraw, ImageFont
# # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # from fastapi.responses import StreamingResponse, FileResponse
# # # # # # # import uvicorn

# # # # # # # app = FastAPI()

# # # # # # # # Define the upload endpoint
# # # # # # # @app.post("/upload")
# # # # # # # async def upload(files: List[UploadFile] = File(...)):
# # # # # # #     output_directory = "static/output"
# # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # #     for i, file in enumerate(files):
# # # # # # #         # Save the uploaded file temporarily
# # # # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # # #         with open(temp_path, "wb") as f:
# # # # # # #             f.write(await file.read())

# # # # # # #         # Process the image
# # # # # # #         process_image(temp_path, i)

# # # # # # #     # Get a list of processed image file paths
# # # # # # #     processed_images = []
# # # # # # #     for filename in os.listdir(output_directory):
# # # # # # #         if filename.startswith("out") and filename.endswith(".png"):
# # # # # # #             processed_images.append(filename)

# # # # # # #     return {"message": "Images processed successfully", "processed_images": processed_images}


# # # # # # # # Serve the static files
# # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")


# # # # # # # # Define the endpoint to view the output image
# # # # # # # @app.get("/output/{index}")
# # # # # # # async def view_output_image(index: int):
# # # # # # #     output_file_path = f"static/output/output_{index}.png"
# # # # # # #     return FileResponse(output_file_path)


# # # # # # # # Define the endpoint to get all the image previews
# # # # # # # @app.get("/img")
# # # # # # # async def get_image_previews():
# # # # # # #     previews = []

# # # # # # #     output_directory = "static/output"
# # # # # # #     for filename in os.listdir(output_directory):
# # # # # # #         if filename.startswith("output_") and filename.endswith(".png"):
# # # # # # #             output_file_path = os.path.join(output_directory, filename)
# # # # # # #             previews.append(output_file_path)

# # # # # # #     def stream():
# # # # # # #         for preview_path in previews:
# # # # # # #             with open(preview_path, "rb") as f:
# # # # # # #                 yield f.read()

# # # # # # #     return StreamingResponse(stream(), media_type="image/png")


# # # # # # # # Utility function to process the image
# # # # # # # def process_image(temp_path, index):
# # # # # # #     # Read the image using OpenCV
# # # # # # #     img = cv2.imread(temp_path)

# # # # # # #     # Create a mask using the GrabCut algorithm
# # # # # # #     mask = np.zeros(img.shape[:2], np.uint8)
# # # # # # #     bgd_model = np.zeros((1, 65), np.float64)
# # # # # # #     fgd_model = np.zeros((1, 65), np.float64)
# # # # # # #     rect = (1, 1, img.shape[1] - 1, img.shape[0] - 1)  # Initial rectangular region

# # # # # # #     cv2.grabCut(img, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)

# # # # # # #     # Create a mask with only the probable foreground region
# # # # # # #     mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

# # # # # # #     # Apply the mask to the original image
# # # # # # #     result = img * mask2[:, :, np.newaxis]

# # # # # # #     # Resize the image to 1080x1080
# # # # # # #     resized_result = cv2.resize(result, (1080, 1080))

# # # # # # #     # Save the resulting image
# # # # # # #     output_directory = "static/output"
# # # # # # #     output_file_path = os.path.join(output_directory, f"out{index}.png")
# # # # # # #     cv2.imwrite(output_file_path, resized_result)


# # # # # # # # Start the server
# # # # # # # if __name__ == "__main__":
# # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)
# # # # # # import os
# # # # # # import cv2
# # # # # # import numpy as np
# # # # # # from typing import List
# # # # # # from fastapi import FastAPI, UploadFile, File
# # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # from fastapi.responses import StreamingResponse, FileResponse
# # # # # # import uvicorn

# # # # # # app = FastAPI()

# # # # # # # Define the upload endpoint
# # # # # # @app.post("/upload")
# # # # # # async def upload(files: List[UploadFile] = File(...)):
# # # # # #     output_directory = "static/output"
# # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # #     for i, file in enumerate(files):
# # # # # #         # Save the uploaded file temporarily
# # # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # #         with open(temp_path, "wb") as f:
# # # # # #             f.write(await file.read())

# # # # # #         # Process the image
# # # # # #         process_image(temp_path, i)

# # # # # #     # Get a list of processed image file paths
# # # # # #     processed_images = []
# # # # # #     for filename in os.listdir(output_directory):
# # # # # #         if filename.startswith("out") and filename.endswith(".png"):
# # # # # #             processed_images.append(filename)

# # # # # #     return {"message": "Images processed successfully", "processed_images": processed_images}


# # # # # # # Serve the static files
# # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")


# # # # # # # Define the endpoint to view the output image
# # # # # # @app.get("/output/{index}")
# # # # # # async def view_output_image(index: int):
# # # # # #     output_file_path = f"static/output/output_{index}.png"
# # # # # #     return FileResponse(output_file_path)


# # # # # # # Define the endpoint to get all the image previews
# # # # # # @app.get("/img")
# # # # # # async def get_image_previews():
# # # # # #     previews = []

# # # # # #     output_directory = "static/output"
# # # # # #     for filename in os.listdir(output_directory):
# # # # # #         if filename.startswith("output_") and filename.endswith(".png"):
# # # # # #             output_file_path = os.path.join(output_directory, filename)
# # # # # #             previews.append(output_file_path)

# # # # # #     def stream():
# # # # # #         for preview_path in previews:
# # # # # #             with open(preview_path, "rb") as f:
# # # # # #                 yield f.read()

# # # # # #     return StreamingResponse(stream(), media_type="image/png")


# # # # # # # Utility function to process the image
# # # # # # def process_image(temp_path, index):
# # # # # #     # Read the image using OpenCV
# # # # # #     img = cv2.imread(temp_path)

# # # # # #     # Convert image to RGB format
# # # # # #     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# # # # # #     # Create a mask with white background
# # # # # #     mask = np.zeros(img.shape[:2], np.uint8)

# # # # # #     # Define the background and foreground models
# # # # # #     bgd_model = np.zeros((1, 65), np.float64)
# # # # # #     fgd_model = np.zeros((1, 65), np.float64)

# # # # # #     # Define the bounding rectangle for the foreground object
# # # # # #     rect = (1, 1, img.shape[1] - 1, img.shape[0] - 1)

# # # # # #     # Apply GrabCut algorithm to extract foreground
# # # # # #     cv2.grabCut(img_rgb, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)

# # # # # #     # Create a mask with only the foreground region
# # # # # #     mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

# # # # # #     # Apply the mask to the original image
# # # # # #     result = img * mask[:, :, np.newaxis]

# # # # # #     # Resize the image to 1080x1080
# # # # # #     resized_result = cv2.resize(result, (1080, 1080))

# # # # # #     # Save the resulting image
# # # # # #     output_directory = "static/output"
# # # # # #     output_file_path = os.path.join(output_directory, f"out{index}.png")
# # # # # #     cv2.imwrite(output_file_path, resized_result)


# # # # # # # Start the server
# # # # # # if __name__ == "__main__":
# # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)
# # # # # import os
# # # # # import cv2
# # # # # import numpy as np
# # # # # from typing import List
# # # # # from fastapi import FastAPI, UploadFile, File
# # # # # from fastapi.staticfiles import StaticFiles
# # # # # from fastapi.responses import StreamingResponse, FileResponse
# # # # # import uvicorn

# # # # # app = FastAPI()

# # # # # # Define the upload endpoint
# # # # # @app.post("/upload")
# # # # # async def upload(files: List[UploadFile] = File(...)):
# # # # #     output_directory = "static/output"
# # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # #     for i, file in enumerate(files):
# # # # #         # Save the uploaded file temporarily
# # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # #         with open(temp_path, "wb") as f:
# # # # #             f.write(await file.read())

# # # # #         # Process the image
# # # # #         process_image(temp_path, i)

# # # # #     # Get a list of processed image file paths
# # # # #     processed_images = []
# # # # #     for filename in os.listdir(output_directory):
# # # # #         if filename.startswith("out") and filename.endswith(".png"):
# # # # #             processed_images.append(filename)

# # # # #     return {"message": "Images processed successfully", "processed_images": processed_images}


# # # # # # Serve the static files
# # # # # app.mount("/static", StaticFiles(directory="static"), name="static")


# # # # # # Define the endpoint to view the output image
# # # # # @app.get("/output/{index}")
# # # # # async def view_output_image(index: int):
# # # # #     output_file_path = f"static/output/output_{index}.png"
# # # # #     return FileResponse(output_file_path)


# # # # # # Define the endpoint to get all the image previews
# # # # # @app.get("/img")
# # # # # async def get_image_previews():
# # # # #     previews = []

# # # # #     output_directory = "static/output"
# # # # #     for filename in os.listdir(output_directory):
# # # # #         if filename.startswith("output_") and filename.endswith(".png"):
# # # # #             output_file_path = os.path.join(output_directory, filename)
# # # # #             previews.append(output_file_path)

# # # # #     def stream():
# # # # #         for preview_path in previews:
# # # # #             with open(preview_path, "rb") as f:
# # # # #                 yield f.read()

# # # # #     return StreamingResponse(stream(), media_type="image/png")


# # # # # # Utility function to process the image
# # # # # def process_image(temp_path, index):
# # # # #     # Read the image using OpenCV
# # # # #     img = cv2.imread(temp_path)

# # # # #     # Convert image to RGB format
# # # # #     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# # # # #     # Create a mask with white background
# # # # #     mask = np.zeros(img.shape[:2], np.uint8)

# # # # #     # Define the background and foreground models
# # # # #     bgd_model = np.zeros((1, 65), np.float64)
# # # # #     fgd_model = np.zeros((1, 65), np.float64)

# # # # #     # Define the bounding rectangle for the foreground object
# # # # #     rect = (1, 1, img.shape[1] - 1, img.shape[0] - 1)

# # # # #     # Apply GrabCut algorithm to extract foreground
# # # # #     cv2.grabCut(img_rgb, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)

# # # # #     # Create a mask with only the foreground region
# # # # #     mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

# # # # #     # Apply the mask to the original image
# # # # #     result = img * mask[:, :, np.newaxis]

# # # # #     # Resize the image to 1080x1080
# # # # #     resized_result = cv2.resize(result, (1080, 1080))

# # # # #     # Save the resulting image
# # # # #     output_directory = "static/output"
# # # # #     output_file_path = os.path.join(output_directory, f"out{index}.png")
# # # # #     cv2.imwrite(output_file_path, resized_result)


# # # # # # Define the endpoint to convert uploaded image into cartoon
# # # # # @app.post("/uploadcartoon")
# # # # # async def upload_cartoon(file: UploadFile = File(...)):
# # # # #     # Save the uploaded file temporarily
# # # # #     temp_path = "static/temp/cartoon_input.png"
# # # # #     with open(temp_path, "wb") as f:
# # # # #         f.write(await file.read())

# # # # #     # Process the image to convert it into cartoon style
# # # # #     cartoon_image = convert_to_cartoon(temp_path)

# # # # #     # Save the cartoon image
# # # # #     output_directory = "static/output"
# # # # #     os.makedirs(output_directory, exist_ok=True)
# # # # #     output_file_path = os.path.join(output_directory, "cartoon_output.png")
# # # # #     cv2.imwrite(output_file_path, cartoon_image)

# # # # #     return {"message": "Image converted to cartoon successfully", "cartoon_image": "cartoon_output.png"}


# # # # # # Utility function to convert an image into cartoon style
# # # # # def convert_to_cartoon(image_path):
# # # # #     # Read the image using OpenCV
# # # # #     img = cv2.imread(image_path)

# # # # #     # Convert the image to grayscale
# # # # #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # # # #     # Apply a median blur to reduce noise
# # # # #     blurred = cv2.medianBlur(gray, 5)

# # # # #     # Apply adaptive thresholding to get a binary image
# # # # #     threshold = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

# # # # #     # Create a bilateral filter for stylizing the image
# # # # #     cartoon = cv2.bilateralFilter(img, 9, 300, 300)

# # # # #     # Combine the thresholded image with the stylized image
# # # # #     cartoon = cv2.bitwise_and(cartoon, cartoon, mask=threshold)

# # # # #     return cartoon


# # # # # # Start the server
# # # # # if __name__ == "__main__":
# # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)

# # # # import os
# # # # import cv2
# # # # import numpy as np
# # # # from typing import List
# # # # from fastapi import FastAPI, UploadFile, File
# # # # from fastapi.staticfiles import StaticFiles
# # # # from fastapi.responses import StreamingResponse, FileResponse
# # # # import uvicorn

# # # # app = FastAPI()

# # # # # Define the upload endpoint
# # # # @app.post("/upload")
# # # # async def upload(files: List[UploadFile] = File(...)):
# # # #     output_directory = "static/output"
# # # #     os.makedirs(output_directory, exist_ok=True)

# # # #     for i, file in enumerate(files):
# # # #         # Save the uploaded file temporarily
# # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # #         with open(temp_path, "wb") as f:
# # # #             f.write(await file.read())

# # # #         # Process the image
# # # #         process_image(temp_path, i)

# # # #     # Get a list of processed image file paths
# # # #     processed_images = []
# # # #     for filename in os.listdir(output_directory):
# # # #         if filename.startswith("out") and filename.endswith(".png"):
# # # #             processed_images.append(filename)

# # # #     return {"message": "Images processed successfully", "processed_images": processed_images}


# # # # # Define the uploadcartoon endpoint
# # # # @app.post("/uploadcartoon")
# # # # async def upload_cartoon(files: List[UploadFile] = File(...)):
# # # #     output_directory = "static/cartoon"
# # # #     os.makedirs(output_directory, exist_ok=True)

# # # #     for i, file in enumerate(files):
# # # #         # Save the uploaded file temporarily
# # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # #         with open(temp_path, "wb") as f:
# # # #             f.write(await file.read())

# # # #         # Process the image
# # # #         convert_to_cartoon(temp_path, i)

# # # #     # Get a list of processed cartoon image file paths
# # # #     processed_cartoons = []
# # # #     for filename in os.listdir(output_directory):
# # # #         if filename.startswith("cartoon") and filename.endswith(".png"):
# # # #             processed_cartoons.append(filename)

# # # #     return {"message": "Images converted to cartoons successfully", "processed_cartoons": processed_cartoons}


# # # # # Serve the static files
# # # # app.mount("/static", StaticFiles(directory="static"), name="static")


# # # # # Define the endpoint to view the output image
# # # # @app.get("/output/{index}")
# # # # async def view_output_image(index: int):
# # # #     output_file_path = f"static/output/output_{index}.png"
# # # #     return FileResponse(output_file_path)


# # # # # Define the endpoint to view the cartoon image
# # # # @app.get("/cartoon/{index}")
# # # # async def view_cartoon_image(index: int):
# # # #     cartoon_file_path = f"static/cartoon/cartoon_{index}.png"
# # # #     return FileResponse(cartoon_file_path)


# # # # # Define the endpoint to get all the image previews
# # # # @app.get("/img")
# # # # async def get_image_previews():
# # # #     previews = []

# # # #     output_directory = "static/output"
# # # #     for filename in os.listdir(output_directory):
# # # #         if filename.startswith("output_") and filename.endswith(".png"):
# # # #             output_file_path = os.path.join(output_directory, filename)
# # # #             previews.append(output_file_path)

# # # #     def stream():
# # # #         for preview_path in previews:
# # # #             with open(preview_path, "rb") as f:
# # # #                 yield f.read()

# # # #     return StreamingResponse(stream(), media_type="image/png")


# # # # # Utility function to process the image
# # # # def process_image(temp_path, index):
# # # #     # Read the image using OpenCV
# # # #     img = cv2.imread(temp_path)

# # # #     # Convert image to RGB format
# # # #     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# # # #     # Create a mask with white background
# # # #     mask = np.zeros(img.shape[:2], np.uint8)

# # # #     # Define the background and foreground models
# # # #     bgd_model = np.zeros((1, 65), np.float64)
# # # #     fgd_model = np.zeros((1, 65), np.float64)

# # # #     # Define the bounding rectangle for the foreground object
# # # #     rect = (1, 1, img.shape[1] - 1, img.shape[0] - 1)

# # # #     # Apply GrabCut algorithm to extract foreground
# # # #     cv2.grabCut(img_rgb, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)

# # # #     # Create a mask with only the foreground region
# # # #     mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

# # # #     # Apply the mask to the original image
# # # #     result = img * mask[:, :, np.newaxis]

# # # #     # Resize the image to 1080x1080
# # # #     resized_result = cv2.resize(result, (1080, 1080))

# # # #     # Save the resulting image
# # # #     output_directory = "static/output"
# # # #     output_file_path = os.path.join(output_directory, f"out{index}.png")
# # # #     cv2.imwrite(output_file_path, resized_result)


# # # # # Utility function to convert image to cartoon
# # # # def convert_to_cartoon(temp_path, index):
# # # #     # Read the image using OpenCV
# # # #     img = cv2.imread(temp_path)

# # # #     # Convert image to RGB format
# # # #     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# # # #     # Convert image to grayscale
# # # #     gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

# # # #     # Apply median blur to reduce noise
# # # #     gray = cv2.medianBlur(gray, 5)

# # # #     # Create an edge mask using adaptive thresholding
# # # #     thresholded = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

# # # #     # Apply bilateral filter to smooth colors while preserving edges
# # # #     filtered = cv2.bilateralFilter(img_rgb, 9, 250, 250)

# # # #     # Create a cartoon effect by combining filtered colors with the edge mask
# # # #     cartoon = cv2.bitwise_and(filtered, filtered, mask=thresholded)

# # # #     # Save the resulting cartoon image
# # # #     output_directory = "static/cartoon"
# # # #     output_file_path = os.path.join(output_directory, f"cartoon{index}.png")
# # # #     cv2.imwrite(output_file_path, cartoon)


# # # # # Start the server
# # # # if __name__ == "__main__":
# # # #     uvicorn.run(app, host="0.0.0.0", port=12000)
# # # import os
# # # import cv2
# # # import numpy as np
# # # from typing import List
# # # from fastapi import FastAPI, UploadFile, File
# # # from fastapi.staticfiles import StaticFiles
# # # from fastapi.responses import StreamingResponse, FileResponse
# # # import uvicorn
# # # from sklearn.cluster import KMeans

# # # app = FastAPI()

# # # # Define the upload endpoint
# # # @app.post("/upload")
# # # async def upload(files: List[UploadFile] = File(...)):
# # #     output_directory = "static/output"
# # #     os.makedirs(output_directory, exist_ok=True)

# # #     for i, file in enumerate(files):
# # #         # Save the uploaded file temporarily
# # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # #         with open(temp_path, "wb") as f:
# # #             f.write(await file.read())

# # #         # Process the image
# # #         process_image(temp_path, i)

# # #     # Get a list of processed image file paths
# # #     processed_images = []
# # #     for filename in os.listdir(output_directory):
# # #         if filename.startswith("out") and filename.endswith(".png"):
# # #             processed_images.append(filename)

# # #     return {"message": "Images processed successfully", "processed_images": processed_images}


# # # # Define the uploadcartoon endpoint
# # # @app.post("/uploadcartoon")
# # # async def upload_cartoon(files: List[UploadFile] = File(...)):
# # #     output_directory = "static/cartoon"
# # #     os.makedirs(output_directory, exist_ok=True)

# # #     for i, file in enumerate(files):
# # #         # Save the uploaded file temporarily
# # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # #         with open(temp_path, "wb") as f:
# # #             f.write(await file.read())

# # #         # Process the image
# # #         convert_to_cartoon(temp_path, i)

# # #     # Get a list of processed cartoon image file paths
# # #     processed_cartoons = []
# # #     for filename in os.listdir(output_directory):
# # #         if filename.startswith("cartoon") and filename.endswith(".png"):
# # #             processed_cartoons.append(filename)

# # #     return {"message": "Images converted to cartoons successfully", "processed_cartoons": processed_cartoons}


# # # # Serve the static files
# # # app.mount("/static", StaticFiles(directory="static"), name="static")


# # # # Define the endpoint to view the output image
# # # @app.get("/output/{index}")
# # # async def view_output_image(index: int):
# # #     output_file_path = f"static/output/output_{index}.png"
# # #     return FileResponse(output_file_path)


# # # # Define the endpoint to view the cartoon image
# # # @app.get("/cartoon/{index}")
# # # async def view_cartoon_image(index: int):
# # #     cartoon_file_path = f"static/cartoon/cartoon_{index}.png"
# # #     return FileResponse(cartoon_file_path)


# # # # Define the endpoint to get all the image previews
# # # @app.get("/img")
# # # async def get_image_previews():
# # #     previews = []

# # #     output_directory = "static/output"
# # #     for filename in os.listdir(output_directory):
# # #         if filename.startswith("output_") and filename.endswith(".png"):
# # #             output_file_path = os.path.join(output_directory, filename)
# # #             previews.append(output_file_path)

# # #     def stream():
# # #         for preview_path in previews:
# # #             with open(preview_path, "rb") as f:
# # #                 yield f.read()

# # #     return StreamingResponse(stream(), media_type="image/png")


# # # # Utility function to process the image
# # # def process_image(temp_path, index):
# # #     # Read the image using OpenCV
# # #     img = cv2.imread(temp_path)

# # #     # Convert image to RGB format
# # #     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# # #     # Create a mask with white background
# # #     mask = np.zeros(img.shape[:2], np.uint8)

# # #     # Define the background and foreground models
# # #     bgd_model = np.zeros((1, 65), np.float64)
# # #     fgd_model = np.zeros((1, 65), np.float64)

# # #     # Define the bounding rectangle for the foreground object
# # #     rect = (1, 1, img.shape[1] - 1, img.shape[0] - 1)

# # #     # Apply GrabCut algorithm to extract foreground
# # #     cv2.grabCut(img_rgb, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)

# # #     # Create a mask with only the foreground region
# # #     mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

# # #     # Apply the mask to the original image
# # #     result = img * mask[:, :, np.newaxis]

# # #     # Resize the image to 1080x1080
# # #     resized_result = cv2.resize(result, (1080, 1080))

# # #     # Save the resulting image
# # #     output_directory = "static/output"
# # #     output_file_path = os.path.join(output_directory, f"output_{index}.png")
# # #     cv2.imwrite(output_file_path, resized_result)


# # # # Utility function to convert image to cartoon
# # # def convert_to_cartoon(temp_path, index):
# # #     # Read the image using OpenCV
# # #     img = cv2.imread(temp_path)
# # #     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# # #     # Edge mask generation
# # #     line_size = 7
# # #     blur_value = 7
# # #     gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
# # #     gray_blur = cv2.medianBlur(gray_img, blur_value)
# # #     edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)

# # #     # Color quantization with KMeans clustering
# # #     k = 7
# # #     data = img.reshape(-1, 3)
# # #     kmeans = KMeans(n_clusters=k, random_state=42).fit(data)
# # #     img_reduced = kmeans.cluster_centers_[kmeans.labels_]
# # #     img_reduced = img_reduced.reshape(img.shape)
# # #     img_reduced = img_reduced.astype(np.uint8)

# # #     # Bilateral Filter
# # #     blurred = cv2.bilateralFilter(img_reduced, d=7, sigmaColor=200, sigmaSpace=200)
# # #     cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)

# # #     # Save the resulting cartoon image
# # #     output_directory = "static/cartoon"
# # #     output_file_path = os.path.join(output_directory, f"cartoon_{index}.png")
# # #     cv2.imwrite(output_file_path, cartoon)


# # # # Start the server
# # # if __name__ == "__main__":
# # #     uvicorn.run(app, host="0.0.0.0", port=12000)
# # import os
# # import cv2
# # import numpy as np
# # from typing import List
# # from fastapi import FastAPI, UploadFile, File
# # from fastapi.staticfiles import StaticFiles
# # from fastapi.responses import StreamingResponse, FileResponse
# # import uvicorn
# # from sklearn.cluster import KMeans

# # app = FastAPI()

# # # Define the upload endpoint
# # @app.post("/upload")
# # async def upload(files: List[UploadFile] = File(...)):
# #     output_directory = "static/output"
# #     os.makedirs(output_directory, exist_ok=True)

# #     for i, file in enumerate(files):
# #         # Save the uploaded file temporarily
# #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# #         with open(temp_path, "wb") as f:
# #             f.write(await file.read())

# #         # Process the image
# #         process_image(temp_path, i)

# #     # Get a list of processed image file paths
# #     processed_images = []
# #     for filename in os.listdir(output_directory):
# #         if filename.startswith("out") and filename.endswith(".png"):
# #             processed_images.append(filename)

# #     return {"message": "Images processed successfully", "processed_images": processed_images}


# # # Define the uploadcartoon endpoint
# # @app.post("/uploadcartoon")
# # async def upload_cartoon(files: List[UploadFile] = File(...)):
# #     output_directory = "static/cartoon"
# #     os.makedirs(output_directory, exist_ok=True)

# #     for i, file in enumerate(files):
# #         # Save the uploaded file temporarily
# #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# #         with open(temp_path, "wb") as f:
# #             f.write(await file.read())

# #         # Process the image
# #         convert_to_cartoon(temp_path, i)

# #     # Get a list of processed cartoon image file paths
# #     processed_cartoons = []
# #     for filename in os.listdir(output_directory):
# #         if filename.startswith("cartoon") and filename.endswith(".png"):
# #             processed_cartoons.append(filename)

# #     return {"message": "Images converted to cartoons successfully", "processed_cartoons": processed_cartoons}


# # # Serve the static files
# # app.mount("/static", StaticFiles(directory="static"), name="static")


# # # Define the endpoint to view the output image
# # @app.get("/output/{index}")
# # async def view_output_image(index: int):
# #     output_file_path = f"static/output/output_{index}.png"
# #     return FileResponse(output_file_path)


# # # Define the endpoint to view the cartoon image
# # @app.get("/cartoon/{index}")
# # async def view_cartoon_image(index: int):
# #     cartoon_file_path = f"static/cartoon/cartoon_{index}.png"
# #     return FileResponse(cartoon_file_path)


# # # Define the endpoint to get all the image previews
# # @app.get("/img")
# # async def get_image_previews():
# #     previews = []

# #     output_directory = "static/output"
# #     for filename in os.listdir(output_directory):
# #         if filename.startswith("output_") and filename.endswith(".png"):
# #             output_file_path = os.path.join(output_directory, filename)
# #             previews.append(output_file_path)

# #     def stream():
# #         for preview_path in previews:
# #             with open(preview_path, "rb") as f:
# #                 yield f.read()

# #     return StreamingResponse(stream(), media_type="image/png")


# # # Utility function to process the image
# # def process_image(temp_path, index):
# #     # Read the image using OpenCV
# #     img = cv2.imread(temp_path)

# #     # Convert image to RGB format
# #     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# #     # Create a mask with white background
# #     mask = np.zeros(img.shape[:2], np.uint8)

# #     # Define the background and foreground models
# #     bgd_model = np.zeros((1, 65), np.float64)
# #     fgd_model = np.zeros((1, 65), np.float64)

# #     # Define the bounding rectangle for the foreground object
# #     rect = (1, 1, img.shape[1] - 1, img.shape[0] - 1)

# #     # Apply GrabCut algorithm to extract foreground
# #     cv2.grabCut(img_rgb, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)

# #     # Create a mask with only the foreground region
# #     mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

# #     # Apply the mask to the original image
# #     result = img * mask[:, :, np.newaxis]

# #     # Resize the image to 1080x1080
# #     resized_result = cv2.resize(result, (1080, 1080))

# #     # Save the resulting image
# #     output_directory = "static/output"
# #     output_file_path = os.path.join(output_directory, f"out{index}.png")
# #     cv2.imwrite(output_file_path, resized_result)


# # # Utility function to convert image to cartoon
# # def convert_to_cartoon(temp_path, index):
# #     # Read the image using OpenCV
# #     img = cv2.imread(temp_path)
# #     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# #     # Edge mask generation
# #     line_size = 7
# #     blur_value = 7
# #     gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
# #     gray_blur = cv2.medianBlur(gray_img, blur_value)
# #     edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)

# #     # Color quantization with KMeans clustering
# #     k = 7
# #     data = img.reshape(-1, 3)
# #     kmeans = KMeans(n_clusters=k, random_state=42).fit(data)
# #     img_reduced = kmeans.cluster_centers_[kmeans.labels_]
# #     img_reduced = img_reduced.reshape(img.shape)
# #     img_reduced = img_reduced.astype(np.uint8)

# #     # Bilateral Filter
# #     blurred = cv2.bilateralFilter(img_reduced, d=7, sigmaColor=200, sigmaSpace=200)
# #     cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)

# #     # Save the resulting cartoon image
# #     output_directory = "static/cartoon"
# #     output_file_path = os.path.join(output_directory, f"cartoon{index}.png")
# #     cv2.imwrite(output_file_path, cartoon)


# # # Start the server
# # if __name__ == "__main__":
# #     uvicorn.run(app, host="0.0.0.0", port=12000)
# import os
# import cv2
# import numpy as np
# from typing import List
# from fastapi import FastAPI, UploadFile, File
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import StreamingResponse, FileResponse
# import uvicorn
# from sklearn.cluster import KMeans

# app = FastAPI()

# # Define the upload endpoint
# @app.post("/upload")
# async def upload(files: List[UploadFile] = File(...)):
#     output_directory = "static/output"
#     os.makedirs(output_directory, exist_ok=True)

#     for i, file in enumerate(files):
#         # Save the uploaded file temporarily
#         temp_path = os.path.join(output_directory, f"temp_{i}.png")
#         with open(temp_path, "wb") as f:
#             f.write(await file.read())

#         # Process the image
#         process_image(temp_path, i)

#     # Get a list of processed image file paths
#     processed_images = []
#     for filename in os.listdir(output_directory):
#         if filename.startswith("out") and filename.endswith(".png"):
#             processed_images.append(filename)

#     return {"message": "Images processed successfully", "processed_images": processed_images}


# # Define the uploadcartoon endpoint
# @app.post("/uploadcartoon")
# async def upload_cartoon(files: List[UploadFile] = File(...)):
#     output_directory = "static/cartoon"
#     os.makedirs(output_directory, exist_ok=True)

#     for i, file in enumerate(files):
#         # Save the uploaded file temporarily
#         temp_path = os.path.join(output_directory, f"temp_{i}.png")
#         with open(temp_path, "wb") as f:
#             f.write(await file.read())

#         # Process the image
#         convert_to_cartoon(temp_path, i)

#     # Get a list of processed cartoon image file paths
#     processed_cartoons = []
#     for filename in os.listdir(output_directory):
#         if filename.startswith("cartoon") and filename.endswith(".png"):
#             processed_cartoons.append(filename)

#     return {"message": "Images converted to cartoons successfully", "processed_cartoons": processed_cartoons}


# # Serve the static files
# app.mount("/static", StaticFiles(directory="static"), name="static")


# # Define the endpoint to view the output image
# @app.get("/output/{index}")
# async def view_output_image(index: int):
#     output_file_path = f"static/output/output_{index}.png"
#     return FileResponse(output_file_path)


# # Define the endpoint to view the cartoon image
# @app.get("/cartoon/{index}")
# async def view_cartoon_image(index: int):
#     cartoon_file_path = f"static/cartoon/cartoon_{index}.png"
#     return FileResponse(cartoon_file_path)


# # Define the endpoint to get all the image previews
# @app.get("/img")
# async def get_image_previews():
#     previews = []

#     output_directory = "static/output"
#     for filename in os.listdir(output_directory):
#         if filename.startswith("output_") and filename.endswith(".png"):
#             output_file_path = os.path.join(output_directory, filename)
#             previews.append(output_file_path)

#     def stream():
#         for preview_path in previews:
#             with open(preview_path, "rb") as f:
#                 yield f.read()

#     return StreamingResponse(stream(), media_type="image/png")


# # Utility function to process the image
# def process_image(temp_path, index):
#     # Read the image using OpenCV
#     img = cv2.imread(temp_path)

#     # Convert image to RGB format
#     img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#     # Create a mask with white background
#     mask = np.zeros(img.shape[:2], np.uint8)

#     # Define the background and foreground models
#     bgd_model = np.zeros((1, 65), np.float64)
#     fgd_model = np.zeros((1, 65), np.float64)

#     # Define the bounding rectangle for the foreground object
#     rect = (1, 1, img.shape[1] - 1, img.shape[0] - 1)

#     # Apply GrabCut algorithm to extract foreground
#     cv2.grabCut(img_rgb, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)

#     # Create a mask with only the foreground region
#     mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

#     # Apply the mask to the original image
#     result = img * mask[:, :, np.newaxis]

#     # Resize the image to 1080x1080
#     resized_result = cv2.resize(result, (1080, 1080))

#     # Save the resulting image
#     output_directory = "static/output"
#     output_file_path = os.path.join(output_directory, f"out{index}.png")
#     cv2.imwrite(output_file_path, resized_result)


# # Utility function to convert image to cartoon
# def convert_to_cartoon(temp_path, index):
#     # Read the image using OpenCV
#     img = cv2.imread(temp_path)
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#     # Convert image to grayscale
#     gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

#     # Generate edge mask
#     line_size = 7
#     blur_value = 7
#     gray_blur = cv2.medianBlur(gray_img, blur_value)
#     edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)

#     # Color quantization with KMeans clustering
#     k = 7
#     data = img.reshape(-1, 3)
#     kmeans = KMeans(n_clusters=k, random_state=42).fit(data)
#     img_reduced = kmeans.cluster_centers_[kmeans.labels_]
#     img_reduced = img_reduced.reshape(img.shape)
#     img_reduced = img_reduced.astype(np.uint8)

#     # Apply bilateral filter
#     d = 7
#     sigma_color = 200
#     sigma_space = 200
#     blurred = cv2.bilateralFilter(img_reduced, d=d, sigmaColor=sigma_color, sigmaSpace=sigma_space)

#     # Apply the edge mask to the blurred image
#     cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)

#     # Save the resulting cartoon image
#     output_directory = "static/cartoon"
#     output_file_path = os.path.join(output_directory, f"cartoon{index}.png")
#     cv2.imwrite(output_file_path, cartoon)


# # Start the server
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=12000)
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
