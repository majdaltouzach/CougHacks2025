# main.py
from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from PIL import Image, ExifTags
import os
import shutil
import piexif

from metadata_service import MetadataService

# Directory to store uploaded images
UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()
metadata_service = MetadataService()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def save_upload(file: UploadFile):
    # Save the uploaded file to the upload directory
    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return path

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    # Endpoint to upload an image and extract its metadata
    path = save_upload(file)
    try:
        exif_dict = piexif.load(path)
        exif_data = {}

        for ifd_name in exif_dict:
            if ifd_name == "thumbnail":
                continue
            for tag_id, value in exif_dict[ifd_name].items():
                tag_info = piexif.TAGS[ifd_name].get(tag_id, {"name": tag_id})
                tag_name = tag_info["name"]

                if isinstance(value, bytes):
                    try:
                        value = value.decode("utf-8")
                    except:
                        continue  # skip unreadable binary

                try:
                    exif_data[tag_name] = str(value)
                except:
                    continue

        return {"filename": file.filename, "metadata": exif_data}

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.post("/update-metadata/")
async def update_metadata_api(request: Request):
    # Endpoint to update or delete metadata of an image
    data = await request.json()
    filename = data.get("filename")
    action = data.get("action")
    tag = data.get("tag")
    value = data.get("value")
    path = os.path.join(UPLOAD_DIR, filename)
    try:
        if action == "erase":
            metadata_service.delete_everything(path)
            return {"message": "All metadata erased"}
        elif action in ("edit", "add"):
            metadata_service.update_metadata(path, tag, value)
            return {"message": f"Tag {tag} updated", "value": value}
        elif action == "delete":
            metadata_service.delete_metadata_tag(path, tag)
            return {"message": f"Tag {tag} deleted"}
        else:
            return JSONResponse(status_code=400, content={"error": "Invalid action"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

@app.get("/image/{filename}")
async def get_image(filename: str):
    # Endpoint to retrieve an image by filename
    return FileResponse(os.path.join(UPLOAD_DIR, filename))


# # metadata_service.py
# import piexif
# from piexif import TAGS
# from PIL import Image
# import copy
# from PIL.ExifTags import GPSTAGS

# class MetadataService:
#     def __init__(self):
#         self.ALL_TAGS = {}
#         for ifd_name in piexif.TAGS:
#             for tag_id, tag_info in piexif.TAGS[ifd_name].items():
#                 self.ALL_TAGS[tag_info["name"]] = (ifd_name, tag_id)

#     def resolve_tag(self, tag_name: str):
#         result = self.ALL_TAGS.get(tag_name)
#         if not result:
#             raise ValueError(f"Tag '{tag_name}' not found in known EXIF tags")
#         return result

#     def update_metadata(self, image_path: str, tag_name: str, new_value: str):
#         encoded_value = new_value.encode("utf-8")
#         exif_dict = piexif.load(image_path)
#         ifd, tag_id = self.resolve_tag(tag_name)
#         for ifd_name in exif_dict:
#             if ifd_name == "thumbnail":
#                 continue
#             if tag_id in exif_dict[ifd_name]:
#                 exif_dict[ifd_name][tag_id] = encoded_value
#         exif_bytes = piexif.dump(exif_dict)
#         piexif.insert(exif_bytes, image_path)

#     def delete_metadata_tag(self, image_path: str, tag_name: str):
#         exif_dict = piexif.load(image_path)
#         ifd, tag_id = self.resolve_tag(tag_name)
#         deleted = False
#         for ifd_name in exif_dict:
#             if ifd_name == "thumbnail":
#                 continue
#             if tag_id in exif_dict[ifd_name]:
#                 del exif_dict[ifd_name][tag_id]
#                 deleted = True
#         if not deleted:
#             raise ValueError(f"Tag '{tag_name}' not found in image metadata")
#         exif_bytes = piexif.dump(exif_dict)
#         piexif.insert(exif_bytes, image_path)

#     def delete_everything(self, image_path: str):
#         exif_dict = piexif.load(image_path)
#         exif_dict_ref = copy.deepcopy(exif_dict)
#         for ifd_name in exif_dict_ref:
#             if ifd_name == "thumbnail":
#                 continue
#             for tag_id in exif_dict_ref[ifd_name]:
#                 del exif_dict[ifd_name][tag_id]
#         exif_bytes = piexif.dump(exif_dict)
#         piexif.insert(exif_bytes, image_path)

#     def get_exif_data(self, path: str):
#         return piexif.load(path)

#     def get_gps_info(self, exif_data_raw):
#         gps_info = {}
#         for tag_id, value in exif_data_raw.items():
#             tag_name = GPSTAGS.get(tag_id, tag_id)
#             gps_info[tag_name] = value
#         return gps_info if gps_info else None