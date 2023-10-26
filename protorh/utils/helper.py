from typing import List, Union, Literal
from sqlalchemy import CursorResult
from datetime import date, datetime
import json


SQL_METHOD = Literal["SELECT", "CREATE", "UPDATE", "DELETE"]
TABLES = Literal["event", "users", "request_rh", "department"]


def printer(*items):
    for item in items:
        print(item)
    print("")


def formatDateToString(date: date):
    return date.strftime("%Y-%m-%d")


def formatStringToDate(input: str):
    return datetime.strptime(input, "%Y-%m-%d")


def calc_age(birth: date):
    today = date.today()
    return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))


def json_dump_array(obj: dict):
    res = []

    for val in obj:
        res.append(json.dumps(val))

    return res


def trim(str: str):
    return " ".join(str.split())


def missing(name: str):
    return f"Missing '{name}' in UPDATE method"


def check_id_email(id=None, email=None):
    if id is None and email is None:
        raise Exception(
            "Check_Id_Email(): please pass an id or email"
        )
    if id is not None and email is not None:
        raise Exception(
            "Check_Id_Email(): Can't pass both 'id' and 'email', please pass just 'id' or just 'email'"
        )


def sql_where(id=None, email=None, ):
    """
    return `where` and `prepare`
    """
    check_id_email(id, email)

    prepare = {}
    where = ""
    if id is not None:
        where = "WHERE id = :id"
        prepare["id"] = id
    if email is not None:
        where = "WHERE email = :email"
        prepare["email"] = email

    return where, prepare


def sql_select(table, *, fields=None, id=None, email=None):
    select = ", ".join(fields) if fields is not None else "*"
    where, prepare = sql_where(id, email)

    return trim(f"SELECT {select} FROM {table} {where}"), prepare


def sql_create(table, items, fields, *, rjson=None, rarray=None):
    # throw Error: required fields
    if fields is None:
        raise Exception(missing("fields"))
    if items is None:
        raise Exception(missing("items"))

    select = []
    values = []
    prepare = {}
    if type(items) is not dict:
        items_dumps = items.model_dump()
    else:
        items_dumps = items

    for val in fields:
        if val in items_dumps and items_dumps[val] is not None:
            # check if there's a type dict or list
            # and if rjson and/or rarray are passed
            if type(items_dumps[val]) is dict and (rjson is None):
                raise Exception(missing("rjson"))
            if type(items_dumps[val]) is list and (rarray is None):
                raise Exception(missing("rarray"))

            # for Postgres weird json and json[]
            if rjson and val in rjson:
                values.append(f"(:{val})::json")
                prepare[val] = json.dumps(items_dumps[val])
            elif rarray and val in rarray:
                values.append(f"(:{val})::json[]")
                prepare[val] = json_dump_array(items_dumps[val])
            else:
                values.append(f":{val}")
                prepare[val] = items_dumps[val]

            select.append(val)

    select = ", ".join(select)
    values = ", ".join(values)

    return trim(f"INSERT INTO {table} ({select}) VALUES ({values})"), prepare


def sql_delete(table, id=None, email=None):
    where, prepare = sql_where(id, email)

    return f"DELETE FROM {table} {where}", prepare


def sql_update(table, items, fields, *, id=None, email=None, rjson=None, rarray=None):
    if fields is None:
        raise Exception(missing("fields"))
    if items is None:
        raise Exception(missing("items"))

    values = []
    where, prepare = sql_where(id, email)

    if type(items) is not dict:
        items_dumps = items.model_dump()
    else:
        items_dumps = items

    for val in fields:
        if val in items_dumps and items_dumps[val] is not None:
            # check if there's a type dict or list
            # and if rjson and/or rarray are passed
            if type(items_dumps[val]) is dict and (rjson is None):
                raise Exception(missing("rjson"))
            if type(items_dumps[val]) is list and (rarray is None):
                raise Exception(missing("rarray"))

            # for Postgres weird json and json[]
            if rjson and val in rjson:
                values.append(f"{val} = (:{val})::json")
                prepare[val] = json.dumps(items_dumps[val])
            elif rarray and val in rarray:
                values.append(f"{val} = (:{val})::json[]")
                prepare[val] = json_dump_array(items_dumps[val])
            else:
                values.append(f"{val} = :{val}")
                prepare[val] = items_dumps[val]

    values = ", ".join(values)

    return f"UPDATE {table} SET {values} {where}", prepare


def make_sql(
        q: SQL_METHOD,
        *,
        table: TABLES,
        id: Union[str, int] = None,
        email: str = None,
        items=None,
        fields: List[str] = None,
        rjson: List[str] = None,
        rarray: List[str] = None
):
    """
    ## definition

    * `rjson` is for `json`

    * `rarray` is for `json[]`
    """
    if q == "SELECT":
        res = sql_select(table, fields=fields, id=id, email=email)
    if q == "CREATE":
        res = sql_create(table, items, fields, rjson=rjson, rarray=rarray)
    if q == "DELETE":
        res = sql_delete(table, id, email)
    if q == "UPDATE":
        res = sql_update(
            table, items, fields, id=id,
            email=email, rjson=rjson, rarray=rarray)
    return res


def response(
        status: int,
        message: str,
        *,
        data=None,
        res: CursorResult = None
):
    return {"res": res, "status": status, "message": message, "data": data}
