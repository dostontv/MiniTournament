from datetime import datetime

from loguru import logger
from pydantic import BaseModel, field_validator, computed_field, Field, ConfigDict

from app.schemas import UserRead


class TournamentBase(BaseModel):
    name: str
    max_players: int
    start_at: datetime


class TournamentCreate(TournamentBase):

    @field_validator('start_at', mode='after')
    @classmethod
    def validate(cls, start_at: datetime):
        if start_at < datetime.now():
            logger.error(f'start_at must be before now {start_at}')
            raise ValueError('start_at must be before now')
        return start_at


class TournamentRead(TournamentBase):
    id: int
    players: list[UserRead] = Field(exclude=True)

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def registered_players(self) -> int:
        return len(self.players)


