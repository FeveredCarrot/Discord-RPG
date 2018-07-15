import logging
import discord
import asyncio
import os
import pickle

logging.basicConfig(level=logging.INFO)

prefix = '--'

save_file = ''

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('Invite: https://discordapp.com/oauth2/authorize?client_id={}&scope=bot'.format(client.user.id))
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')


with open(save_file, 'rb') as f:
    if os.path.getsize(save_file) > 0:
        # unpickler = pickle.Unpickler(f)
        accounts = pickle.load(f)
    else:
        print('Bank file empty')

client.run("MjU4MDA0MjM1OTAyMjU1MTA1.DIda-g.j6b0db-C-vg1MAkAqpxtbDw1hw4")
