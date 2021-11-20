from fastapi import FastAPI

from app.v1.router.user_router import router as user_router

app = FastAPI()

app.include_router(user_router)