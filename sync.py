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

async def construct_progress(status, value):
    data = {
        "type": "progress",
        "status": status,
        "value": value,
    }
    return json.dumps(data)

async def start_sync(progress):
    """
    Starts the synchronization process between Tautulli and Letterboxd.

    Args:
        progress: Progress callback function of websocket.send_text.

    Returns:
        None
    """
    await progress(await construct_progress("Reading keys...", "0"))
    keys = read_keys()
    tautulli = Tautulli(url=keys["tautulli"]["url"], key=keys["tautulli"]["api_key"])

    await progress(await construct_progress("Getting watched data...", "10"))
    await tautulli.get_watched(user=keys["tautulli"]["username"])
    await progress(await construct_progress("Checking watched status...", "20"))
    await tautulli.check_watched_status()
    await progress(await construct_progress("Compiling JSON to CSV...", "30"))
    await tautulli.compile_json_to_csv(file="history")

    letterboxd = Letterboxd(
        keys["letterboxd"]["username"], keys["letterboxd"]["password"]
    )
    await letterboxd.login()
    await progress("Logging in to Letterboxd...")
    await letterboxd.import_data(file="history.csv")
    await progress("Importing data to Letterboxd...")
    await letterboxd.match_import_film()
    await progress("Matching imported films...")
    await letterboxd.save_users_imported_imdb_history()
    await progress("Saving user's imported history...")

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
