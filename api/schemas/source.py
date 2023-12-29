from api.schemas import BaseModel, TunedModel, List


class CreateRequestSource(TunedModel):
    name: str
    authors: List[int]
