def format_advice(transcript, condition, advice):
    """
    Input: transcript text, condition, advice
    Output: nicely formatted response
    """
    response = f"Transcribed Symptoms: {transcript}\nCondition: {condition}\nAdvice: {advice}"
    return response
