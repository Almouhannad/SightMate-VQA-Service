from typing import Dict, Optional
from pydantic import BaseModel

from src.domain.models.input.image_input import ImageInput


class CaptioningInput(BaseModel):
    image: ImageInput
    options: Optional[Dict[str, object]] = None