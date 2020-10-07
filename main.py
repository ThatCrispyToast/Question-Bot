# Import Modules
import discord
import envariables
import logging
from xml.etree import ElementTree
import aiohttp
import asyncio
from random import choice

# TODO: Create File to Store Previously Asked Questions and Pull from them Instead of Constantly Accessing Wolfram API (and taking up all my fuckin queries)

# Logs Discord DEBUG Logs to discord.log
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Accesses Discord Client
client = discord.Client()

# Initializes Tokens and API Keys from envariables
discordToken = envariables.discordToken
wolframToken = envariables.wolframToken


# Informs of Bot Connection Information on Ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await client.change_presence(activity=discord.Game(name='"Q? help"'))
    await client.get_channel(762093041116381198).send('Bot Enabled.')


# Detects Message Send Events
# TODO: Make Bot Only Search Messages with Prefix "Q? " Instead of all Messages
@client.event
async def on_message(message):
    # Ignores all Messages Sent by Bot
    if message.author == client.user:
        return

    # Only Parses Message If Proceeded with Prefix
    if message.content.startswith('Q? '):     
        messageContent = message.content[3:]
        
        # Admin Commands
        if message.author.id == 330116875755323393:
            if messageContent == 'admin' or messageContent == 'admin help':
                await message.channel.send("""
                    Q? admin servers - Lists Servers Bot is In\n
                    Q? admin change_presence <input> - Changes Bot Rich Presence\n
                    Q? admin :clown: <input> - q? aDmiN :clown:
                    """)
                
            if messageContent == 'admin servers':
                await message.channel.send(f'In {len(client.guilds)} servers.')
                for server in client.guilds:
                    await message.channel.send(server.name)
                    
            if messageContent == 'admin change_presence':
                await client.change_presence(activity=discord.Game(name=message.content[25:]))
                
            if messageContent == 'admin :clown:':
                await message.channel.send(''.join(choice((str.upper, str.lower))(c) for c in message.content[17:]))
                
        # Regular Commands
        title = f'{str(message.author)} asked, "{messageContent}"'
        answer = await message.channel.send(
            embed=discord.Embed(title=title,
                                description="Answering...",
                                color=0xffff00))
        color = 0x00ff00
        
        # Predefined Responses
        if 'who am i' in messageContent.lower():
            description = f'You are {str(message.author)}.'

        elif 'who are you' in messageContent.lower() or 'your name' in messageContent.lower():
            description = f'I am {str(client.user)}.'

        elif 'where am i' in messageContent.lower():
            description = f'You are in the #{message.channel} channel on {message.guild}.'

        elif messageContent.lower().startswith('help'):
            description = 'Ask me any question and I\'ll do my best to answer it!'

        # Sends Message to Wolfram API and Returns Result as Embed
        else:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://api.wolframalpha.com/v2/query?input={messageContent.replace("+", "plus")}&appid={wolframToken}') as response:
                        # TODO: Change WolframAlpha Output Data Type from XML to JSON
                        tree = ElementTree.fromstring(await response.content.read())
                        # ? Should I Keep the Special Orange Empty Message Embed or Defaut to the Red One?
                        if tree[1][0].find('plaintext').text == None or tree[1][0].find('plaintext').text == '':
                            description = 'Answer is Empty or Missing...'
                            color = 0xff8000

                        else:
                            description = tree[1][0].find('plaintext').text

            # Returns if Answer Cannot be Found
            except IndexError:
                description = 'Unable to Answer Question'
                color = 0xff0000

        # Applies title, description, and color Changes
        await answer.edit(
                    embed=discord.Embed(title=title,
                                        description=description,
                                        color=color))


# Runs Bot... Obviously
client.run(envariables.discordToken)
