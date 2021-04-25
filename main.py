import atexit

from fastapi import FastAPI, Depends

from common.auth import authorizer
from common.router import router
from common.tasks import scheduler

app = FastAPI(
    title="Download Manager API",
    description="This is the api documentation for the Download Manager server\n\n"
    "For authentication, you must send the `authorization` header",
    version="1.0",
    docs_url="/",
    dependencies=[Depends(authorizer)],
    openapi_tags=[
        {"name": "Files", "description": "Everything about your files"},
    ],
)

atexit.register(lambda: scheduler.shutdown())
scheduler.start()

app.include_router(router, prefix="/api/v1")
