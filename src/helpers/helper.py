
def to_bool(value):
    """
    Converts 'something' to boolean. Raises exception if it gets a string it doesn't handle.
    Case is ignored for strings. These string values are handled:
      True: 'True', "1", "TRue", "yes", "y", "t"
      False: "", "0", "faLse", "no", "n", "f"
    Non-string values are passed to bool.
    """
    if type(value) == type(''):
        if value.lower() in ("yes", "y", "true",  "t", "1"):
            return True
        if value.lower() in ("no",  "n", "false", "f", "0", ""):
            return False
        raise Exception('Invalid value for boolean conversion: ' + value)
    return bool(value)


