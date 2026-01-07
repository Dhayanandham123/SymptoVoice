from flask import Flask, render_template, request
from app.speech_to_text import transcribe_audio
from app.medical_nlp import analyze_symptoms
from app.response_generator import format_advice
from app.text_to_speech import text_to_audio
import os
import uuid # Used to generate unique filenames

# Correctly configure app paths
app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Define the directory for audio files and ensure it exists
output_audio_dir = os.path.join(app.static_folder, "output_audio")
os.makedirs(output_audio_dir, exist_ok=True)

@app.route("/")
def index():
    """Renders the main homepage."""
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Handles audio processing from either a live recording or a file upload.
    """
    if "audio_file" not in request.files:
        return "No audio file found in the request.", 400

    audio_file = request.files["audio_file"]

    # Create a unique, temporary path to save the incoming audio
    temp_filename = f"{uuid.uuid4()}_{audio_file.filename or 'recording.wav'}"
    temp_audio_path = os.path.join(output_audio_dir, temp_filename)
    audio_file.save(temp_audio_path)

    try:
        # --- AI Processing Pipeline ---
        transcript = transcribe_audio(temp_audio_path)
        condition, advice = analyze_symptoms(transcript)
        response_text = format_advice(transcript, condition, advice)
        
        # --- Generate Unique Audio Response ---
        # This prevents the browser from caching old audio results
        tts_output_filename = f"response_{uuid.uuid4()}.mp3"
        tts_path = os.path.join(output_audio_dir, tts_output_filename)
        text_to_audio(response_text, output_path=tts_path)

        # This is the relative path for the template's <audio> tag
        final_audio_path_for_template = f"output_audio/{tts_output_filename}"

    except Exception as e:
        # Log the error for debugging and return a user-friendly message
        print(f"An error occurred: {e}")
        return "An error occurred during the analysis. Please try again.", 500
    
    finally:
        # --- Cleanup ---
        # Always remove the temporary uploaded file to save server space
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

    # --- Render Results ---
    return render_template("index.html", 
                           transcript=transcript, 
                           advice=response_text, 
                           audio_file=final_audio_path_for_template)