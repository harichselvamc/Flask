# # # # # # # # # # import os
# # # # # # # # # # import cv2
# # # # # # # # # # import numpy as np
# # # # # # # # # # from typing import List
# # # # # # # # # # from fastapi import FastAPI, UploadFile, Request, File
# # # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # # from fastapi.responses import HTMLResponse, FileResponse
# # # # # # # # # # from fastapi.templating import Jinja2Templates
# # # # # # # # # # import uvicorn
# # # # # # # # # # from rembg import remove

# # # # # # # # # # app = FastAPI()
# # # # # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")
# # # # # # # # # # templates = Jinja2Templates(directory="templates")

# # # # # # # # # # def create_static_folder():
# # # # # # # # # #     base_directory = os.getcwd()
# # # # # # # # # #     static_directory = os.path.join(base_directory, "static")
# # # # # # # # # #     overlayed_images_directory = os.path.join(static_directory, "overlayed_images")

# # # # # # # # # #     print("Base Directory:", base_directory)
# # # # # # # # # #     print("Static Directory:", static_directory)
# # # # # # # # # #     print("Overlayed Images Directory:", overlayed_images_directory)

# # # # # # # # # #     if not os.path.exists(static_directory):
# # # # # # # # # #         os.makedirs(static_directory)
# # # # # # # # # #         print("Static Directory Created.")

# # # # # # # # # #     if not os.path.exists(overlayed_images_directory):
# # # # # # # # # #         os.makedirs(overlayed_images_directory)
# # # # # # # # # #         print("Overlayed Images Directory Created.")


# # # # # # # # # # def get_next_file_number():
# # # # # # # # # #     overlayed_images = os.listdir("static/overlayed_images")
# # # # # # # # # #     file_numbers = [
# # # # # # # # # #         int(file.split("_")[1].split(".")[0])
# # # # # # # # # #         for file in overlayed_images
# # # # # # # # # #         if file.startswith("output_")
# # # # # # # # # #     ]
# # # # # # # # # #     if file_numbers:
# # # # # # # # # #         return max(file_numbers) + 1
# # # # # # # # # #     else:
# # # # # # # # # #         return 0


# # # # # # # # # # @app.get("/", response_class=HTMLResponse)
# # # # # # # # # # async def home(request: Request):
# # # # # # # # # #     return templates.TemplateResponse("home.html", {"request": request})


# # # # # # # # # # @app.post("/upload")
# # # # # # # # # # async def upload(files: List[UploadFile] = File(...), text: str = None):
# # # # # # # # # #     output_directory = "static/overlayed_images"
# # # # # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # # # # #     download_urls = []
# # # # # # # # # #     instructions = []

# # # # # # # # # #     next_file_number = get_next_file_number()

# # # # # # # # # #     for i, file in enumerate(files):
     
# # # # # # # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # # # # # #         with open(temp_path, "wb") as f:
# # # # # # # # # #             f.write(await file.read())

      
# # # # # # # # # #         with open(temp_path, "rb") as image_file:
# # # # # # # # # #             image_data = image_file.read()
# # # # # # # # # #             output_data = remove(image_data)

# # # # # # # # # #         image_array = np.frombuffer(output_data, np.uint8)

# # # # # # # # # #         image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

# # # # # # # # # #         image = cv2.resize(image, (1080, 1080))

       
# # # # # # # # # #         file_name = file.filename
# # # # # # # # # #         file_name_without_extension, file_extension = os.path.splitext(file_name)

# # # # # # # # # #         if text:
# # # # # # # # # #             overlay_text = text
# # # # # # # # # #         else:
# # # # # # # # # #             overlay_text = f"{file_name_without_extension}{file_extension}"

# # # # # # # # # #         font = cv2.FONT_HERSHEY_SIMPLEX
# # # # # # # # # #         font_scale = 2
# # # # # # # # # #         font_thickness = 5
# # # # # # # # # #         text_color = (0, 0, 238)

# # # # # # # # # #         (text_width, text_height), _ = cv2.getTextSize(
# # # # # # # # # #             overlay_text, font, font_scale, font_thickness
# # # # # # # # # #         )

# # # # # # # # # #         x = int((image.shape[1] - text_width) / 2)  
# # # # # # # # # #         y = image.shape[0] - int(text_height) - 30  

# # # # # # # # # #         cv2.putText(
# # # # # # # # # #             image, overlay_text, (x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA
# # # # # # # # # #         )

     
# # # # # # # # # #         output_file_path = os.path.join(output_directory, f"output_{next_file_number}.png")
# # # # # # # # # #         cv2.imwrite(output_file_path, image)

# # # # # # # # # #         download_url = f"/static/overlayed_images/output_{next_file_number}.png"
# # # # # # # # # #         download_urls.append(download_url)

# # # # # # # # # #         instruction = f"Image {file_name} processed. Download: {download_url}"
# # # # # # # # # #         instructions.append(instruction)

# # # # # # # # # #         next_file_number += 1

# # # # # # # # # #     return {"download_urls": download_urls, "instructions": instructions}



# # # # # # # # # # create_static_folder()


# # # # # # # # # # @app.get("/download/{filename}")
# # # # # # # # # # async def download(filename: str):

# # # # # # # # # #     file_path = os.path.join("static", "overlayed_images", filename)

# # # # # # # # # #     if os.path.isfile(file_path):
    
# # # # # # # # # #         return FileResponse(file_path)

# # # # # # # # # #     return {"detail": "File not found"}


# # # # # # # # # # @app.get("/data")
# # # # # # # # # # async def get_data():
# # # # # # # # # #     overlayed_images = os.listdir("static/overlayed_images")
# # # # # # # # # #     return {"overlayed_images": overlayed_images}


# # # # # # # # # # @app.get("/url")
# # # # # # # # # # async def get_shareable_link(request: Request):
# # # # # # # # # #     base_url = request.base_url
# # # # # # # # # #     return {"shareable_link": base_url}


# # # # # # # # # # @app.get("/images")
# # # # # # # # # # async def get_images():
# # # # # # # # # #     overlayed_images = os.listdir("static/overlayed_images")
# # # # # # # # # #     image_urls = [
# # # # # # # # # #         f"http://localhost:12000/static/overlayed_images/{image}" for image in overlayed_images
# # # # # # # # # #     ]
# # # # # # # # # #     return {"image_urls": image_urls}


# # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)

# # # # # # # # # import os
# # # # # # # # # import cv2
# # # # # # # # # import numpy as np
# # # # # # # # # from typing import List
# # # # # # # # # from fastapi import FastAPI, UploadFile, Request, File
# # # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # # from fastapi.responses import HTMLResponse, FileResponse
# # # # # # # # # from fastapi.templating import Jinja2Templates
# # # # # # # # # import uvicorn
# # # # # # # # # from rembg import remove

# # # # # # # # # app = FastAPI()
# # # # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")
# # # # # # # # # templates = Jinja2Templates(directory="templates")

# # # # # # # # # def create_static_folder():
# # # # # # # # #     base_directory = os.getcwd()
# # # # # # # # #     static_directory = os.path.join(base_directory, "static")
# # # # # # # # #     overlayed_images_directory = os.path.join(static_directory, "overlayed_images")

