from abc import ABC, abstractmethod

from src.domain.models.input.captioning_input import CaptioningInput
from src.domain.models.input.question_input import QuestionInput
from src.domain.models.output.response import Response

class VqaPort(ABC):

    @abstractmethod
    def process_captioning(self, captioning_input: CaptioningInput) -> Response:
        pass

    @abstractmethod
    def process_question(self, question_input: QuestionInput) -> Response:
        pass
