import json
import logging
import asyncio
from typing import Callable
from api.tautulli_api import Tautulli
from api.letterboxd import Letterboxd
from enum import Enum


def read_keys():
    """
    Reads the keys from the 'keys.json' file and returns them.

    Returns:
        dict: A dictionary containing the keys.
    """
    with open("keys.json") as f:
        keys = json.load(f)
    return keys


def setup_logging():
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


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


def construct_progress(status: str, value: str) -> str:
    logging.info(f"{status} - {value}")
    data = {
        "type": "progress",
        "status": status,
        "value": value,
    }
    return json.dumps(data)


class ProgressState(Enum):
    READING_KEYS = "Reading keys..."
    GETTING_WATCHED_DATA = "Getting watched data..."
    CHECKING_WATCHED_STATUS = "Checking watched status..."
    COMPILING_JSON_TO_CSV = "Compiling JSON to CSV..."
    LOGGING_IN_LETTERBOXD = "Logging in to Letterboxd..."
    IMPORTING_DATA_LETTERBOXD = "Importing data to Letterboxd..."
    MATCHING_IMPORTED_FILMS = "Matching imported films..."
    SAVING_IMPORTED_HISTORY = "Saving imported history..."
    SYNC_COMPLETE = "Synchronization complete."


async def report_progress(
    progress: Callable[[str], None], state: ProgressState, percentage: int
) -> None:
    """
    Reports the progress to the given callback function.

    Args:
        progress: Progress callback function of websocket.send_text.
        state: The current state of the progress.
        percentage: The percentage of completion.

    Returns:
        None
    """
    message = construct_progress(state.value, str(percentage))
    logging.info(message)
    await progress(message)


async def start_sync(progress: Callable[[str], None]) -> None:
    """
    Starts the synchronization process between Tautulli and Letterboxd.

    Args:
        progress: Progress callback function of websocket.send_text.

    Returns:
        None
    """
    try:
        setup_logging()
        await report_progress(progress, ProgressState.READING_KEYS, 0)
        keys = read_keys()
        tautulli = Tautulli(
            url=keys["tautulli"]["url"], key=keys["tautulli"]["api_key"]
        )

        await report_progress(progress, ProgressState.GETTING_WATCHED_DATA, 5)
        tautulli.get_watched(user=keys["tautulli"]["username"])

        await report_progress(progress, ProgressState.CHECKING_WATCHED_STATUS, 10)
        tautulli.check_watched_status()

        await report_progress(progress, ProgressState.COMPILING_JSON_TO_CSV, 15)
        tautulli.compile_json_to_csv()

        letterboxd = Letterboxd(
            keys["letterboxd"]["username"], keys["letterboxd"]["password"]
        )

        await report_progress(progress, ProgressState.LOGGING_IN_LETTERBOXD, 20)
        letterboxd.login()

        num_files = len(tautulli.chunkfiles)
        # allocate 60% of the progress bar for importing data
        progress_increment_per_file = (80 - 20) / num_files

        for index, file in enumerate(tautulli.chunkfiles):
            current_progress = 20 + index * progress_increment_per_file
            await report_progress(progress, ProgressState.IMPORTING_DATA_LETTERBOXD, current_progress)
            letterboxd.import_data(file=file)

            await report_progress(progress, ProgressState.MATCHING_IMPORTED_FILMS, current_progress + (progress_increment_per_file / 3))
            letterboxd.match_import_film()

            await report_progress(progress, ProgressState.SAVING_IMPORTED_HISTORY, current_progress + (2 * progress_increment_per_file / 3))
            letterboxd.save_users_imported_imdb_history()

        await report_progress(progress, ProgressState.SYNC_COMPLETE, 100)

    except Exception as e:
        logging.error("Error during synchronization: %s", e)
        await progress(f"Error: {e}")


if __name__ == "__main__":
    start_sync()
