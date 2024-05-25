from tautulli import RawAPI
import csv
import json

class Tautulli():
    def __init__(self, url, key) -> None:
        self.url = url
        self.key = key

    def get_watched(self, user):
        self.api = RawAPI(base_url=self.url, api_key=self.key)
        self.history = self.api.get_history(user=user, media_type='movie', length=1000)
        try:
            with open('history.json', 'w') as f:
                f.write(json.dumps(self.history, indent=4, sort_keys=True))
        finally:
            f.close()
        return self.history
    
    def compile_json_to_csv(self):
        pass
        