import requests
from .utils import find_film_ids, get_dates, parse_film_jsons


class Letterboxd:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.film_count = 0

    async def login(self):
        self.session = requests.Session()
        self.session.get("https://letterboxd.com/")
        self.csrf = self.session.cookies._cookies[".letterboxd.com"]["/"][
            "com.xk72.webparts.csrf"
        ].value
        data = {
            "username": self.username,
            "password": self.password,
            "__csrf": self.csrf,
        }
        try:
            self.result = self.session.post(
                "https://letterboxd.com/user/login.do", data=data
            )
            self.result.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    async def import_data(self, file):
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
        files = {"file": content}
        try:
            self.result = self.session.post(
                "https://letterboxd.com/import/csv/", data=data, files=files
            )
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    async def match_import_film(self):
        data_json_decoded = parse_film_jsons(self.result.content)

        data = {
            "json": data_json_decoded,
            "__csrf": self.csrf,
        }
        try:
            self.result = self.session.post(
                "https://letterboxd.com/import/watchlist/match-import-film/", data=data
            )
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    async def save_users_imported_imdb_history(self):
        film_ids = find_film_ids(self, self.result.content)
        import_watched_dates = get_dates(self.result.content)

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
        should_import_films = [
            ("shouldImportFilm", "true") for _ in range(self.film_count)
        ]
        default_data.extend(should_import_films)
        encoded_data = [
            (key.encode("utf-8"), value.encode("utf-8")) for key, value in default_data
        ]
        try:
            self.result = self.session.post(
                "https://letterboxd.com/s/save-users-imported-imdb-history",
                data=encoded_data,
            )
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        print(
            f"Successfully imported {self.film_count} films from {self.file} to Letterboxd."
        )
