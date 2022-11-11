from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from bastion.apps import api_router
from bastion.config import settings
from bastion.database.database import Base, engine

def create_app() -> FastAPI:
    app = FastAPI()
    # app.add_middleware(
    #     CORSMiddleware,
    #     # allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    #     allow_origins=["*"],
    #     allow_credentials=True,
    #     allow_methods=["*"],
    #     allow_headers=["*"],
    # )
    app.include_router(api_router)

    print("app created")
    return app


app = create_app()


@app.get("/")
def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True if settings.DEBUG else False,
    )
