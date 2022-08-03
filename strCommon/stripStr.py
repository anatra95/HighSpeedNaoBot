def stripAll(string):
    if string != "":
        print("debug: string( " + string + " ) is not \"\"")
        while string[0].isspace() or string[-1].isspace():
            string = string.strip()
            print("debug: we got strip string : " + string)
    return string