from pydantic import BaseModel

class HistoryItem(BaseModel):
    question: str
    answer: str