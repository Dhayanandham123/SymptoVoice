import whisper

# Load Whisper model (small.en)
model = whisper.load_model("small.en")

def transcribe_audio(audio_path):
    """
    Input: path to audio file (.wav/.mp3)
    Output: transcribed text
    """
    result = model.transcribe(audio_path)
    return result['text']
