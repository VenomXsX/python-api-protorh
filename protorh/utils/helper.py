from typing import List, Union
from sqlalchemy import CursorResult


class NewString:

    def __init__(self, data):
        self.data = data


def concat_set(container: NewString, attr_name: str):
    container.data += " " + attr_name + " = :" + attr_name + ","


def remove_last_comma(container: NewString):
    container.data = container.data[:-1]


def trim(str: str):
    return " ".join(str.split())


def make_fields(items, fields_name: List[str], *, id: Union[int, str] = None):
    str = NewString("")
    values = {}
    items_dump = items.model_dump()

    if id:
        values["id"] = id

    for i in range(len(fields_name)):
        if items_dump[fields_name[i]]:
            concat_set(str, fields_name[i])
            values[fields_name[i]] = items_dump[fields_name[i]]

    remove_last_comma(str)

    return str.data, values


def response(status: int, message: str, *, data=None, res: CursorResult = None):
    return {"res": res, "status": status, "message": message, "data": data}
