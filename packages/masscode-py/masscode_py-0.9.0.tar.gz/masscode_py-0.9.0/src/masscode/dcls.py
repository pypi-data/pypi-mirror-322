from dataclasses import dataclass, field,asdict
from datetime import datetime
from typing import Any
from masscode.modelApi import MasscodeApi
from masscode.model import Content
import threading

class BaseMeta(type):
    _instances = {}

    def __call__(cls, id : str, **kwargs):
        if cls.__name__ not in cls._instances:
            cls._instances[cls.__name__] = {}

        if id not in cls._instances[cls.__name__]:
            cls._instances[cls.__name__][id] = super().__call__(id=id, **kwargs)
        else:
            instance : BASE = cls._instances[cls.__name__][id]
            instance.__toggle_update__ = False

            for key, value in kwargs.items():
                if key.startswith("_"):
                    continue
                setattr(instance, key, value)

            instance.__toggle_update__ = True
        return cls._instances[cls.__name__][id]

@dataclass()
class BASE:

    def __post_init__(self):
        self._update_timer = None
        self.__toggle_update__ = True

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_"):
            return super().__setattr__(name, value)
        
        if not hasattr(self, "__toggle_update__") or not self.__toggle_update__:
            return super().__setattr__(name, value)

        if name in ["id", "createdAt", "updatedAt"]:
            raise AttributeError(f"Cannot set {name} attribute")
        if name in self.__dataclass_fields__:
            # Cancel the previous timer if it exists
            if self._update_timer is not None:
                self._update_timer.cancel()
            # Set the attribute
            super().__setattr__(name, value)
            # Start a new timer
            self._update_timer = threading.Timer(0.5, self.__trigger_update)
            self._update_timer.start()
        return super().__setattr__(name, value)

    def __trigger_update(self):
        data = asdict(self)
        method = getattr(MasscodeDclsApi._API, f"update_{self.__class__.__name__.lower()}")
        method(data)
        self._update_timer = None

    def refetch(self):
        match self.__class__.__name__:
            case "Snippet":
                MasscodeDclsApi.get_snippet(self.id)
            case "Tag":
                MasscodeDclsApi.get_tag(self.id)
            case "Folder":
                MasscodeDclsApi.get_folder(self.id)

    @property
    def created(self):
        return datetime.fromtimestamp(self.createdAt)

    @property
    def updated(self):
        return datetime.fromtimestamp(self.updatedAt)

@dataclass()
class Snippet(BASE):
    
    id : str = field()
    createdAt: int = field()
    updatedAt: int = field()


    name: str = field()
    description: str | None = field()
    folderId: str = field()
    isFavorites: bool = field()
    isDeleted: bool = field()
    content: list[Content] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    @property
    def folder(self):
        if self.folderId:
            return MasscodeDclsApi.get_folder(self.folderId)
        return None
    
    @property
    def tagObjs(self):
        return [MasscodeDclsApi.get_tag(tag) for tag in self.tagsIds]

@dataclass()
class Tag(BASE):

    id : str = field()
    createdAt: int = field()
    updatedAt: int = field()


    name: str = field()

@dataclass()
class Folder(BASE):

    id : str = field()
    createdAt: int = field()
    updatedAt: int = field()

    name : str = field()
    parentId: str | None = field()
    isOpen: bool = field()
    isSystem: bool = field()
    defaultLanguage: str = field()
    index: int = field()
    icon: str = field()

    @property
    def parent(self):
        if self.parentId:
            return MasscodeDclsApi.get_folder(self.parentId)
        return None
    
    @property
    def children(self):
        pass

class MasscodeDclsApi:
    _API = MasscodeApi

    SNIPPET = Snippet
    TAG = Tag
    FOLDER = Folder

    LAZY_LOAD : bool = False

    @classmethod
    def folders(cls, params : dict[str, Any] = {}):
        return [Folder(**folder) for folder in cls._API.folders(**params)]
    
    @classmethod
    def snippets(cls, params : dict[str, Any] = {}):
        return [Snippet(**snippet) for snippet in cls._API.snippets(**params)]
    
    @classmethod
    def tags(cls, params : dict[str, Any] = {}):
        return [Tag(**tag) for tag in cls._API.tags(**params)]
    
    @classmethod
    def get_folder(cls, id : str):
        if cls.LAZY_LOAD and id in BaseMeta._instances["Folder"]:
            return BaseMeta._instances["Folder"][id]

        return Folder(**cls._API.get_folder(id))
    
    @classmethod
    def get_snippet(cls, id : str):
        if cls.LAZY_LOAD and id in BaseMeta._instances["Snippet"]:
            return BaseMeta._instances["Snippet"][id]

        return Snippet(**cls._API.get_snippet(id))
    
    @classmethod
    def get_tag(cls, id : str):
        if cls.LAZY_LOAD and id in BaseMeta._instances["Tag"]:
            return BaseMeta._instances["Tag"][id]

        return Tag(**cls._API.get_tag(id))
    

