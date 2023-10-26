from database import SessionLocal
from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text, CursorResult, RowMapping
from utils.helper import make_sql, response, printer, check_id_email
import serializers
from lib.auth import verify_password, get_password_hash
from pydantic import BaseModel


router = APIRouter(
    prefix='/test',
    tags=['test']
)


db = SessionLocal()


@router.get("/")
def GetAll():
    check_id_email(id="s", email="azd")
    return "ok"
    # q, _ = make_sql("SELECT", table="test")
    # res: RowMapping = db.execute(text(q)).mappings().all()
    # db.commit()
    # raise HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="You're not authorized",
    #     headers={"WWW-Authenticate": "Bearer"}
    # )
    # return response(
    #     200,
    #     "Test found" if len(res) != 0 else "No test found",
    #     data=res
    # )


@router.get("/{id}")
def GetById(id):
    q, values = make_sql("SELECT", table="test", id=id)
    # useing mappings to turn it as Array
    # because it return CursorResult by default
    res: RowMapping = db.execute(text(q), values).mappings().all()
    db.commit()
    if len(res) == 0:
        return response(404, "No test found. id: " + id)
    return response(200, "test found. id: " + id, data=res[0])


# testing

class Testing(BaseModel):
    password: str
    hashed: str


@router.post("/test")
def testing(items: Testing):
    return {
        "hashed": get_password_hash(items.password),
        "is_valid": verify_password(items.password, items.hashed)
    }


@router.post("/create")
def Create(items: serializers.TestOptional):
    q, values = make_sql(
        "CREATE",
        table="test",
        items=items,
        fields=["name", "number", "date", "rjson", "rarray", "opened"],
        rjson=["rjson"],
        rarray=["rarray"]
    )
    res: CursorResult = db.execute(text(q), values)
    db.commit()
    if res.rowcount == 0:
        return response(
            400,
            "Oops an error occured, please retry",
            data=values,
            res=res
        )
    return response(200, "Successfully addded", data=values, res=res)


@router.delete("/{id}")
def Delete(id):
    q, values = make_sql(
        "DELETE",
        table="test",
        id=id
    )
    res: CursorResult = db.execute(text(q), values)
    db.commit()
    if res.rowcount == 0:
        return response(
            400,
            "This test does not exist, id: " + id,
            res=res
        )
    return response(200, "Sucessfully deleted, id: " + id, res=res)


@router.patch("/{id}")
def Update(id, items: serializers.TestOptional):
    q, values = make_sql(
        "UPDATE",
        table="test",
        id=id,
        items=items,
        fields=["name", "number", "date", "rjson", "rarray", "opened"],
        rjson=["rjson"],
        rarray=["rarray"]
    )
    res: CursorResult = db.execute(text(q), values)
    db.commit()
    if res.rowcount == 0:
        return response(
            400,
            "Nothing updated, please double check the 'id'",
            data=values,
            res=res
        )

    return response(
        200,
        "Successfully updated, id: " + id,
        data=values,
        res=res
    )


@router.put("/{id}")
def UpdateOrCreate(id, items: serializers.TestOptional):  # required
    q, values = make_sql(
        "UPDATE",
        table="test",
        items=items,
        id=id,
        fields=["name", "number", "date", "rjson", "rarray", "opened"],
        rjson=["rjson"],
        rarray=["rarray"]
    )
    res: CursorResult = db.execute(text(q), values)
    db.commit()

    if res.rowcount == 0:
        return Create(items)

    return response(
        200,
        "Successfully updated, id: " + id,
        data=values,
        res=res
    )


# example test

@router.post("/testing example")
def test(items: serializers.TestOptional):
    print(items)
    # select
    "SELECT * FROM event"
    "SELECT * FROM event WHERE id = :id LIMIT 1"

    # create
    "INSERT INTO event"
    "(name, date, description, user_id, department_id)"
    "VALUES"
    "(:name, :date, :description, :user_id, :department_id)"

    # delete
    "DELETE FROM event WHERE id = :id"

    # update
    "UPDATE event SET"
    "name = :name, description = :description"
    "WHERE id = :id"

    # scripts here

    # select
    printer(
        make_sql("SELECT", table="table"),
        make_sql("SELECT", table="table", id=5),
        make_sql("SELECT", table="table", id=123,
                 fields=["name", "desc", "date"])
    )

    # create
    printer(
        make_sql("CREATE", table="table",
                 items=items, fields=["name", "number", "date"]),
        make_sql("CREATE", table="table", items=items, fields=[
            "name", "number", "date", "json"], rjson=["json"]),
        make_sql("CREATE", table="table", items=items, fields=[
            "name", "number", "date", "json", "json_array"],
            rjson=["json"],
            rarray=["json_array"])
    )

    # delete
    printer(
        make_sql("DELETE", table="table", id=5)
    )

    # update
    printer(
        make_sql(
            "UPDATE",
            table="table",
            id=5,
            items=items,
            fields=["name", "desc", "date"]
        ),
        make_sql(
            "UPDATE",
            table="table",
            id=5,
            items=items,
            fields=["name", "desc", "date", "meta"],
            rjson=["meta"]
        ),
        make_sql(
            "UPDATE",
            table="table",
            id=5,
            items=items,
            fields=["name", "desc", "date", "meta", "history"],
            rjson=["meta"],
            rarray=["history"])
    )

    # q = text()
    # print(q)
    return response(
        200,
        "script executed",
    )
