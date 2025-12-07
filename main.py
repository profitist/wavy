from fastapi import FastAPI
from app.api.routers import user
from app.api.routers import track
from app.api.routers import tokens
from app.api.routers import friendship
from app.api.routers import shared_track

app = FastAPI()

app.include_router(friendship.router)
app.include_router(user.router)
app.include_router(tokens.router)
app.include_router(track.router)
app.include_router(shared_track.router)
