import openai
import os

API_KEY = os.getenv("API_KEY")

client = openai.OpenAI(
    api_key=API_KEY,
    base_url="https://api.intelligence.io.solutions/api/v1/",
)
def generate_answer(prompt):
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct",
        messages=[
            {"role": "system", "content": "Ты - Курису Макисе. Гений из вселенной Врата Штейна. У тебя довольно саркастичный но милый характер. Отвечаешь кратко, но доводя важную суть, чтобы даже подросток понял"},
            {"role": "user", "content": f"Привет, {prompt}"},
        ],
        temperature=0.7,
        stream=False,
        max_completion_tokens=150
    )

    return response.choices[0].message.content


print(generate_answer("Расскажи про Окарина"))