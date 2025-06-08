from src.domain.ports.vqa_port import VqaPort
from src.infrastructure.adapters.vqa.registry import get_adapter
from src.core.config import CONFIG

# Instantiate once and reuse (like a singleton)
_adapter_instance: VqaPort | None = None

def get_vqa_port() -> VqaPort:
    global _adapter_instance
    if _adapter_instance is None:
        AdapterCls = get_adapter(CONFIG.vqa_adapter)
        _adapter_instance = AdapterCls()
    return _adapter_instance