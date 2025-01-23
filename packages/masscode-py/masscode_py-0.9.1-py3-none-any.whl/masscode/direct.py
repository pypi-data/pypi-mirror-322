
from functools import cache
import os
from masscode.modelApi import MasscodeApi
import json

class MasscodeDirectFileAccess:
    _API = MasscodeApi

    MAKE_A_BKUP : bool = False

    @classmethod
    @cache
    def get_preferences(cls):
        with open(cls._API.PREFERENCES_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    @classmethod
    def get_storagepath(cls):
        return cls.get_preferences()["storagePath"]

    DB = None
    DB_LAST_MODIFIED = None

    @classmethod
    def get_db(cls):
        if cls.DB is not None and cls.DB_LAST_MODIFIED == os.path.getmtime(os.path.join(cls.get_storagepath(), "db.json")):
            return cls.DB

        with open(os.path.join(cls.get_storagepath(), "db.json"), "r", encoding="utf-8") as f:
            cls.DB = json.load(f)
            cls.DB_LAST_MODIFIED = os.path.getmtime(os.path.join(cls.get_storagepath(), "db.json"))
        return cls.DB

    def snippets(self):
        return self.get_db()["snippets"]

    def folders(self):
        return self.get_db()["folders"]

    def tags(self):
        return self.get_db()["tags"]

    def get_snippet(self, id : str):
        for snippet in self.snippets():
            if snippet["id"] == id:
                return snippet
        return None

    def get_folder(self, id : str):
        for folder in self.folders():
            if folder["id"] == id:
                return folder
        return None

    def get_tag(self, id : str):
        for tag in self.tags():
            if tag["id"] == id:
                return tag
        return None

    def save(self):
        with open(os.path.join(self.get_storagepath(), "db.json"), "w", encoding="utf-8") as f:
            json.dump(self.get_db(), f, indent=4, ensure_ascii=False)
