# Keywords that may indicate crisis
CRISIS_KEYWORDS = ["suicide", "kill myself", "hopeless", "depressed", "panic"]

HELPLINES = {
    "KIRAN": "1800 599 0019",
    "AASRA": "91-9820466726",
    "Snehi": "022-2772 6771"
}

def check_crisis(text):
    # Detect crisis keywords and return helpline info
    text_lower = text.lower()
    for word in CRISIS_KEYWORDS:
        if word in text_lower:
            return True, HELPLINES
    return False, None
