from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import io

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
