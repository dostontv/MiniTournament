from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey, Table, UniqueConstraint, DateTime
from sqlalchemy.orm import Mapped, relationship

from app.db import Base
from app.models import User


class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True)
    max_players = Column(SmallInteger)
    players: Mapped[list[User]] = relationship(secondary='tournament_user_association', lazy='selectin')
    start_at = Column(DateTime(timezone=True))


tournament_user_association = Table(
    "tournament_user_association",
    Base.metadata,
    Column("tournament_id", ForeignKey(Tournament.id)),
    Column("user_id", ForeignKey(User.id)),
    UniqueConstraint("tournament_id", "user_id", name="unique_tournament_user")
)
