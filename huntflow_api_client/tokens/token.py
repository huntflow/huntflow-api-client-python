from dataclasses import dataclass, fields
from typing import Optional


@dataclass
class HuntflowApiToken:
    access_token: str
    refresh_token: Optional[str]
    expiration_timestamp: Optional[float] = None
    last_refresh_timestamp: Optional[float] = 0.0

    @classmethod
    def from_dict(cls, dict_: dict):
        attrs = {field.name for field in fields(cls)}
        return cls(**{k: v for k, v in dict_.items() if k in attrs})
