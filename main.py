from fastapi import FastAPI
from app.api.routers import user
from app.api.routers import track
from app.api.routers import tokens
from app.api.routers import friendship


app = FastAPI()

app.include_router(friendship.router)
app.include_router(user.router)
app.include_router(tokens.router)
app.include_router(track.router)

