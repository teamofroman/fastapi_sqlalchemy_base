from dao.base_dao import BaseDAO
from models.user import User


class UserDao(BaseDAO[User]):
    """DAO для работы с пользователями."""

    model = User


user_dao = UserDao()
