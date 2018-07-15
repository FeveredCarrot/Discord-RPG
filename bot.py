import logging
import discord
import asyncio
import os
import pickle
import items
import enemies
import player

logging.basicConfig(level=logging.INFO)

prefix = '--'

save_file = ''
token_file = 'bot_token.txt'
token = ''

client = discord.Client()


with open(token_file, 'r') as f:
    if os.path.getsize(token_file) > 0:
        token = f.readline()
    else:
        print(token_file + ' is empty!')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('Invite: https://discordapp.com/oauth2/authorize?client_id={}&scope=bot'.format(client.user.id))
    print('------')

@client.event
async def on_message(message):
    print(message.author.name)
    if message.channel.name == 'memes' or message.channel.name == 'memedumps':
        pass
    elif message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!weapon'):
        await client.send_message(message.channel, str(items.Weapon.get_random_weapon(items.Item.get_item_rarity())))
    elif message.content.startswith('!armour'):
        await client.send_message(message.channel, str(items.Armour.get_random_armour(items.Item.get_item_rarity())))

print(items.Item.test_item_balance('weapon', None, 10000))

i = 1
while i <= 10:
    print(items.Weapon.get_random_weapon())
    i += 1

client.run("NDU4NDY2NzUwOTkzMDA2NTk0.DigNdg.gWBlaevMP_wcIKd0CuOzT0ZhVp4")
