from src.domain.models.input.captioning_input import CaptioningInput
from src.domain.models.input.question_input import QuestionInput
from src.domain.models.output.response import Response
from src.domain.ports.vqa_port import VqaPort
from src.infrastructure.adapters.vqa.registry import register_adapter
from src.infrastructure.adapters.vqa.smsa.SMSA_lib import SMSA
from src.infrastructure.adapters.vqa.smsa.config import smsa_settings

@register_adapter("smsa")
class SMSAVqaAdapter(VqaPort):
    def __init__(self):
        self.__smsa = SMSA(model_path=smsa_settings.model_path, selector_path=smsa_settings.selector_path)
        self.__smsa.initialize()

    def process_captioning(self, captioning_input: CaptioningInput) -> Response:
        image_bytes = captioning_input.image.bytes
        answer = self.__smsa.process_ic(
            image_bytes= image_bytes,
            TAU=smsa_settings.TAU,
            threshold=smsa_settings.threshold)
        
        return Response(output=answer)
    
    def process_question(self, question_input: QuestionInput) -> Response:
        image_bytes = question_input.image.bytes
        question = question_input.question
        answer = self.__smsa.process_vqa(
            image_bytes= image_bytes,
            question=question,
            TAU=smsa_settings.TAU,
            threshold=smsa_settings.threshold)
        return Response(output=answer)