# # # # # # # # #     print("Base Directory:", base_directory)
# # # # # # # # #     print("Static Directory:", static_directory)
# # # # # # # # #     print("Overlayed Images Directory:", overlayed_images_directory)

# # # # # # # # #     if not os.path.exists(static_directory):
# # # # # # # # #         os.makedirs(static_directory)
# # # # # # # # #         print("Static Directory Created.")

# # # # # # # # #     if not os.path.exists(overlayed_images_directory):
# # # # # # # # #         os.makedirs(overlayed_images_directory)
# # # # # # # # #         print("Overlayed Images Directory Created.")

# # # # # # # # # def create_home_html():
# # # # # # # # #     templates_directory = os.path.join(os.getcwd(), "templates")
# # # # # # # # #     home_html_path = os.path.join(templates_directory, "home.html")

# # # # # # # # #     if not os.path.exists(home_html_path):
# # # # # # # # #         with open(home_html_path, "w") as f:
# # # # # # # # #             f.write(
# # # # # # # # #                 """
# # # # # # # # #                 <html>
# # # # # # # # #                 <head>
# # # # # # # # #                     <title>Upload Images</title>
# # # # # # # # #                 </head>
# # # # # # # # #                 <body>
# # # # # # # # #                     <h1>Upload Images</h1>
# # # # # # # # #                     <form action="/upload" enctype="multipart/form-data" method="post">
# # # # # # # # #                         <input name="files" type="file" multiple>
# # # # # # # # #                         <input type="text" name="text" placeholder="Overlay Text">
# # # # # # # # #                         <input type="submit">
# # # # # # # # #                     </form>
# # # # # # # # #                 </body>
# # # # # # # # #                 </html>
# # # # # # # # #                 """
# # # # # # # # #             )
# # # # # # # # #         print("home.html created.")

# # # # # # # # # @app.get("/", response_class=HTMLResponse)
# # # # # # # # # async def home(request: Request):
# # # # # # # # #     return templates.TemplateResponse("home.html", {"request": request})

# # # # # # # # # @app.post("/upload")
# # # # # # # # # async def upload(files: List[UploadFile] = File(...), text: str = None):
# # # # # # # # #     output_directory = "static/overlayed_images"
# # # # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # # # #     download_urls = []
# # # # # # # # #     instructions = []

# # # # # # # # #     next_file_number = get_next_file_number()

# # # # # # # # #     for i, file in enumerate(files):
# # # # # # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # # # # #         with open(temp_path, "wb") as f:
# # # # # # # # #             f.write(await file.read())

# # # # # # # # #         with open(temp_path, "rb") as image_file:
# # # # # # # # #             image_data = image_file.read()
# # # # # # # # #             output_data = remove(image_data)

# # # # # # # # #         image_array = np.frombuffer(output_data, np.uint8)

# # # # # # # # #         image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

# # # # # # # # #         image = cv2.resize(image, (1080, 1080))

# # # # # # # # #         file_name = file.filename
# # # # # # # # #         file_name_without_extension, file_extension = os.path.splitext(file_name)

# # # # # # # # #         if text:
# # # # # # # # #             overlay_text = text
# # # # # # # # #         else:
# # # # # # # # #             overlay_text = f"{file_name_without_extension}{file_extension}"

# # # # # # # # #         font = cv2.FONT_HERSHEY_SIMPLEX
# # # # # # # # #         font_scale = 2
# # # # # # # # #         font_thickness = 5
# # # # # # # # #         text_color = (0, 0, 238)

# # # # # # # # #         (text_width, text_height), _ = cv2.getTextSize(
# # # # # # # # #             overlay_text, font, font_scale, font_thickness
# # # # # # # # #         )

# # # # # # # # #         x = int((image.shape[1] - text_width) / 2)
# # # # # # # # #         y = image.shape[0] - int(text_height) - 30

# # # # # # # # #         cv2.putText(
# # # # # # # # #             image, overlay_text, (x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA
# # # # # # # # #         )

# # # # # # # # #         output_file_path = os.path.join(output_directory, f"output_{next_file_number}.png")
# # # # # # # # #         cv2.imwrite(output_file_path, image)

# # # # # # # # #         download_url = f"/static/overlayed_images/output_{next_file_number}.png"
# # # # # # # # #         download_urls.append(download_url)

# # # # # # # # #         instruction = f"Image {file_name} processed. Download: {download_url}"
# # # # # # # # #         instructions.append(instruction)

# # # # # # # # #         next_file_number += 1

# # # # # # # # #     return {"download_urls": download_urls, "instructions": instructions}

# # # # # # # # # def get_next_file_number():
# # # # # # # # #     overlayed_images = os.listdir("static/overlayed_images")
# # # # # # # # #     file_numbers = [
# # # # # # # # #         int(file.split("_")[1].split(".")[0])
# # # # # # # # #         for file in overlayed_images
# # # # # # # # #         if file.startswith("output_")
# # # # # # # # #     ]
# # # # # # # # #     if file_numbers:
# # # # # # # # #         return max(file_numbers) + 1
# # # # # # # # #     else:
# # # # # # # # #         return 0

# # # # # # # # # create_static_folder()
# # # # # # # # # create_home_html()

# # # # # # # # # @app.get("/download/{filename}")
# # # # # # # # # async def download(filename: str):
# # # # # # # # #     file_path = os.path.join("static", "overlayed_images", filename)

# # # # # # # # #     if os.path.isfile(file_path):
# # # # # # # # #         return FileResponse(file_path)

# # # # # # # # #     return {"detail": "File not found"}

# # # # # # # # # @app.get("/data")
# # # # # # # # # async def get_data():
# # # # # # # # #     overlayed_images = os.listdir("static/overlayed_images")
# # # # # # # # #     return {"overlayed_images": overlayed_images}

# # # # # # # # # @app.get("/url")
# # # # # # # # # async def get_shareable_link(request: Request):
# # # # # # # # #     base_url = request.base_url
# # # # # # # # #     return {"shareable_link": base_url}

# # # # # # # # # @app.get("/images")
# # # # # # # # # async def get_images():
# # # # # # # # #     overlayed_images = os.listdir("static/overlayed_images")
# # # # # # # # #     image_urls = [
# # # # # # # # #         f"http://localhost:12000/static/overlayed_images/{image}" for image in overlayed_images
# # # # # # # # #     ]
# # # # # # # # #     return {"image_urls": image_urls}

# # # # # # # # # if __name__ == "__main__":
# # # # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)

# # # # # # # # import os
# # # # # # # # import cv2
# # # # # # # # import numpy as np
# # # # # # # # from typing import List
# # # # # # # # from fastapi import FastAPI, UploadFile, Request, File, BackgroundTasks
# # # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # # from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse
# # # # # # # # from fastapi.templating import Jinja2Templates
# # # # # # # # import uvicorn
# # # # # # # # from rembg import remove
# # # # # # # # from multiprocessing import Process

# # # # # # # # app = FastAPI()
# # # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")
# # # # # # # # templates = Jinja2Templates(directory="templates")

