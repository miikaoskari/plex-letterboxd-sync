import requests
import json
import bs4
import html
import pandas as pd
from datetime import datetime

class Letterboxd:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.film_count = 0

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
    
    def find_film_ids(self, content):
        soup = bs4.BeautifulSoup(content, 'html.parser')
        film_elements = soup.find_all("div")
        film_ids = []
        for film in film_elements:
            film_id = film.get("data-film-id")
            if film_id:
                film_ids.append(("importFilmId", film_id))
                self.film_count += 1
        return film_ids
    
    def get_dates_from_csv(self):
        df = pd.read_csv(self.file)
        watched_dates = df["WatchedDate"].tolist()
        dates = []
        for _ in range(self.film_count):
            try:
                date = watched_dates.pop(0)
                dates.append(("importWatchedDate", date))
            except IndexError:
                dates.append(("importWatchedDate", ""))
        return dates
    
    def get_dates(self, content):
        soup = bs4.BeautifulSoup(content, 'html.parser')
        date_elements = soup.find_all("p", class_="view-date")
        dates = []
        for date in date_elements:
            date = date.text.replace("Watched ", "")
            date_object = datetime.strptime(date, "%b %d, %Y")
            formatted_date = date_object.strftime("%Y-%m-%d")
            dates.append(("importWatchedDate", formatted_date))
        return dates

    def import_data(self, file):
        self.file = file
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
            "json": data_json_decoded,
            "__csrf": self.csrf,
        }
        try:
            result = self.session.post("https://letterboxd.com/import/watchlist/match-import-film/", data=data)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        

        film_ids = self.find_film_ids(result.content)
        import_watched_dates = self.get_dates(result.content)

        default_data = [
            ("__csrf", self.csrf),
            ("filmListId", ""),
            ("name", ""),
            ("publicList", ""),
            ("numberedList", ""),
            ("notes", ""),
            ("tags", ""),
            ("shouldMarkAsWatched", "true"),
            ("shouldImportWatchedDates", "true"),
        ]

        import_ratings = [("importRating", "") for _ in range(self.film_count)]
        default_data.extend(import_ratings)
        import_reviews = [("importReview", "") for _ in range(self.film_count)]
        default_data.extend(import_reviews)
        import_tags = [("importTags", "") for _ in range(self.film_count)]
        default_data.extend(import_tags)
        default_data.extend(import_watched_dates)
        import_rewatch = [("importRewatch", "false") for _ in range(self.film_count)]
        default_data.extend(import_rewatch)
        default_data.extend(film_ids)
        import_viewing_ids = [("importViewingId", "") for _ in range(self.film_count)]
        default_data.extend(import_viewing_ids)
        should_import_films = [("shouldImportFilm", "true") for _ in range(self.film_count)]
        default_data.extend(should_import_films)
        encoded_data = [(key.encode('utf-8'), value.encode('utf-8')) for key, value in default_data]
        try:
            result = self.session.post("https://letterboxd.com/s/save-users-imported-imdb-history", data=encoded_data)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        print(f"Successfully imported {self.film_count} films from {file} to Letterboxd.")
