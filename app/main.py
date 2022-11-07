import logging

import uvicorn
from fastapi import FastAPI

from app.api.routes import api
from app.core.app_events import create_start_app_handler, create_stop_app_handler
from app.core.config import config

logger = logging.getLogger("uvicorn.error")


def get_application() -> FastAPI:
    application = FastAPI(
        title=config.SERVICE_NAME,
        description=config.DESCRIPTION,
        debug=config.DEBUG,
    )
    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))

    application.include_router(api.api_router, prefix=config.API_V1_STR)
    application.include_router(api.employees_router, prefix=config.API_V1_STR)

    return application


app = get_application()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
