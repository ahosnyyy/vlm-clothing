from pydantic import BaseModel, Field
from typing import Literal, List

class AnalyzeRequest(BaseModel):
    model: str = "llama3.2-vision:11b"

class ClothingAnalysis(BaseModel):
    description: str = Field(
        ...,
        description=(
            "A concise yet informative description of the person's clothing in the image. "
            "Mention each clothing item, its type, material, color, and key features. "
            "In 3-4 short sentences, assess whether the outfit is suited for warm or cold weather "
            "and provide brief reasoning based on the visible clothing layers and materials. "
            "Be clear and focused while providing sufficient detail."
        )
    )
    clothing_type: List[Literal[
        "t-shirt", "shirt", "sweater", "hoodie", "jacket", "coat", "blazer",
        "pants", "dress pants", "dress", "tank top", "suit", "vest", "cardigan", "polo t-shirt",
        "jeans", "trousers", "shorts", "skirt", "leggings", "joggers"
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
            "Must be between 0.0 and 3.0. Detailed scale: "
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
        )

    )
    clo_insulation_text: str = Field(
        ...,
        description=(
            "Focus on the technical aspects of the CLO value that complement the general description. "
            "Include specific temperature ranges this outfit would be comfortable in, "
            "potential modifications to improve thermal comfort (adding/removing layers), "
            "and physiological considerations (e.g., activity level impact, wind/humidity effects). "
            "Avoid repeating general weather suitability already covered in the description."
        )
    )