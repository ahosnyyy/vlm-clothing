import ollama
import os
import json
from app.schemas.clothing import ClothingAnalysis
from app.core.settings import settings
from app.services.clo_service import calculate_clo_value

def analyze_image(image_path: str, model: str = settings.model_name) -> ClothingAnalysis:
    response = ollama.chat(
        model=model,
        options={'temperature': settings.model_temperature},
        format=ClothingAnalysis.model_json_schema(),
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an assistant that describes clothing in images CONCISELY yet INFORMATIVELY. "
                    "You MUST NOT describe or speculate about the person's age. "
                    "Focus exclusively on visible clothing, accessories, colors, materials, and thermal properties. "
                    "Keep your descriptions focused and informative - use 3-4 short sentences. "
                    "Be clear about whether the clothing is suited for warm or cold weather and provide brief reasoning.\n\n"
                    "Be precise in your CLO estimation based on visible layers, fabric thickness, and coverage."
                )
            },
            {
            'role': 'user',
            'content': (
                "description: What is in this image? Please analyze the person in this image and provide a CONCISE yet INFORMATIVE description (4-5 short sentences) of their clothing. Include details about the type of clothing items, materials, colors, and key features. Assess whether the outfit is suited for warm or cold weather and provide brief reasoning based on the visible clothing layers and materials.\n\n"
                "After the description, please answer the following questions:\n"
                "1. What type of clothing is the person wearing? (e.g., t-shirt, sweater, jacket, etc.)\n"
                "2. Is the sleeve length short, long, or sleeveless?\n"
                "3. What is the color of the clothing?\n"
                "4. Is the person wearing glasses? (Yes or No)\n"
                "5. Is the person wearing any headwear? (Yes or No)\r\n"
                "6. Is the person wearing any accessories? (e.g., scarf, gloves, belt, etc.)\r\n"
                "7. Estimate the CLO value of the clothing based on its thermal insulation properties using this precise scale:\n"
                    "0.0 = Nude (no clothing)\n"
                    "0.1–0.3 = Very minimal clothing (e.g., underwear, tank top alone, very thin shorts)\n"
                    "0.4–0.6 = Light summer clothing:\n"
                    "   - T-shirt or polo t-shirt with shorts\n"
                    "   - Tank top with light pants/jeans/skirt\n"
                    "   - Light dress\n"
                    "   - Shorts with light shirt\n"
                    "0.7–0.9 = Light business casual or moderate clothing:\n"
                    "   - Shirt with trousers/pants/jeans\n"
                    "   - Dress with light cardigan\n"
                    "   - Polo t-shirt with pants/jeans\n"
                    "   - Light sweater with pants/leggings\n"
                    "   - Vest over shirt with pants\n"
                    "1.0 = Typical business suit or equivalent:\n"
                    "   - Full suit (blazer and trousers)\n"
                    "   - Dress with blazer\n"
                    "   - Shirt, vest, and trousers combination\n"
                    "1.1–1.4 = Light winter clothing or heavier business wear:\n"
                    "   - Light jacket with shirt and pants/jeans\n"
                    "   - Hoodie with jeans/pants/joggers\n"
                    "   - Cardigan over shirt with pants/skirt\n"
                    "   - Sweater with pants/jeans/leggings\n"
                    "1.5–1.9 = Multiple layers, medium winter clothing:\n"
                    "   - Jacket over sweater/hoodie with pants/jeans\n"
                    "   - Light coat with multiple layers underneath\n"
                    "   - Blazer over sweater with pants and accessories\n"
                    "2.0–2.5 = Heavy winter clothing:\n"
                    "   - Heavy coat with sweater/hoodie and pants/jeans\n"
                    "   - Multiple thick layers (e.g., coat, jacket, sweater combination)\n"
                    "   - Thick winter jacket with thermal layers\n"
                    "2.6–3.0 = Arctic or extreme cold weather gear:\n"
                    "   - Heavy insulated coat with multiple thermal layers\n"
                    "   - Specialized extreme weather clothing\n\n"
                "8. For the clo_insulation_text field, provide a single short sentence that states the exact CLO value and explains what it means for thermal comfort. Example: 'CLO value of 0.8 provides light insulation for mild conditions.' Keep it extremely brief (max 15 words)."

            ),
            'images': [image_path]
        }]
    )
    # Parse the JSON response
    content = response['message']['content']
    
    # Convert the JSON string to a ClothingAnalysis object
    analysis = ClothingAnalysis.model_validate_json(content)
    
    # Calculate the CLO value based on the detected clothing items
    calculated_clo = calculate_clo_value(analysis)
    
    # Update the CLO value in the analysis
    analysis.clo_insulation = calculated_clo
    
    # Generate a short text about the CLO value
    analysis.clo_insulation_text = f"CLO value of {calculated_clo} provides {get_thermal_comfort(calculated_clo)}."
    
    return analysis

def get_thermal_comfort(clo_value: float) -> str:
    """
    Returns a very brief description of the thermal comfort for a given CLO value.
    
    Args:
        clo_value: The calculated CLO value
        
    Returns:
        A brief thermal comfort description
    """
    if clo_value < 0.3:
        return "minimal insulation for very hot conditions"
    elif clo_value < 0.6:
        return "light insulation for warm conditions"
    elif clo_value < 1.0:
        return "moderate insulation for mild conditions"
    elif clo_value < 1.5:
        return "standard insulation for cool conditions"
    elif clo_value < 2.0:
        return "substantial insulation for cold conditions"
    elif clo_value < 2.6:
        return "heavy insulation for very cold conditions"
    else:
        return "maximum insulation for extreme cold"

# Function removed as we're now using the VLM-generated text directly