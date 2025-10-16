from fastapi import FastAPI

from kubiya.server.routes import router


def create_app():
    app = FastAPI()
    app.include_router(router)
    return app
