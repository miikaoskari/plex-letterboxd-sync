import requests
import json

class Letterboxd:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        self.session = requests.Session()
        self.session.get("https://letterboxd.com/")
        self.csrf = self.session.cookies._cookies['.letterboxd.com']['/']['com.xk72.webparts.csrf'].value
        data = {
            "username": self.username,
            "password": self.password,
            "__csrf": self.csrf
        }
        try:
            response = self.session.post("https://letterboxd.com/user/login.do", data=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def import_data(self, file):
        try:
            content = open(file, "rb")
        except FileNotFoundError as e:
            print(f"File {file} not found")
            return
        data = {
            "__csrf": self.csrf,
        }
        files = {
            "file": content
        }
        try:
            self.session.post("https://letterboxd.com/import/csv", data=data, files=files)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
