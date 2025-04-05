from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from PIL import Image, ExifTags
import os
import shutil

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
        img = Image.open(path)
        exif_data_raw = img._getexif()
        if not exif_data_raw:
            return {"filename": file.filename, "metadata": {}}
        exif_data = {}
        for tag_id, value in exif_data_raw.items():
            tag_name = ExifTags.TAGS.get(tag_id, tag_id)
            exif_data[tag_name] = str(value)

        gps_info = metadata_service.get_gps_info(exif_data_raw)
        if gps_info:
            exif_data["GPSInfo"] = gps_info

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
