from fastapi import APIRouter

from api.endpoints.v1.users import router as user_router

router = APIRouter(
    prefix='/api_v1',
)

# TODO: Добавить роутеры для версии 1
router.include_router(
    user_router,
    prefix='/users',
    tags=['users'],
)
