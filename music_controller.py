from datastructures import Queue
import ytdownload as yt
from discord import FFmpegPCMAudio
import asyncio

class MusicController:

    q = None
    player = None
    voice = None
    currentsong = None
    currentsong_seconds_played = 0
    loop = False
    leave_delay = 60 * 2

    def __init__(self):
        self.q = Queue()

    async def Play(self, song, voice):
        # Add Song To Queue
        err = await self.AddSong(song)
        # Check If Queue Is Full
        if err != None: return False
        # If Already Playing Return
        if self.voice is not None: return False
        # If Not Playing
        self.voice = voice
        while not self.q.Empty():
            self.currentsong = self.q.Dequeue()
            if self.currentsong == None: continue
            self.player = await createPlayer(self.currentsong.url)
            if self.player == None: continue # Skips If Unable To Play
            self.voice.play(self.player)
            # Sleep While Playing or Paused
            while self.voice.is_playing() or self.voice.is_paused():
                await asyncio.sleep(1)
                if self.voice.is_playing(): self.currentsong_seconds_played += 1
                if len(self.voice.channel.members) <= 1:
                    return True
            await self.Skip() # Clears Playlist & Sets Player To None
            if self.loop: self.q.EnqueueFront(self.currentsong)
            # Delay Before Leaving
            if self.q.Empty():
                count = self.leave_delay
                while count > 0:
                    await asyncio.sleep(1)
                    if not self.q.Empty():
                        break
                    count -= 1
            # reset
            self.currentsong = None
            self.currentsong_seconds_played = 0
        # Return True - All Songs Have Been Played
        self.voice = None
        return True


    async def AddSong(self, song):
        if not self.q.Full():
            print(f'Adding Song {song.url}')
            self.q.Enqueue(song)
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
        self.currentsong_seconds_played = 0
        self.currentsong = None

    async def Clear(self):
        self.q.Clear()

    async def ToggleLoop(self):
        if self.loop:
            self.loop = False
        else:
            self.loop = True

    async def GetPlayList(self):
        return self.q.queue

    # time until last song plays - used when a new song is added
    def TimeUntilPlays(self):
        if self.currentsong.duration == None:
            seconds = 0
        else:
            seconds = self.currentsong.duration - self.currentsong_seconds_played
        for song in self.q.queue[:self.q.Size()-1]:
            seconds += song.duration
        return seconds

async def createPlayer(url):
    data = yt.getAudio(url)
    if data == None: return None
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
    return FFmpegPCMAudio(data["url"], **FFMPEG_OPTIONS)