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
                "8. For the clo_insulation_text field, focus on technical aspects that complement the general description. Include specific temperature ranges this outfit would be comfortable in (e.g., '65-75°F/18-24°C'), potential modifications to improve thermal comfort (adding/removing layers), and physiological considerations (e.g., activity level impact, wind/humidity effects). Avoid repeating general weather suitability already covered in the description."

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
    analysis.clo_insulation_text = f"The estimated CLO value is {calculated_clo:.1f}. {get_clo_description(calculated_clo).format(calculated_clo)}"
    
    return analysis

def get_clo_description(clo_value: float) -> str:
    """
    Returns a technical description of what the CLO value indicates about thermal comfort,
    focusing on aspects that complement the general clothing description.
    
    Args:
        clo_value: The calculated CLO value
        
    Returns:
        A technical description of thermal comfort considerations
    """
    if clo_value < 0.3:
        return "this outfit provides minimal thermal insulation (CLO {:.1f}) and would be comfortable in temperatures above 85°F/29°C. For cooler environments, adding layers would be necessary. This ensemble is best suited for high-activity situations where heat dissipation is important."
    elif clo_value < 0.6:
        return "this outfit provides light thermal insulation (CLO {:.1f}) and would be comfortable in temperatures between 75-85°F/24-29°C. In breezier conditions or air-conditioned spaces, a light additional layer might be beneficial."
    elif clo_value < 1.0:
        return "this outfit provides moderate thermal insulation (CLO {:.1f}) and would be comfortable in temperatures between 65-75°F/18-24°C. The outfit balances heat retention and breathability, making it versatile for varying indoor and outdoor activities."
    elif clo_value < 1.5:
        return "this outfit provides business-casual thermal insulation (CLO {:.1f}) and would be comfortable in temperatures between 55-65°F/13-18°C. For windy conditions or prolonged outdoor exposure, an additional outer layer might be beneficial."
    elif clo_value < 2.0:
        return "this outfit provides substantial thermal insulation (CLO {:.1f}) and would be comfortable in temperatures between 40-55°F/4-13°C. The layering allows for adaptation to changing conditions by removing or adding pieces as needed."
    elif clo_value < 2.6:
        return "this outfit provides significant thermal insulation (CLO {:.1f}) and would be comfortable in temperatures between 20-40°F/-7-4°C. The heavy insulation works best for low-activity situations; during higher activity, overheating may occur."
    else:
        return "this outfit provides maximum thermal insulation (CLO {:.1f}) and would be comfortable in temperatures below 20°F/-7°C. This level of insulation is specifically designed for extreme conditions and limited mobility should be expected due to the bulkiness."