# app/api/character.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import async_session
from app.models.character import Character
from app.schemas.character_schema import CharacterCreate, CharacterUpdate, CharacterOut

router = APIRouter(prefix="/characters", tags=["Character"])

@router.get("/", response_model=list[CharacterOut])
async def get_characters(db: AsyncSession = Depends(async_session)):
    result = await db.execute(select(Character))
    return result.scalars().all()

@router.post("/", response_model=CharacterOut)
async def create_character(
    character_in: CharacterCreate,
    db: AsyncSession = Depends(async_session)
):
    new_char = Character(**character_in.dict())
    db.add(new_char)
    await db.commit()
    await db.refresh(new_char)
    return new_char

@router.get("/{char_id}", response_model=CharacterOut)
async def get_character(char_id: int, db: AsyncSession = Depends(async_session)):
    result = await db.execute(select(Character).where(Character.id == char_id))
    character = result.scalar_one_or_none()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character

@router.put("/{char_id}", response_model=CharacterOut)
async def update_character(
    char_id: int,
    character_in: CharacterUpdate,
    db: AsyncSession = Depends(async_session)
):
    result = await db.execute(select(Character).where(Character.id == char_id))
    character = result.scalar_one_or_none()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    for field, value in character_in.dict(exclude_unset=True).items():
        setattr(character, field, value)

    await db.commit()
    await db.refresh(character)
    return character

@router.delete("/{char_id}")
async def delete_character(char_id: int, db: AsyncSession = Depends(async_session)):
    result = await db.execute(select(Character).where(Character.id == char_id))
    character = result.scalar_one_or_none()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    await db.delete(character)
    await db.commit()
    return {"detail": "Character deleted"}
