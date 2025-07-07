from unsloth import FastVisionModel
import torch
import torch.nn as nn
from SMSA.helpers.embeddings import generate_output_embedding
from SMSA.helpers.samples_generator import generate_vqa_sample, generate_instructions_sample

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class SMSA:
    def __init__(self, model_path: str, selector_path: str):
        self.__model_path = model_path
        self.__selector_path = selector_path
        self.__initialized = False

    class __SMSASelector(nn.Module):
        def __init__(self):
            super().__init__()
            self.net = nn.Sequential(
                nn.LayerNorm(3584),
                nn.Linear(3584, 512),
                nn.ReLU(),
                nn.Dropout(0.25),
                nn.Linear(512, 1))
        def forward(self, x): return self.net(x).squeeze(-1)             

    def initialize(self):
        # First, load model
        self.__model, self.__tokenizer = FastVisionModel.from_pretrained(
            self.__model_path,
            load_in_4bit=True,
            use_gradient_checkpointing="unsloth"
        )
        FastVisionModel.for_inference(self.__model)
        self.__model = self.__model.to(torch.bfloat16)
        # Second, load selector
        self.__selector = self.__SMSASelector()
        self.__selector.load_state_dict(torch.load(self.__selector_path))
        self.__selector.to(DEVICE, dtype=torch.bfloat16)
        self.__selector.eval()
        
        self.__initialized = True

    
    def process_vqa(self, image_bytes: list[int], question: str,  TAU: float = 0.65, threshold: float = 0.67):
        if not self.__initialized:
            self.initialize()
        vqa_sample = generate_vqa_sample(image_bytes=image_bytes, question=question)
        answer_vec, question_vec, answer_text = generate_output_embedding(
            model=self.__model, tokenizer=self.__tokenizer, sample=vqa_sample)
        
        selector_input = TAU * question_vec + (1 - TAU) * answer_vec
        selector_input.to(DEVICE, torch.bfloat16)
        selector_output = 0.0
        with torch.no_grad():
            out = self.__selector(selector_input)
            selector_output = out.item()

        answer_text_cleaned = answer_text.strip('\'"').lower()
        if answer_text_cleaned in ['unanswerable', 'unsuitable', 'unsuitable image', 'unreadable'] \
            or selector_output < threshold:

            instructions_sample = generate_instructions_sample(image_bytes=image_bytes, question=question)
            _, _, instructions_text = generate_output_embedding(
                model=self.__model, tokenizer=self.__tokenizer, sample=instructions_sample)
            
            return instructions_text.strip('\'"')
        
        return answer_text.strip('\'"')

            


