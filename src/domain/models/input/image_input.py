from typing import Dict, List, Optional
import pydantic

class ImageInput(pydantic.BaseModel):
    bytes: List[int]
    metadata: Optional[Dict[str, object]] = None