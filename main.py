from fastapi import FastAPI

from routers import router

app = FastAPI(
    title="API_WALLET"
)

app.include_router(router)