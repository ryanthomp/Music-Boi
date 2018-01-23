import discord
import urllib.request
import urllib.parse
import re
import asyncio
import os


count = 0
queue = []
playing = False
stop = False
player = 0
num = 0
voice = 0
final = 0
link = 0
discord.opus.load_opus('libopus-0.x64.dll')
client = discord.Client()
print("CLIENT")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


async def search(title, message):
    global link
    global final
    global queue
    print("PLAY")
    msg = queue[0]
    print(msg)
    title = msg.replace(" ", "+")
    print(title)
    html_content = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + title)
    print("HTML")
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    print("SEARCH")
    final = ("http://www.youtube.com/watch?v=" + search_results[0])
    print("FINAL")
    await play(message)


async def play(message):  # What is playing the song at all times
    global playing
    global count
    global stop
    global queue
    global player
    global num
    global voice
    global final
    while not client.is_closed:
        if count > 0:
            # server = message.author.server
            # channel = message.author.voice.voice_channel
            print("CHANNEL")
            # voice = await client.join_voice_channel(channel)
            print(voice)
            print("VOICE")
            player = await voice.create_ytdl_player(final)
            print(player)
            print("PLAYER")
            duration = player.duration
            print(duration)
            playing = True      
            player.start()
            title = player.title
            await client.send_message(message.channel, "Now playing `%s`." % title)
            await client.change_presence(game=discord.Game(name=title))
            print("START")
            print(count)
            num = duration
            while num > 0:
                num -= 1
                await asyncio.sleep(1)
                print("PLAY WHILE NUM", num)
            if num <= 0:
                playing = False
                count = count - 1
                print("PLAY COUNT 0", count)
                print(queue)
                del queue[0]
                print(queue)
                print("SONG COMPLETE")
                if count <= 0:
                    print("count is 0 therefore i stop")
                    await player.stop()
                else:
                    print("time to play xd")
                    await play(message)


@client.event
async def on_message(message):
    global count
    global player
    global num
    global queue
    global voice
    if message.content.startswith(">play"):
        print(message)
        print("PLAY")
        server = message.author.server
        print(server)
        connected = client.is_voice_connected(server)
        if not connected:
            print("NOT CONNECTED")
            try:
                print("FALSE")
                channel = message.author.voice.voice_channel
                print(channel)
                voice = await client.join_voice_channel(channel)
                msg = message.content
                auth = message.author
                if count == 0:
                    print("COUNT IS 0")
                    print(msg)
                    print(auth)
                    msg = msg[6:]
                    print(msg)
                    count += 1
                    queue.append(msg)
                    await search(msg, message)
                    print("PLAYING")
                    #client.loop.close()
                else:
                    print("COUNT ISN'T 0")
                    print(count)
                    print(msg)
                    print(auth)
                    msg = msg[6:]
                    print(msg)
                    count = count + 1
                    await client.send_message(message.channel, "Added `%s` to the queue" % msg)
                    queue.append(msg)
                    print("ADDED TO QUEUE")
            except discord.errors.InvalidArgument:
                count = count - 1
                await client.send_message(message.channel, "Connected to a voice channel first")

        if connected:
            print("CONNECTED")
            msg = message.content
            auth = message.author
            if count == 0:
                print("COUNT IS 0")
                print(msg)
                print(auth)
                msg = msg[6:]
                print(msg)
                count = count + 1
                queue.append(msg)
                await search(msg, message)
                print("PLAYING")
                #client.loop.close()
            else:
                print("COUNT ISN'T 0")
                print(msg)
                print(auth)
                msg = msg[6:]
                print(msg)
                count = count + 1
                await client.send_message(message.channel, "Added `%s` to the queue" % msg)
                queue.append(msg)
                print(queue)
                print("ADDED TO QUEUE")

    elif message.content == ">stop":
        print("STOP")
        server = message.author.server
        print(server)
        voice = server.voice_client
        print(voice)
        num = 0
        count = 0
        queue = []
        await voice.disconnect()
        print("LEFT")

    elif message.content == '>ping':
        print("PING")
        server = message.author.server
        print(server)
        voice = server.voice_client
        address = voice.endpoint
        i = 0
        while i < 1:
            ping = os.popen("ping %s -n 1", address)
            result = ping.readlines()
            msline = result[-1].strip()
            print(msline.split(' = ')[-1])

    elif message.content == ">skip":
        print("SKIP")
        player.stop()
        del queue[0]
        count -= 1
        #num = 0
        print("SKIP COUNT NOT 1", count)
        print("SKIP NUM NOT 1", num)
        await play(message)

    elif message.content.startswith == ">volume ":
        print("VOLUME")
        msg = message.content
        print(msg)
        msg = msg[8:]
        print(msg)
        player.volume = msg

    elif message.content == '>queue':
        await client.send_message(message.channel, queue)

client.run('')
