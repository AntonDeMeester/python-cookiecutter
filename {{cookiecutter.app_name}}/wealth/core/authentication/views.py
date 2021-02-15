from fastapi import APIRouter, Depends

from wealth.core.authentication.jwt import CustomJwt
from wealth.database.api import engine
from wealth.database.models import User

from .models import CreateUser, LoginUser, Settings, UpdateUser, ViewUser

router = APIRouter()


@CustomJwt.load_config
def get_config():
    return Settings()


@router.post("/login")
async def login(user: LoginUser, authorize: CustomJwt = Depends()):
    await authorize.login_user(user)

    # subject identifier for who this token is for example id or username from database
    access_token = authorize.create_access_token(subject=user.email, fresh=True)
    refresh_token = authorize.create_refresh_token(subject=user.email)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh")
def refresh(authorize: CustomJwt = Depends()):
    """
    The jwt_refresh_token_required() function insures a valid refresh
    token is present in the request before running any code below that function.
    we can use the get_jwt_subject() function to get the subject of the refresh
    token, and use the create_access_token() function again to make a new access token
    """
    authorize.jwt_refresh_token_required()

    current_user = authorize.get_jwt_subject()
    new_access_token = authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}


@router.get("/user", response_model=ViewUser)
def get_user(authorize: CustomJwt = Depends()):
    authorize.jwt_required()

    current_user = authorize.get_jwt_user()
    return ViewUser.parse_obj(current_user)


@router.post("/user", response_model=ViewUser)
async def create_user(user: CreateUser, authorize: CustomJwt = Depends()):
    await user.async_validate()
    authorize.jwt_forbidden()

    db_user = User.parse_obj(user.dict())
    # TODO Create the user
    return_user = ViewUser.parse_obj(db_user.dict())
    return return_user


@router.put("/user", response_model=ViewUser)
async def update_user(user: UpdateUser, authorize: CustomJwt = Depends()):
    authorize.fresh_jwt_required()

    current_user = await authorize.get_jwt_user()
    # TODO Update the user

    return_user = ViewUser.parse_obj(current_user.dict())
    return return_user


# Password reset
