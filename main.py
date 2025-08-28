import os
import queue
import sounddevice as sd
import vosk
import sys
import json

from voice import *
from functions import *
from ai_sort import *

import torch
# Задаём параметры аудио
samplerate = 16000  
device = None       
channels = 1
chunk = 1024  

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
    voice_callback('ready', chunk)
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = rec.Result()
            text = json.loads(result).get("text", "")
            
            if flag_ready:
                if text=='хан':
                    voice_callback('hello-night', chunk)
                    flag_ready=False
                    flag_commands=True
                    request_count+=1
                elif text == 'хан' and request_count >= 1:
                    voice_callback('hello', chunk)
                    flag_ready=False
                    flag_commands=True
            
            if flag_commands:
                if text.strip() == "":
                    continue
                answer = final_query_handler(text)
                print('Флаг включен')
                if answer == 'погода':
                    print(get_weather(text))
                    voice_for_answer(get_weather(text), chunk)
                elif answer == 'браузер':
                    pass
                elif answer == 'время':
                    pass
                elif answer == 'стим':
                    pass
                elif answer == 'музыка':
                    pass
            listening_for_activation = True
            listening_for_commands = False
        else:
            partial_result = rec.PartialResult()
            



# if text == 'хан':
#                 voice_callback('hello-night', chunk)
#                 flag=True
#                 request_count+=1
#                 if flag:
#                     result = rec.Result()
#                     text = json.loads(result).get("text", "")
#                     answer = final_query_handler(text)
#                     print('Флаг включен')
#                     if answer == 'погода':
#                         print(get_weather(text))
#                         voice_for_answer(get_weather(text), chunk)
#                     elif answer == 'браузер':
#                         pass
#                     elif answer == 'время':
#                         pass
#                     elif answer == 'стим':
#                         pass
#                     elif answer == 'музыка':
#                         pass
                    
#                     flag = False 
#             elif text == 'хан' and request_count >= 1:
#                 voice_callback('hello', chunk)
#                 flag=True    
#                 if flag:
#                     answer = final_query_handler(text)
#                     print('Флаг включен')
#                     if answer == 'погода':
#                         print(get_weather(text))
#                         voice_for_answer(get_weather(text), chunk)
#                     elif answer == 'браузер':
#                         pass
#                     elif answer == 'время':
#                         pass
#                     elif answer == 'стим':
#                         pass
#                     elif answer == 'музыка':
#                         pass
                    
#                     flag = False
                
            