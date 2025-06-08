from typing import Dict, Optional
import pydantic

class ImageInput(pydantic.BaseModel):
    bytes: bytes
    metadata: Optional[Dict[str, object]] = None