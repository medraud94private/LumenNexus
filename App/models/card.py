# app/models/card.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False) 
    ruby = Column(String(100), nullable=True)      # 루비(읽는 법)
    frame = Column(Integer, nullable=True)         # 속도
    damage = Column(Integer, nullable=True)        # 대미지
    pos = Column(String(3), nullable=True)         # 판정 (상단/중단/하단 등)
    body = Column(String(10), nullable=True)       # 부위 (손/발/등등)
    text = Column(Text, nullable=True)             # 카드 효과
    hit = Column(String(4), nullable=True)
    guard = Column(String(4), nullable=True)
    counter = Column(String(4), nullable=True)
    special = Column(String(20), nullable=True)    # 특수판정
    g_top = Column(String(5), nullable=True)       # 상단방어
    g_mid = Column(String(5), nullable=True)       # 중단방어
    g_bot = Column(String(5), nullable=True)       # 하단방어
    type = Column(String(10), nullable=False, default='공격')  # 공격/수비/특수/...
    code = Column(String(20), nullable=True)       # 카드 코드

    # 캐릭터와의 관계
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=True)
    character = relationship("Character", back_populates="cards")

    # 이미지 필드
    image_url = Column(String, nullable=True)
    image_mid_url = Column(String, nullable=True)
    image_sm_url = Column(String, nullable=True)

    # 검색 관련
    hidden_keyword = Column(String(255), nullable=True, default='')
    keyword = Column(String(255), nullable=True, default='')
    search = Column(String(255), nullable=True, default='')
