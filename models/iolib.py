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
    for i in d:
        output += i + sep2 + d[i] + sep
    output = output[:len(sep)] + end
