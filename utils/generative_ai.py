import random

# A list of journaling prompts to inspire the user
DAILY_PROMPTS = [
    "What is one thing that made you smile today?",
    "Describe a challenge you faced and how you handled it.",
    "What are you grateful for at this moment?",
    "Write about a goal you have for this week.",
    "What is something you learned recently?",
    "Describe a place where you feel completely at peace.",
    "What does your ideal day look like?"
]

def get_daily_prompt():
    """Returns a random prompt to inspire journaling."""
    return random.choice(DAILY_PROMPTS)

# We can keep the old function for other potential uses, but it won't be used in the main app
PROMPTS = {
    "positive": "Keep up the good vibes! How about journaling your favorite moment today?",
    "negative": "It's okay to feel down. Try writing about something that makes you calm.",
    "neutral": "Reflect on your day and note one thing you learned."
}

def get_feedback_prompt(rating):
    if rating >= 4:
        return PROMPTS["positive"]
    elif rating <= 2:
        return PROMPTS["negative"]
    else:
        return PROMPTS["neutral"]