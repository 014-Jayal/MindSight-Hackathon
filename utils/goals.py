import json
from datetime import datetime

FILENAME = "daily_goals.json"

def get_today_key():
    """Returns the key for today's date, e.g., '2025-09-18'."""
    return datetime.now().strftime("%Y-%m-%d")

def load_goals():
    """Loads all goals from the JSON file."""
    try:
        with open(FILENAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_goals(goals):
    """Saves the goals dictionary to the JSON file."""
    with open(FILENAME, "w") as f:
        json.dump(goals, f, indent=4)

def get_todays_goals():
    """Gets the list of goals for the current day."""
    all_goals = load_goals()
    today_key = get_today_key()
    return all_goals.get(today_key, [])

def add_goal(new_goal):
    """Adds a new goal for today."""
    all_goals = load_goals()
    today_key = get_today_key()
    
    if today_key not in all_goals:
        all_goals[today_key] = []
        
    all_goals[today_key].append({"text": new_goal, "completed": False})
    save_goals(all_goals)

def update_goal_status(goal_index, completed):
    """Updates the completion status of a specific goal for today."""
    all_goals = load_goals()
    today_key = get_today_key()
    
    if today_key in all_goals and 0 <= goal_index < len(all_goals[today_key]):
        all_goals[today_key][goal_index]["completed"] = completed
        save_goals(all_goals)

def remove_goal(goal_index):
    """Removes a specific goal by its index for today."""
    all_goals = load_goals()
    today_key = get_today_key()
    
    if today_key in all_goals and 0 <= goal_index < len(all_goals[today_key]):
        all_goals[today_key].pop(goal_index)
        save_goals(all_goals)