# # # # # # # # def create_static_folder():
# # # # # # # #     base_directory = os.getcwd()
# # # # # # # #     static_directory = os.path.join(base_directory, "static")
# # # # # # # #     overlayed_images_directory = os.path.join(static_directory, "overlayed_images")

# # # # # # # #     print("Base Directory:", base_directory)
# # # # # # # #     print("Static Directory:", static_directory)
# # # # # # # #     print("Overlayed Images Directory:", overlayed_images_directory)

# # # # # # # #     if not os.path.exists(static_directory):
# # # # # # # #         os.makedirs(static_directory)
# # # # # # # #         print("Static Directory Created.")

# # # # # # # #     if not os.path.exists(overlayed_images_directory):
# # # # # # # #         os.makedirs(overlayed_images_directory)
# # # # # # # #         print("Overlayed Images Directory Created.")

# # # # # # # # def create_home_html():
# # # # # # # #     templates_directory = os.path.join(os.getcwd(), "templates")
# # # # # # # #     home_html_path = os.path.join(templates_directory, "home.html")

# # # # # # # #     if not os.path.exists(home_html_path):
# # # # # # # #         with open(home_html_path, "w") as f:
# # # # # # # #             f.write(
# # # # # # # #                 """
# # # # # # # #                 <html>
# # # # # # # #                 <head>
# # # # # # # #                     <title>Upload Images</title>
# # # # # # # #                 </head>
# # # # # # # #                 <body>
# # # # # # # #                     <h1>Upload Images</h1>
# # # # # # # #                     <form action="/upload" enctype="multipart/form-data" method="post">
# # # # # # # #                         <input name="files" type="file" multiple>
# # # # # # # #                         <input type="text" name="text" placeholder="Overlay Text">
# # # # # # # #                         <input type="submit">
# # # # # # # #                     </form>
# # # # # # # #                 </body>
# # # # # # # #                 </html>
# # # # # # # #                 """
# # # # # # # #             )
# # # # # # # #         print("home.html created.")

# # # # # # # # @app.get("/", response_class=HTMLResponse)
# # # # # # # # async def home(request: Request):
# # # # # # # #     return templates.TemplateResponse("home.html", {"request": request})

# # # # # # # # def process_image(file: UploadFile, text: str):
# # # # # # # #     output_directory = "static/overlayed_images"
# # # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # # #     with open(f"{output_directory}/{file.filename}", "wb") as f:
# # # # # # # #         f.write(file.file.read())

# # # # # # # #     with open(f"{output_directory}/{file.filename}", "rb") as image_file:
# # # # # # # #         image_data = image_file.read()
# # # # # # # #         output_data = remove(image_data)

# # # # # # # #     image_array = np.frombuffer(output_data, np.uint8)

# # # # # # # #     image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

# # # # # # # #     image = cv2.resize(image, (1080, 1080))

# # # # # # # #     file_name_without_extension, file_extension = os.path.splitext(file.filename)

# # # # # # # #     if text:
# # # # # # # #         overlay_text = text
# # # # # # # #     else:
# # # # # # # #         overlay_text = f"{file_name_without_extension}{file_extension}"

# # # # # # # #     font = cv2.FONT_HERSHEY_SIMPLEX
# # # # # # # #     font_scale = 2
# # # # # # # #     font_thickness = 5
# # # # # # # #     text_color = (0, 0, 238)

# # # # # # # #     (text_width, text_height), _ = cv2.getTextSize(
# # # # # # # #         overlay_text, font, font_scale, font_thickness
# # # # # # # #     )

# # # # # # # #     x = int((image.shape[1] - text_width) / 2)
# # # # # # # #     y = image.shape[0] - int(text_height) - 30

# # # # # # # #     cv2.putText(
# # # # # # # #         image, overlay_text, (x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA
# # # # # # # #     )

# # # # # # # #     output_file_path = os.path.join(output_directory, file.filename)
# # # # # # # #     cv2.imwrite(output_file_path, image)

# # # # # # # # @app.post("/upload")
# # # # # # # # async def upload(files: List[UploadFile] = File(...), text: str = None, background_tasks: BackgroundTasks = None):
# # # # # # # #     instructions = []

# # # # # # # #     for file in files:
# # # # # # # #         p = Process(target=process_image, args=(file, text))
# # # # # # # #         p.start()
# # # # # # # #         p.join()

# # # # # # # #         instruction = f"Image {file.filename} processing has started."
# # # # # # # #         instructions.append(instruction)

# # # # # # # #     return {"instructions": instructions}

# # # # # # # # @app.get("/download/{filename}")
# # # # # # # # async def download(filename: str):
# # # # # # # #     file_path = os.path.join("static", "overlayed_images", filename)

# # # # # # # #     if os.path.isfile(file_path):
# # # # # # # #         return FileResponse(file_path)

# # # # # # # #     return {"detail": "File not found"}

# # # # # # # # @app.get("/data")
# # # # # # # # async def get_data():
# # # # # # # #     overlayed_images = os.listdir("static/overlayed_images")
# # # # # # # #     return {"overlayed_images": overlayed_images}

# # # # # # # # @app.get("/url")
# # # # # # # # async def get_shareable_link(request: Request):
# # # # # # # #     base_url = request.base_url
# # # # # # # #     return {"shareable_link": base_url}

# # # # # # # # @app.get("/images")
# # # # # # # # async def get_images():
# # # # # # # #     overlayed_images = os.listdir("static/overlayed_images")
# # # # # # # #     image_urls = [
# # # # # # # #         f"http://localhost:12000/static/overlayed_images/{image}" for image in overlayed_images
# # # # # # # #     ]
# # # # # # # #     return {"image_urls": image_urls}

# # # # # # # # if __name__ == "__main__":
# # # # # # # #     create_static_folder()
# # # # # # # #     create_home_html()
# # # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000, timeout_keep_alive=900)

# # # # # # # import os
# # # # # # # import cv2
# # # # # # # import numpy as np
# # # # # # # from typing import List
# # # # # # # from fastapi import FastAPI, UploadFile, Request, File
# # # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # # from fastapi.responses import HTMLResponse, FileResponse
# # # # # # # from fastapi.templating import Jinja2Templates
# # # # # # # import uvicorn
# # # # # # # from rembg import remove
# # # # # # # import multiprocessing
# # # # # # # import asyncio
# # # # # # # import time


# # # # # # # app = FastAPI()
# # # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")
# # # # # # # templates = Jinja2Templates(directory="templates")

# # # # # # # def create_static_folder():
# # # # # # #     base_directory = os.getcwd()
# # # # # # #     static_directory = os.path.join(base_directory, "static")
# # # # # # #     overlayed_images_directory = os.path.join(static_directory, "overlayed_images")

# # # # # # #     print("Base Directory:", base_directory)
# # # # # # #     print("Static Directory:", static_directory)
# # # # # # #     print("Overlayed Images Directory:", overlayed_images_directory)

# # # # # # #     if not os.path.exists(static_directory):
# # # # # # #         os.makedirs(static_directory)
# # # # # # #         print("Static Directory Created.")

# # # # # # #     if not os.path.exists(overlayed_images_directory):
# # # # # # #         os.makedirs(overlayed_images_directory)
# # # # # # #         print("Overlayed Images Directory Created.")

