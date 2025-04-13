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
            raw_response = analyze_image(temp_path, model)
        except Exception as e:
            # Capture Ollama service errors
            error_detail = str(e)
            stack_trace = traceback.format_exc()
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Error communicating with Ollama service",
                    "error": error_detail,
                    "trace": stack_trace
                }
            )

        try:
            structured = json.loads(raw_response)
            parsed = ClothingAnalysis(**structured)

            return parsed.model_dump()
        
        except json.JSONDecodeError as e:
            return JSONResponse(
                status_code=400, 
                content={
                    "error": "Invalid JSON response from model",
                    "detail": str(e),
                    "raw": raw_response
                }
            )
        except Exception as e:
            return JSONResponse(
                status_code=422, 
                content={
                    "error": "Failed to validate model response",
                    "detail": str(e),
                    "raw": raw_response
                }
            )
    finally:
        remove_temp_image(temp_path)
