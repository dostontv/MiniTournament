import logging

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.exeptions import UserAlreadyExistsError, TournamentNotFoundError, TournamentFullError
from app.repositories import create_tournament
from app.repositories.tournament import add_user_to_tournament, get_players
from app.schemas import TournamentCreate, UserCreate, TournamentRead
from app.schemas.user import UserBase

tournament_router = APIRouter()


@tournament_router.post("/", response_model=TournamentRead, status_code=status.HTTP_201_CREATED)
async def create_tournament_api(tournament: TournamentCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_tournament(db=db, tournament=tournament)
    except IntegrityError:
        logger.error(f"Tournament {tournament.name} already exists")
        raise HTTPException(status_code=409, detail=f"Tournament {tournament.name} already exists")
    except Exception as e:
        logger.error(f"Create tournament error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@tournament_router.post(path="/{id}/register/", response_model=TournamentRead, status_code=status.HTTP_201_CREATED)
async def add_user_to_tournament_api(id: int, user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await add_user_to_tournament(db, id, user)
    except TournamentFullError:
        raise HTTPException(status_code=409, detail=f"Tournament with id {id} is full")
    except TournamentNotFoundError:
        logger.error(f"Tournament with id {id} not found")
        raise HTTPException(status_code=404, detail=f"Tournament with id {id} not found")
    except UserAlreadyExistsError as e:
        logger.error(f"User {user.name} already exists")
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        logger.exception(f'Create user error: {e}')
        raise HTTPException(status_code=500, detail="Internal server error")


@tournament_router.get("/{id}/players", response_model=list[UserBase], status_code=status.HTTP_200_OK)
async def get_tournament_players_api(id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await get_players(db, id)
    except TournamentNotFoundError:
        logger.error(f"Tournament with id {id} not found")
        raise HTTPException(status_code=404, detail=f"Tournament with id {id} not found")
    except Exception as e:
        logger.log(logging.WARNING, f'Get tournament players error: {e}')
        raise HTTPException(status_code=500, detail="Internal server error")
