from PIL import Image
from io import BytesIO

def generate_vqa_sample(image_bytes: list[int], question: str):
    SYSTEM_PROMPT  = \
    """You are a visual question answering assistant for visually impaired users.
    When given an image with a question, answer the question with a single detailed sentence that shows the answer and explains the most important visual elements related to the answer of the question (objects, actions, context, colors, and spatial relationships).
    Answer in no more than one short sentence.
    Use simple words. Output the answer only.
    If you can't answer, tell that."""
    image = Image.open(BytesIO(bytes(image_bytes)))
    image = image.resize((512, 512))  
    conversation = [
        {
            "role": "system",
            "content": [{"type": "text", "text": SYSTEM_PROMPT}],
        },
        {
            "role": "user",
            "content" : [
                {"type" : "text",  "text"  : question},
                {"type" : "image", "image" : image}
            ]
        }
    ]
    return { "messages" : conversation }    


def generate_instructions_sample(image_bytes: list[int], question: str):
    SYSTEM_PROMPT = \
    """You are assisting a blind user who has submitted an image along with a question, but the image does not provide enough information to answer it. Gently guide the user to retake the image by giving a single, clear sentence that includes both the necessary instruction and supportive encouragement. Your response must be:
    Feasible for a blind user (use concepts like phone positioning, body references, or audio cues). 
    Emotionally supportive and respectful. 
    Concise—only one helpful and encouraging sentence per response."""
    image = Image.open(BytesIO(bytes(image_bytes)))
    image = image.resize((512, 512))  
    conversation = [
        {
            "role": "system",
            "content": [{"type": "text", "text": SYSTEM_PROMPT}],
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": question},
                {"type": "image", "image": image}
            ]
        }
    ]
    return {"messages": conversation}
