import atexit

from fastapi import FastAPI, Depends

from downloads.auth import authorizer
from downloads.tasks import scheduler
from downloads.views import router as api_router

app = FastAPI(
    title="Download Manager",
    version="1.0",
    docs_url="/",
    dependencies=[Depends(authorizer)]
)

atexit.register(lambda: scheduler.shutdown())
scheduler.start()

app.include_router(api_router, prefix='/api/v1')
