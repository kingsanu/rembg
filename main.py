from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Query
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove
from io import BytesIO
from PIL import Image
import requests
import os
import uuid
from typing import Optional

app = FastAPI()

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Cloud storage API endpoint
CLOUD_STORAGE_API = "https://business.foodyqueen.com/admin/UploadMedia"

@app.post("/rbg")
async def remove_bg(
    file: UploadFile = File(...),
    upload_form: Optional[bool] = Form(None, alias="upload"),
    upload_query: Optional[bool] = Query(None, alias="upload"),
    user_id_form: Optional[str] = Form(None, alias="user_id"),
    user_id_query: Optional[str] = Query(None, alias="user_id"),
    filename_form: Optional[str] = Form(None, alias="filename"),
    filename_query: Optional[str] = Query(None, alias="filename")
):
    # Prioritize form data over query parameters
    upload = upload_form if upload_form is not None else (upload_query if upload_query is not None else False)
    user_id = user_id_form if user_id_form is not None else (user_id_query if user_id_query is not None else "anonymous")
    filename = filename_form if filename_form is not None else filename_query
    # Read image bytes
    image_bytes = await file.read()

    # Remove background
    output_bytes = remove(image_bytes)

    # Load the output into a PIL Image to return as PNG
    output_image = Image.open(BytesIO(output_bytes))
    byte_io = BytesIO()
    output_image.save(byte_io, format="PNG")
    byte_io.seek(0)

    # If upload is not requested, return the image directly
    if not upload:
        return StreamingResponse(byte_io, media_type="image/png")

    # If upload is requested, upload to cloud storage
    try:
        # Generate a unique filename if none provided
        if not filename:
            original_filename = file.filename
            file_extension = os.path.splitext(original_filename)[1] if original_filename else ".png"
            filename = f"{uuid.uuid4()}{file_extension}"
        # Ensure filename has an extension
        elif not os.path.splitext(filename)[1]:
            filename = f"{filename}.png"

        # Reset file pointer for upload
        byte_io.seek(0)

        # Prepare the form data for upload
        files = {
            "stream": (filename, byte_io.getvalue()),
            "filename": (None, filename),
            "senitize": (None, "false")
        }

        # Upload to cloud storage
        response = requests.post(CLOUD_STORAGE_API, files=files)

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to upload to cloud storage")

        # Get the URL from cloud storage
        image_url = response.text

        # Return the URL and metadata
        return JSONResponse({
            "url": image_url,
            "filename": filename,
            "userId": user_id
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading image: {str(e)}")
