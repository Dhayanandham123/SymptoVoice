from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load Bio_ClinicalBERT
MODEL_NAME = "emilyalsentzer/Bio_ClinicalBERT"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

def analyze_symptoms(text):
    """
    Input: transcribed text
    Output: possible conditions + simple advice
    """
    # For demo: simple encoding, softmax to get probabilities
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = model(**inputs).logits

    # Simplified: just pick highest scoring label (demo)
    # In practice, map logits → actual medical conditions using your labels
    probs = torch.softmax(outputs, dim=1)
    top_idx = torch.argmax(probs, dim=1).item()
    
    # Demo conditions (replace with real mapping)
    CONDITIONS = ["Flu", "Cold", "Allergy", "Headache", "Heartburn"]
    condition = CONDITIONS[top_idx % len(CONDITIONS)]
    advice = f"Based on your symptoms, possible condition: {condition}. Please consult a doctor if symptoms persist."

    return condition, advice
