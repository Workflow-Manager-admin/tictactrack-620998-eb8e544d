from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..models.models import Game, GameMove, GameStatus
from ..database.database import get_db
from ..database.schema import Game as GameDB, GameHistory as GameHistoryDB, User as UserDB
from ..auth.auth import get_current_user
from ..game.game_logic import check_winner, is_board_full, make_move, is_valid_move

router = APIRouter()


@router.post("/games", response_model=Game)
def create_game(
    opponent_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new game with another player."""
    opponent = db.query(UserDB).filter(UserDB.id == opponent_id).first()
    if not opponent:
        raise HTTPException(status_code=404, detail="Opponent not found")

    if opponent.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot create game with yourself")

    game = GameDB(
        player1_id=current_user.id,
        player2_id=opponent.id,
        current_player_id=current_user.id,
        board=" " * 9,
        status=GameStatus.IN_PROGRESS,
    )

    db.add(game)
    db.commit()
    db.refresh(game)
    return game


@router.post("/games/{game_id}/move", response_model=Game)
def make_game_move(
    game_id: int,
    move: GameMove,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Make a move in the game."""
    game = db.query(GameDB).filter(GameDB.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    if game.status != GameStatus.IN_PROGRESS:
        raise HTTPException(status_code=400, detail="Game is already finished")

    if game.current_player_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not your turn")

    if not is_valid_move(game.board, move.position):
        raise HTTPException(status_code=400, detail="Invalid move")

    # Make the move
    player_symbol = "X" if current_user.id == game.player1_id else "O"
    game.board = make_move(game.board, move.position, player_symbol)

    # Record the move in history
    history = GameHistoryDB(
        game_id=game.id,
        player_id=current_user.id,
        position=move.position
    )
    db.add(history)

    # Check game status
    winner = check_winner(game.board)
    if winner:
        game.status = GameStatus.COMPLETED
        game.winner_id = game.player1_id if winner == "X" else game.player2_id
    elif is_board_full(game.board):
        game.status = GameStatus.DRAW
    else:
        # Switch current player
        next_player = (
            game.player2_id if current_user.id == game.player1_id else game.player1_id
        )
        game.current_player_id = next_player

    db.commit()
    db.refresh(game)
    return game


@router.get("/games/active", response_model=List[Game])
def get_active_games(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all active games for the current user."""
    games = (
        db.query(GameDB)
        .filter(
            (GameDB.player1_id == current_user.id)
            | (GameDB.player2_id == current_user.id)
            & (GameDB.status == GameStatus.IN_PROGRESS)
        )
        .all()
    )
    return games


@router.get("/games/history", response_model=List[Game])
def get_game_history(
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get completed game history for the current user."""
    games = (
        db.query(GameDB)
        .filter(
            (GameDB.player1_id == current_user.id)
            | (GameDB.player2_id == current_user.id)
            & (GameDB.status != GameStatus.IN_PROGRESS)
        )
        .all()
    )
    return games
