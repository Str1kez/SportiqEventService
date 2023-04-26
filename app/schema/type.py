from pydantic import BaseModel


class TypesResponse(BaseModel):
    types: list[str] = []
