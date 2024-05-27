import requests
import json
import bs4
import html

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
        
    def parse_film_jsons(self, content):
        soup = bs4.BeautifulSoup(content, 'html.parser')
        import_films = soup.find_all("li", class_="import-film")
        data = []
        for film in import_films:
            data_json_encoded = film.get("data-json")
            data_json_decoded = html.unescape(data_json_encoded)
            data.append(json.loads(data_json_decoded))
        # letterboxd wants to have 100 films in the import list
        # rest is filled with "undefined"
        while len(data) < 100:
            data.append("undefined")

        wrapped_data = {
            "importType": "diary",
            "importFilms": data,
        }
        return json.dumps(wrapped_data)

    def import_data(self, file):
        try:
            file_handle = open(file, "rb")
            content = file_handle.read()
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
            result = self.session.post("https://letterboxd.com/import/csv/", data=data, files=files)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        data_json_decoded = self.parse_film_jsons(result.content)
        
        data = {
            "__csrf": self.csrf,
            "data": data_json_decoded,
        }
        try:
            result = self.session.post("https://letterboxd.com/import/watchlist/match-import-film/", data=data)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        
        data = {
            "__csrf": self.csrf,
            "filmListId": "",
            "name": "",
            "publicList": "",
            "numberedList": "",
            "notes": "",
            "tags": "",
            "shouldMarkAsWatched": "true",
            "shouldImportWatchedDates": "true",
            "importRating": "",
            
        }
        try:
            self.session.post("https://letterboxd.com/s/save-users-imported-imdb-history/")
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
