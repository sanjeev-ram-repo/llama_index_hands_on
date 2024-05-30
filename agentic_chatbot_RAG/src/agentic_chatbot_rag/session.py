import os

import yaml
from settings import SESSION_FILE, STORAGE_PATH


def save_session(state: dict) -> None:
    """Saves the session state as a YAML file.

    Args:
        state (dict): A dictionary of the state details.
    """
    try:
        state = {key: value for key, value in state.items()}
        with open(SESSION_FILE, "w") as state_file:
            yaml.dump(state, state_file)
    except Exception as e:
        raise Exception(f"Cannot save the state: {str(e)}")


def load_session(state: dict) -> bool:
    """Loads the state and returns whether successful or not.

    Args:
        state (dict): State as dictionary.

    Returns:
        bool: True if successful else False.
    """
    try:
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, "r") as session_state:
                loaded_state: dict = yaml.safe_load(session_state) or {}
                for key, value in loaded_state.items():
                    state[key] = value
                return True
    except Exception as e:
        print(e)
        return False


def delete_session(state: dict) -> None:
    """Delete current session from the state variable.

    Args:
        state (dict): State dictionary.
    """
    try:
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
        for filename in os.listdir(STORAGE_PATH):
            file_path = os.path.join(STORAGE_PATH, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
        for key in list(state.keys()):
            del state[key]
    except Exception as e:
        raise Exception(f"Unable to delete the session {str(e)}")
