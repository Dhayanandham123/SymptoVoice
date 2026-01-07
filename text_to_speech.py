from gtts import gTTS
import os

def text_to_audio(text, output_path="static/output_audio/output.mp3"):
    """
    Input: text
    Output: saves audio file
    """
    tts = gTTS(text)
    tts.save(output_path)
    return output_path
