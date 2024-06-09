from util import HMSTimeStamp

class Song:

    def __init__(self, url, label=None, duration=None):
        self.url = url
        self.label = label
        self.duration = int(duration)

    def Details(self) -> str:
        return f'{self.label}: {HMSTimeStamp(self.duration)}'
    
    def Print(self):
        print(self.Details() + " " + self.url)