# # # # # # # def create_home_html():
# # # # # # #     templates_directory = os.path.join(os.getcwd(), "templates")
# # # # # # #     home_html_path = os.path.join(templates_directory, "home.html")

# # # # # # #     if not os.path.exists(home_html_path):
# # # # # # #         with open(home_html_path, "w") as f:
# # # # # # #             f.write(
# # # # # # #                 """
# # # # # # #                 <html>
# # # # # # #                 <head>
# # # # # # #                     <title>Upload Images</title>
# # # # # # #                 </head>
# # # # # # #                 <body>
# # # # # # #                     <h1>Upload Images</h1>
# # # # # # #                     <form action="/upload" enctype="multipart/form-data" method="post">
# # # # # # #                         <input name="files" type="file" multiple>
# # # # # # #                         <input type="text" name="text" placeholder="Overlay Text">
# # # # # # #                         <input type="submit">
# # # # # # #                     </form>
# # # # # # #                 </body>
# # # # # # #                 </html>
# # # # # # #                 """
# # # # # # #             )
# # # # # # #         print("home.html created.")

# # # # # # # @app.get("/", response_class=HTMLResponse)
# # # # # # # async def home(request: Request):
# # # # # # #     return templates.TemplateResponse("home.html", {"request": request})

# # # # # # # async def process_image(file, text, output_directory, next_file_number):
# # # # # # #     temp_path = os.path.join(output_directory, f"temp_{file.filename}")
# # # # # # #     with open(temp_path, "wb") as f:
# # # # # # #         f.write(await file.read())

# # # # # # #     with open(temp_path, "rb") as image_file:
# # # # # # #         image_data = image_file.read()
# # # # # # #         output_data = remove(image_data)

# # # # # # #     image_array = np.frombuffer(output_data, np.uint8)

# # # # # # #     image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

# # # # # # #     image = cv2.resize(image, (1080, 1080))

# # # # # # #     file_name = file.filename
# # # # # # #     file_name_without_extension, file_extension = os.path.splitext(file_name)

# # # # # # #     if text:
# # # # # # #         overlay_text = text
# # # # # # #     else:
# # # # # # #         overlay_text = f"{file_name_without_extension}{file_extension}"

# # # # # # #     font = cv2.FONT_HERSHEY_SIMPLEX
# # # # # # #     font_scale = 2
# # # # # # #     font_thickness = 5
# # # # # # #     text_color = (0, 0, 238)

# # # # # # #     (text_width, text_height), _ = cv2.getTextSize(
# # # # # # #         overlay_text, font, font_scale, font_thickness
# # # # # # #     )

# # # # # # #     x = int((image.shape[1] - text_width) / 2)
# # # # # # #     y = image.shape[0] - int(text_height) - 30

# # # # # # #     cv2.putText(
# # # # # # #         image, overlay_text, (x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA
# # # # # # #     )

# # # # # # #     output_file_path = os.path.join(output_directory, f"output_{next_file_number}.png")
# # # # # # #     cv2.imwrite(output_file_path, image)

# # # # # # #     download_url = f"/static/overlayed_images/output_{next_file_number}.png"

# # # # # # #     return file.filename, download_url

# # # # # # # @app.post("/upload")
# # # # # # # async def upload(files: List[UploadFile] = File(...), text: str = None):
# # # # # # #     output_directory = "static/overlayed_images"
# # # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # # #     next_file_number = get_next_file_number()

# # # # # # #     tasks = []
# # # # # # #     for file in files:
# # # # # # #         tasks.append(process_image(file, text, output_directory, next_file_number))
# # # # # # #         next_file_number += 1

# # # # # # #     results = await asyncio.gather(*tasks)

# # # # # # #     download_urls = [result[1] for result in results]
# # # # # # #     instructions = [f"Image {result[0]} processed. Download: {result[1]}" for result in results]

# # # # # # #     return {"download_urls": download_urls, "instructions": instructions}

# # # # # # # def get_next_file_number():
# # # # # # #     overlayed_images = os.listdir("static/overlayed_images")
# # # # # # #     file_numbers = [
# # # # # # #         int(file.split("_")[1].split(".")[0])
# # # # # # #         for file in overlayed_images
# # # # # # #         if file.startswith("output_")
# # # # # # #     ]
# # # # # # #     if file_numbers:
# # # # # # #         return max(file_numbers) + 1
# # # # # # #     else:
# # # # # # #         return 0

# # # # # # # create_static_folder()
# # # # # # # create_home_html()

# # # # # # # @app.get("/download/{filename}")
# # # # # # # async def download(filename: str):
# # # # # # #     file_path = os.path.join("static", "overlayed_images", filename)

# # # # # # #     if os.path.isfile(file_path):
# # # # # # #         return FileResponse(file_path)

# # # # # # #     return {"detail": "File not found"}

# # # # # # # @app.get("/data")
# # # # # # # async def get_data():
# # # # # # #     overlayed_images = os.listdir("static/overlayed_images")
# # # # # # #     return {"overlayed_images": overlayed_images}

# # # # # # # @app.get("/url")
# # # # # # # async def get_shareable_link(request: Request):
# # # # # # #     base_url = request.base_url
# # # # # # #     return {"shareable_link": base_url}

# # # # # # # @app.get("/images")
# # # # # # # async def get_images():
# # # # # # #     overlayed_images = os.listdir("static/overlayed_images")
# # # # # # #     image_urls = [
# # # # # # #         f"http://localhost:12000/static/overlayed_images/{image}" for image in overlayed_images
# # # # # # #     ]
# # # # # # #     return {"image_urls": image_urls}

# # # # # # # if __name__ == "__main__":
# # # # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)
# # # # # # #     time.sleep(900)  # Wait for 15 minutes
# # # # # # #     uvicorn.stop()



# # # # # # import os
# # # # # # from PIL import Image
# # # # # # from typing import List
# # # # # # from fastapi import FastAPI, UploadFile, Request, File
# # # # # # from fastapi.staticfiles import StaticFiles
# # # # # # from fastapi.responses import FileResponse, JSONResponse
# # # # # # from fastapi.templating import Jinja2Templates
# # # # # # import rembg

# # # # # # app = FastAPI()
# # # # # # app.mount("/static", StaticFiles(directory="static"), name="static")
# # # # # # templates = Jinja2Templates(directory="templates")

# # # # # # # Define the upload endpoint
# # # # # # @app.post("/upload")
# # # # # # async def upload(files: List[UploadFile] = File(...), text: str = None):
# # # # # #     output_directory = "static/output"
# # # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # # #     download_urls = []
# # # # # #     instructions = []

# # # # # #     for i, file in enumerate(files):
# # # # # #         try:
# # # # # #             # Save the uploaded file temporarily
# # # # # #             temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # # #             with open(temp_path, "wb") as f:
# # # # # #                 f.write(await file.read())

# # # # # #             # Remove the background using rembg
# # # # # #             output_path = os.path.join(output_directory, f"output_{i}.png")
# # # # # #             with open(temp_path, "rb") as img_file, open(output_path, "wb") as output_file:
# # # # # #                 img_data = img_file.read()
# # # # # #                 output_data = rembg.remove(img_data)
# # # # # #                 output_file.write(output_data)

