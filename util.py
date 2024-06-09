import re

def getURL(ctx):
    url = ctx.content.split(" ")
    if len(url) != 2 or not re.match("^https:\/\/.+$", url[1]):
        return None
    return url[1]

def secondsToHMS(seconds):
    h, m, s = 0, 0, 0
    while seconds > 0:
        if seconds - 3600 >= 0:
            h += 1
            seconds -= 3600
        elif seconds - 60 >= 0:
            m += 1
            seconds -= 60
        elif seconds - 1 >= 0:
            s += 1
            seconds -= 1
    return h, m, s

def HMSTimeStamp(seconds):
    h, m, s = secondsToHMS(seconds)
    return f'{h:02}:{m:02}:{s:02}'