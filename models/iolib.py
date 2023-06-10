def listToStr(l: list, sep: str = " "):
    output = str()
    for i in l:
        output += i + sep
    return output[:-len(sep)]

def strToList(s: str, sep: str):
    return s.split(sep)