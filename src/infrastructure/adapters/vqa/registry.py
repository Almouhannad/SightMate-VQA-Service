from typing import Type

from src.domain.ports.vqa_port import VqaPort


_ADAPTERS: dict[str, Type[VqaPort]] = {}

def register_adapter(name: str):
    """
    Decorator to register an VQA adapter implementation.
    
    Args:
        name: Unique identifier for the adapter
        
    Returns:
        Decorator function that registers the adapter class
    """
    def decorator(cls: Type[VqaPort]):
        _ADAPTERS[name] = cls
        return cls
    return decorator

def get_adapter(name: str) -> Type[VqaPort]:
    """
    Get an VQA adapter class by name.
    
    Args:
        name: Name of the registered adapter
        
    Returns:
        The adapter class
        
    Raises:
        ValueError: If no adapter is registered with the given name
    """
    try:
        return _ADAPTERS[name]
    except KeyError:
        raise ValueError(f"No VQA adapter registered under name {name!r}")

def list_available_adapters() -> list[str]:
    """
    Get a list of all registered adapter names.
    
    Returns:
        List of registered adapter names
    """
    return list(_ADAPTERS.keys()) 