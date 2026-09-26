from typing import Optional, List
from pydantic import BaseModel


class TokenData(BaseModel):
    sub: str
    email: Optional[str] = None
    roles: List[str] = []
    team_id: Optional[int] = None
