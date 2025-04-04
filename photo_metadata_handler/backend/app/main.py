from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from PIL import Image, ExifTags
import os
import shutil
import piexif

UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper: Save uploaded file
def save_upload(file: UploadFile):
    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return path

# 1. Upload & Extract Metadata
@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    path = save_upload(file)
    try:
        exif_dict = piexif.load(path)
        exif_data = {k: str(v) for k, v in exif_dict["0th"].items()}
        return {"filename": file.filename, "metadata": exif_data}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

# 2. Erase Metadata
@app.post("/erase-metadata/")
async def erase_metadata(filename: str = Form(...)):
    path = os.path.join(UPLOAD_DIR, filename)
    piexif.remove(path)
    return {"message": "Metadata erased", "filename": filename}

# 3. Edit Metadata (simple overwrite example)
@app.post("/edit-metadata/")
async def edit_metadata(
    filename: str = Form(...), tag: str = Form(...), value: str = Form(...)
):
    path = os.path.join(UPLOAD_DIR, filename)
    exif_dict = piexif.load(path)
    exif_dict["0th"][piexif.ImageIFD.Make] = value.encode()
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, path)
    return {"message": "Metadata updated", "tag": tag, "value": value}

# 4. Serve the Image (for testing)
@app.get("/image/{filename}")
async def get_image(filename: str):
    return FileResponse(os.path.join(UPLOAD_DIR, filename))
