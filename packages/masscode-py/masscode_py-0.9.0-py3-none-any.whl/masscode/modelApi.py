from contextlib import contextmanager
import logging
import os
from time import sleep
import typing
import requests
import json
from masscode.model import Folder, Snippet, Tag
from masscode.utils import Config, kill_masscode_1, extract_masscode_path, detach_open, is_port_in_use

class MasscodeApi:
    API_URL = "http://localhost:3033"
    CONFIG_DIR = os.path.join(os.path.expandvars("%APPDATA%"), "masscode", "v2")
    PREFERENCES_JSON = os.path.join(CONFIG_DIR, "preferences.json")
    
    WAIT_START = 3

    @classmethod
    def switch_profile(cls, path : str):
        extract_masscode_path()
        kill_masscode_1()
        with open(cls.PREFERENCES_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert os.path.exists(path)
        assert os.path.isdir(path)
        data["storagePath"] = path
        with open(cls.PREFERENCES_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        
        cls.start_masscode()

    @classmethod
    def start_masscode(cls):
        extract_masscode_path()
        if is_port_in_use(3033):
            print("Port 3033 is already in use.")
            return
        detach_open(Config.get("MASSCODE_EXE_PATH"))
        sleep(cls.WAIT_START)

    @classmethod
    def kill_masscode(cls):
        kill_masscode_1()
    

    @classmethod
    @contextmanager
    def context_switch(cls, path : str):
        try:
            # get current path first
            with open(cls.PREFERENCES_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
            current_path = data["storagePath"]
            # switch back to current path
            cls.switch_profile(path)
            yield
        except Exception as e:
            raise e
        finally:
            # switch back to current path
            cls.switch_profile(current_path)

    @classmethod
    def _handle_request(cls, method : typing.Literal["get", "post", "put", "delete"], path : str, data : typing.Any = None, params : dict[str, typing.Any] = {}, **kwargs) -> typing.Any:
        extract_masscode_path()

        logging.debug(f"using method {method} to request {path}")

        match method:
            case "get": 
                method = requests.get
            case "post": 
                method = requests.post
            case "put": 
                method = requests.put
            case "delete": 
                method = requests.delete
            case "patch": 
                method = requests.patch
            case _: 
                raise ValueError(f"Invalid method: {method}")

        response = method(f"{cls.API_URL}/{path}", json=data, params=params, **kwargs)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request failed with status code {response.status_code}")

    @classmethod
    def folders(cls, params: dict[str, typing.Any] = {}) -> list[Folder]:
        response = cls._handle_request("get", "folders", params=params)
        return [Folder(**folder) for folder in response]
    
    @classmethod
    def snippets(cls, params: dict[str, typing.Any] = {}) -> list[Snippet]:
        response = cls._handle_request("get", "snippets", params=params)
        return [Snippet(**snippet) for snippet in response]

    @classmethod
    def tags(cls, params: dict[str, typing.Any] = {}) -> list[Tag]:
        response = cls._handle_request("get", "tags", params=params)
        return [Tag(**tag) for tag in response]

    @classmethod
    def add_folder(cls, folder: Folder, params: dict[str, typing.Any] = {}) -> Folder:
        response = cls._handle_request("post", "folders", folder, params=params)
        return Folder(**response)

    @classmethod
    def add_snippet(cls, snippet: Snippet, params: dict[str, typing.Any] = {}) -> Snippet:
        response = cls._handle_request("post", "snippets", snippet, params=params)
        return Snippet(**response)

    @classmethod
    def add_tag(cls, tag: Tag, params: dict[str, typing.Any] = {}) -> Tag:
        response = cls._handle_request("post", "tags", tag, params=params)
        return Tag(**response)

    @classmethod
    def update_folder(cls, folder: Folder, params: dict[str, typing.Any] = {}) -> Folder:
        response = cls._handle_request("put", f"folders/{folder['id']}", folder, params=params)
        return Folder(**response)

    @classmethod
    def update_snippet(cls, snippet: Snippet, params: dict[str, typing.Any] = {}) -> Snippet:
        response = cls._handle_request("put", f"snippets/{snippet['id']}", snippet, params=params)
        return Snippet(**response)

    @classmethod
    def update_tag(cls, tag: Tag, params: dict[str, typing.Any] = {}) -> Tag:
        response = cls._handle_request("put", f"tags/{tag['id']}", tag, params=params)
        return Tag(**response)

    @classmethod
    def delete_folder(cls, folder_id: str, params: dict[str, typing.Any] = {}) -> None:
        cls._handle_request("delete", f"folders/{folder_id}", params=params)
    
    @classmethod
    def delete_snippet(cls, snippet_id: str, params: dict[str, typing.Any] = {}) -> None:
        cls._handle_request("delete", f"snippets/{snippet_id}", params=params)

    @classmethod
    def delete_tag(cls, tag_id: str, params: dict[str, typing.Any] = {}) -> None:
        cls._handle_request("delete", f"tags/{tag_id}", params=params)

    @classmethod
    def get_folder(cls, id : str) -> Folder:
        response = cls._handle_request("get", f"folders/{id}")
        return Folder(**response)

    @classmethod
    def get_snippet(cls, id : str) -> Snippet:
        response = cls._handle_request("get", f"snippets/{id}")
        return Snippet(**response)

    @classmethod
    def get_tag(cls, id : str) -> Tag:
        response = cls._handle_request("get", f"tags/{id}")
        return Tag(**response)
