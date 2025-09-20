from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def analyze_text(entry):
    result = sentiment_pipeline(entry)[0]
    label = result.get('label', "3 stars")
    
    try:
        numeric_rating = int(label.split()[0])
    except:
        numeric_rating = 3
        
    # Convert numeric rating to a simple label
    if numeric_rating >= 4:
        simple_label = "Positive"
    elif numeric_rating <= 2:
        simple_label = "Negative"
    else:
        simple_label = "Neutral"
        
    return simple_label, numeric_rating