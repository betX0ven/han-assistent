from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

MODEL_NAME = "yandex/YandexGPT-5-Lite-8B-pretrain"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, legacy=False)
model = AutoModelForCausalLM.from_pretrained(
   MODEL_NAME,
   device_map="auto",
   torch_dtype="auto",
)
model = torch.compile(model)

input_text = "расскажи про квантовую механику"
input_ids = tokenizer(input_text, return_tensors="pt")

outputs = model.generate(**input_ids, max_new_tokens=18)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
