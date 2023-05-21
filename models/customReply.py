import random


class GenReply():
    def __init__(self, replyDict: dict):
        self.reply = replyDict

    def generateReply(self, status, *, msgs=None, param="", sep="\n"):
        if status not in self.reply:
            raise KeyError(f"Status {status} not found in replyList")
        r = ""
        if msgs:
            for msg in msgs:
                r += f"{random.choice(self.reply[status]).replace('{$param}', msg)}{sep}" if msg == "{$reply}" else f"{msg}{sep}"
            return r
        else:
            return f"{random.choice(self.reply[status]).replace('{$param}', param)}"
