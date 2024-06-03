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


def start_sync(websocket=None):
    """
    Starts the synchronization process between Tautulli and Letterboxd.

    Args:
        websocket: Optional WebSocket connection.

    Returns:
        None
    """
    keys = read_keys()

    tautulli = Tautulli(url=keys["tautulli"]["url"], key=keys["tautulli"]["api_key"])
    tautulli.get_watched(user=keys["tautulli"]["username"])
    tautulli.check_watched_status()
    tautulli.compile_json_to_csv(file="history")

    letterboxd = Letterboxd(
        keys["letterboxd"]["username"], keys["letterboxd"]["password"]
    )
    letterboxd.login()
    letterboxd.import_data(file="history.csv")
    letterboxd.match_import_film()
    letterboxd.save_users_imported_imdb_history()


if __name__ == "__main__":
    start_sync()
