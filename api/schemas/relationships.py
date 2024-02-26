from typing import List

from api.schemas.user import ShowUser
from api.schemas.mashup import ShowMashup
from api.schemas.source import ShowSource
from api.schemas.author import ShowAuthor


class ShowUserWithRel(ShowUser):
    mashups: List[ShowMashup]


class ShowMashupWithRel(ShowMashup):
    user: ShowUser
    sources: List[ShowSource]


class ShowSourceWithRel(ShowSource):
    mashups: List[ShowMashup]
    author: ShowAuthor


class ShowAuthorWithRel(ShowAuthor):
    sources: List[ShowSource]
