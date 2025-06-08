from typing import Dict, Optional
from pydantic import BaseModel

from src.domain.models.input.image_input import ImageInput


class Response(BaseModel):
    output: str
    details: Optional[Dict[str, object]] = None