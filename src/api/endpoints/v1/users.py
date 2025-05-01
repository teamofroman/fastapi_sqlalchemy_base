from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_session_with_commit
from dao.user_dao import user_dao
from schemas.user import UserCreate, UserDB, UserUpdate

router = APIRouter()


@router.get(
    '/',
    response_model=list[UserDB],
)
async def get_all_users(
    session: AsyncSession = Depends(get_session_with_commit),
) -> list[UserDB]:
    """Получение списка пользователей."""
    user_list = await user_dao.find_all(session=session)

    return user_list or []


@router.post(
    '/',
    response_model=UserDB,
)
async def create_user(
    new_user: UserCreate,
    session: AsyncSession = Depends(get_session_with_commit),
) -> UserDB:
    """Создание пользователя."""
    return await user_dao.create(session=session, new_object=new_user)


@router.patch(
    '/{user_id}',
    response_model=UserDB,
)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: AsyncSession = Depends(get_session_with_commit),
) -> UserDB:
    """Обновляем пользователя."""
    user = await user_dao.get_one_or_none_by_id(session=session, obj_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден.')

    return await user_dao.update(
        session=session,
        update_object=user,
        update_data=user_update,
    )


@router.delete(
    '/{user_id}',
    response_class=Response,
)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session_with_commit),
) -> Response:
    """Удаляем пользователя из БД."""
    user = await user_dao.get_one_or_none_by_id(session=session, obj_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail='Пользователь не найден.')

    await user_dao.delete(session=session, delete_object=user)
    return Response(status_code=204)
