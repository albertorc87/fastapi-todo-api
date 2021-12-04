from fastapi import FastAPI

from app.v1.router.user_router import router as user_router
from app.v1.router.todo_router import router as todo_router

app = FastAPI()

app.include_router(user_router)
app.include_router(todo_router)