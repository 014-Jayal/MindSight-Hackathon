import json
import random

FILENAME = "memory_vault.json"

def load_memories():
    """Loads all memories from the JSON file."""
    try:
        with open(FILENAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_memories(memories):
    """Saves the list of memories to the JSON file."""
    with open(FILENAME, "w") as f:
        json.dump(memories, f, indent=4)

def add_memory(new_memory):
    """Adds a new memory to the vault."""
    memories = load_memories()
    if new_memory not in memories: # Avoid duplicate entries
        memories.append(new_memory)
        save_memories(memories)

def get_random_memory():
    """Returns a random memory from the vault."""
    memories = load_memories()
    if memories:
        return random.choice(memories)
    return None

def remove_memory(memory_to_remove):
    """Removes a specific memory by its text content."""
    memories = load_memories()
    if memory_to_remove in memories:
        memories.remove(memory_to_remove)
        save_memories(memories)