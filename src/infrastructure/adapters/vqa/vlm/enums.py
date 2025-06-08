from enum import Enum
class PromptNames(Enum):
    CAPTIONING = 'captioning'
    QUESTION = 'question'    

class GenerationParams(Enum):
    MODEL = "model"
    TEMPERATURE = "temperature"
    TOP_K = "top_k"
    TOP_P = "top_p"
    MIN_P = "min_p"
    REPEAT_PENALTY = "repeat_penalty"
