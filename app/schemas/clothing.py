from pydantic import BaseModel
from typing import Literal, List

class AnalyzeRequest(BaseModel):
    model: str = "gemma3:12b"

class ClothingAnalysis(BaseModel):
    description: str
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
