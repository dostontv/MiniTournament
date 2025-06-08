from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.exeptions import TournamentNotFoundError, UserAlreadyExistsError, TournamentFullError
from app.models import Tournament, User
from app.repositories import create_user


async def create_tournament(db, tournament):
    db_tournament = Tournament(**tournament.model_dump())
    db.add(db_tournament)
    await db.commit()
    await db.refresh(db_tournament)

    return db_tournament


async def add_user_to_tournament(db: AsyncSession, tournament_id: int, user):
    result = await db.execute(
        select(Tournament).options(selectinload(Tournament.players)).filter_by(id=tournament_id)
    )
    tournament: Tournament = result.scalars().first()
    if not tournament:
        raise TournamentNotFoundError(f"Tournament with id {tournament_id} not found")

    if len(tournament.players) + 1 > tournament.max_players:
        raise TournamentFullError(f"Tournament with id {tournament_id} is full")


    user_exists = (await db.execute(select(User).filter_by(email=user.email))).scalars().first()
    if not user_exists:
        user_exists = await create_user(db, user)

    if user_exists not in tournament.players:
        tournament.players.append(user_exists)
        db.add(tournament)
        await db.commit()
        await db.refresh(tournament)
        return tournament
    raise UserAlreadyExistsError(f"User with email {user.email} already exists")


async def get_players(db: AsyncSession, tournament_id: int):
    result = await db.execute(select(Tournament).filter_by(id=tournament_id))
    tournament = result.scalars().first()
    if not tournament:
        raise TournamentNotFoundError(f"Tournament with id {tournament_id} not found")
    return tournament.players
