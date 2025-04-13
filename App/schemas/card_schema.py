# app/schemas/card_schema.py
from pydantic import BaseModel
from typing import Optional

class CardBase(BaseModel):
    name: str
    ruby: Optional[str] = None
    frame: Optional[int] = None
    damage: Optional[int] = None
    pos: Optional[str] = None
    body: Optional[str] = None
    text: Optional[str] = None
    hit: Optional[str] = None
    guard: Optional[str] = None
    counter: Optional[str] = None
    special: Optional[str] = None
    g_top: Optional[str] = None
    g_mid: Optional[str] = None
    g_bot: Optional[str] = None
    type: Optional[str] = '공격'
    code: Optional[str] = None
    image_url: Optional[str] = None
    image_mid_url: Optional[str] = None
    image_sm_url: Optional[str] = None
    hidden_keyword: Optional[str] = None
    keyword: Optional[str] = None
    search: Optional[str] = None

class CardCreate(CardBase):
    character_id: Optional[int] = None

class CardUpdate(CardBase):
    character_id: Optional[int] = None

class CardOut(CardBase):
    id: int
    character_id: Optional[int]

    class Config:
        orm_mode = True
