from typing import Dict, Optional
from pydantic import BaseModel

from src.domain.models.input.image_input import ImageInput


class QuestionInput(BaseModel):
    image: ImageInput
    question: str
    options: Optional[Dict[str, object]] = None