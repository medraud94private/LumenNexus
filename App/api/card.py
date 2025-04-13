# app/api/card.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.card import Card
from app.schemas.card_schema import CardCreate, CardUpdate, CardOut


router = APIRouter(prefix="/cards", tags=["Card"])

@router.get("/", response_model=list[CardOut])
async def get_cards(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Card))
    return result.scalars().all()

@router.post("/", response_model=CardOut)
async def create_card(
    card_in: CardCreate,
    db: AsyncSession = Depends(get_db)
):
    new_card = Card(**card_in.dict())
    db.add(new_card)
    await db.commit()
    await db.refresh(new_card)
    return new_card

@router.get("/{card_id}", response_model=CardOut)
async def get_card(card_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Card).where(Card.id == card_id))
    card = result.scalar_one_or_none()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card

@router.put("/{card_id}", response_model=CardOut)
async def update_card(
    card_id: int,
    card_in: CardUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Card).where(Card.id == card_id))
    card = result.scalar_one_or_none()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    for field, value in card_in.dict(exclude_unset=True).items():
        setattr(card, field, value)

    await db.commit()
    await db.refresh(card)
    return card

@router.delete("/{card_id}")
async def delete_card(card_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Card).where(Card.id == card_id))
    card = result.scalar_one_or_none()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    await db.delete(card)
    await db.commit()
    return {"detail": "Card deleted"}