# # # # # #             # Resize the image to 1080x1080 and add overlay text
# # # # # #             image = Image.open(output_path)
# # # # # #             image = image.resize((1080, 1080))
# # # # # #             image_with_text = add_text_overlay(image, file.filename, text)
# # # # # #             image_with_text.save(output_path)

# # # # # #             # Remove the temporary file
# # # # # #             os.remove(temp_path)

# # # # # #             # Generate the download link URL for the output image
# # # # # #             download_url = f"/static/output/output_{i}.png"
# # # # # #             download_urls.append(download_url)

# # # # # #             # Add instruction
# # # # # #             instruction = f"Image {file.filename} processed. Download: {download_url}"
# # # # # #             instructions.append(instruction)
# # # # # #         except Exception as e:
# # # # # #             # Log the error and continue with the next file
# # # # # #             error_message = f"Error processing file {file.filename}: {str(e)}"
# # # # # #             print(error_message)

# # # # # #     # Return the download URLs and instructions in the API response
# # # # # #     return {"download_urls": download_urls, "instructions": instructions}


# # # # # # def add_text_overlay(image, filename, text):
# # # # # #     from PIL import ImageDraw, ImageFont

# # # # # #     overlay_text = text or filename
# # # # # #     font = ImageFont.truetype("arial.ttf", 100)
# # # # # #     draw = ImageDraw.Draw(image)
# # # # # #     text_width, text_height = draw.textsize(overlay_text, font=font)
# # # # # #     x = int((image.width - text_width) / 2)
# # # # # #     y = image.height - text_height - 30
# # # # # #     draw.text((x, y), overlay_text, font=font, fill=(0, 0, 238))

# # # # # #     return image


# # # # # # @app.get("/download/{filename}")
# # # # # # async def download(filename: str):
# # # # # #     # Making the file path
# # # # # #     file_path = os.path.join("static", "output", filename)

# # # # # #     # Check if the file exists
# # # # # #     if os.path.isfile(file_path):
# # # # # #         # If the file exists, return it as a response
# # # # # #         return FileResponse(file_path)

# # # # # #     # If the file does not exist, return a 404 Not Found response
# # # # # #     return {"detail": "File not found"}


# # # # # # @app.get("/data")
# # # # # # async def get_data():
# # # # # #     overlayed_images = os.listdir("static/output")
# # # # # #     return {"overlayed_images": overlayed_images}


# # # # # # @app.get("/url")
# # # # # # async def get_shareable_link(request: Request):
# # # # # #     base_url = request.base_url
# # # # # #     return {"shareable_link": base_url}


# # # # # # @app.get("/images")
# # # # # # async def get_images():
# # # # # #     overlayed_images = os.listdir("static/output")
# # # # # #     image_urls = [
# # # # # #         f"/static/output/{image}" for image in overlayed_images
# # # # # #     ]
# # # # # #     return {"image_urls": image_urls}

# # # # # import os
# # # # # import cv2
# # # # # from typing import List
# # # # # from fastapi import FastAPI, UploadFile, Request, File
# # # # # from fastapi.staticfiles import StaticFiles
# # # # # from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
# # # # # from fastapi.templating import Jinja2Templates
# # # # # import uvicorn

# # # # # app = FastAPI()
# # # # # app.mount("/static", StaticFiles(directory="static"), name="static")
# # # # # templates = Jinja2Templates(directory="templates")

# # # # # # Define the home page
# # # # # @app.get("/", response_class=HTMLResponse)
# # # # # async def home(request: Request):
# # # # #     return templates.TemplateResponse("home.html", {"request": request})


# # # # # # Define the upload endpoint
# # # # # @app.post("/upload")
# # # # # async def upload(files: List[UploadFile] = File(...), text: str = None):
# # # # #     output_directory = "static/output"
# # # # #     os.makedirs(output_directory, exist_ok=True)

# # # # #     download_urls = []
# # # # #     instructions = []

# # # # #     for i, file in enumerate(files):
# # # # #         # Save the uploaded file temporarily
# # # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # # #         with open(temp_path, "wb") as f:
# # # # #             f.write(await file.read())

# # # # #         # Read the image using OpenCV
# # # # #         image = cv2.imread(temp_path)

# # # # #         # Get the name from the uploaded file
# # # # #         file_name = file.filename
# # # # #         file_name_without_extension, file_extension = os.path.splitext(file_name)

# # # # #         # Prepare the text to overlay on the image
# # # # #         if text:
# # # # #             overlay_text = text
# # # # #         else:
# # # # #             overlay_text = f"{file_name_without_extension}{file_extension}"

# # # # #         font = cv2.FONT_HERSHEY_SIMPLEX
# # # # #         font_scale = 2
# # # # #         font_thickness = 5
# # # # #         text_color = (0, 0, 238)

# # # # #         # Set the text size
# # # # #         (text_width, text_height), _ = cv2.getTextSize(
# # # # #             overlay_text, font, font_scale, font_thickness
# # # # #         )

# # # # #         # Calculate the position to place the text
# # # # #         x = int((image.shape[1] - text_width) / 2)  # Centered horizontally
# # # # #         y = int((image.shape[0] + text_height) - 30)  # Centered vertically

# # # # #         # Overlay the text on the image
# # # # #         cv2.putText(
# # # # #             image, overlay_text, (x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA
# # # # #         )

# # # # #         # Set the output file path
# # # # #         output_file_path = os.path.join(output_directory, f"output_{i}.png")

# # # # #         # Save the resulting image
# # # # #         cv2.imwrite(output_file_path, image)

# # # # #         # Remove the temporary file
# # # # #         os.remove(temp_path)

# # # # #         # Generate the download link URL for the output image
# # # # #         download_url = f"/static/output/output_{i}.png"
# # # # #         download_urls.append(download_url)

# # # # #         # Add instruction
# # # # #         instruction = f"Image {file_name} processed. Download: {download_url}"
# # # # #         instructions.append(instruction)

# # # # #     # Return the download URLs and instructions in the API response
# # # # #     return {"download_urls": download_urls, "instructions": instructions}


# # # # # @app.get("/download/{filename}")
# # # # # async def download(filename: str):
# # # # #     # Making the file path
# # # # #     file_path = os.path.join("static", "output", filename)

# # # # #     # Check if the file exists
# # # # #     if os.path.isfile(file_path):
# # # # #         # If the file exists, return it as a response
# # # # #         return FileResponse(file_path)

# # # # #     # If the file does not exist, return a 404 Not Found response
# # # # #     return {"detail": "File not found"}


# # # # # @app.get("/data")
# # # # # async def get_data():
# # # # #     overlayed_images = os.listdir("static/output")
# # # # #     return {"overlayed_images": overlayed_images}


# # # # # @app.get("/url")
# # # # # async def get_shareable_link(request: Request):
# # # # #     base_url = request.base_url
# # # # #     return {"shareable_link": base_url}


