import discord
import logging
import random
import os
import items
import creatures
import rooms
import test

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.propagate = False

stream_formatter = logging.Formatter('%(levelname)s:%(message)s')
file_formatter = logging.Formatter('%(levelno)s:%(asctime)s:%(message)s')

file_handler = logging.FileHandler('bot.log')
file_handler.setFormatter(file_formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(stream_formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

# test.run_tests()

prefix = '--'

save_file = ''
token_file = f'{os.path.dirname(__file__)}/bot_token.txt'
token = ''

inspect_target = None

client = discord.Client()

logger.info('Starting Discord RPG...')

with open(token_file, 'r') as f:
    if os.path.getsize(token_file) > 0:
        token = f.readline()
        logger.debug(f'Token is {token}')
    else:
        raise Exception(f'{token_file} is empty!')


def get_command_arguments(message):
    arguments = []
    space_indexes = [len(message)]
    i = 0
    while i < len(message) - 1:
        if message[i] == ' ':
            space_indexes.append(i)
        i += 1

    space_indexes.sort()

    i = 0
    while i < len(space_indexes) - 1:
        if message[space_indexes[i] + 1:space_indexes[i+1]] != '':
            arguments.append(message[space_indexes[i] + 1:space_indexes[i+1]])
        i += 1
    return arguments

@client.event
async def on_ready():
    logger.info('Logged in as')
    logger.info(client.user.name)
    logger.info(client.user.id)
    logger.info(f'Invite: https://discordapp.com/oauth2/authorize?client_id={client.user.id}&scope=bot')
    logger.info('------')

@client.event
async def on_message(message):
    global inspect_target
    if message.content.startswith(prefix):
        logger.info(f'{message.author.name} sent the command: {message.content[len(prefix):]}')

    if message.content.startswith(f'{prefix} test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, f'You have {counter} messages.')

    elif message.content.startswith(f'{prefix}weapon'):
        inspect_target = items.Weapon.get_random_weapon(items.Item.get_level())
        await client.send_message(message.channel, str(inspect_target))

    elif message.content.startswith(f'{prefix}armour'):
        inspect_target = items.Armour.get_random_armour(items.Item.get_level())
        await client.send_message(message.channel, str(inspect_target))

    elif message.content.startswith(f'{prefix}enemy'):
        inspect_target = creatures.EnemyHumanoid.get_random_enemy()
        await client.send_message(message.channel, str(inspect_target))

    elif message.content.startswith(f'{prefix}room'):
        inspect_target = rooms.Room.generate_room()
        await client.send_message(message.channel, str(inspect_target))

    elif message.content.startswith(f'{prefix}inspect '):
        item_name = message.content[len(prefix) + 8:]
        logger.debug(f'Item name: {item_name}')
        inspect_string = ''
        if inspect_target:
            if type(inspect_target) == items.Weapon or type(inspect_target) == items.Armour or type(inspect_target) == creatures.EnemyHumanoid:
                inspect_string = str(inspect_target)
            elif type(inspect_target == rooms.Room):
                for item in inspect_target.items:
                    if item.name == item_name:
                        inspect_string = str(item)

                for enemy in inspect_target.enemies:
                    if f'{enemy.enemy_type} {enemy.enemy_class} {enemy.name}' == item_name:
                        inspect_string = str(enemy)

                if inspect_string == '':
                    inspect_string = 'Invalid item name!'
            await client.send_message(message.channel, inspect_string)

    elif message.content.startswith(f'{prefix}shutdown'):
        logger.warning('Shutting down...')
        await client.send_message(message.channel, 'Shutting down...')
        try:
            await client.close()
        except TypeError:
            logger.warning('Discord RPG shut down succesfully\nPress enter to continue...')
            input()

    elif message.content.startswith(prefix):
        logger.info(f'Stupid {message.author.name} sent an invalid command: {message.content[len(prefix):]}')
        await client.send_message(message.channel, f'Stupid {message.author.name}, that\'s an invalid command!')


# print(items.Item.test_item_balance('weapon', None, 10000))

# i = 1
# while i <= 10:
#     print(items.Weapon.get_random_weapon())
#     i += 1

client.run(token)
