from typing import List, Union, Annotated
import serializers
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import text, CursorResult, RowMapping
from database import engine
from utils.helper import make_sql, response, calc_age
from lib.auth import get_password_hash, hash_djb2, get_user, get_current_user, verify_password
from env import SALT


router = APIRouter(
    prefix='/departments',
    tags=['department']
)


@router.get("/{id}/users")
async def department_get(id: int, current_user: Annotated[serializers.UserOut, Depends(get_current_user)]):
    q = text(
        "SELECT * "
        "FROM users u "
        "JOIN department d ON u.department_id = d.id "
        "WHERE d.id = :id"
    )
    values = {
        "id": id
    }
    with engine.begin() as conn:
        result: RowMapping = conn.execute(q, values).mappings().all()
        users = []
        for item in result:
            # apprend views depend on user role
            users.append(
                serializers.UserAdminView(**dict(item))
                if current_user.role == "admin" else
                serializers.UserView(**dict(item))
            )
        if len(users) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No department or user assigned"
            )

    return users
