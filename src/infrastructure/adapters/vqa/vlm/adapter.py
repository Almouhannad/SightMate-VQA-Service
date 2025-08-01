from src.core.config import CONFIG
from src.domain.models.input.captioning_input import CaptioningInput
from src.domain.models.input.question_input import QuestionInput
from src.domain.models.output.response import Response
from src.domain.ports.vqa_port import VqaPort
from src.infrastructure.adapters.vqa.registry import register_adapter
from src.infrastructure.adapters.vqa.vlm.config import vlm_settings
from src.infrastructure.adapters.vqa.vlm.enums import PromptNames
from src.infrastructure.adapters.vqa.vlm.initialization_helpers import load_prompt
from src.infrastructure.adapters.vqa.vlm.processing_helpers import build_payload, call_model_api, parse_model_response

@register_adapter("vlm")
class VlmVqaAdapter(VqaPort):
    def __init__(self):
        # Build base API URL
        self.api_url = vlm_settings.get_full_api_url(CONFIG.lms_api)
        # Load prompts
        self._prompts_texts = {}
        self._prompts_texts[PromptNames.QUESTION] = load_prompt(PromptNames.QUESTION)
        self._prompts_texts[PromptNames.CAPTIONING] = load_prompt(PromptNames.CAPTIONING)

    def process_captioning(self, captioning_input: CaptioningInput) -> Response:
        image_bytes = captioning_input.image.bytes
        overrides = captioning_input.options

        payload = build_payload(
            image_bytes=image_bytes,
            system_prompt=self._prompts_texts[PromptNames.CAPTIONING],
            overrides=overrides,
            history=captioning_input.history
        )

        raw_response = call_model_api(self.api_url, payload)
        parsed_output = parse_model_response(raw_response)
        
        return Response(output=parsed_output)
    
    def process_question(self, question_input: QuestionInput) -> Response:
        image_bytes = question_input.image.bytes
        question = question_input.question
        overrides = question_input.options

        payload = build_payload(
            image_bytes=image_bytes,
            system_prompt=self._prompts_texts[PromptNames.QUESTION],
            overrides=overrides,
            text=question,
            history=question_input.history
        )

        raw_response = call_model_api(self.api_url, payload)
        parsed_output = parse_model_response(raw_response)
        # print(payload)
        return Response(output=parsed_output)