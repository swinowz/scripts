import discord

intents = discord.Intents.default()
client = discord.Client(intents=intents)

TOKEN = ''

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    
    channel = client.get_channel("channel_id")  
    await channel.send('message')

client.run(TOKEN)
