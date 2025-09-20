import json
import plotly.express as px
from datetime import datetime

def save_entry(entry, score, filename="journal_log.json"):
    # Save journal entry with sentiment score and timestamp
    try:
        with open(filename, "r") as f:
            log = json.load(f)
    except:
        log = []
    
    # Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log.append({"entry": entry, "score": score, "timestamp": timestamp})
    
    with open(filename, "w") as f:
        json.dump(log, f)
    return log

def plot_trends(log):
    # Plot mood trend over time
    if not log:
        return px.line(title="Mood Trend Over Time (No data yet)")
        
    scores = [e["score"] for e in log]
    timestamps = [e.get("timestamp") for e in log] # Use .get for safety
    
    # Use timestamps for the x-axis
    fig = px.line(x=timestamps, y=scores, labels={'x': 'Date', 'y':'Mood Score (1-5)'}, title="Mood Trend Over Time")
    return fig