import logging

from fastapi import FastAPI

from database import check_db_connection
from routes.health import router as health_router
from routes.rules import router as rules_router

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

app = FastAPI(title="Praxis Rules Engine", version="0.1.0")

app.include_router(health_router)
app.include_router(rules_router)


@app.on_event("startup")
async def startup():
    await check_db_connection()
    logger.info("Praxis Rules Engine started on port 8004")
