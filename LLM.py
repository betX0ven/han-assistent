from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

GENMODEL = "google/flan-t5-large"   
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

tok = AutoTokenizer.from_pretrained(GENMODEL)
gen = AutoModelForSeq2SeqLM.from_pretrained(GENMODEL).to(DEVICE)

def generateanswer(prompt, max_new_tokens=800):
    prompt = f'Answer this question in detail (200-300 words): {prompt}'
    inputs = tok(prompt, return_tensors="pt", truncation=True, max_length=1024).to(DEVICE)
    out = gen.generate(
    **inputs,
    max_new_tokens=800,
    do_sample=True,
    temperature=0.8,
    top_p=0.9,
    top_k=50,
    no_repeat_ngram_size=3,
    )
    answer = tok.decode(out[0], skip_special_tokens=True)
    return answer

print(generateanswer("tell me about ai"))
