from tautulli import RawAPI
import pandas as pd
import json
from datetime import datetime
from io import StringIO


class Tautulli():
    def __init__(self, url, key) -> None:
        self.url = url
        self.key = key

    def get_watched(self, user):
        self.api = RawAPI(base_url=self.url, api_key=self.key)
        self.json_data = self.api.get_history(user=user, media_type='movie', length=1000)
        try:
            with open('history.json', 'w') as f:
                f.write(json.dumps(self.json_data, indent=4, sort_keys=True))
        finally:
            f.close()
        return self.json_data
    
    def check_watched_status(self):
        self.filtered_json = []
        for item in self.json_data["data"]:
                if item['watched_status'] == 1:
                    watched_date = datetime.utcfromtimestamp(item["date"]).strftime('%Y-%m-%d')
                    appendable_item = {
                        "Title": item["title"],
                        "Year": item["year"],
                        "WatchedDate": watched_date,
                    }
                    self.filtered_json.append(appendable_item)

    def compile_json_to_csv(self, file):
        df = pd.read_json(StringIO(json.dumps(self.filtered_json)))
        df.to_csv(f'{file}.csv', encoding='utf-8', index=False)
        