from typing import List, Union, Literal
from sqlalchemy import CursorResult
import json


class NewString:

    def __init__(self, data):
        self.data = data


def json_dump_array(obj: dict):
    res = []

    for val in obj:
        res.append(json.dumps(val))

    return res


def concat_set(container: NewString, attr_name: str):
    container.data += " " + attr_name + " = :" + attr_name + ","


def remove_last_comma(container: NewString):
    container.data = container.data[:-1]


def trim(str: str):
    return " ".join(str.split())


def missing(name: str):
    return f"Missing '{name}' in UPDATE method"


def make_fields(items, fields_name: List[str], *, id: Union[int, str] = None):
    str = NewString("")
    values = {}
    items_dump = items.model_dump()

    if id:
        values["id"] = id

    for i in range(len(fields_name)):
        if items_dump[fields_name[i]] != None:
            concat_set(str, fields_name[i])
            values[fields_name[i]] = items_dump[fields_name[i]]

    remove_last_comma(str)

    return str.data, values


def sql_select(table: str, *, fields: List[str] = None, id=None):
    select = ", ".join(fields) if fields != None else "*"
    where = ""
    prepare = {}
    if id != None:
        where = " WHERE id = :id"
        prepare["id"] = id
    return trim(f"SELECT {select} FROM {table} {where}"), prepare


def sql_create(table: str, items, fields: List[str], *, rjson: List[str] = None, rarray: List[str] = None):
    # throw Error: required fields
    if fields == None:
        raise Exception(missing("fields"))
    if items == None:
        raise Exception(missing("items"))

    select = []
    values = []
    prepare = {}
    items_dumps = items.model_dump()

    for val in fields:
        if val in items_dumps and items_dumps[val] != None:
            # check if there's a type dict or list and if rjson and/or rarray are passed
            if type(items_dumps[val]) is dict and (rjson == None):
                raise Exception(missing("rjson"))
            if type(items_dumps[val]) is list and (rarray == None):
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


def sql_delete(table: str, id: Union[str, int]):
    if id == None:
        raise Exception(missing("id"))
    prepare = {}
    prepare["id"] = id
    return f"DELETE FROM {table} WHERE id = :id", prepare


def sql_update(table: str, id: Union[str, int], items, fields: List[str], *, rjson: List[str] = None, rarray: List[str] = None):
    if id == None:
        raise Exception(missing("id"))
    if fields == None:
        raise Exception(missing("fields"))
    if items == None:
        raise Exception(missing("items"))

    new_fields = []
    prepare = {}
    items_dumps = items.model_dump()

    prepare['id'] = id

    for val in fields:
        if val in items_dumps and items_dumps[val] != None:
            # check if there's a type dict or list and if rjson and/or rarray are passed
            if type(items_dumps[val]) is dict and (rjson == None):
                raise Exception(missing("rjson"))
            if type(items_dumps[val]) is list and (rarray == None):
                raise Exception(missing("rarray"))

            # for Postgres weird json and json[]
            if rjson and val in rjson:
                new_fields.append(f"{val} = (:{val})::json")
                prepare[val] = json.dumps(items_dumps[val])
            elif rarray and val in rarray:
                new_fields.append(f"{val} = (:{val})::json[]")
                prepare[val] = json_dump_array(items_dumps[val])
            else:
                new_fields.append(f"{val} = :{val}")
                prepare[val] = items_dumps[val]

    values = ", ".join(new_fields)

    return f"UPDATE {table} SET {values} WHERE id = :id", prepare


def make_sql(q: Literal["SELECT", "CREATE", "UPDATE", "DELETE"], *, table: str, id: Union[str, int] = None,  items=None, fields: List[str] = None, rjson: List[str] = None, rarray: List[str] = None):
    """
    ## definition

    * `rjson` is for `json`

    * `rarray` is for `json[]`
    """
    if q == "SELECT":
        res = sql_select(table, fields=fields, id=id)
    if q == "CREATE":
        res = sql_create(table, items, fields, rjson=rjson, rarray=rarray)
    if q == "DELETE":
        res = sql_delete(table, id)
    if q == "UPDATE":
        res = sql_update(table, id, items, fields,
                         rjson=rjson, rarray=rarray)
    return res


def response(status: int, message: str, *, data=None, res: CursorResult = None):
    return {"res": res, "status": status, "message": message, "data": data}
