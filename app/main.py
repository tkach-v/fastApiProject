import uvicorn
from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from app.routers.users import router as users_router
from app.routers.orders import router as orders_router

from app.core.config import settings


app = FastAPI(title="Repair Workshop")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(tags=["Health Check"])


@router.get("/health")
def health_check():
    return {"status_code": 200, "detail": "ok", "result": "working"}


app.include_router(router)
app.include_router(users_router)
app.include_router(orders_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
