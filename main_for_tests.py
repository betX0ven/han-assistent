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

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

from LLM2 import generate_answer

request_count = 0
flag_ready = True
flag_commands = False
flag_browser = False

thanks = ["urwelcome", "urwelcome2", "urwelcome3"]

while True:
  text = input('>>> ')
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
          print(weather)
      elif answer == 'браузер':
          voice_fast_callback('run-browser', chunk)
          print('Что мне вбить в поиск?')
          flag_browser = True
          flag_commands = False
          continue
      elif answer == 'время':
          print(get_time())
      elif answer == 'стим':
          pass
      elif answer == 'музыка':
          pass
      elif answer == 'for_ai':
          answer = generate_answer(text)
          print(answer)
  if "благодарю" in text or "спасибо" in text.lower():
    voice_fast_callback(random.choice(thanks), chunk)
    
  flag_ready = True
  flag_commands = False
  