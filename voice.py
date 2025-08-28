import pyaudio  
import wave  
  
#define stream chunk   
chunk = 1024  
  
  
def voice_callback(ans_text, chank):
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
  
