import discord
import logging
import random
import asyncio
import os
import json
import datetime
import pytz
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
token = ''

save_file = f'{os.path.dirname(__file__)}/save_data.json'
settings_file = f'{os.path.dirname(__file__)}/settings.json'

settings = None
save_data = None

inspect_target = None
player_list = []
room_list = []

last_message = None

client = discord.Client()

logger.info('Starting Discord RPG...')


async def update_save_data():
    save_data['player_list'] = player_list
    save_data['room_list'] = room_list
    save_data['game_state'] = {}
    logger.debug(f'Save data : {save_data}')


async def save_settings(settings_dict):
    """Write the settings to the settings json file"""
    with open(settings_file, 'w') as f:
        f.write(json.dumps(settings_dict, indent=2))


async def save_game():
    """
    Write the save data to the save json file.
    Auto converts game data to json readable format
    """
    await update_save_data()

    player_jsons = []
    for player in player_list:
        player_jsons.append(player.json_readable())

    room_jsons = []
    for room in room_list:
        room_jsons.append(room.json_readable())

    save_dict = {
        'player_list': player_jsons,
        'room_list': room_jsons,
        'game_state': {}
    }

    with open(save_file, 'w') as f:
        f.write(json.dumps(save_dict, indent=2))

    logger.info('Game saved')
    logger.debug(save_data)


async def load_settings():
    global settings
    global token
    with open(settings_file, 'a+') as f:
        f.seek(0)
        if os.path.getsize(settings_file) > 0:
            settings = json.loads(f.read())
            token = settings['bot_token']
            logger.debug(f'Settings dict : \n{settings}')
        else:
            settings = {
                'bot_token': '',
                'time_zone': 'UTC'
            }
            await save_settings(settings)
            raise Exception('Settings file empty! Cannot run bot without bot token!')


async def load_save():
    logger.info('Loading save')
    global save_data
    with open(save_file, 'a+') as f:
        f.seek(0)
        if os.path.getsize(save_file) > 0:
            save_data = json.loads(f.read())
            # logger.debug(f'Save dict :\n{save_data}')

            for player_attributes in save_data['player_list']:
                player = creatures.Player.load_from_save(player_attributes)
                player_list.append(player)

            for room_attributes in save_data['room_list']:
                room = rooms.Room.load_from_save(room_attributes)
                room_list.append(room)
                logger.debug(f'room {room}')

            await update_save_data()
        else:
            save_data = {
                'player_list': [],
                'room_list': [],
                'game_state': {}
            }
            await save_game()
            logger.warning('No save data found. Created blank save.')


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


async def auto_save(interval):
    while True:
        await asyncio.sleep(interval)
        await update_save_data()
        await save_game(save_data)


# async def get_reply(author_id):
#     while last_message.id != author_id:
#         await asyncio.sleep(0.1)
#     return last_message

async def add_reacts(message, react_list):
    for emoji in react_list:
        await client.add_reaction(message, emoji)
        await asyncio.sleep(0.1)


def remove_spaces(string):
    string_list = get_command_arguments(string)

    combined_string = ''
    for string in string_list:
        combined_string == string

    return combined_string


