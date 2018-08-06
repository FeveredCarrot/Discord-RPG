import items
import creatures
import random
import logging
import os
import sys
import asyncio
import discord
import datetime
from game import GameObject
from game import Vector2
from PIL import Image, ImageDraw
from PIL import PSDraw

logger = logging.getLogger(__name__)
# if __name__ == '__main__':
logger.setLevel(logging.DEBUG)
logger.propagate = False
stream_formatter = logging.Formatter('%(levelname)s:%(message)s')
file_formatter = logging.Formatter('%(levelno)s:%(asctime)s:%(message)s')

file_handler = logging.FileHandler('bot.log')
file_handler.setFormatter(file_formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(stream_formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


class Room:
    def __init__(
            self,
            level,
            size_vector,
            doors, biome,
            items, enemies,
            position=None,
            entrance_direction=None,
            exit_directions=None):

        self.level = level
        self.size_vector = Vector2(int(size_vector.x), int(size_vector.y))
        self.doors = doors
        self.biome = biome
        self.items = items
        self.enemies = enemies

        if not position:
            self.position = None
        else:
            self.position = Vector2(int(position.x), int(position.y))

        self.entrance_direction = entrance_direction
        self.exit_directions = exit_directions

        self.area = size_vector.x * size_vector.y

    biome_list = ('dungeon',)
    dungeon_adjectives = ('cold', 'dark', 'stone', 'wet', 'mossy', 'moldy')
    dungeon_enemies = {
        'goblin': 0.9,
        'ork': 0.8,
        'outlaw': 1,
        'skeleton': 1.2,
        'undead': 1.1,
        'bat person': 1.1
    }

    @property
    def total_enemy_power(self):
        enemy_power = 0
        for enemy in self.enemies:
            enemy_power += enemy.power_level
        return enemy_power

    @property
    def total_loot(self):
        loot_value = 0
        for item in self.items:
            loot_value += item.item_stats['total_value']
        return loot_value

    def json_readable(self):
        item_list = []
        for item in self.items:
            item_list.append(item.json_readable())

        enemy_list = []
        for enemy in self.enemies:
            enemy_list.append(enemy.json_readable())

        if self.position:
            position = self.position.json_readable()
        else:
            position = None

        return {
            'level': self.level,
            'size_vector': self.size_vector.json_readable(),
            'doors': self.doors,
            'biome': self.biome,
            'items': item_list,
            'enemies': enemy_list,
            'position': position
        }

    def __str__(self):
        room_string = f'Room level: {self.level}\n' \
                      f'Room dimentions: {self.size_vector.x} x {self.size_vector.y}\n' \
                      f'Number of items: {len(self.items)}\n' \
                      f'---------------\n'

        chest_list = []
        for item in self.items:
            if type(item) is not items.Chest:
                room_string += f'Value {item.total_value}  -- Level {str(int(item.item_stats["rarity"] * 10))} {str(item.name)}\n'
            else:
                chest_list.append(item)

        room_string += '---------------\n' \
                       'Chests:\n'

        for chest in chest_list:
            room_string += f'\n{chest.material} chest holding\n'
            for item in chest.inventory:
                room_string += f'Value {item.total_value} -- Level {str(int(item.item_stats["rarity"] * 10))} {str(item.name)}\n'

        room_string += f'---------------\n' \
                       f'Total enemy power: {self.total_enemy_power}\n' \
                       f'Enemies:\n' \
                       f'---------------\n'

        for enemy in self.enemies:
            room_string += f'Power level {enemy.power_level} -- Level {str(enemy.level)} {enemy.enemy_type} {enemy.enemy_class} {enemy.name}\n'

        return room_string

    def __repr__(self):
        return f'Room: level {self.level}\n' \
               f'Items: {len(self.items)}\n' \
               f'Enemies: {len(self.enemies)}\n'

    @classmethod
    def load_from_save(cls, attribute_dict):
        size_vector = Vector2.load_from_save(attribute_dict['size_vector'])
        position = Vector2.load_from_save(attribute_dict['position'])

        item_list = []
        for item in attribute_dict['items']:
            if item['item_stats']['item_type'] in items.Armour.armour_materials:
                item_list.append(items.Armour.load_from_save(item))

            elif item['item_stats']['item_type'] in items.Weapon.weapon_types:
                item_list.append(items.Weapon.load_from_save(item))

            elif item['item_stats']['item_type'] == 'chest':
                item_list.append(items.Chest.load_from_save(item))

        enemy_dict = []
        for enemy in attribute_dict['enemies']:
            enemy_dict.append(creatures.EnemyHumanoid.load_from_save(enemy))

        return cls(
            attribute_dict['level'],
            size_vector,
            attribute_dict['doors'],
            attribute_dict['biome'],
            item_list,
            enemy_dict,
            position
        )

    @classmethod
    def empty(cls, size_vector=Vector2.zero(), position=Vector2.zero()):
        return cls(None, size_vector, None, None, None, None, position, None, None)

    @classmethod
    def generate_room(
            cls,
            doors=None,
            size_vector=None,
            level=None,
            enemy_power=None,
            total_loot=None,
            biome=None,
            enemy_distribution=None,
            loot_distribution=None,
            position=None,
            entrance_direction=None,
            exit_directions=None):

        if not doors:
            doors = {
                'north': random.randint(0, 1) == 1,
                'south': random.randint(0, 1) == 1,
                'east': random.randint(0, 1) == 1,
                'west': random.randint(0, 1) == 1,
                     }
        if not size_vector:
            size_vector = Vector2(0, 0)
            size_vector.x = random.randint(2, 20)
            size_vector.y = random.randint(2, 20)
        if not level:
            level = GameObject.get_level() * 10

        if not enemy_power:
            enemy_power = (level**2 * GameObject.get_level() * 1) - (random.randint(-5, 13))

        if not total_loot:
            total_loot = GameObject.get_level() * ((size_vector.x * size_vector.y) / 500) * (level ** 2 - GameObject.zero_to_range(level ** 2))

        if not biome:
            biome = cls.biome_list[random.randint(0, len(cls.biome_list) - 1)]

        if not enemy_distribution:
            enemy_distribution = random.uniform(0.5, 2)

        if not loot_distribution:
            loot_distribution = random.uniform(0.5, 2)

        level = int(level)
        enemy_power = int(enemy_power)
        total_loot = int(total_loot)

        loot_list = items.Item.generate_loot(level, total_loot, loot_distribution)

        chest_list = []
        for _ in range(0, 3):
            if random.uniform(0, 1) < 0.1 or len(loot_list) > 5:
                chest_inventory = []
                chest_value = total_loot
                chest_value = chest_value // 3

                while chest_value > 0 and len(loot_list) > 0:
                    loot_item = loot_list[-1]
                    chest_inventory.append(loot_item)
                    chest_value -= loot_item.total_value
                    loot_list.remove(loot_item)

                chest_list.append(items.Chest(None, chest_inventory))

        for chest in chest_list:
            chest.position = Vector2(random.randint(0, size_vector.x),
                                     random.randint(0, size_vector.y))

            chest.inventory.sort(key=items.Item.value_sort_key, reverse=True)
            loot_list.append(chest)

        for item in loot_list:
            item.position = Vector2(random.randint(0, size_vector.x),
            random.randint(0, size_vector.y))

        enemy_list = creatures.EnemyHumanoid.generate_enemies(level, enemy_power, enemy_distribution)
        enemy_list.sort(key=creatures.Creature.power_sort_key, reverse=True)

        for enemy in enemy_list:
            enemy.position = Vector2(random.randint(0, size_vector.x),
                                     random.randint(0, size_vector.y))

        room_instance = cls(
            level,
            size_vector,
            doors,
            biome,
            loot_list,
            enemy_list,
            position,
            entrance_direction,
            exit_directions)

        return room_instance


class Map:
    """Holds multiple rooms and their relation to each other"""
    def __init__(self, level, biome, room_list=[]):
        self.room_list = room_list
        self.level = level
        self.biome = biome

    def print_map(self, export_file=None):

        map_bounds = self.get_map_bounds()
        ascii_pixel_matrix = []

        for y in range(map_bounds['position'].y - 20, map_bounds['dimensions'].y + map_bounds['position'].y + 20):
            ascii_pixel_row = ['']

            for x in range(map_bounds['position'].x - 10, map_bounds['dimensions'].x + map_bounds['position'].x + 10):

                pixel_collider = Room.empty(Vector2(1, 1), Vector2(x, y))
                collides = False

                room_level = 0
                for room in self.room_list:
                    if Map.check_collision(room, pixel_collider):
                        collides = True
                        room_level = room.level

                if collides:
                    if room_level < 10:
                        ascii_pixel_row.append(f'{room_level}')
                    else:
                        ascii_pixel_row.append('#')
                else:
                    ascii_pixel_row.append(' ')

            ascii_pixel_matrix.append(ascii_pixel_row)

        map_string = f'{map_bounds}\n'

        for room in self.room_list:
            map_string += f'Room level {room.level} dimensions: {room.size_vector}\n'

        for row in ascii_pixel_matrix:
            row_string = ''

            for pixel in row:
                row_string += pixel

            map_string = f'{map_string}\n{row_string}'

        if export_file:
            export_file = f'{os.path.dirname(os.path.realpath(__file__))}/Maps/{export_file}'

            with open(export_file, 'w') as file:
                file.seek(0)
                file.write(map_string)

        return map_string

    def export_map_image(self, export_file='map.png', resolution=10):

        export_file = f'{os.path.dirname(os.path.realpath(__file__))}/{export_file}'
        map_bounds = self.get_map_bounds()

        y_offset = 0
        for room in self.room_list:
            if room.position.y < y_offset:
                y_offset = room.position.y

        image = Image.new(mode='RGBA', size=(map_bounds['dimensions'].x,
                                             map_bounds['dimensions'].y + 1),
                          color=(0, 0, 0, 0))

        # print(image.size)
        for room in self.room_list:
            if room is self.room_list[0]:
                color = (255, 255, 255, 255)
            else:
                color = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                    255
                )

            for y in range(0, room.size_vector.y):
                for x in range(0, room.size_vector.x):

                    image.putpixel((room.position.x + x - map_bounds['position'].x,
                                    room.position.y + y - map_bounds['position'].y),
                                   color)

        image = image.resize((map_bounds['dimensions'].x * resolution,
                              map_bounds['dimensions'].y * resolution),
                             resample=Image.NEAREST)

        image = image.transpose(Image.FLIP_TOP_BOTTOM)

        image.save(export_file, 'PNG')

        return image

    def get_map_bounds(self):
        left_most = 0
        right_most = 0
        top_most = 0
        bottom_most = 0

        for room in self.room_list:
            if room.position.x < left_most:
                left_most = room.position.x

            if room.position.x + room.size_vector.x > right_most:
                right_most = room.position.x + room.size_vector.x

            if room.position.y + room.size_vector.y > top_most:
                top_most = room.position.y + room.size_vector.y

            if room.position.y < bottom_most:
                bottom_most = room.position.y

        width = abs(right_most - left_most)
        height = abs(top_most - bottom_most)

        return {'dimensions': Vector2(width, height), 'position': Vector2(left_most, bottom_most)}

    @staticmethod
    def room_level_sort_key(room):
        return room.level

    @staticmethod
    def check_collision(room_1, room_2):
        """
            Checks if the left of room_1 is to the left of any part of room 2 and
            Checks if the right of room_1 is to the right of any part of room 2 and
            Checks if the bottom of room_1 is under any part of room 2 and
            Checks if the top of room_1 is above any part of room 2
        """
        if (room_1.position.x < room_2.position.x + room_2.size_vector.x and
                room_1.position.x + room_1.size_vector.x > room_2.position.x and
                room_1.position.y < room_2.position.y + room_2.size_vector.y and
                room_1.size_vector.y + room_1.position.y > room_2.position.y):

            return True
        else:
            return False

    @staticmethod
    def check_touching(room_1, room_2):
        """
            Checks if the left of room_1 is to the left of any part of room 2 and
            Checks if the right of room_1 is to the right of any part of room 2 and
            Checks if the bottom of room_1 is under any part of room 2 and
            Checks if the top of room_1 is above any part of room 2
        """
        if (room_1.position.x < room_2.position.x + room_2.size_vector.x and
                room_1.position.x + room_1.size_vector.x > room_2.position.x and
                room_1.position.y < room_2.position.y + room_2.size_vector.y and
                room_1.size_vector.y + room_1.position.y > room_2.position.y):

            return True
        else:
            return False

    @staticmethod
    def check_horizontal_alignment(room_1, room_2):
        """
            Checks if the left of room_1 is to the left of any part of room 2 and
            Checks if the right of room_1 is to the right of any part of room 2 and
        """

        if (room_1.position.x < room_2.position.x + room_2.size_vector.x and
                room_1.position.x + room_1.size_vector.x > room_2.position.x):

            return True
        else:
            return False
    
    @staticmethod
    def check_vertical_alignment(room_1, room_2):
        """
            Checks if the bottom of room_1 is under any part of room 2 and
            Checks if the top of room_1 is above any part of room 2
        """

        if (room_1.position.y < room_2.position.y + room_2.size_vector.y and
                room_1.size_vector.y + room_1.position.y > room_2.position.y):

            return True
        else:
            return False

    @classmethod
    def check_all_collision(cls, room, room_list):
        for other_room in room_list:

            if room is other_room:
                continue

            if cls.check_collision(room, other_room):
                return True
            
        return False

    @classmethod
    async def generate_map(
            cls,
            map_size=None,
            connectivity=None,
            biome=None,
            level=None,
            level_interval=2,
            current_map=[],
            special_rooms=[],
            special_room_occurance=0.01,
            client=None,
            progress_message=None
    ):

        """
        Generates a series of linked rooms
        :param map_size: number of rooms in the map
        :param connectivity: how many hallways in the map
        :param biome: map biome
        :param level: map starting level, goes up by level_interval for each room
        :param current_map: The map that this map will build upon
        :param special_rooms: list of premade rooms
        :param special_room_occurance: how often premade rooms appear as percent (0, 1)
        :return: Map()
        """

        start_time = datetime.datetime.now()

        if not map_size:
            map_size = random.randint(5, 30)
            logger.debug(map_size)

        if not connectivity:
            connectivity = random.uniform(0, 1)

        if not biome:
            biome = Room.biome_list[random.randint(0, len(Room.biome_list) - 1)]

        if not level:
            level = GameObject.get_level()

        if current_map:
            room_list = current_map
        else:
            room_list = [
                Room(
                    items=None,
                    enemies=None,
                    doors={'north': True, 'south': False, 'east': False, 'west': False},
                    position=Vector2.zero(),
                    size_vector=Vector2(random.randint(2, 8), random.randint(2, 8)),
                    biome=biome,
                    level=level,
                    entrance_direction=None,
                    exit_directions=['north']
                )]

        map_size = int(map_size)
        level = int(level)

        message_content = progress_message.content
        progress_message = await client.edit_message(progress_message, message_content +
                                                     f'\nProgress: []')

        list_index = 0
        while list_index <= map_size - 2:
            last_room = room_list[list_index]
            room_succesful = False
            level += level_interval

            entrance_direction = GameObject.opposite_direction(
                last_room.exit_directions[random.randint(0, len(last_room.exit_directions) - 1)])

            room_tries = 0
            while room_tries < 100:

                doors = {
                    'north': random.randint(0, 1) == 1,
                    'south': random.randint(0, 1) == 1,
                    'east': random.randint(0, 1) == 1,
                    'west': random.randint(0, 1) == 1
                }
                pass        # get rid of pycharm formatting bug
                doors[entrance_direction] = True

                exit_directions = []

                for direction in doors:
                    if direction != entrance_direction and doors[direction]:
                            exit_directions.append(direction)

                if len(exit_directions) == 0:
                    # room_tries += 1
                    # logger.debug(f'No exit {room_tries}')
                    continue

                if random.uniform(0, 1) < special_room_occurance and len(special_rooms) > 0:

                    room = special_rooms[random.randint(0, len(special_rooms) - 1)]

                else:

                    room = Room(
                        items=None,
                        enemies=None,
                        doors=doors,
                        biome=biome,
                        level=level,
                        position=Vector2.zero(),
                        size_vector=Vector2(random.randint(2, 20), random.randint(2, 20)),
                        entrance_direction=entrance_direction,
                        exit_directions=exit_directions
                        )

                # if room is above last_room
                if entrance_direction == 'north':
                    room.position.x = random.randint(last_room.position.x - room.size_vector.x + 1,
                                                     last_room.position.x + last_room.size_vector.x - 1)

                    room.position.y = int(last_room.position.y + last_room.size_vector.y)

                # if room is below last_room
                elif entrance_direction == 'south':
                    room.position.x = random.randint(last_room.position.x - room.size_vector.x + 1,
                                                     last_room.position.x + last_room.size_vector.x - 1)

                    room.position.y = int(last_room.position.y - room.size_vector.y)

                # if room to the right of last_room
                elif entrance_direction == 'east':
                    room.position.x = int(last_room.position.x + last_room.size_vector.x)

                    room.position.y = room.position.y = random.randint(last_room.position.y - room.size_vector.y + 1,
                                                                       last_room.position.y + last_room.size_vector.y - 1)

                # if room to the left of last_room
                elif entrance_direction == 'west':
                    room.position.x = int(last_room.position.x - room.size_vector.x)

                    room.position.y = random.randint(last_room.position.y - room.size_vector.y + 1,
                                                     last_room.position.y + last_room.size_vector.y - 1)

                if cls.check_all_collision(room, room_list):
                    room_tries += 1
                    # logger.debug(f'room tries: {room_tries}')
                    continue

                room_list.append(room)
                logger.info(f'rooms: {len(room_list)}')
                # last_room = room
                room_tries = 100000
                room_succesful = True
                wip_map = Map(level, biome, room_list)
                wip_map.print_map(f'{level}.txt')
                list_index += 1

            if not room_succesful:
                logger.info(f'level {level} room unsuccesful')
                level -= 1 * level_interval
                for _ in range(0, 5):
                    if list_index > 0:
                        level -= 1 * level_interval
                        list_index -= 1
                        del(room_list[-1])

            progress_message = await client.edit_message(progress_message, message_content +
                                                         f'\nProgress: '
                                                         f'{GameObject.progress_bar(int((len(room_list) / map_size) * 100), map_size)}')

        # for room in room_list:
        #     for other_room in room_list:
        #
        #         hallway = None
        #
        #         # if room is underneath or above other_room
        #         if cls.check_horizontal_alignment(room, other_room) and \
        #                 random.uniform(0, 1) < connectivity:
        #
        #             hallway_pos = Vector2.zero()
        #             hallway_size = Vector2(2, 0)
        #
        #             # if room is below other_room
        #             if room.position.y - other_room.position.y < 0:
        #                 if other_room.position.y - room.position.y < 15 > 2 and \
        #                         room.doors['north'] and other_room.doors['south']:
        #
        #                     hallway_pos.y = room.position.y + room.size_vector.y
        #                     hallway_size.y = other_room.position.y - room.position.y + room.size_vector.y
        #
        #                     if hallway_size.y < 2:
        #                         continue
        #                 else:
        #                     continue
        #
        #             # if room is above other_room
        #             elif room.position.y - other_room.position.y > 0:
        #                 if room.position.y - other_room.position.y < 15 > 2 and \
        #                         room.doors['south'] and other_room.doors['north']:
        #
        #                     hallway_pos.y = other_room.position.y + other_room.size_vector.y
        #                     hallway_size.y = room.position.y - other_room.position.y + other_room.size_vector.y
        #
        #                     if hallway_size.y < 2:
        #                         continue
        #                 else:
        #                     continue
        #
        #             hallway_pos.x = ((room.position.x + room.size_vector.x / 2) +
        #                              (other_room.position.x + other_room.size_vector.x / 2)) // 2
        #
        #             hallway = Room.generate_room(doors={
        #                 'north': True,
        #                 'south': True,
        #                 'east': False,
        #                 'west': False},
        #                 level=int(level/2),
        #                 size_vector=hallway_size,
        #                 position=hallway_pos
        #             )
        #
        #             if cls.check_all_collision(hallway, room_list):
        #                 hallway = None
        #             else:
        #                 logger.debug(f'Created vertical hallway between {hallway.position.y} and {hallway.position.y + hallway.size_vector.y}')
        #
        #         # if room is to the left or right of other_room
        #         if cls.check_vertical_alignment(room, other_room) and \
        #                 random.uniform(0, 1) < connectivity:
        #
        #             hallway_pos = Vector2.zero()
        #             hallway_size = Vector2(0, 2)
        #
        #             # if room is to the left of other room
        #             if room.position.x - other_room.position.x < 0:
        #                 if other_room.position.x - room.position.x < 15 and \
        #                         room.doors['east'] and other_room.doors['west']:
        #
        #                     hallway_pos.x = room.position.x + room.size_vector.x
        #                     hallway_size.x = other_room.position.x - room.position.x + room.size_vector.x
        #
        #                     if hallway_size.x < 2:
        #                         continue
        #                 else:
        #                     continue
        #
        #             # if room is to the right of other_room
        #             else:
        #                 if room.position.x - other_room.position.x < 15 and \
        #                         room.doors['west'] and other_room.doors['east']:
        #
        #                     hallway_pos.x = other_room.position.x + other_room.size_vector.x
        #                     hallway_size.x = room.position.x - other_room.position.x + other_room.size_vector.x
        #
        #                     if hallway_size.x < 2:
        #                         continue
        #                 else:
        #                     continue
        #
        #             hallway_pos.y = ((room.position.y + room.size_vector.y / 2) +
        #                              (other_room.position.y + other_room.size_vector.y / 2)) // 2
        #
        #             hallway = Room.generate_room(doors={
        #                 'north': False,
        #                 'south': False,
        #                 'east': True,
        #                 'west': True},
        #                 level=int(level / 2),
        #                 size_vector=hallway_size,
        #                 position=hallway_pos
        #             )
        #
        #             if cls.check_all_collision(hallway, room_list):
        #                 hallway = None
        #             else:
        #                 logger.debug(f'Created horizontal hallway between {hallway.position.x} and {hallway.position.x + hallway.size_vector.x}')
        #
        #         if hallway:
        #             room_list.append(hallway)
        #             await asyncio.sleep(0.1)

        room_list.sort(key=Map.room_level_sort_key)

        for room in room_list:
            populated_room = Room.generate_room(
                room.doors,
                room.size_vector,
                room.level,
                biome=biome,
                position=room.position,
                entrance_direction=room.entrance_direction,
                exit_directions=room.exit_directions)
            room_list.remove(room)
            room_list.append(populated_room)

        generation_time = datetime.datetime.now() - start_time
        logger.info(f'Map of size {map_size} generated in {generation_time}')

        return cls(level, biome, room_list)


if __name__ == '__main__':
    for i in range(1, 2):
        map = Map.generate_map(level=1, map_size=30, connectivity=1)
        map.export_map_image(f'map_test_{i}.png', resolution=10)
