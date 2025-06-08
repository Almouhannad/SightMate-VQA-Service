from typing import Any, Dict, Optional
from src.infrastructure.adapters.vqa.vlm.enums import GenerationParams, PromptNames
from src.infrastructure.adapters.vqa.vlm.config import vlm_settings

def load_prompt(prompt: PromptNames) -> str:
    path = ''
    try:
        path = getattr(vlm_settings, f"{prompt.value}_prompt_path")
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise RuntimeError(f"Prompt '{prompt.value}' file not found at {path}")
    except Exception as e:
        raise RuntimeError(f"Error loading prompt '{prompt.value}' file: {str(e)}")

def get_generation_params(
    overrides: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    required_keys = [
        GenerationParams.MODEL,
        GenerationParams.TEMPERATURE,
        GenerationParams.TOP_K,
        GenerationParams.TOP_P,
        GenerationParams.MIN_P,
        GenerationParams.REPEAT_PENALTY,
    ]

    missing = [param.value for param in required_keys if not hasattr(vlm_settings, param.value)]
    if missing:
        raise RuntimeError(f"Missing generation settings in vlm_settings: {missing}")

    gen_params: Dict[str, Any] = {
        GenerationParams.MODEL.value: vlm_settings.model,
        GenerationParams.TEMPERATURE.value: vlm_settings.temperature,
        GenerationParams.TOP_K.value: vlm_settings.top_k,
        GenerationParams.TOP_P.value: vlm_settings.top_p,
        GenerationParams.MIN_P.value: vlm_settings.min_p,
        GenerationParams.REPEAT_PENALTY.value: vlm_settings.repeat_penalty,
    }

    if overrides:
        allowed_keys = {param.value for param in GenerationParams}
        for k, v in overrides.items():
            if k not in allowed_keys:
                raise RuntimeError(f"Unknown hyperparameter override: {k}")
            gen_params[k] = v

    return gen_params
