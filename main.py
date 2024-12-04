from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.config import start_db

from routes.user import USER_ROUTES
from routes.anime import ANIME_ROUTES
from routes.pref import PREF_ROUTES


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_db()
    yield

app = FastAPI(lifespan=lifespan)
GRAPHQL_URL = "https://graphql.anilist.co"

@app.get("/")
def health_checkup():
    return {"msg": "Hi, The Backend is running"}

app.include_router(ANIME_ROUTES, prefix="/anime" ,tags=["anime"])
app.include_router(USER_ROUTES, prefix="/auth" ,tags=["auth"])
app.include_router(PREF_ROUTES, prefix="/user" ,tags=["user"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)