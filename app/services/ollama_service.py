import ollama
import os
from app.schemas.clothing import ClothingAnalysis
from app.core.settings import settings

def analyze_image(image_path: str, model: str = settings.model_name) -> str:
    response = ollama.chat(
        model=model,
        options={'temperature': settings.model_temperature},
        format=ClothingAnalysis.model_json_schema(),
        messages=[{
            'role': 'user',
            'content': (
                "What is in this image? Please analyze the person in this image and begin with a detailed natural language description (at least 4 sentences) of their appearance. Focus particularly on their clothing—describe the type of clothing items they are wearing, the materials (e.g., thick, light, breathable), colors, patterns, and any distinctive features or textures. Assess whether the clothing suggests the person is dressed for warm or cold weather, and explain why based on the visible attire.\n\n"
                "After the description, please answer the following questions:\n"
                "1. What type of clothing is the person wearing, including layers? (e.g., t-shirt, sweater, jacket, etc.)\n"
                "2. Is the sleeve length short, long, or sleeveless?\n"
                "3. What is the color of the clothing?\n"
                "4. Is the person wearing glasses? (Yes or No)\n"
                "5. Is the person wearing any headwear? (Yes or No)\n"
                "6. Is the person wearing any accessories? (e.g., scarf, gloves, belt, etc.)"
            ),
            'images': [image_path]
        }]
    )
    return response['message']['content']
