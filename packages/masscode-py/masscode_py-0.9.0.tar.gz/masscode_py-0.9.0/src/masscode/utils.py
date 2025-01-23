
import platform
import socket
from time import sleep
import os
import json

class Config:
    TOGGLE_STORE :  bool = False
    CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".masscode", "config.json")
    CONFIG = {}
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            CONFIG = json.load(f)

    @classmethod
    def get(cls, key : str, default  = None):
        return cls.CONFIG.get(key, default)

    @classmethod
    def set(cls, key : str, value : str):
        if not value:
            return
        cls.CONFIG[key] = value
        if not cls.TOGGLE_STORE:
            return
        
        os.makedirs(os.path.dirname(cls.CONFIG_PATH), exist_ok=True)
        with open(cls.CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cls.CONFIG, f)

    @classmethod
    def cache(cls, key : str):
        def wrapper(func):
            def inner(*args, **kwargs):
                if key in cls.CONFIG:
                    return cls.CONFIG[key]
                else:
                    value = func(*args, **kwargs)
                    cls.set(key, value)
                    return value
            return inner
        return wrapper

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def kill_masscode_1():
    if platform.system() == "Windows":
        os.system("taskkill /f /im masscode.exe")
    elif platform.system() == "Darwin":
        os.system("killall -9 masscode")
    elif platform.system() == "Linux":
        os.system("killall -9 masscode")
    sleep(1.5)

@Config.cache("MASSCODE_EXE_PATH")
def extract_masscode_path():
    if platform.system() == "Windows":
        raw = os.popen("wmic process where \"name='masscode.exe'\" get ExecutablePath").read().strip()
        try:
            path = raw.splitlines()[2].strip()
        except IndexError:
            path = None
    else:
        path = None

    if not path or path.startswith("No Instance"):
        raise RuntimeError("Masscode is not running")
    return path

def detach_open(path : str):
    import subprocess

    return subprocess.Popen(
        path,
        creationflags=(
            subprocess.DETACHED_PROCESS
            | subprocess.CREATE_NEW_PROCESS_GROUP
            | subprocess.CREATE_BREAKAWAY_FROM_JOB
        ),
    )