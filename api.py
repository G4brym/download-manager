import atexit

from fastapi import FastAPI, Depends

from main.auth import authorizer
from main.router import router
from main.tasks import scheduler

app = FastAPI(
    title="Download Manager",
    version="1.0",
    docs_url="/",
    openapi_prefix="/api/v1",
    dependencies=[Depends(authorizer)],
)

atexit.register(lambda: scheduler.shutdown())
scheduler.start()

app.include_router(router)
