import pandas as pd
import bs4
import html
import json
from datetime import datetime
    
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


def parse_film_jsons(content):
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

def get_dates(content):
    soup = bs4.BeautifulSoup(content, 'html.parser')
    date_elements = soup.find_all("p", class_="view-date")
    dates = []
    for date in date_elements:
        date = date.text.replace("Watched ", "")
        date_object = datetime.strptime(date, "%b %d, %Y")
        formatted_date = date_object.strftime("%Y-%m-%d")
        dates.append(("importWatchedDate", formatted_date))
    return dates

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