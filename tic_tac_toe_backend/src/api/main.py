from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .auth_routes import router as auth_router
from .game_routes import router as game_router
from ..database.database import engine
from ..database.schema import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Tic Tac Toe API",
    description="Backend API for the Tic Tac Toe game",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(game_router, prefix="/api", tags=["Game"])


@app.get("/")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Tic Tac Toe API is running"}
