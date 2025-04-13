from pydantic import BaseModel
from typing import Literal, List

class AnalyzeRequest(BaseModel):
    model: str = "llama3.2-vision:11b"

class ClothingAnalysis(BaseModel):
    description: str = Field(
        ...,
        description=(
            "A detailed natural language description of the person in the image. "
            "Focus on their clothing: mention each clothing item, its type, material "
            "(e.g., thick or light), color, patterns, textures, and other noticeable features. "
            "Also, assess whether the person appears dressed for warm or cold weather, and explain why "
            "based on the clothing."
        )
    )
    clothing_type: List[Literal[
        "t-shirt", "shirt", "sweater", "hoodie", "jacket", "coat", "blazer",
        "dress", "tank top", "suit", "vest", "cardigan",
        "jeans", "pants", "trousers", "shorts", "skirt", "leggings", "joggers"
    ]]
    sleeve_length: Literal['short', 'long', 'sleeveless', 'unknown']
    color: str
    glasses: bool
    headwear: bool
    accessories: List[Literal[
        "scarf", "gloves", "belt", "watch", "necklace", "bracelet", "earrings", "bag", "tie", "none"
    ]]
