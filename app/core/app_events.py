import logging
from typing import Callable


def create_start_app_handler() -> Callable:
    async def start_app() -> None:
        from app.db.base import database

        logging.info("connecting to a postgresql")
        await database.connect()
        logging.info("Database connection - successful")

    return start_app


def create_stop_app_handler() -> Callable:
    async def stop_app() -> None:
        from app.db.base import database

        logging.info("Closing connection to postgresql")
        await database.disconnect()
        logging.info("Database connection - closed")

    return stop_app
