import yt_dlp

def downloadAudio(url):
    try:
        yt_dlp_opts = {
            "format": "m4a/bestaudio/best",
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',}]
        }
        ydl = yt_dlp.YoutubeDL(yt_dlp_opts)
        err = ydl.download(url)
    except:
        return None

def getAudio(url):
    try:
        yt_dlp_opts = {
            # "quiet": True,
            "format": "m4a/bestaudio/best",
            "noplaylist": True,
        }
        ydl = yt_dlp.YoutubeDL(yt_dlp_opts)
        song_info = ydl.extract_info(url, download=False)
        print(song_info['url'])
        return song_info
    except:
        return None
    

if __name__ == '__main__':
    downloadAudio("https://www.youtube.com/watch?v=hzfHnrXCn9Y&ab_channel=SamLink")