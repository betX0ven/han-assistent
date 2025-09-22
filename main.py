import os
import queue
import sounddevice as sd
import vosk
import sys
import json

from tts import *
from functions import *
from ai_sort import *
import torch

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

GENMODEL = "google/flan-t5-large"   
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

tok = AutoTokenizer.from_pretrained(GENMODEL)
gen = AutoModelForSeq2SeqLM.from_pretrained(GENMODEL).to(DEVICE)

from LLM2 import generate_answer

# Задаём параметры аудио
samplerate = 16000  
device = None       
channels = 1
chunk = 1024  

tts=TTS()

model_path = "vosk-model-ru-0.10"
if not os.path.exists(model_path):
    print(f"Модель не найдена по пути '{model_path}'")
    sys.exit(1)

model = vosk.Model(model_path)

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

rec = vosk.KaldiRecognizer(model, samplerate)


request_count = 0
flag_ready = True
flag_commands = False
with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
                       channels=channels, callback=callback):
    print("Начинаю распознавание. Говорите...\n")
    voice_fast_callback('ready', chunk)
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = rec.Result()
            text = json.loads(result).get("text", "")
            # print(text)
            if flag_ready:
                if text=='хан' and request_count == 0:
                    voice_fast_callback('hello-night', chunk)
                    flag_ready=False
                    flag_commands=True
                    text=""
                    request_count+=1
                elif text == 'хан' and request_count >= 1:
                    voice_fast_callback('hello', chunk)
                    flag_ready=False
                    flag_commands=True
                    text=""
            
            if flag_commands:
                print(text)
                if text.strip() == "":
                    continue
                answer = final_query_handler(text)
                print(answer)
                if answer == 'погода':
                    weather = get_weather('Южно-Сахалинск')
                    tts.text2speech(weather)
                elif answer == 'браузер':
                    pass
                elif answer == 'время':
                    pass
                elif answer == 'стим':
                    pass
                elif answer == 'музыка':
                    pass
                elif answer == 'for_ai':
                    answer = generate_answer(text)
                    tts.text2speech(answer)
            flag_ready = True
            flag_commands = False
        else:
            partial_result = rec.PartialResult()
            