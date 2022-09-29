import os
from collections import deque

import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import youtube_dl
from discord.utils import get

prefix = "."
client = commands.Bot(command_prefix=prefix)

queue = deque()
songs = {}

global ydl_opts
ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }


def play_url(url, namesong, id_server):
    try:
        os.remove(namesong)
    except:
        pass

    url = str(url)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, namesong)
    voice.play(discord.FFmpegPCMAudio(namesong), after=lambda e: play_url(songs[id_server].popleft(), namesong, id_server))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07




@client.event
async def on_ready():
    print('log in')


# clear message
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount+1)


# hello
@client.command(pass_context=True)
async def hello(ctx, arg=""):
    author=ctx.message.author
    if arg == "":
        await ctx.channel.send(f'hello, Mr.{author.mention} ')
    else:
        await ctx.channel.send(f'hello, Mr.{author.mention} ' + arg)


# join voice channel
@client.command(pass_context=True)
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f'бот присоеденился к каналу: {channel}')


# leave voice channel
@client.command()
async def leave(ctx):
    # global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f'бот отключился от канала: {channel}')


@client.command(pass_context=True, brief="This will play a song 'play [url]'", aliases=['pl'])
async def play(ctx, url):
    voice = get(client.voice_clients, guild=ctx.guild)

    id_server=ctx.message.guild.id
    namesong = "song"+str(id_server)+".mp3"
    print(f'{id_server}')
    if not(id_server in songs):
        songs[id_server] = deque()
    songs[id_server].append(url)

    print(f'aaaaaaaaaaaa{len(songs[id_server])}')
    if voice and voice.is_playing():
        print("FFFFFFFFFFFFFFFFFF")
        return
    else:
        print(f'aaaaaaaaaaaa{len(songs[id_server])}')
        song_there = os.path.isfile(namesong)
        try:
            if song_there:
                os.remove(namesong)
        except:
            pass
        if not (voice and voice.is_playing()):
            play_url(songs[id_server].popleft(), namesong, id_server)
        print(f'aaaaaaaaaaaa{len(songs[id_server])}')


@client.command(pass_context=True)
async def pause(ctx):
    if voice and voice.is_playing():
        await ctx.send(':pause_button: Pause song.')
        voice.pause()


@client.command(pass_context=True)
async def resume(ctx):
    if voice and voice.is_paused():
        await ctx.send(':play_pause: Resume song.')
        voice.resume()


@client.command(pass_context=True)
async def stop(ctx):
    queue.clear()
    if voice and voice.is_playing():
        await ctx.send(':stop_button: Stop songs')
        voice.stop()


@client.command(pass_context=True)
async def skip(ctx):
    await ctx.send(':track_next: Next song.')
    voice.stop()
    try:
        os.remove("song.mp3")
    except:
        pass
    play_url(queue.popleft())

token = open('token.txt', 'r').readline()
client.run(token)