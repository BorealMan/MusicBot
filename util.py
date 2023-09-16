import re

def getURL(ctx):
    url = ctx.content.split(" ")
    if len(url) != 2 or not re.match("^https:\/\/.+$", url[1]):
        return None
    return url[1]