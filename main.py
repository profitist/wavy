from fastapi import FastAPI
from app.api.routers import user
from app.api.routers import track


app = FastAPI()

app.include_router(user.router)
app.include_router(track.router)