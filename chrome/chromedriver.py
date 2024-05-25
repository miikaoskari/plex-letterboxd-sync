import zipfile
import requests


class ChromeDriver:
    def __init__(self, url, version, platform):
        self.url = url
        self.version = version
        self.platform = platform

    def fetch_known_good_versions(self):
        response = requests.get(self.url)
        self.response = response.json()
        return self.response

    def find_desired_version(self):
        if self.version == "latest":
            try:
                self.fetch_known_good_versions()
                for download in self.response["versions"][-1]["downloads"]["chrome"]:
                    if download["platform"] == self.platform:
                        print(download["url"])
                        return download["url"]
            except Exception as e:
                print(e)

    def download_chromedriver(self):
        url = self.find_desired_version()
        response = requests.get(url)
        with open("chromedriver.zip", "wb") as f:
            f.write(response.content)
        with zipfile.ZipFile("chromedriver.zip", "r") as zip_ref:
            zip_ref.extractall("chromedriver")


if __name__ == "__main__":
    url = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
    version = "latest"
    platform = "linux64"
    chrome_driver = ChromeDriver(url, version, platform)
    chrome_driver.download_chromedriver()
