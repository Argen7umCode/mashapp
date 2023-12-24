from api.schemas import BaseModel, UUID, TunedModel, List


class CreateRequestSource(TunedModel):
    name: str
    authors: List[UUID]
    