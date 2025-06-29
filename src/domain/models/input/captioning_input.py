from typing import Dict, List, Optional
from pydantic import BaseModel

from src.domain.models.input.history_item import HistoryItem
from src.domain.models.input.image_input import ImageInput


class CaptioningInput(BaseModel):
    image: ImageInput
    history: Optional[List[HistoryItem]] = None
    options: Optional[Dict[str, object]] = None