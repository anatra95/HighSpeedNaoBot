def stripAll(string):
    if string != "":
        while string[0].isspace() or string[-1].isspace():
            string = string.strip()
    return string