@property
def current_datetime():
    return datetime.datetime.now(tz=pytz.UTC)


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
    global last_message
    last_message = message
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
        room_list.append(inspect_target)
        await client.send_message(message.channel, str(inspect_target))

    elif message.content.startswith(f'{prefix}inspect '):
        item_name = message.content[len(prefix) + 8:]
        logger.debug(f'Item name: {item_name}')
        inspect_string = ''
        if inspect_target:
            if type(inspect_target) == items.Weapon or type(inspect_target) == items.Armour or type(inspect_target) == creatures.EnemyHumanoid:
                inspect_string = str(inspect_target)
            elif type(inspect_target == room_list.Room):
                for item in inspect_target.items:
                    if item.name == item_name:
                        inspect_string = str(item)

                for enemy in inspect_target.enemies:
                    if f'{enemy.enemy_type} {enemy.enemy_class} {enemy.name}' == item_name:
                        inspect_string = str(enemy)

                if inspect_string == '':
                    inspect_string = 'Invalid item name!'
            await client.send_message(message.channel, inspect_string)

    elif message.content.startswith(f'{prefix}save'):
        await save_game()
        await client.send_message(message.channel, 'Game Saved')

    elif message.content.startswith(f'{prefix}create character'):
        for player in player_list:

            if player.stat_dict['player_id'] == message.author.id:

                bot_message = await client.send_message(message.channel, 'Warning: You already have a character. \n'
                                                                         'Do you want to overwrite your current character?')

                await add_reacts(bot_message, ['✅', '❌'])
                reply = await client.wait_for_reaction(['✅', '❌'], user=message.author, timeout=30)
                if reply:

                    if reply.reaction.emoji == '❌':
                        await client.send_message(message.channel, 'Ok')
                        return

                    elif reply.reaction.emoji == '✅':
                        player_list.remove(player)
                        break

                else:
                    return

        await client.send_message(message.channel, 'Please type your character name.')
        player_name = await client.wait_for_message(timeout=30, author=message.author)
        if not player_name:
            return
        player_name = player_name.content.capitalize()

        if player_name[:len(prefix)] == '--':
            player_name == player_name[len(prefix):]

        await client.send_message(message.channel, f'Please type your character\'s class. \n'
                                                   f'Type {prefix}classes to see a list of available classes.')

        player_class = await client.wait_for_message(timeout=30, author=message.author)
        if not player_class:
            return
        player_class = player_class.content.lower()

        while player_class not in creatures.EnemyHumanoid.enemy_class_list:
            if not player_class:
                return

            if player_class[:len(prefix)] != prefix:
                await client.send_message(message.channel, f'That is not a valid class type. \n'
                                                           f'Type {prefix}classes to see a list of available classes.')
            player_class = await client.wait_for_message(timeout=30, author=message.author)
            player_class = player_class.content.lower()

        player_stats = {
                'hp': 100,
                'height': round(random.uniform(1.6, 1.9), 2),
                'weight': round(random.uniform(120, 200), 1),
                'arm_length': round(random.uniform(0.55, 0.65), 2),
                'carry_capacity': 100,
                'speed': 0.2,
                'ap': 100,
                'max_ap': 100
        }

        if player_class == 'assassin':
            player_stats['player_class'] = 'assassin'
            player_stats['hp'] = int(player_stats['hp'] * 0.9)
            player_weapon = items.Weapon.get_random_weapon(random.uniform(0.03, 0.08), 'dagger')

            player_armour = items.Armour.get_armour_set(random.uniform(0.03, 0.08), 'leather',
                                                        ['cloth', 'leather', 'chainmail'], 0.6)

            player_stats['weapon_slots'] = {'left_hand': None, 'right_hand': player_weapon}

            player_stats['armour_slots'] = {'helmet': None, 'chestpiece': None,
                                            'arm guards': None, 'gloves': None, 'leggings': None}

        elif player_class == 'archer':
            player_stats['player_class'] = 'archer'
            player_stats['hp'] = int(player_stats['hp'] * 1)
            player_weapon = items.Weapon.get_random_weapon(random.uniform(0.03, 0.08), 'bow')

            player_armour = items.Armour.get_armour_set(random.uniform(0.03, 0.08), 'leather',
                                                        ['cloth'], 0.7)

            player_stats['weapon_slots'] = {'left_hand': None, 'right_hand': player_weapon}

            player_stats['armour_slots'] = {'helmet': None, 'chestpiece': None,
                                            'arm guards': None, 'gloves': None, 'leggings': None}

        elif player_class == 'knight':
            player_stats['player_class'] = 'knight'
            player_stats['hp'] = int(player_stats['hp'] * 1.2)
            player_weapon = items.Weapon.get_random_weapon(random.uniform(0.03, 0.08), 'sword')

            player_armour = items.Armour.get_armour_set(random.uniform(0.03, 0.08), 'iron',
                                                        ['leather', 'chainmail', 'bronze', 'steel'], 0.9)

            player_stats['weapon_slots'] = {'left_hand': None, 'right_hand': player_weapon}

            player_stats['armour_slots'] = {'helmet': None, 'chestpiece': None,
                                            'arm guards': None, 'gloves': None, 'leggings': None}

        elif player_class == 'samurai':
            player_stats['player_class'] = 'samurai'
            player_stats['hp'] = int(player_stats['hp'] * 1.1)
            player_weapon = items.Weapon.get_random_weapon(random.uniform(0.03, 0.08), 'katana')

            player_armour = items.Armour.get_armour_set(random.uniform(0.03, 0.08), 'wooden',
                                                        ['leather', 'chainmail', 'iron', 'bronze', 'steel'], 0.7)

            player_stats['weapon_slots'] = {'left_hand': None, 'right_hand': player_weapon}

            player_stats['armour_slots'] = {'helmet': None, 'chestpiece': None,
                                            'arm guards': None, 'gloves': None, 'leggings': None}
        elif player_class == 'thug':
            player_stats['player_class'] = 'thug'
            player_stats['hp'] = int(player_stats['hp'] * 1)
            player_weapon = items.Weapon.get_random_weapon(random.uniform(0.03, 0.08), 'axe')

            player_armour = items.Armour.get_armour_set(random.uniform(0.03, 0.08), 'leather',
                                                        ['chainmail', 'iron', 'bronze', 'steel'], 0.5)

            player_stats['weapon_slots'] = {'left_hand': None, 'right_hand': player_weapon}

            player_stats['armour_slots'] = {'helmet': None, 'chestpiece': None,
                                            'arm guards': None, 'gloves': None, 'leggings': None}
        elif player_class == 'mage':
            player_stats['player_class'] = 'mage'
            player_stats['hp'] = int(player_stats['hp'] * 0.9)
            player_weapon = items.Weapon.get_random_weapon(random.uniform(0.03, 0.08), 'wand')

            player_armour = items.Armour.get_armour_set(random.uniform(0.03, 0.08), 'cloth',
                                                        ['leather', 'chainmail', 'iron', 'bronze', 'steel'], 0.8)

            player_stats['weapon_slots'] = {'left_hand': None, 'right_hand': player_weapon}

            player_stats['armour_slots'] = {'helmet': None, 'chestpiece': None,
                                            'arm guards': None, 'gloves': None, 'leggings': None}
        elif player_class == 'brawler':
            player_stats['player_class'] = 'brawler'
            player_stats['hp'] = int(player_stats['hp'] * 1)
            player_weapon = items.Weapon.get_random_weapon(random.uniform(0.03, 0.08), 'caestus')

            player_armour = items.Armour.get_armour_set(random.uniform(0.03, 0.08), 'leather',
                                                        ['chainmail', 'iron', 'bronze', 'steel'], 0.7)

            player_stats['weapon_slots'] = {'left_hand': None, 'right_hand': player_weapon}

            player_stats['armour_slots'] = {'helmet': None, 'chestpiece': None,
                                            'arm guards': None, 'gloves': None, 'leggings': None}

        elif player_class == 'viking':
            player_stats['player_class'] = 'viking'
            player_stats['hp'] = int(player_stats['hp'] * 1.2)
            player_weapon = items.Weapon.get_random_weapon(random.uniform(0.03, 0.08), 'axe')

            player_armour = items.Armour.get_armour_set(random.uniform(0.03, 0.08), 'leather',
                                                        ['chainmail', 'iron', 'wooden'], 0.7)

            player_stats['weapon_slots'] = {'left_hand': None, 'right_hand': player_weapon}

            player_stats['armour_slots'] = {'helmet': None, 'chestpiece': None,
                                            'arm guards': None, 'gloves': None, 'leggings': None}

        player_instance = creatures.Player(player_stats, player_name, 1, [], message.author.id, None)
        player_instance.equip_armour(player_armour)
        player_list.append(player_instance)
        await client.send_message(message.channel, f'Player {player_name} created!\n {str(player_instance)}')
        logger.debug(str(player_instance))

    elif message.content.startswith(f'{prefix}classes'):
        class_string = 'Classes: '
        for player_class in creatures.EnemyHumanoid.enemy_class_list:
            class_string += player_class + ', '
        await client.send_message(message.channel, class_string[:-2] + '.')

    elif message.content.startswith(f'{prefix}poll'):
        pass

    elif message.content.startswith(f'{prefix}shutdown'):
        logger.warning('Shutting down...')
        await client.send_message(message.channel, 'Shutting down...')
        try:
            await save_settings(settings)
            await client.logout()
            await client.close()
        except TypeError:
            logger.warning('Discord RPG shut down succesfully\nPress enter to continue...')
            input()

    elif message.content.startswith(prefix):
        logger.info(f'Stupid {message.author.name} sent an invalid command: {message.content[len(prefix):]}')
        await client.send_message(message.channel, f'Stupid {message.author.name}, that\'s an invalid command!')


async def main():
    await load_settings()
    await load_save()
    loop = asyncio.get_event_loop()
    auto_save_task = loop.create_task(auto_save(10))
    client_start_task = loop.create_task(client.start(token))
    await asyncio.wait([auto_save_task, client_start_task])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
