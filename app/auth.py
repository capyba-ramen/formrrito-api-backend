from datetime import datetime, timedelta
from typing import Dict, List, Annotated, Union

from fastapi import Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api_user import crud
from app.main import get_db
from .main import app


def authorize_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.headers["Authorization"]
    user = crud.get_user(db, int(user_id))

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    method = request.method
    path = request.url.path

    resource = get_resource_name(path)

    # 判斷角色權限
    role = user.role

    permissions = RolePermission.role_permissions[role]

    if resource not in permissions:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user.username


def get_resource_name(path: str):
    first_slash_index = path.find('/')
    second_slash_index = path.find('/', first_slash_index + 1)
    third_slash_index = path.find('/', second_slash_index + 1)
    resource = path[second_slash_index + 1:third_slash_index]
    return resource


class RolePermission:
    ORDINARY = 0
    ADMIN = 1

    role_permissions: Dict[int, List[str]] = {
        0: ["todo"],
        1: ["user", "todo"]
    }


# ==================OAuth2 for Authentication=========================
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "66c22844474a942ec6274060bdcba41d4c734c3940baed271bb2a6c6b21ecb47"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    """
    Use passlib[bcrypt] for hashing
    """
    return password_context.hash(password)


def verify_password(password: str, hashed_password):
    return password_context.verify(password, hashed_password)


def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_user_by_username(db, username)
    if not user or not verify_password(password, user.password):
        return False

    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db)

):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@app.post(
    "/token"
)
def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)
):
    """
    The response should be a JSON object
    The response should have a token_type: "bearer"
    """

    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
