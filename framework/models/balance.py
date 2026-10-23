from pydantic import BaseModel, ConfigDict

class Balance(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)
    asset: str
    available: str
    locked: str
