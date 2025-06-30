from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


class GameStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DRAW = "draw"


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class GameMove(BaseModel):
    position: int
    player_id: int


class Game(BaseModel):
    id: int
    player1_id: int
    player2_id: int
    current_player_id: int
    board: str  # Stores the board as a string of 9 characters (e.g., "X O X O")
    status: GameStatus
    winner_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GameHistory(BaseModel):
    id: int
    game_id: int
    player_id: int
    position: int
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
