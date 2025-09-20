import json
import re

# Keywords to track for insights
KEYWORD_CATEGORIES = {
    "Social": ["friend", "friends", "family", "party", "talked"],
    "Activity": ["walk", "exercise", "gym", "run", "hike", "swim"],
    "Rest": ["sleep", "rest", "nap", "relaxed", "calm"],
    "Work": ["work", "meeting", "project", "deadline", "office"]
}

def analyze_journal_insights(filename="journal_log.json"):
    """
    Analyzes the journal log to find correlations between keywords and mood scores.
    """
    try:
        with open(filename, "r") as f:
            log = json.load(f)
    except FileNotFoundError:
        return {"error": "No journal entries found yet."}

    if not log:
        return {"error": "Not enough data to generate insights."}

    insights = {}
    for category, keywords in KEYWORD_CATEGORIES.items():
        mood_with_keyword = []
        mood_without_keyword = []
        
        for entry in log:
            text = entry.get("entry", "").lower()
            score = entry.get("score", 3)
            
            # Check if any keyword in the category is present
            if any(re.search(r'\b' + keyword + r'\b', text) for keyword in keywords):
                mood_with_keyword.append(score)
            else:
                mood_without_keyword.append(score)
        
        if mood_with_keyword:
            avg_with = sum(mood_with_keyword) / len(mood_with_keyword)
            avg_without = sum(mood_without_keyword) / len(mood_without_keyword) if mood_without_keyword else avg_with
            
            if avg_with > avg_without * 1.1: # At least 10% higher
                insights[category] = f"Your mood is, on average, **{int(((avg_with / avg_without) - 1) * 100)}% higher** on days you mention **{category.lower()}** activities. (Avg score: {avg_with:.2f})"
            elif avg_with < avg_without * 0.9: # At least 10% lower
                insights[category] = f"Your mood is, on average, **{int((1 - (avg_with / avg_without)) * 100)}% lower** on days you mention **{category.lower()}**. (Avg score: {avg_with:.2f})"

    return insights if insights else {"message": "No strong correlations found yet. Keep journaling to discover more about your patterns!"}