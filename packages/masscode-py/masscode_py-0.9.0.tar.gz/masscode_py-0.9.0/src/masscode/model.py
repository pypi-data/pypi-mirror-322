
from typing import TypedDict


class Folder(TypedDict):
    name : str
    parentId: str | None
    isOpen: bool
    isSystem: bool
    defaultLanguage: str
    id: str
    createdAt: int
    updatedAt: int
    index: int
    icon: str

class Content(TypedDict):
    label : str
    language : str
    value : str

class Snippet(TypedDict):
    isDeleted: bool
    isFavorites: bool
    folderId: str
    tagsIds: list[str]
    description: str | None
    name: str
    content: list[Content]
    id: str
    createdAt: int
    updatedAt: int

class Tag(TypedDict):
    name: str
    id: str
    createdAt: int
    updatedAt: int


