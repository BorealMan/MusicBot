import requests
import re
import urllib.parse


def encodeQuery(query):
    return urllib.parse.quote_plus(query)

def createQuery(query):
    return "https://www.youtube.com/results?search_query=" + encodeQuery(query)

def queryYT(query):
    # Create Query String
    url = createQuery(query)
    print(f'Requesting: {url}')

    # Make Request
    r = requests.request("GET", url)

    # Search Results For Watch Links
    watch_links = re.findall('\/watch\?[^"]+', str(r.content))

    if len(watch_links) < 1:
        return None

    # Return First Result
    return "https://www.youtube.com" + watch_links[0]

# Testing
if __name__ == '__main__':
    query = "Askylit Drive - A Reason For Broken Wings HQ"
    result = queryYT(query)
    print(f'Result: {result}')

