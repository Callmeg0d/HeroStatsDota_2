from pydantic import BaseModel

class HeroData(BaseModel):
    id: int
    name: str
    localized_name: str
    primary_attr: str
    attack_type: str

class HeroMatchup(BaseModel):
    hero_id: int
    games_played: int
    wins: int
    win_rate: float
