from app.asgi import get_asgi_application

from app.db import database


app = get_asgi_application()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
