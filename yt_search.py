import requests
import re
import urllib.parse
from song import Song

def encodeQuery(query):
    return urllib.parse.quote_plus(query)

def createQuery(query):
    return "https://www.youtube.com/results?search_query=" + encodeQuery(query)

def queryYT(query):
    # Create Query String
    url = createQuery(query)

    # Make Request
    r = requests.request("GET", url)

    data = str(r.content)

    # Search Results For Watch Links
    watch_links = re.findall('\/watch\?[^"]+', data)

    if len(watch_links) < 1:
        return None
    
    label, duration = extractSongMetaData(data)
    url = "https://www.youtube.com" + watch_links[0]

    song = Song(url, label, duration)

    return song


def getSongByURL(url):
    r = requests.request("GET", url)

    data = str(r.content)

    label = str(re.findall('"title":"[^"]+', data)[0]).replace('"title":"', "").replace("\\", "")
    duration = str(re.findall('"lengthSeconds":"[^"]+', data)[0]).replace('"lengthSeconds":"', "")

    song = Song(url, label, duration)

    return song

def extractSongMetaData(data):
    try:
        label = str(re.findall('"' + "[\w\s\d\[\]\(\)-]+ - [\w\s\d\\\\']+(?=by|)", data, re.I)[0])[1:-1].replace("\\", "").replace("/", "")
    except:
        print(f"Unable to extract label")
        label = None

    match = re.findall('{"accessibilityData":{"label":"[\w\s\d,]+[^}]}},', data)[0]

    try:
        hours = int(str(re.findall('\d+ hour', match)[0]).replace(" hours", "")[0])
    except:
        hours = 0

    try:
        minutes = int(str(re.findall('\d+ minute', match)[0]).replace(" minutes", "")[0])
    except:
        minutes = 0

    try:
        seconds = int(str(re.findall('\d+ second', match)[0]).replace(" seconds", "")[0])
    except:
        seconds = 0

    duration = hours*3600 + minutes*60 + seconds

    return label, duration



# Testing
if __name__ == '__main__':
    # query = "Rick Astley - Never Gonna Give You Up"
    # song = queryYT(query)
    # song.Print()

    song = getSongByURL("https://www.youtube.com/watch?v=8d4DEmYiQN8&list=PLAhFuvrDwg_MVuXcjoD7P9sC4ZwMnP5X3&index=3")
    song.Print()