from chrome.chromedriver import ChromeDriver
from api.tautulli_api import Tautulli
import json

def read_keys():
    with open('keys.json') as f:
        keys = json.load(f)
    return keys

if __name__ == "__main__":
    keys = read_keys()

    url = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
    version = "latest"
    platform = "linux64"
    chrome_driver = ChromeDriver(url, version, platform)
    chrome_driver.download_chromedriver()

    tautulli = Tautulli(keys["url"], keys["api_key"])
    tautulli.get_watched(keys["username"])
    