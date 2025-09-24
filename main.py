import os
import queue
import sounddevice as sd
import vosk
import sys
import json
import random
from tts import *
from functions import *
from ai_sort import *
import torch

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

thanks = ["urwelcome", "urwelcome2", "urwelcome3"]
request_count = 0
flag_ready = True
flag_commands = False
flag_browser = False
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
            
            if flag_browser:
                if text.strip() == "":
                    continue
                search_web(text)
                flag_browser = False
            
            if flag_commands and not flag_browser:
                print(text)
                if text.strip() == "":
                    continue
                answer = final_query_handler(text)
                print(answer)
                if answer == 'погода':
                    weather = get_weather('Южно-Сахалинск')
                    tts.text2speech(weather)
                elif answer == 'браузер':
                    voice_fast_callback('run-browser', chunk)
                    tts.text2speech('Что мне вбить в поиск?')
                    flag_browser = True
                    flag_commands = False
                    continue
                elif answer == 'время':
                    tts.text2speech(get_time())
                elif answer == 'стим':
                    pass
                elif answer == 'музыка':
                    pass
                elif answer == 'for_ai':
                    answer = generate_answer(text)
                    tts.text2speech(answer)
            
            if "благодарю" in text or "спасибо" in text.lower():
                voice_fast_callback(random.choice(thanks), chunk)   
            flag_ready = True
            flag_commands = False
        else:
            partial_result = rec.PartialResult()
            