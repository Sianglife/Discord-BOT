from datetime import datetime
def listToStr(l: list, sep: str = " "):
    output = str()
    for i in l:
        output += i + sep
    return output[:-len(sep)]

def strToList(s: str, sep: str):
    return s.split(sep)

def dictToStr(d: dict, sep: str = " ", sep2: str = ":", start: str = "", end: str = ""):
    output = start
    for i in d.items():
        output += i[0] + sep2 + i[1][0] + sep
    output = output[:len(output)-len(sep)] + end
    return output
