from pydantic import BaseModel, ValidationError
import ollama
import json
from datetime import datetime
from typing import Literal, List

# Define a Pydantic model for structured JSON output
class ClothingAnalysis(BaseModel):
    description: str
    clothing_type: List[Literal[
        # Upper body
        "t-shirt", "shirt", "sweater", "hoodie", "jacket", "coat", "blazer", 
        "dress", "tank top", "suit", "vest", "cardigan",
        # Lower body
        "jeans", "pants", "trousers", "shorts", "skirt", "leggings", "joggers"
    ]]
    sleeve_length: Literal['short', 'long', 'sleeveless', 'unknown']
    color: str
    glasses: bool  # True if wearing glasses, False otherwise
    headwear: bool  # True if wearing headwear, False otherwise
    accessories: List[Literal[
        "scarf", "gloves", "belt", "watch", "necklace", "bracelet", "earrings", "bag", "tie", "none"
    ]]

# Step 1: Ask targeted questions to analyze the image
image_response = ollama.chat(
    model='gemma3:12b',
    format=ClothingAnalysis.model_json_schema(),
    messages=[{
        'role': 'user',
        'content': (
            "What is in this image? Please analyze the person in this image and start by giving a short natural language description of the person's appearance, "
            "focusing especially on their clothing. Mention the type, material (thick or light), color, and any noticeable features or textures. "
            "Include whether the person appears dressed for warm or cold weather.\n\n"
            "After the description, please answer the following questions:\n"
            "1. What type of clothing is the person wearing? (e.g., t-shirt, sweater, jacket, etc.)\n"
            "2. Is the sleeve length short, long, or sleeveless?\n"
            "3. What is the color of the clothing?\n"
            "4. Is the person wearing glasses? (Yes or No)\n"
            "5. Is the person wearing any headwear? (Yes or No)\n"
            "6. Is the person wearing any accessories? (e.g., scarf, gloves, belt, etc.)"
        ),
        'images': ['samples/F2.JPG']
    }]
)

# Step 2: Parse and validate the structured response
try:
    structured_data = json.loads(image_response['message']['content'])
    clothing_analysis = ClothingAnalysis(**structured_data)
except json.JSONDecodeError:
    print("Error: The response is not valid JSON.")
    print("Raw response:", image_response['message']['content'])
    clothing_analysis = None
except ValidationError as e:
    print("Error: The JSON structure does not match the expected schema.")
    print(e.json())
    clothing_analysis = None

# Step 3: Construct final output
output = {
    "processed_result": clothing_analysis.model_dump() if clothing_analysis else {},
    "metadata": {
        "model_used": ["gemma3:12b"],
        "timestamp": datetime.now().isoformat()
    }
}

# Step 4: Pretty print the result
print(json.dumps(output, indent=2))
