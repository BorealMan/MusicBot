import discord
import util
import config
import music_controller as mc
import yt_search

# Dictionary Server Storage
rooms = {}

# Client Object Intents
intents = discord.Intents.default()
client = discord.Client(command_prefix='!', intents=intents)
intents.message_content = True

async def joinChannel(voice, channel):
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()


async def playMusic(ctx):
    # Check If It's a URL
    url = util.getURL(ctx)

    # If Not URL, Search YouTube
    if url == None: 
        url = yt_search.queryYT(ctx.content.replace("!play ", "", 1))
        # If No Result Found, Error
        if url == None:
            await ctx.channel.send("Cannot Find That Song - Try Again")
            return
        # Send Song Link
        await ctx.channel.send(f'I Found {url}')
    
    channel = ctx.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    # Move To Correct Channel
    await joinChannel(voice, channel)

    if not ctx.guild.id in rooms.keys():
        print(f'Creating A New Music Controller For {ctx.guild.id}')
        rooms[ctx.guild.id] = mc.MusicController()

    # Get Voice Again - To Avoid joinChannel Issue
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    finished = await rooms[ctx.guild.id].Play(url, voice)

    if finished:
        await Quit(ctx)
    else:
        await ctx.channel.send(f'Added To Queue Position ({rooms[ctx.guild.id].q.qsize()})')

async def Quit(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        del rooms[ctx.guild.id]
        await voice.disconnect()
        await ctx.channel.send('Happy Music')

async def Skip(ctx):
    await rooms[ctx.guild.id].Skip()
    await ctx.channel.send(f'Skipping - Queue Size ({rooms[ctx.guild.id].q.qsize()})')

async def Clear(ctx):
    await rooms[ctx.guild.id].Clear()
    await ctx.channel.send(f'Cleared Queue')

async def Pause(ctx):
    await rooms[ctx.guild.id].Pause()
    await ctx.channel.send("Pausing Music")

async def Resume(ctx):
    await rooms[ctx.guild.id].Resume()
    await ctx.channel.send("Resuming Music")

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

    if ctx.content.startswith('!play'):
        await playMusic(ctx)

    elif ctx.content.startswith('!skip'):
        await Skip(ctx)

    elif ctx.content.startswith("!pause") or ctx.content.startswith("!stop"):
        await Pause(ctx)

    elif ctx.content.startswith('!resume'):
        await Resume(ctx)

    elif ctx.content.startswith('!clear'):
        await Clear(ctx)

    elif ctx.content.startswith('!quit'):
        await Quit(ctx)

    elif ctx.content.startswith('!help'):
        await Help(ctx)

# Running Client
client.run(config.TOKEN)
