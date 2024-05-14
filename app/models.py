from pydantic import BaseModel


class SpreadAlert(BaseModel):
    spread: float
    market: str
