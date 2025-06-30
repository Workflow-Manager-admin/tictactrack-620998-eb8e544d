from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
from ..models.models import GameStatus


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    games_as_player1 = relationship(
        "Game", foreign_keys="Game.player1_id", back_populates="player1"
    )
    games_as_player2 = relationship(
        "Game", foreign_keys="Game.player2_id", back_populates="player2"
    )


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    player1_id = Column(Integer, ForeignKey("users.id"))
    player2_id = Column(Integer, ForeignKey("users.id"))
    current_player_id = Column(Integer, ForeignKey("users.id"))
    board = Column(String)
    status = Column(Enum(GameStatus))
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    player1 = relationship(
        "User", foreign_keys=[player1_id], back_populates="games_as_player1"
    )
    player2 = relationship(
        "User", foreign_keys=[player2_id], back_populates="games_as_player2"
    )
    moves = relationship("GameHistory", back_populates="game")


class GameHistory(Base):
    __tablename__ = "game_history"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    player_id = Column(Integer, ForeignKey("users.id"))
    position = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    game = relationship("Game", back_populates="moves")
