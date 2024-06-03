from api.tautulli_api import Tautulli
from api.letterboxd import Letterboxd
import json


def read_keys():
    """
    Reads the keys from the 'keys.json' file and returns them.

    Returns:
        dict: A dictionary containing the keys.
    """
    with open("keys.json") as f:
        keys = json.load(f)
    return keys


def debug():
    """
    Set up environment variables for debugging with Burp Suite.

    This function sets the following environment variables:
    - REQUESTS_CA_BUNDLE: Path to the certificate file for SSL/TLS verification.
    - HTTP_PROXY: URL of the HTTP proxy server.
    - HTTPS_PROXY: URL of the HTTPS proxy server.

    These environment variables are commonly used when debugging network requests
    with Burp Suite, a popular web application security testing tool.

    Note: Make sure to replace the values with the appropriate paths and URLs
    for your specific debugging setup.
    """
    import os

    os.environ["REQUESTS_CA_BUNDLE"] = "cert.pem"
    os.environ["HTTP_PROXY"] = "http://127.0.0.1:8080"
    os.environ["HTTPS_PROXY"] = "http://127.0.0.1:8080"


def start_sync(websocket):
    """
    Starts the synchronization process between Tautulli and Letterboxd.

    Args:
        websocket: WebSocket connection.

    Returns:
        None
    """
    keys = read_keys()

    tautulli = Tautulli(url=keys["tautulli"]["url"], key=keys["tautulli"]["api_key"])
    tautulli.get_watched(user=keys["tautulli"]["username"])
    websocket.send_text("Retrieved watched history from Tautulli.")
    tautulli.check_watched_status()
    websocket.send_text("Checked watched status.")
    tautulli.compile_json_to_csv(file="history")
    websocket.send_text("Compiled JSON to CSV.")

    letterboxd = Letterboxd(
        keys["letterboxd"]["username"], keys["letterboxd"]["password"]
    )
    letterboxd.login()
    websocket.send_text("Logged in to Letterboxd.")
    letterboxd.import_data(file="history.csv")
    websocket.send_text("Imported data to Letterboxd.")
    letterboxd.match_import_film()
    websocket.send_text("Matched imported films.")
    letterboxd.save_users_imported_imdb_history()
    websocket.send_text("Saved imported history.")

def start_sync_daemon(websocket):
    """
    Starts the synchronization process between Tautulli and Letterboxd as a daemon.

    Args:
        websocket: WebSocket connection.

    Returns:
        None
    """
    pass

def stop_sync_daemon():
    """
    Stops the synchronization process between Tautulli and Letterboxd.

    Returns:
        None
    """
    pass


if __name__ == "__main__":
    start_sync()
