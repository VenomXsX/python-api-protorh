from database import SessionLocal
import serializers
from fastapi import APIRouter
from sqlalchemy import text, CursorResult, RowMapping
from utils import helper


router = APIRouter(
    prefix='/requests',
    tags=['request']
)


db = SessionLocal()


@router.get("/")
def GetEventAll():
    q = text("SELECT * FROM request_rh")
    res: RowMapping = db.execute(q).mappings().all()
    db.commit()
    return helper.response(
        200,
        "RequestRHs found" if len(res) != 0 else "No requestRHs found",
        data=res
    )


@router.get("/{id}")
def GetEvent(id):
    q = text("SELECT * FROM request_rh WHERE id = :id LIMIT 1")
    # useing mappings to turn it as Array
    # because it return CursorResult by default
    res: RowMapping = db.execute(q, {"id": id}).mappings().all()
    db.commit()
    if len(res) == 0:
        return helper.response(404, "No requestRH found. id: " + id)
    return helper.response(200, "Event found. id: " + id, data=res[0])


@router.post("/create")
def Create(item: serializers.RequestRHRequired):
    q = text(
        "INSERT INTO request_rh"
        "(user_id, content, registration_date,"
        "visibility, close, last_action, content_history)"
        "VALUES"
        "(:user_id, :content, :registration_date,"
        ":visibility, :close, :last_action,"
        "(:content_history)::json[])"
    )
    values = {
        "user_id": item.user_id,
        "content": item.content,
        "registration_date": item.registration_date,
        "visibility": item.visibility,
        "close": item.close,
        "last_action": item.last_action,
        "content_history": helper.dict_to_sql_array(item.content_history)
    }
    res: CursorResult = db.execute(q, values)
    db.commit()
    if res.rowcount == 0:
        return helper.response(
            400,
            "Oops an error occured, please retry",
            data=values,
            res=res
        )
    return helper.response(200, "Successfully addded", data=values, res=res)


@router.delete("/{id}")
def Delete(id):
    q = text("DELETE FROM request_rh WHERE id = :id")
    res: CursorResult = db.execute(q, {"id": id})
    db.commit()
    if res.rowcount == 0:
        return helper.response(
            400,
            "This requestRH does not exist, id: " + id,
            res=res
        )
    return helper.response(200, "Sucessfully deleted, id: " + id, res=res)


@router.put("/{id}")
def Update(id, item: serializers.RequestRHOptional):
    set_string, values = helper.make_fields(
        item,
        ["user_id", "content", "registration_date", "visibility",
            "close", "last_action"],
        id=id
    )

    # set current history if exist
    content_history = ""
    if item.content_history != None:
        values["content_history"] = helper.dict_to_sql_array(
            item.content_history)
        content_history = ",content_history = (:content_history)::json[]"

    q = text(helper.trim(
        f"UPDATE request_rh SET {set_string} {content_history}"
        "WHERE id = :id"
    ))
    res: CursorResult = db.execute(q, values)
    db.commit()
    if res.rowcount == 0:
        return helper.response(
            400,
            "Nothing updated, please double check the id",
            data=values,
            res=res
        )

    return helper.response(
        200,
        "Successfully updated, id: " + id,
        data=values,
        res=res
    )
