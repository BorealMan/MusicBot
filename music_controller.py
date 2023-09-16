import queue
import ytdownload as yt
from discord import FFmpegPCMAudio
import asyncio

class MusicController:

    q = None
    player = None
    voice = None
    leave_delay = 60 * 2 # Seconds * Minutes

    def __init__(self):
        self.q = queue.Queue(100)

    async def Play(self, url, voice):
        # Add Song To Queue
        err = await self.AddSong(url)
        # Check If Queue Is Full
        if err != None:
            return False
        # If Already Playing Return
        if self.voice is not None:
            return False
        # If Not Playing
        self.voice = voice
        while not self.q.empty():
            self.player = await createPlayer(self.q.get())
            if self.player == None: continue # Skips If Unable To Play
            self.voice.play(self.player)
            # Sleep While Playing or Paused
            while self.voice.is_playing() or self.voice.is_paused():
                await asyncio.sleep(1)
                # If Only Channel Member Is Bot, Return Finished
                if len(self.voice.channel.members) <= 1:
                    return True
            await self.Skip() # Clears Playlist & Sets Player To None
            # Delay Before Leaving
            if self.q.empty():
                count = self.leave_delay
                while count > 0:
                    await asyncio.sleep(1)
                    if not self.q.empty():
                        break
                    count -= 1
        # Return True - All Songs Have Been Played
        self.voice = None
        return True


    async def AddSong(self, url):
        if not self.q.full():
            print(f'Adding Song {url}')
            self.q.put(url)
            return None
        else:
            return "Queue Is Full"

    async def Pause(self):
        if self.voice.is_playing():
            self.voice.pause()

    async def Resume(self):
        if self.voice.is_paused():
            self.voice.resume()

    async def Skip(self):
        self.voice.stop()
        self.player.cleanup()

    async def Clear(self):
        self.q = queue.Queue(0)


async def createPlayer(url):
    data = yt.getAudio(url)
    if data == None: return None
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
    return FFmpegPCMAudio(data["url"], **FFMPEG_OPTIONS)