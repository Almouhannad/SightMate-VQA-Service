import torch
from torch.nn.functional import normalize
DEVICE  = "cuda" if torch.cuda.is_available() else "cpu"
def generate_input_embedding(model, tokenizer, sample):
    
    messages = [sample["messages"][0], sample["messages"][1]]
    image = sample["messages"][1]["content"][1]['image']

    conversation_template = tokenizer.apply_chat_template(messages, add_generation_prompt=True)
    inputs = tokenizer \
    (
        images=[image],
        text  = conversation_template,
        add_special_tokens=False, # Template already contain those
        return_tensors="pt",
    ).to(DEVICE)
    with torch.no_grad(): # don’t allocate or compute any backwards info (inference only)
        outs = model \
        (
            **inputs,
            output_hidden_states=True,
            return_dict=True
        )
    last = outs.hidden_states[-1]
    mask = inputs['attention_mask'] # To distinguish between original and padding tokens
    question_vec = (last * mask.unsqueeze(-1)).sum(1) / mask.sum(1, keepdim=True) # Mean pooling
    question_vec = normalize(question_vec, dim=-1) # L2 norm
    
    return question_vec, inputs, image, messages

def generate_output_embedding(model, tokenizer, sample):
    question_vec, inputs, image, messages = generate_input_embedding(model, tokenizer, sample)    
    gen_ids = model.generate \
    (
        **inputs,
        max_new_tokens=128,
        do_sample=False
    )
    q_len = inputs.input_ids.shape[1]
    answer_txt = tokenizer.decode(gen_ids[0, q_len:], skip_special_tokens=True).strip()
    messages2  = \
    [
        messages[0],
        messages[1],
        {
            "role": "assistant",
            "content": 
            [
                {"type": "text",  "text": answer_txt},
            ]
        }
    ]
    templ2 = tokenizer.apply_chat_template(messages2, tokenize=False)
    full_in = tokenizer \
    (
        text = templ2,
        images = [image],
        return_tensors="pt"
    ).to(DEVICE)

    with torch.no_grad():
        ans_out = model \
        (
            **full_in,
            output_hidden_states=True,
            return_dict=True
        )

    ans_last  = ans_out.hidden_states[-1][:, q_len:, :] # Get only the answer embedding
    ans_mask  = full_in['attention_mask'][:, q_len:]
    # mean pooling + L2 norm
    answer_vec = (ans_last * ans_mask.unsqueeze(-1)).sum(1) / ans_mask.sum(1, keepdim=True)
    answer_vec = normalize(answer_vec, dim=-1)

    return answer_vec, question_vec, answer_txt
