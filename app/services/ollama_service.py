import ollama
import os
from app.schemas.clothing import ClothingAnalysis
from app.core.settings import settings

def analyze_image(image_path: str, model: str = settings.model_name) -> str:
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
                    "0.0 = Nude (no clothing); "
                    "0.1–0.3 = Very minimal clothing (e.g., underwear); "
                    "0.4–0.6 = Light summer clothing (e.g., T-shirt and shorts); "
                    "0.7–0.9 = Light business casual (e.g., shirt and trousers); "
                    "1.0 = Typical business suit; "
                    "1.1–1.4 = Light winter clothing or heavier business wear; "
                    "1.5–1.9 = Multiple layers, medium winter clothing; "
                    "2.0–2.5 = Heavy winter clothing (e.g., coat, thermal layers); "
                    "2.6–3.0 = Arctic or extreme cold weather gear.\n"
                "8. Include the insulation value (CLO) as a sentence in the clo_insulation_text, e.g., 'The estimated CLO value is X, which means...'. Explain what the CLO value indicates about thermal comfort and appropriate weather conditions."

            ),
            'images': [image_path]
        }]
    )
    return response['message']['content']