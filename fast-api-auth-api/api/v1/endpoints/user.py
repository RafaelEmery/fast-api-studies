from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

# It's better to name models with sufix "Model" to avoid conflicts with schemas
from models.user import User as UserModel
# It's better to name schemas with sufix "Schema" to avoid conflicts with models
from schemas.user import BaseUser, UserCreate, UserUpdate, UserArticles

from core.deps import get_session, get_current_user
from core.security import generate_hash_password
from core.auth import authenticate, create_access_token


router = APIRouter()


@router.get('/logged', response_model=BaseUser, status_code=status.HTTP_200_OK)
def get_logged_user(user: UserModel = Depends(get_current_user)):
    """
    Get logged user. In other contexts this endpoint is name "/me".
    """
    return user


@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=BaseUser)
async def create_user(request_user: UserCreate, db: AsyncSession = Depends(get_session)):
    """
    Create a new user and return user schema without password.
    """
    async with db() as session:
        try:
            new_user = UserModel(
                name=request_user.name, 
                last_name=request_user.last_name,
                email=request_user.email, 
                password=generate_hash_password(request_user.password),
                is_admin=request_user.is_admin
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)

            return new_user
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email already exists")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post('/login')
async def login(request: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    """
    Login user and return access token.
    The request parameter is a form data type with email and password.
    """
    user = await authenticate(request.email, request.password, db)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    return JSONResponse(content={"access_token": create_access_token(user.id), "token_type": "bearer"})

@router.get('/', response_model=List[BaseUser])
async def get_users(db: AsyncSession = Depends(get_session)):
    """
    Get all users.
    """
    async with db() as session:
        result = await session.execute(select(UserModel))
        users: List[BaseUser] = result.scalars().unique().all()

        return users


@router.get('/{user_id}', response_model=UserArticles)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    """
    Get user by id with all articles.
    """
    async with db() as session:
        result = await session.execute(select(UserModel).filter(UserModel.id == user_id))
        user: UserModel = result.scalars().unique().one_or_none()

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user


@router.put('/{user_id}', response_model=BaseUser, status_code=status.HTTP_202_ACCEPTED)
async def update_user(user_id: int, request_user: UserUpdate, db: AsyncSession = Depends(get_session)):
    """
    Update user by id.
    """
    async with db() as session:
        result = await session.execute(select(UserModel).filter(UserModel.id == user_id))
        user: UserModel = result.scalars().unique().one_or_none()

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user.name = request_user.name
        user.last_name = request_user.last_name
        user.email = request_user.email
        user.password = generate_hash_password(request_user.password)
        user.is_admin = request_user.is_admin

        await session.commit()

        return user
    

@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    """
    Delete user by id.
    """
    async with db() as session:
        result = await session.execute(select(UserModel).filter(UserModel.id == user_id))
        user: UserModel = result.scalars().unique().one_or_none()

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        session.delete(user)
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    