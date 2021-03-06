from typing import Optional

import bcrypt
from fastapi import WebSocket
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import JWTDecodeError

from wealth.database.api import engine
from wealth.database.models import User

from .models import LoginUser
from .passwords import check_password


class CustomJwt(AuthJWT):
    async def get_jwt_user(self) -> User:
        user_id = self.get_jwt_user()
        user = None  # TODO Implement get user from database
        if user is None:
            raise JWTDecodeError(
                status_code=401,
                message=f"User in header {self._header_name} is not a valid user",
            )
        return user

    async def jwt_required_and_get_user(self) -> User:
        self.jwt_required()
        return await self.get_jwt_user()

    def jwt_forbidden(
        self,
        auth_from: str = "request",
        token: Optional[str] = None,
        websocket: Optional[WebSocket] = None,
        csrf_token: Optional[str] = None,
    ):
        """
        Checks that there is not JWT
        """
        self.jwt_optional(auth_from, token, websocket, csrf_token)
        if self.get_jwt_subject() is not None:
            raise JWTDecodeError(
                status_code=422,
                message=f"Header {self._header_name} is not allowed to be present",
            )

    async def login_user(self, user: LoginUser) -> User:
        db_user = await engine.find_one(User, User.email == user.email)
        if not db_user or not check_password(user.password, db_user.password):
            raise JWTDecodeError(status_code=401, message="User and password combination not correct")
        return db_user
