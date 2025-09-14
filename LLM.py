from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

GENMODEL = "google/flan-t5-large"   
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

tok = AutoTokenizer.from_pretrained(GENMODEL)
gen = AutoModelForSeq2SeqLM.from_pretrained(GENMODEL).to(DEVICE)

def generateanswer(prompt, max_new_tokens=150):
    inputs = tok(prompt, return_tensors="pt", truncation=True, max_length=2048).to(DEVICE)
    out = gen.generate(**inputs, max_new_tokens=max_new_tokens)
    answer = tok.decode(out[0], skip_special_tokens=True)
    return answer

# query = "tell me a lot about AI"
# answer = generateanswer(query)
# print("Запрос\n", query)
# print("\nСгенерированный ответ\n", answer)