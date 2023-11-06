from typing import List, Annotated
import serializers
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import text, CursorResult, RowMapping
from database import engine
from utils.helper import make_sql
from lib.auth import get_current_user


router = APIRouter(
    prefix='/departments',
    tags=['department']
)


# Endpoint : /api/departments
# Type : GET
# JWT required : False
# get all department
@router.get("/")
async def get_all():
    q, _ = make_sql("SELECT", table="department")
    with engine.begin() as conn:
        res: RowMapping = conn.execute(text(q)).mappings().all()
        if len(res) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There's no departments"
            )

    return res


# Endpoint : /api/departments
# Type : POST
# JWT required : False
# create a department
@router.post("/")
async def create(items: serializers.DepartmentRequired):
    q, values = make_sql(
        "CREATE",
        table="department",
        items=items,
        fields=["name"]
    )
    with engine.begin() as conn:
        res: CursorResult = conn.execute(text(q), values)
        if res.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something went wrong, please retry"
            )

    return {
        "message": "Successfully added: " + items.name}


# Endpoint : /api/departments/{department_id}/users
# Type : GET
# JWT required : True
# get users from department
@router.get("/{department_id}/users")
async def department_users_get(department_id: int, current_user: Annotated[serializers.UserOut, Depends(get_current_user)]):
    q = text(
        "SELECT * "
        "FROM users u "
        "JOIN department d ON u.department_id = d.id "
        f"WHERE d.id = {department_id}"
    )
    with engine.begin() as conn:
        result: RowMapping = conn.execute(q).mappings().all()
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


# Endpoint : /api/departments/{department_id}/users/add
# Type : POST
# JWT required : True
# add users in department
@router.post("/{department_id}/users/add")
async def department_users_add(department_id: int, user_ids: List[int], current_user: Annotated[serializers.UserOut, Depends(get_current_user)]):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You're not admin"
        )

    # convert to str: 1,2,3
    update_user_ids = ",".join(map(str, user_ids))
    q = text(
        "UPDATE users "
        f"SET department_id = {department_id} "
        f"WHERE id IN ({update_user_ids})"
    )
    with engine.begin() as conn:
        result: CursorResult = conn.execute(q)
    return f"updated successfully, {result.rowcount} affected"


# Endpoint : /api/departments/{department_id}/users/remove
# Type : POST
# JWT required : True
# remove users from department
@router.post("/{department_id}/users/remove")
async def department_users_remove(department_id: int, user_ids: List[int], current_user: Annotated[serializers.UserOut, Depends(get_current_user)]):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You're not admin"
        )

    update_user_ids = ",".join(map(str, user_ids))
    q = text(
        "UPDATE users "
        "SET department_id = null "
        f"WHERE department_id = {department_id} AND id IN ({update_user_ids})"
    )
    with engine.begin() as conn:
        result: CursorResult = conn.execute(q)
    return f"deleted successfully, {result.rowcount} affected"
