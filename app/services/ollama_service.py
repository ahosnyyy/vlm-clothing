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
                "You are a professional fashion analyst. Provide a detailed paragraph (at least 6 sentences) describing this person's clothing and appearance. Be thorough and avoid summarizing too briefly. Mention clothing type, materials (e.g., thick or light), colors, patterns, textures, and accessories. Also, describe what kind of weather they seem dressed for.\n\n"
                "Do not summarize. Instead, describe each clothing item individually.\n\n"
                "Example: The person is wearing a thick, bright red hoodie made of fleece material, with a front pocket and drawstrings. The sleeves are long, suggesting it’s suitable for cold weather...\n\n"
                "After the description, please answer the following questions:\n"
                "1. What type of clothing is the person wearing? (e.g., t-shirt, sweater, jacket, etc.)\n"
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
