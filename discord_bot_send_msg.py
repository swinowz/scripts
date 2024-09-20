import discord

intents = discord.Intents.default()
client = discord.Client(intents=intents)

TOKEN = ''

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    
    channel_id = 1283358461282746379  # Channel ID should be an integer
    channel = client.get_channel(channel_id)
    
    if channel:
        guild = channel.guild
        role = discord.utils.get(guild.roles, name="reminder")
        if role:
            await channel.send(f'Test {role.mention}!')
        else:
            print('Role named "reminder" not found')
    else:
        print('Channel not found')

client.run(TOKEN)



import discord

intents = discord.Intents.default()
client = discord.Client(intents=intents)

TOKEN = ''

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    
    channel_id = 1283358461282746379  # Channel ID should be an integer
    channel = client.get_channel(channel_id)
    
    if channel:
        guild = channel.guild
        role = discord.utils.get(guild.roles, name="reminder")
        if role:
            await channel.send(f'test {role.mention}')
        else:
            print('Role named "reminder" not found')
    else:
        print('Channel not found')

client.run(TOKEN)
