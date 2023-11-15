import datetime
import json

from database.dao.camera import CameraDAO
from database.dao.person import PersonDAO
from database.dao.user import UserDAO
from database.models.user import UserModel
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from utils import authentication
from utils.authentication import password as auth_password
from web.api.user.schema import UserOutputDTO

router = APIRouter(prefix="/auth")


@router.post("/sign-in")
async def sign_in(input_data: OAuth2PasswordRequestForm = Depends()) -> Response:
    """
    User sign in.

    Args:
        input_data (OAuth2PasswordRequestForm): Input data. Defaults to Depends().

    Raises:
        HTTPException: HTTP error code

    Returns:
        Response: Response for user
    """
    # Generate token for user
    user = await authentication.authenticate(input_data.username, input_data.password)
    # Raise error when user is None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate token
    token = authentication.encode_token(data={"id": user.user_id})

    # Set header and content
    headers = {
        "Authorization": f"Bearer {token}",
    }
    content = json.dumps(
        {
            "access_token": token,
            "token_type": "bearer",
        },
    )

    # Create response
    response = Response(
        content=content,
        headers=headers,
        status_code=201,
    )

    # Return response
    return response


@router.post(
    "/sign-up",
    response_model=UserOutputDTO,
    status_code=status.HTTP_201_CREATED,
)
async def sign_up(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_dao: UserDAO = Depends(),
) -> UserModel:
    """
    User sign up.

    Args:
        form_data (OAuth2PasswordRequestForm): form data. Defaults to Depends().
        user_dao (UserDAO): user dao object. Defaults to Depends().

    Raises:
        HTTPException: HTTP error code

    Returns:
        UserModel: User object
    """
    # Destructuring
    username = form_data.username
    password = form_data.password

    # Raise error if user already exist
    if await authentication.is_user_exist(username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exist",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Hash password
    hashed_password = auth_password.hash_password(password)

    # Create user
    return await user_dao.create(name=username, username=username, password=hashed_password)


@router.get("/me", response_model=UserOutputDTO)
async def me(user: UserModel = Depends(authentication.get_current_user)) -> UserModel:
    """
    Find user.

    Args:
        user (UserModel): User object. Defaults to Depends(auth.get_current_user).

    Returns:
        UserModel: User object
    """
    return user
