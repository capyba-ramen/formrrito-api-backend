from typing import Dict, List

from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api_user import crud
from app.main import get_db


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
