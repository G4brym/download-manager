import atexit

from fastapi import FastAPI, Depends

from common.auth import authorizer
from common.router import router
from common.tasks import scheduler

app = FastAPI(
    title="Download Manager",
    version="1.0",
    docs_url="/",
    dependencies=[Depends(authorizer)],
)

atexit.register(lambda: scheduler.shutdown())
scheduler.start()

app.include_router(router, prefix="/api/v1")
