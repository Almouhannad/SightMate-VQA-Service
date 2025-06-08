from src.core.config import CONFIG
from src.domain.models.input.captioning_input import CaptioningInput
from src.domain.models.input.question_input import QuestionInput
from src.domain.models.output.response import Response
from src.domain.ports.vqa_port import VqaPort
from src.infrastructure.adapters.vqa.vlm.config import vlm_settings
from src.infrastructure.adapters.vqa.vlm.enums import PromptNames
from src.infrastructure.adapters.vqa.vlm.initialization_helpers import get_generation_params, load_prompt


class VlmVqaAdapter(VqaPort):
    def __init__(self):
        # Build base API URL
        self.api_url = vlm_settings.get_full_api_url(CONFIG.lms_api)
        # Load prompts
        self._prompts_texts = {}
        self._prompts_texts[PromptNames.QUESTION] = load_prompt(PromptNames.QUESTION)
        self._prompts_texts[PromptNames.CAPTIONING] = load_prompt(PromptNames.CAPTIONING)
        # Load generation hyperparameters
        self._generation_params = get_generation_params()

    def process_captioning(self, captioning_input: CaptioningInput) -> Response:
        return Response(output='')
    
    def process_question(self, question_input: QuestionInput) -> Response:
        return Response(output='')