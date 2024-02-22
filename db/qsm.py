from typing import Callable, NoReturn, Union
from sqlalchemy import select, Select

from db.models import Base, User, Mashup, Source, Author


class QuerySearchMaker:
    fields_to_get = {}

    def get_query(self, data: dict) -> Select:
        query = select(self.model)
        for field, row in self.fields_to_get.items():
            if from_data := data.get(field):
                query.where(row == from_data)
        return query


class UserQSM(QuerySearchMaker):
    def __init__(self) -> None:
        self.model = User
        self.fields_to_get = {
            "name": self.model.name, 
            "mashup_id": Mashup.id,
            "email" : self.model.email

        }


class MashupQSM(QuerySearchMaker):
    def __init__(self) -> None:
        self.model = Mashup
        self.fields_to_get = {
            "name": self.model.name,
            "user_id": self.model.user_id,
            "source_id": Source.id,
        }


class SourceQSM(QuerySearchMaker):
    def __init__(self) -> None:
        self.model = Source
        self.fields_to_get = {
            "name": self.model.name,
            "mashup_id": Mashup.id,
            "author_id": self.model.author_id,
        }


class AuthorQSM(QuerySearchMaker):
    def __init__(self) -> None:
        self.model = Author
        self.fields_to_get = {
            "name": self.model.name,
            "source_id": Source.id,
        }


class QSMFactory:
    @staticmethod
    def get_qsm(model: Base) -> Union[QuerySearchMaker|NoReturn]:
        raw_subclasses_ = QuerySearchMaker.__subclasses__()
        classes = {
            c().model: c for c in raw_subclasses_
        }
        class_ = classes.get(model, None)
        if class_ is not None:
            return class_

        raise ValueError

