import base64
import requests
from typing import Any, Dict, List, Optional
from src.infrastructure.adapters.vqa.vlm.config import vlm_settings
from src.infrastructure.adapters.vqa.vlm.initialization_helpers import get_generation_params


def build_payload(
    image_bytes: List[int],
    system_prompt: str,
    overrides: Optional[Dict[str, Any]] = None,
    text: Optional[str] = None
) -> Dict[str, Any]:
    # encode image
    img_b64 = base64.b64encode(bytes(image_bytes)).decode("ascii")
    data_uri = f"data:image/png;base64,{img_b64}"

    # build content array
    content_items: List[Dict[str, Any]] = []
    if text is not None:
        content_items.append({"type": "text", "text": text})
    content_items.append({
        "type": "image_url",
        "image_url": {"url": data_uri}
    })

    # assemble messages
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": content_items},
    ]

    # merge generation params
    generation_params = get_generation_params(overrides)

    return {
        "messages": messages,
        **generation_params
    }

def call_model_api(api_url: str, payload: Dict[str, Any]) -> str:
    try:
        response = requests.post(
            api_url,
            headers=vlm_settings.headers,
            json=payload
        )
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"API request failed: {str(e)}")

    data = response.json()
    return data["choices"][0]["message"]["content"]


def parse_model_response(response_text: str) -> str:
    if vlm_settings.strip_json_markers: # If needed
        if response_text.startswith("```json"):
            response_text = response_text[len("```json\n"):]
        if response_text.endswith("```"):
            response_text = response_text[:-3].strip()

    return response_text