# # # # # @app.get("/images")
# # # # # async def get_images():
# # # # #     overlayed_images = os.listdir("static/output")
# # # # #     image_urls = [
# # # # #         f"http://localhost:12000/static/output/{image}" for image in overlayed_images
# # # # #     ]
# # # # #     return {"image_urls": image_urls}


# # # # # # Start the server
# # # # # if __name__ == "__main__":
# # # # #     uvicorn.run(app, host="0.0.0.0", port=12000)


# # # # import os
# # # # import cv2
# # # # from typing import List
# # # # from fastapi import FastAPI, UploadFile, Request, File
# # # # from fastapi.staticfiles import StaticFiles
# # # # from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
# # # # from fastapi.templating import Jinja2Templates
# # # # import uvicorn
# # # # import numpy as np
# # # # from rembg import remove

# # # # app = FastAPI()
# # # # app.mount("/static", StaticFiles(directory="static"), name="static")
# # # # templates = Jinja2Templates(directory="templates")

# # # # # Define the home page
# # # # @app.get("/", response_class=HTMLResponse)
# # # # async def home(request: Request):
# # # #     return templates.TemplateResponse("home.html", {"request": request})


# # # # # Define the upload endpoint
# # # # @app.post("/upload")
# # # # async def upload(files: List[UploadFile] = File(...), text: str = None):
# # # #     output_directory = "static/output"
# # # #     os.makedirs(output_directory, exist_ok=True)

# # # #     download_urls = []
# # # #     instructions = []

# # # #     for i, file in enumerate(files):
# # # #         # Save the uploaded file temporarily
# # # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # # #         with open(temp_path, "wb") as f:
# # # #             f.write(await file.read())

# # # #         # Remove the background of the image using rembg module
# # # #         with open(temp_path, "rb") as image_file:
# # # #             image_data = image_file.read()
# # # #             output_data = remove(image_data)

# # # #         # Convert the image data to a NumPy array
# # # #         image_array = np.frombuffer(output_data, np.uint8)

# # # #         # Decode the image array
# # # #         image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

# # # #         # Get the name from the uploaded file
# # # #         file_name = file.filename
# # # #         file_name_without_extension, file_extension = os.path.splitext(file_name)

# # # #         # Prepare the text to overlay on the image
# # # #         if text:
# # # #             overlay_text = text
# # # #         else:
# # # #             overlay_text = f"{file_name_without_extension}{file_extension}"

# # # #         font = cv2.FONT_HERSHEY_SIMPLEX
# # # #         font_scale = 2
# # # #         font_thickness = 5
# # # #         text_color = (0, 0, 238)

# # # #         # Set the text size
# # # #         (text_width, text_height), _ = cv2.getTextSize(
# # # #             overlay_text, font, font_scale, font_thickness
# # # #         )

# # # #         # Calculate the position to place the text
# # # #         x = int((text_width - image.shape[1]) / 2)  # Centered horizontally
# # # #         y = int((image.shape[0] + text_height) - 30)  # Centered vertically

# # # #         # Overlay the text on the image
# # # #         cv2.putText(
# # # #             image, overlay_text, (x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA
# # # #         )

# # # #         # Set the output file path
# # # #         output_file_path = os.path.join(output_directory, f"output_{i}.png")

# # # #         # Save the resulting image
# # # #         cv2.imwrite(output_file_path, image)

# # # #         # Remove the temporary file
# # # #         os.remove(temp_path)

# # # #         # Generate the download link URL for the output image
# # # #         download_url = f"/static/output/output_{i}.png"
# # # #         download_urls.append(download_url)

# # # #         # Add instruction
# # # #         instruction = f"Image {file_name} processed. Download: {download_url}"
# # # #         instructions.append(instruction)

# # # #     # Return the download URLs and instructions in the API response
# # # #     return {"download_urls": download_urls, "instructions": instructions}


# # # # @app.get("/download/{filename}")
# # # # async def download(filename: str):
# # # #     # Making the file path
# # # #     file_path = os.path.join("static", "output", filename)

# # # #     # Check if the file exists
# # # #     if os.path.isfile(file_path):
# # # #         # If the file exists, return it as a response
# # # #         return FileResponse(file_path)

# # # #     # If the file does not exist, return a 404 Not Found response
# # # #     return {"detail": "File not found"}


# # # # @app.get("/data")
# # # # async def get_data():
# # # #     overlayed_images = os.listdir("static/output")
# # # #     return {"overlayed_images": overlayed_images}


# # # # @app.get("/url")
# # # # async def get_shareable_link(request: Request):
# # # #     base_url = request.base_url
# # # #     return {"shareable_link": base_url}


# # # # @app.get("/images")
# # # # async def get_images():
# # # #     overlayed_images = os.listdir("static/output")
# # # #     image_urls = [
# # # #         f"http://localhost:12000/static/output/{image}" for image in overlayed_images
# # # #     ]
# # # #     return {"image_urls": image_urls}


# # # # # Start the server
# # # # if __name__ == "__main__":
# # # #     uvicorn.run(app, host="0.0.0.0", port=12000)


# # # import os
# # # import cv2
# # # from typing import List
# # # from fastapi import FastAPI, UploadFile, Request, File
# # # # from fastapi.staticfiles import StaticFiles
# # # from fastapi.responses import FileResponse, JSONResponse
# # # from fastapi.templating import Jinja2Templates
# # # import uvicorn

# # # app = FastAPI()
# # # app.mount("/static", StaticFiles(directory="static"), name="static")
# # # templates = Jinja2Templates(directory="templates")

# # # # Define the upload endpoint
# # # @app.post("/upload")
# # # async def upload(files: List[UploadFile] = File(...), text: str = None):
# # #     output_directory = "static/output"
# # #     os.makedirs(output_directory, exist_ok=True)

# # #     download_urls = []
# # #     instructions = []

# # #     for i, file in enumerate(files):
# # #         # Save the uploaded file temporarily
# # #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# # #         with open(temp_path, "wb") as f:
# # #             f.write(await file.read())

# # #         # Read the image using OpenCV
# # #         image = cv2.imread(temp_path)

# # #         # Resize the image to 1080x1080
# # #         image = cv2.resize(image, (1080, 1080))

# # #         # Remove the background using Rembg (requires Rembg library installed)
# # #         try:
# # #             import rembg
# # #             image = rembg.remove(image)
# # #         except ImportError:
# # #             return JSONResponse(
# # #                 {"error": "Rembg library not found. Please install it to remove the background."},
# # #                 status_code=500,
# # #             )

# # #         # Prepare the text to overlay on the image
# # #         if text:
# # #             overlay_text = text
# # #         else:
# # #             file_name = file.filename
# # #             file_name_without_extension, file_extension = os.path.splitext(file_name)
# # #             overlay_text = f"{file_name_without_extension}{file_extension}"

# # #         font = cv2.FONT_HERSHEY_SIMPLEX
# # #         font_scale = 2
# # #         font_thickness = 5
# # #         text_color = (0, 0, 238)

# # #         # Set the text size
# # #         (text_width, text_height), _ = cv2.getTextSize(
# # #             overlay_text, font, font_scale, font_thickness
# # #         )

