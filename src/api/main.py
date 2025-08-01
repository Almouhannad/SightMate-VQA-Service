from fastapi import Depends, FastAPI
from src.api.dependencies.authentication import authenticate_api_key
from src.api.dependencies.vqa_adapter import get_vqa_port
from src.core.config import CONFIG
from src.domain.authentication.api_key import ApiKey
from src.domain.models.input.captioning_input import CaptioningInput
from src.domain.models.input.question_input import QuestionInput
from src.domain.models.output.response import Response
from src.domain.ports.vqa_port import VqaPort
from src.api.schemas import HealthResponse
from src.infrastructure.authentication.api_key_repositories.registry import get_api_key_repository

app = FastAPI(title="VQA Service")

@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse()

@app.post(
    "/vqa/captioning",
    response_model=Response,
    summary="Run IC on an uploaded image",
    description="Accepts an image file, performs IC, and returns image caption"
)
def predict(
    captioning_input: CaptioningInput,
    vqa_port: VqaPort = Depends(get_vqa_port),
    _ = Depends(authenticate_api_key),
) -> Response:
    response = vqa_port.process_captioning(captioning_input)
    return response

@app.get("/create_key", response_model=ApiKey)
async def create_api_key() -> ApiKey:
    api_key_repo = get_api_key_repository(CONFIG.api_key_repository)()
    return await api_key_repo.create()

@app.post(
    "/vqa/question",
    response_model=Response,
    summary="Answer question about uploaded image.",
    description="Accepts an image file, performs QA, and returns anwer"
)
def answer(
    question_input: QuestionInput,
    vqa_port: VqaPort = Depends(get_vqa_port),
    _ = Depends(authenticate_api_key),
) -> Response:
    response = vqa_port.process_question(question_input)
    return response