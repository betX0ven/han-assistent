import pyaudio  
import wave  

from answer_create import *

#define stream chunk   
chunk = 1024  
  
  
def voice_callback(ans_text, chunk):
  try:
    #open a wav format music  
    f = wave.open(f"answers/{ans_text}.wav","rb")  
    #instantiate PyAudio  
    p = pyaudio.PyAudio()  
    #open stream  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    #read data  
    data = f.readframes(chunk)  
      
    #play stream  
    while data:  
        stream.write(data)  
        data = f.readframes(chunk)  
      
    #stop stream  
    stream.stop_stream()  
    stream.close()  
      
    #close PyAudio  
    p.terminate()  
  except Exception:
    #open a wav format music  
    f = wave.open(f"answers/error.wav","rb")  
    #instantiate PyAudio  
    p = pyaudio.PyAudio()  
    #open stream  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    #read data  
    data = f.readframes(chunk)  
      
    #play stream  
    while data:  
        stream.write(data)  
        data = f.readframes(chunk)  
      
    #stop stream  
    stream.stop_stream()  
    stream.close()  
      
    #close PyAudio  
    p.terminate()  
  
  
def voice_for_answer(ans_text, chunk):
  try:
    #open a wav format music  
    f = wave.open(f"{ans_text}.wav","rb")  
    #instantiate PyAudio  
    p = pyaudio.PyAudio()  
    #open stream  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    #read data  
    data = f.readframes(chunk)  
      
    #play stream  
    while data:  
        stream.write(data)  
        data = f.readframes(chunk)  
      
    #stop stream  
    stream.stop_stream()  
    stream.close()  
      
    #close PyAudio  
    p.terminate()  
  except Exception:
    #open a wav format music  
    f = wave.open(f"answers/error.wav","rb")  
    #instantiate PyAudio  
    p = pyaudio.PyAudio()  
    #open stream  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    #read data  
    data = f.readframes(chunk)  
      
    #play stream  
    while data:  
        stream.write(data)  
        data = f.readframes(chunk)  
      
    #stop stream  
    stream.stop_stream()  
    stream.close()  
      
    #close PyAudio  
    p.terminate()    
  
def voice_answer(text):
  text_to_speech(text)
  voice_for_answer(text, chunk)