# # #         # Calculate the position to place the text
# # #         x = int((image.shape[1] - text_width) / 2)  # Centered horizontally
# # #         y = int((image.shape[0] + text_height) - 30)  # Placed at the bottom

# # #         # Overlay the text on the image
# # #         cv2.putText(
# # #             image, overlay_text, (x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA
# # #         )

# # #         # Set the output file path
# # #         output_file_path = os.path.join(output_directory, f"output_{i}.png")

# # #         # Save the resulting image
# # #         cv2.imwrite(output_file_path, image)

# # #         # Remove the temporary file
# # #         os.remove(temp_path)

# # #         # Generate the download link URL for the output image
# # #         download_url = f"/static/output/output_{i}.png"
# # #         download_urls.append(download_url)

# # #         # Add instruction
# # #         instruction = f"Image {file.filename} processed. Download: {download_url}"
# # #         instructions.append(instruction)

# # #     # Return the download URLs and instructions in the API response
# # #     return {"download_urls": download_urls, "instructions": instructions}


# # # @app.get("/download/{filename}")
# # # async def download(filename: str):
# # #     # Making the file path
# # #     file_path = os.path.join("static", "output", filename)

# # #     # Check if the file exists
# # #     if os.path.isfile(file_path):
# # #         # If the file exists, return it as a response
# # #         return FileResponse(file_path)

# # #     # If the file does not exist, return a 404 Not Found response
# # #     return {"detail": "File not found"}


# # # @app.get("/data")
# # # async def get_data():
# # #     overlayed_images = os.listdir("static/output")
# # #     return {"overlayed_images": overlayed_images}


# # # @app.get("/url")
# # # async def get_shareable_link(request: Request):
# # #     base_url = request.base_url
# # #     return {"shareable_link": base_url}


# # # @app.get("/images")
# # # async def get_images():
# # #     overlayed_images = os.listdir("static/output")
# # #     image_urls = [
# # #         f"http://localhost:12000/static/output/{image}" for image in overlayed_images
# # #     ]
# # #     return {"image_urls": image_urls}


# # # # Start the server
# # # if __name__ == "__main__":
# # #     uvicorn.run(app, host="0.0.0.0", port=12000)
# # import os
# # import cv2
# # import numpy as np
# # from typing import List
# # from fastapi import FastAPI, UploadFile, Request, File
# # from fastapi.staticfiles import StaticFiles
# # from fastapi.responses import FileResponse, JSONResponse
# # from fastapi.templating import Jinja2Templates
# # import uvicorn
# # from PIL import Image

# # app = FastAPI()
# # app.mount("/static", StaticFiles(directory="static"), name="static")
# # templates = Jinja2Templates(directory="templates")

# # # Define the upload endpoint
# # @app.post("/upload")
# # async def upload(files: List[UploadFile] = File(...), text: str = None):
# #     output_directory = "static/output"
# #     os.makedirs(output_directory, exist_ok=True)

# #     download_urls = []
# #     instructions = []

# #     for i, file in enumerate(files):
# #         # Save the uploaded file temporarily
# #         temp_path = os.path.join(output_directory, f"temp_{i}.png")
# #         with open(temp_path, "wb") as f:
# #             f.write(await file.read())

# #         # Read the image using OpenCV
# #         img = cv2.imread(temp_path)

# #         # Remove the background using the provided code
# #         original = img.copy()

# #         l = int(max(5, 6))
# #         u = int(min(6, 6))

# #         ed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# #         edges = cv2.GaussianBlur(img, (21, 51), 3)
# #         edges = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)
# #         edges = cv2.Canny(edges, l, u)

# #         _, thresh = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# #         kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
# #         mask = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=4)

# #         data = mask.tolist()
# #         sys.setrecursionlimit(10**8)
# #         for i in range(len(data)):
# #             for j in range(len(data[i])):
# #                 if data[i][j] != 255:
# #                     data[i][j] = -1
# #                 else:
# #                     break
# #             for j in range(len(data[i])-1, -1, -1):
# #                 if data[i][j] != 255:
# #                     data[i][j] = -1
# #                 else:
# #                     break
# #         image = np.array(data)
# #         image[image != -1] = 255
# #         image[image == -1] = 0

# #         mask = np.array(image, np.uint8)

# #         result = cv2.bitwise_and(original, original, mask=mask)
# #         result[mask == 0] = 255
# #         cv2.imwrite('bg.png', result)

# #         img = Image.open('bg.png')
# #         img.convert("RGBA")
# #         datas = img.getdata()

# #         newData = []
# #         for item in datas:
# #             if item[0] == 255 and item[1] == 255 and item[2] == 255:
# #                 newData.append((255, 255, 255, 0))
# #             else:
# #                 newData.append(item)

# #         img.putdata(newData)
# #         img_path = os.path.join(output_directory, f"output_{i}.png")
# #         img.save(img_path, "PNG")

# #         # Prepare the text to overlay on the image
# #         if text:
# #             overlay_text = text
# #         else:
# #             file_name = file.filename
# #             file_name_without_extension, file_extension = os.path.splitext(file_name)
# #             overlay_text = f"{file_name_without_extension}{file_extension}"

# #         font = cv2.FONT_HERSHEY_SIMPLEX
# #         font_scale = 2
# #         font_thickness = 5
# #         text_color = (0, 0, 238)

# #         # Set the text size
# #         (text_width, text_height), _ = cv2.getTextSize(
# #             overlay_text, font, font_scale, font_thickness
# #         )

# #         # Calculate the position to place the text
# #         x = int((img.shape[1] - text_width) / 2)  # Centered horizontally
# #         y = int((img.shape[0] + text_height) - 30)  # Placed at the bottom

# #         # Overlay the text on the image
# #         cv2.putText(
# #             img, overlay_text, (x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA
# #         )

# #         # Set the output file path
# #         output_file_path = os.path.join(output_directory, f"output_{i}.png")

# #         # Save the resulting image
# #         cv2.imwrite(output_file_path, img)

# #         # Generate the download link URL for the output image
# #         download_url = f"/static/output/output_{i}.png"
# #         download_urls.append(download_url)

# #         # Add instruction
# #         instruction = f"Image {file.filename} processed. Download: {download_url}"
# #         instructions.append(instruction)

# #     # Return the download URLs and instructions in the API response
# #     return {"download_urls": download_urls, "instructions": instructions}


# # @app.get("/download/{filename}")
# # async def download(filename: str):
# #     # Making the file path
# #     file_path = os.path.join("static", "output", filename)

# #     # Check if the file exists
# #     if os.path.isfile(file_path):
# #         # If the file exists, return it as a response
# #         return FileResponse(file_path)

# #     # If the file does not exist, return a 404 Not Found response
# #     return {"detail": "File not found"}


# # @app.get("/data")
# # async def get_data():
# #     overlayed_images = os.listdir("static/output")
# #     return {"overlayed_images": overlayed_images}


# # @app.get("/url")
# # async def get_shareable_link(request: Request):
# #     base_url = request.base_url
# #     return {"shareable_link": base_url}


# # @app.get("/images")
# # async def get_images():
# #     overlayed_images = os.listdir("static/output")
# #     image_urls = [
# #         f"http://localhost:12000/static/output/{image}" for image in overlayed_images
# #     ]
# #     return {"image_urls": image_urls}


