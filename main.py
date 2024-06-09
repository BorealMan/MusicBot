import discord
import config
from util import *
from yt_search import getSongByURL, queryYT
from music_controller import MusicController

# Dictionary Server Storage
rooms = {}

# Client Object Intents
intents = discord.Intents.default()
client = discord.Client(command_prefix='!', intents=intents)
intents.message_content = True

async def JoinChannel(voice, channel):
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

async def PlayMusic(ctx):
    # Check If It's a URL
    url = getURL(ctx)
    # log command
    print(f'{ctx.guild.id}: {ctx.content}')

    # If Not URL, Search YouTube
    if url == None: 
        song = queryYT(ctx.content.replace("!play ", "", 1))
        # If No Result Found, Error
        if song == None:
            await ctx.channel.send("Cannot Find That Song - Try Again")
            return
        # Send Song Link
        if (len(song.url) < 250):
            await ctx.channel.send(f'I Found {song.url}')
    else:
        # Create Song Object
        song = getSongByURL(url)
    
    channel = ctx.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    # Move To Correct Channel
    await JoinChannel(voice, channel)

    if not ctx.guild.id in rooms.keys():
        print(f'Creating A New Music Controller For {ctx.guild.id}')
        rooms[ctx.guild.id] = MusicController()

    # Get Voice Again - To Avoid joinChannel Issue
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    finished = await rooms[ctx.guild.id].Play(song, voice)

    if finished:
        await Quit(ctx)
        pass
    else:
        await ctx.channel.send(f'Added To Queue Position ({rooms[ctx.guild.id].q.Size()})')
        await ctx.channel.send(f'Plays in {HMSTimeStamp(rooms[ctx.guild.id].TimeUntilPlays())}')

async def Quit(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        del rooms[ctx.guild.id]
        await voice.disconnect()
        await ctx.channel.send('Happy Music')

async def Skip(ctx):
    await rooms[ctx.guild.id].Skip()
    await ctx.channel.send(f'Skipping - Queue Size ({rooms[ctx.guild.id].q.Size()})')

async def Clear(ctx):
    await rooms[ctx.guild.id].Clear()
    await ctx.channel.send(f'Cleared Queue')

async def Pause(ctx):
    await rooms[ctx.guild.id].Pause()
    await ctx.channel.send("Pausing Music")

async def Resume(ctx):
    await rooms[ctx.guild.id].Resume()
    await ctx.channel.send("Resuming Music")

async def Loop(ctx):
    await rooms[ctx.guild.id].ToggleLoop()
    currentsong = rooms[ctx.guild.id].currentsong
    if rooms[ctx.guild.id].loop:
        await ctx.channel.send(f'Looping {currentsong.Details()}')
    else:
        await ctx.channel.send(f'Looping disabled')

async def PlayList(ctx):
    embed = discord.Embed(
        title="MusicQT Playlist",
        description="Current Playlist",
        color=0xFF5733,
        url= config.SITE_URL if config.SITE_URL != None else "https://github.com/BorealMan/MusicQT",
    )
    try:
        playlist = await rooms[ctx.guild.id].GetPlayList()
        currentsong = rooms[ctx.guild.id].currentsong
        currentsong_seconds_played = rooms[ctx.guild.id].currentsong_seconds_played
        if len(playlist) == 0 and currentsong == None:
            embed.add_field(name="No Songs", value="", inline=False)
        else:
            seconds = currentsong.duration - currentsong_seconds_played
            embed.add_field(name=f"Now Playing: {currentsong.label} | {HMSTimeStamp(seconds)}", value="", inline=False)
            for song in playlist:
                embed.add_field(name=f'{song.label}: playing in {HMSTimeStamp(seconds)}', value="", inline=False)
                seconds += song.duration
    except:
        embed.add_field(name="No Songs Playing!", value="", inline=False)

    await ctx.channel.send(embed=embed)

async def RickRoll(ctx):
    query = "Rick Astley - Never Gonna Give You Up"

    rooms[ctx.guild.id].loop = True

    if not ctx.guild.id in rooms.keys():
        print(f'Creating A New Music Controller For {ctx.guild.id}')
        rooms[ctx.guild.id] = MusicController()
        ctx.content = "!play " + query
        await PlayMusic(ctx)
    else:
        song = queryYT(query)
        rooms[ctx.guild.id].q.EnqueueFront(song)
        await rooms[ctx.guild.id].Skip()



async def Help(ctx):
    embed = discord.Embed(
        title="MusicQT Commands",
        description="Commands To Control The Music Player",
        color=0xFF5733,
        url= config.SITE_URL if config.SITE_URL != None else "https://github.com/BorealMan/MusicQT",
    )
    embed.add_field(name="!play [song]", value="Accepts links and song title - band. If already playing adds song to queue.", inline=False)
    embed.add_field(name="!skip", value="Skips current song.", inline=False)
    embed.add_field(name="!pause or !stop", value="Pauses current song.", inline=False)
    embed.add_field(name="!resume", value="Resumes playing.", inline=False)
    embed.add_field(name="!loop", value="Loop current song.", inline=False)
    embed.add_field(name="!playlist", value="Display current playlist details.", inline=False)
    embed.add_field(name="!clear", value="Clears the queue.", inline=False)
    embed.add_field(name="!quit", value="Stopings playing and leaves.", inline=False)
    embed.add_field(name="!help", value="Displays help.", inline=False)
    await ctx.channel.send(embed=embed)

@client.event
async def on_ready():
    print(f'{client.user} has joined a new Guild.')


@client.event
async def on_message(ctx):
    if ctx.author == client.user:
        return

    # command needs case sensitive comparison - fussy Ian
    command = ctx.content.lower()

    print(command)

    if command.startswith("!playlist"):
        await PlayList(ctx)

    elif command.startswith('!play'): 
        await PlayMusic(ctx)

    elif command.startswith('!skip'):
        await Skip(ctx)

    elif command.startswith("!pause") or command.startswith("!stop"):
        await Pause(ctx)

    elif command.startswith('!resume'):
        await Resume(ctx)

    elif command.startswith('!loop'):
        await Loop(ctx)

    elif command.startswith('!clear'):
        await Clear(ctx)

    elif command.startswith('!quit'):
        await Quit(ctx)

    elif command.startswith('!help'):
        await Help(ctx)

    elif command.startswith('!rick'):
        await RickRoll(ctx)

# Running Client
client.run(config.TOKEN)
