import json

USER_DATA_FILE = 'user_data.json'

def load_user_ids():
    """Loads user IDs from the JSON file."""
    try:
        with open(USER_DATA_FILE, 'r') as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_user_ids(user_ids):
    """Saves a set of user IDs to the JSON file."""
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(list(user_ids), f)
