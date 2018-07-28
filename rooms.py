import items
import creatures
import random
import logging
from game import GameObject
from game import Vector2
from PIL import Image

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


class Room:
    def __init__(self, level, size_vector, doors, biome, items, enemies):
        self.level = level
        self.size_vector = size_vector
        self.doors = doors
        self.biome = biome
        self.items = items
        self.enemies = enemies

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

    def __str__(self):
        room_string = f'Room level: {self.level}\n' \
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
            room_string += f'{chest.material} chest holding\n'
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
        room_string = f'Room level: {self.level}\n' \
                      f'Total loot value: {total_loot}\n' \
                      f'Loot distribution: {loot_distribution}\n' \
                      f'Number of items: {len(loot_list)}\n' \
                      f'---------------\n'

        chest_list = []
        for item in self.items:
            if type(item) is not items.Chest:
                room_string += f'Value {item.total_value} - {str(item)}\n'
            else:
                chest_list.append(item)

        room_string += '---------------\n' \
                       'Chests:'

        for chest in chest_list:
            room_string += f'{chest.material} chest holding\n'
            for item in chest.inventory:
                room_string += f'Value {item.total_value} -- {str(item)}\n'

        room_string += f'---------------\n' \
                       f'Total enemy power: {danger}\n' \
                       f'Enemy distribution\n' \
                       f'Enemies:\n' \
                       f'---------------\n'

        for enemy in self.enemies:
            room_string += f'Power level {enemy.power_level} -- {enemy}\n'

        return room_string

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
            loot_distribution=None):

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
            total_loot = GameObject.get_level() * 0.1 * (level ** 2 - GameObject.zero_to_range(level ** 2))

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
        for i in range(0, 3):
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

        enemy_list = creatures.EnemyHumanoid.generate_enemies(level, enemy_power, enemy_distribution)
        enemy_list.sort(key=creatures.Creature.power_sort_key, reverse=True)

        for enemy in enemy_list:
            enemy.position = Vector2(random.randint(0, size_vector.x),
                                     random.randint(0, size_vector.y))


        room_instance = cls(level, size_vector, doors, biome, loot_list, enemy_list)
        return room_instance


for i in range(0, 10):
    logger.debug(Room.generate_room(None, None, (i+1) * 10))
