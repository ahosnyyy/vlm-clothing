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
        "dress", "tank top", "suit", "vest", "cardigan", "polo t-shirt",
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
            "Must be between 0.0 and 3.0. Approximate scale: "
            "0.0 = Nude (no clothing); "
            "0.1–0.3 = Very minimal clothing (e.g., underwear); "
            "0.4–0.6 = Light summer clothing (e.g., T-shirt and shorts); "
            "0.7–0.9 = Light business casual (e.g., shirt and trousers); "
            "1.0 = Typical business suit; "
            "1.1–1.4 = Light winter clothing or heavier business wear; "
            "1.5–1.9 = Multiple layers, medium winter clothing; "
            "2.0–2.5 = Heavy winter clothing (e.g., coat, thermal layers); "
            "2.6–3.0 = Arctic or extreme cold weather gear."
        )

    )
    clo_insulation_text: str = Field(
        ...,
        description=(
            "Include the insulation value (CLO) as a sentence, e.g., 'The estimated CLO value is X, which means...'. "
            "Explain what the CLO value indicates about thermal comfort and appropriate weather conditions. "
        )
    )