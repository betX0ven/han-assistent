import os
import queue
import sounddevice as sd
import vosk
import sys
import json

from voice import voice_callback
from functions import *

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


with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
                       channels=channels, callback=callback):
    print("Начинаю распознавание. Говорите...\n")
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = rec.Result()
            text = json.loads(result).get("text", "")
            print(f"Распознано: {text}")
            
            flag = False
            
            if text == 'кира':
                voice_callback('test', chunk)
                flag=True
            if flag:
                pass
            
            
        else:
            partial_result = rec.PartialResult()
            

            