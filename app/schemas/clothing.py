from pydantic import BaseModel, Field
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
    clo_insulation: float = Field(
        ...,
        ge=0,
        le=3.0,
        description=(
            "Estimated CLO value based on the clothing's thermal insulation properties. "
            "Must be between 0 and 3.0. (e.g., naked ≈ 0, light summer shirt ≈ 0.5 CLO, winter coat ≈ 3.0 CLO)"
        )
    )
    clo_insulation_text: str = Field(
        ...,
        description=(
            "Include the insulation value (CLO) as a sentence, e.g., 'The estimated CLO value is X, which means...'. "
        )
    )