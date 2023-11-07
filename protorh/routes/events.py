from database import SessionLocal
import serializers
from fastapi import APIRouter
from sqlalchemy import text, CursorResult, RowMapping
from utils.helper import make_sql, response

router = APIRouter(
    prefix="/events",
    tags=["event"]
)


db = SessionLocal()


# Endpoint : /events
# Type : GET
# JWT required : False
# get all events
@router.get("/")
def GetEventAll():
    q, _ = make_sql("SELECT", table="event")
    res: RowMapping = db.execute(text(q)).mappings().all()
    db.commit()
    return response(
        200,
        "Events found" if len(res) != 0 else "No events found",
        data=res
    )


# Endpoint : /events
# Type : GET
# JWT required : False
# get event by id
@router.get("/{id}")
def GetEvent(id):
    q, values = make_sql("SELECT", table="event", id=id)
    # using mappings to turn it as Array
    # because it return CursorResult by default
    res: RowMapping = db.execute(text(q), values).mappings().all()
    db.commit()
    if len(res) == 0:
        return response(404, "No event found. id: " + id)
    return response(200, "Event found. id: " + id, data=res[0])


# Endpoint : /events/create
# Type : POST
# JWT required : False
# create an event
@router.post("/create")
def Create(items: serializers.EventRequired):
    q, values = make_sql(
        "CREATE",
        table="event",
        items=items,
        fields=[
            "name",
            "date",
            "description",
            "user_id",
            "department_id"
        ]
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


# Endpoint : /events/{event_id}
# Type : DELETE
# JWT required : False
# delete an event
@router.delete("/{id}")
def Delete(id):
    q, values = make_sql(
        "DELETE",
        table="event",
        id=id
    )
    res: CursorResult = db.execute(text(q), values)
    db.commit()
    if res.rowcount == 0:
        return response(
            400,
            "This event does not exist, id: " + id,
            res=res
        )
    return response(200, "Sucessfully deleted, id: " + id, res=res)


# Endpoint : /events/{event_id}
# Type : PATCH
# JWT required : False
# update an event by id
@router.patch("/{id}")
def Update(id, items: serializers.EventOptional):
    q, values = make_sql(
        "UPDATE",
        table="event",
        id=id,
        items=items,
        fields=[
            "name",
            "date",
            "description",
            "user_id",
            "department_id"
        ]
    )
    res: CursorResult = db.execute(text(q), values)
    db.commit()
    if res.rowcount == 0:
        return response(
            400,
            "Nothing updated, please double check the id",
            data=values,
            res=res
        )

    return response(
        200,
        "Successfully updated, id: " + id,
        data=values,
        res=res
    )


# Endpoint : /events/{event_id}
# Type : PUT
# JWT required : False
# update an event or create new one
@router.put("/{id}")
def UpdateOrCreate(id, items: serializers.EventRequired):
    q, values = make_sql(
        "UPDATE",
        table="event",
        items=items,
        id=id,
        fields=[
            "name",
            "date",
            "description",
            "user_id",
            "department_id"
        ]
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
