
# app/schemas/character_schema.py
from pydantic import BaseModel
from typing import Optional, Dict

class CharacterBase(BaseModel):
    name: str
    description: Optional[str] = None
    group: Optional[str] = None
    hp_hand: Optional[Dict[str, int]] = None  # { '5': 6, '3': 7 ... } 등
    image_url: Optional[str] = None

class CharacterCreate(CharacterBase):
    pass

class CharacterUpdate(CharacterBase):
    pass

class CharacterOut(CharacterBase):
    id: int

    class Config:
        orm_mode = True
