from datetime import datetime

from settings import LOG_FILE


def log_action(action: str, action_type: str) -> None:
    """Logs the action by the user in the log file along with the timestamp.

    Args:
        action (str): Action by the user.
        action_type (str): Action type by the user.
    """
    try:
        timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry: str = f"{timestamp} - {action_type} - {action} \n"
        with open(LOG_FILE, "a") as log:
            log.write(entry)
    except Exception as e:
        raise Exception(f"Unable to log entry to the log file : {str(e)}")


def reset_log():
    """Clears the log"""
    try:
        with open(LOG_FILE, "w") as log:
            log.truncate(0)
    except Exception as e:
        raise Exception(f"Unable to clear the log file {str(e)}")
