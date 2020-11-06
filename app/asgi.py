from fastapi import FastAPI


def get_asgi_application() -> FastAPI:

    app = FastAPI()

    return app
