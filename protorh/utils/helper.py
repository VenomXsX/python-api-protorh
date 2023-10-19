def concat_set(str: str, attr_name: str, comma=True):
    str += " " + attr_name + "=" + attr_name + "," if comma else ""
