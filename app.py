from fastapi import FastAPI
from routes.user import user

app = FastAPI(
    title="My first API",
    description="Esta es mi primer api realizado con sudor",
    version="0.0.1",
    openapi_tags=[
        {
            "name": "users",
            "description": "CRUD de usuarios"
        }
    ]
)

app.include_router(user)