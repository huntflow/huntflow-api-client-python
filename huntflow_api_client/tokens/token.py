from dataclasses import asdict, dataclass, fields
from typing import Any, Dict, Optional


@dataclass
class ApiToken:
    access_token: str
    refresh_token: Optional[str] = None
    expiration_timestamp: Optional[float] = None
    last_refresh_timestamp: Optional[float] = 0.0

    @classmethod
    def from_dict(cls, dict_: Dict[str, Any]) -> "ApiToken":
        attrs = {field.name for field in fields(cls)}
        return cls(**{k: v for k, v in dict_.items() if k in attrs})

    def dict(self) -> Dict[str, Any]:
        return asdict(self)