# # # Start the server
# # if __name__ == "__main__":
# #     uvicorn.run(app, host="0.0.0.0", port=12000)
# import os
# import cv2
# import numpy as np
# from typing import List
# from fastapi import FastAPI, UploadFile, Request, File
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse, JSONResponse
# from fastapi.templating import Jinja2Templates
# import uvicorn
# from PIL import Image

# app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

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
#             contents = await file.read()  # Read the file contents
#             f.write(contents)

#         # Read the image using OpenCV
#         img = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_UNCHANGED)

#         # Remove the background using the provided code
#         original = img.copy()

#         l = int(max(5, 6))
#         u = int(min(6, 6))

#         ed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         edges = cv2.GaussianBlur(img, (21, 51), 3)
#         edges = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)
#         edges = cv2.Canny(edges, l, u)

#         _, thresh = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#         kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
#         mask = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=4)

#         data = mask.tolist()
#         sys.setrecursionlimit(10**8)
#         for i in range(len(data)):
#             for j in range(len(data[i])):
#                 if data[i][j] != 255:
#                     data[i][j] = -1
#                 else:
#                     break
#             for j in range(len(data[i])-1, -1, -1):
#                 if data[i][j] != 255:
#                     data[i][j] = -1
#                 else:
#                     break
#         image = np.array(data)
#         image[image != -1] = 255
#         image[image == -1] = 0

#         mask = np.array(image, np.uint8)

#         result = cv2.bitwise_and(original, original, mask=mask)
#         result[mask == 0] = 255
#         cv2.imwrite('bg.png', result)

#         img = Image.open('bg.png')
#         img.convert("RGBA")
#         datas = img.getdata()

#         newData = []
#         for item in datas:
#             if item[0] == 255 and item[1] == 255 and item[2] == 255:
#                 newData.append((255, 255, 255, 0))
#             else:
#                 newData.append(item)

#         img.putdata(newData)
#         img_path = os.path.join(output_directory, f"output_{i}.png")
#         img.save(img_path, "PNG")

#         # Prepare the text to overlay on the image
#         if text:
#             overlay_text = text
#         else:
#             file_name = file.filename
#             file_name_without_extension, file_extension = os.path.splitext(file_name)
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
#         x = int((img.shape[1] - text_width) / 2)  # Centered horizontally
#         y = int((img.shape[0] + text_height) - 30)  # Placed at the bottom

#         # Overlay the text on the image
#         cv2.putText(
#             img, overlay_text, (x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA
#         )

#         # Set the output file path
#         output_file_path = os.path.join(output_directory, f"output_{i}.png")

#         # Save the resulting image
#         cv2.imwrite(output_file_path, img)

#         # Generate the download link URL for the output image
#         download_url = f"/static/output/output_{i}.png"
#         download_urls.append(download_url)

#         # Add instruction
#         instruction = f"Image {file.filename} processed. Download: {download_url}"
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
import cv2
import numpy as np
from typing import List
from fastapi import FastAPI, UploadFile, Request, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from PIL import Image

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
        # Save the uploaded file temporarily
        temp_path = os.path.join(output_directory, f"temp_{i}.png")
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        # Read the image using OpenCV
        img = cv2.imread(temp_path)

        # Resize the image to 1080x1080
        img = cv2.resize(img, (1080, 1080))

        # Remove the background using the provided code
        original = img.copy()

        l = int(max(5, 6))
        u = int(min(6, 6))

        ed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.GaussianBlur(img, (21, 51), 3)
        edges = cv2.cvtColor(edges, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(edges, l, u)

        _, thresh = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=4)

        data = mask.tolist()
        for i in range(len(data)):
            for j in range(len(data[i])):
                if data[i][j] != 255:
                    data[i][j] = -1
                else:
                    break
            for j in range(len(data[i])-1, -1, -1):
                if data[i][j] != 255:
                    data[i][j] = -1
                else:
                    break
        image = np.array(data)
        image[image != -1] = 255
        image[image == -1] = 0

        mask = np.array(image, np.uint8)

        result = cv2.bitwise_and(original, original, mask=mask)
        result[mask == 0] = 255
        cv2.imwrite('bg.png', result)

        img = Image.open('bg.png')
        img.convert("RGBA")
        datas = img.getdata()

        newData = []
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        img.putdata(newData)
        img_path = os.path.join(output_directory, f"output_{i}.png")
        img.save(img_path, "PNG")

        # Prepare the text to overlay on the image
        if text:
            overlay_text = text
        else:
            file_name = file.filename
            file_name_without_extension, file_extension = os.path.splitext(file_name)
            overlay_text = f"{file_name_without_extension}{file_extension}"

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2
        font_thickness = 5
        text_color = (0, 0, 238)

        # Set the text size
        text_width, text_height = cv2.getTextSize(
            overlay_text, font, font_scale, font_thickness
        )[0]

        # Calculate the position to place the text
        img_width, img_height = img.size
        x = int((img_width - text_width) / 2)  # Centered horizontally
        y = int((img_height + text_height) - 30)  # Placed at the bottom

        # Overlay the text on the image
        cv2.putText(
            np.array(img), overlay_text, (x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA
        )

        # Set the output file path
        output_file_path = os.path.join(output_directory, f"output_{i}.png")

        # Save the resulting image
        img.save(output_file_path, "PNG")

        # Generate the download link URL for the output image
        download_url = f"/static/output/output_{i}.png"
        download_urls.append(download_url)

        # Add instruction
        instruction = f"Image {file.filename} processed. Download: {download_url}"
        instructions.append(instruction)

    # Return the download URLs and instructions in the API response
    return {"download_urls": download_urls, "instructions": instructions}


# Define the download endpoint
@app.get("/download/{filename}")
async def download(filename: str):
    # Making the file path
    file_path = os.path.join("static", "output", filename)

    # Check if the file exists
    if os.path.isfile(file_path):
        # If the file exists, return it as a response
        return FileResponse(file_path)

    # If the file does not exist, return a 404 Not Found response
    return JSONResponse({"detail": "File not found"}, status_code=404)


# Define the data endpoint
@app.get("/data")
async def get_data():
    overlayed_images = os.listdir("static/output")
    return {"overlayed_images": overlayed_images}


# Define the shareable link endpoint
@app.get("/url")
async def get_shareable_link(request: Request):
    base_url = request.base_url
    return {"shareable_link": base_url}


# Define the images endpoint
@app.get("/images")
async def get_images():
    overlayed_images = os.listdir("static/output")
    image_urls = [
        f"http://localhost:12000/static/output/{image}" for image in overlayed_images
    ]
    return {"image_urls": image_urls}


# Define the preview endpoint
@app.get("/preview/{filename}")
async def preview(filename: str):
    # Making the file path
    file_path = os.path.join("static", "output", filename)

    # Check if the file exists
    if os.path.isfile(file_path):
        # If the file exists, return it as a response
        return FileResponse(file_path)

    # If the file does not exist, return a 404 Not Found response
    return JSONResponse({"detail": "File not found"}, status_code=404)


# Start the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=12000)
