from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from app.schemas.clothing import ClothingAnalysis
from app.services.ollama_service import analyze_image
from app.utils.file_handler import save_spooled_temp_image, remove_temp_image
from datetime import datetime
import json
import traceback

router = APIRouter()

@router.post("/",  response_model=ClothingAnalysis)
async def analyze_clothing(
    image: UploadFile = File(...),
    model: str = Form("llama3.2-vision:11b")
):
    if not image.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File uploaded is not an image")
        
    temp_path = save_spooled_temp_image(image)

    try:
        try:
            # The analyze_image function now returns a ClothingAnalysis object directly
            analysis = analyze_image(temp_path, model)
            return analysis.model_dump()
        except Exception as e:
            # Capture any errors from the analyze_image function
            error_detail = str(e)
            stack_trace = traceback.format_exc()
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Error processing image",
                    "error": error_detail,
                    "trace": stack_trace
                }
            )
    finally:
        remove_temp_image(temp_path)
