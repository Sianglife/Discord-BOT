import random


def listToStr(l: list, sep: str = " "):
    output = str()
    for i in l:
        output += i + sep
    return output[:-len(sep)] if sep != "" else output


def strToList(s: str, sep: str):
    return s.split(sep)


def dictToStr(d: dict, sep: str = " ", sep2: str = ":", start: str = "", end: str = "", inListIndex: int = None):
    output = start
    for i in d.items():
        if inListIndex == None:
            output += i[0] + sep2 + i[1] + sep
        else:
            output += i[0] + sep2 + i[1][inListIndex] + sep
    output = output[:len(output)-len(sep)] + end
    return output


def randUniqueStr(l: list, length: int = 8):
    number_of_letters = random.randint(length//2, length)
    number_of_numbers = length-number_of_letters
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
               'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    print(l)

    result = [random.choice(letters) for _ in range(
        number_of_letters)] + [random.choice(numbers) for _ in range(number_of_numbers)]
    result = listToStr(result, "")
    while result in l:
        result = [random.choice(letters) for _ in range(
            number_of_letters)] + [random.choice(numbers) for _ in range(number_of_numbers)]
        result = listToStr(result, "")
    return result
