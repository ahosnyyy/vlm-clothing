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
                    "You are an assistant that describes clothing in images. "
                    "You MUST NOT describe or speculate about the person's age. "
                    "Focus exclusively on visible clothing, accessories, colors, materials, and thermal properties. "
                    "Pay particular attention to the type of fabric, insulation, breathability, and whether the clothing is suited for warm or cold weather. "
                    "The description MUST be at least **4 sentences** and should help assess the thermal comfort and insulation value of the outfit.\n\n"
                    "Be precise in your CLO estimation based on visible layers, fabric thickness, and coverage."
                )
            },
            {
            'role': 'user',
            'content': (
                "description: What is in this image? Please analyze the person in this image and begin with a detailed natural language description (at least 4 sentences) of their appearance. Focus particularly on their clothing—describe the type of clothing items they are wearing, the materials (e.g., thick, light, breathable), colors, patterns, and any distinctive features or textures. Assess whether the clothing suggests the person is dressed for warm or cold weather, and explain why based on the visible attire.\n\n"
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
                "8. Include the insulation value (CLO) as a sentence in the clo_insulation_text, e.g., 'The estimated CLO value is X, which means...'. Explain what the CLO value indicates about thermal comfort and appropriate weather conditions."

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
    
    # Update the CLO text description
    analysis.clo_insulation_text = f"The estimated CLO value is {calculated_clo}, which means {get_clo_description(calculated_clo)}"
    
    return analysis

def get_clo_description(clo_value: float) -> str:
    """
    Returns a description of what the CLO value indicates about thermal comfort.
    
    Args:
        clo_value: The calculated CLO value
        
    Returns:
        A description of the thermal comfort
    """
    if clo_value < 0.3:
        return "the person is dressed in very minimal clothing suitable only for very hot environments or indoor settings with high temperatures."
    elif clo_value < 0.6:
        return "the person is dressed in light summer clothing suitable for warm weather conditions."
    elif clo_value < 1.0:
        return "the person is dressed in moderate clothing suitable for mild or temperate weather conditions."
    elif clo_value < 1.5:
        return "the person is dressed in business attire or light winter clothing suitable for cool weather conditions."
    elif clo_value < 2.0:
        return "the person is dressed in medium winter clothing with multiple layers suitable for cold weather conditions."
    elif clo_value < 2.6:
        return "the person is dressed in heavy winter clothing suitable for very cold weather conditions."
    else:
        return "the person is dressed in extreme cold weather gear suitable for arctic or extremely cold conditions."