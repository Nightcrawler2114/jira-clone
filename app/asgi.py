from fastapi import FastAPI

from app.routers import projects, sprints, tasks, users

def get_asgi_application() -> FastAPI:

    app = FastAPI()

    app.include_router(users.router)
    app.include_router(projects.router)
    app.include_router(sprints.router)
    app.include_router(tasks.router)

    return app
