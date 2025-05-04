from pydantic import BaseModel, Field
from typing import Literal, List

class AnalyzeRequest(BaseModel):
    model: str = "llama3.2-vision:11b"

class ClothingAnalysis(BaseModel):
    description: str = Field(
        ...,
        description=(
            "A detailed natural language description of the person in the image."
            "**DO NOT describe or infer the person's age in any way. Avoid all age-related terms (e.g., young, old, elderly, child, etc.).**\n\n"
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
    clo_insulation: float = Field(
        ...,
        description=(
            "Estimated CLO value based on the clothing's thermal insulation properties. "
            "For example, a light summer shirt ≈ 0.3 CLO, a full winter coat ≈ 1.0 CLO."
        )
    )
