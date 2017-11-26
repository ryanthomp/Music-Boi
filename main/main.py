import discord
import youtube_dl

discord.opus.load_opus('libopus.so')
client = discord.Client()
print("CLIENT")


@client.event
async def on_ready():
    # info
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content == "`play":
        print("PLAY")
        server = message.author.server
        me = server.me
        print(server)
        connected = client.is_voice_connected(server)
        if not connected:
            print("FALSE")
            channel = message.author.voice.voice_channel
            print(channel)
            voice = await client.join_voice_channel(channel)
            print("VOICE")
            player = await voice.create_ytdl_player('')
            print("PLAYER")
            player.start()
            print("START")

        if connected:
            print("TRUE")
            server = message.author.server
            voice = server.voice_client
            player = await voice.create_ytdl_player('')
            print("PLAYER")
            player.start()
            print("START")

    elif message.content == "`nick":
        print("NICK")
        server = message.author.server
        me = server.me
        await client.change_nickname(me)

    elif message.content == "`leave":
        print("LEAVE")
        server = message.author.server
        print(server)
        voice = server.voice_client
        print(voice)
        await voice.disconnect()
        print("LEFT")


client.run('')
