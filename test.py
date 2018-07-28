import logging
from items import Item
from items import Weapon
from items import Armour
from creatures import Player
from creatures import EnemyHumanoid
from rooms import Room

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
logger.propagate = False

stream_formatter = logging.Formatter('%(levelname)s:%(message)s')
file_formatter = logging.Formatter('%(levelno)s:%(asctime)s:%(message)s')

file_handler = logging.FileHandler('bot.log')
file_handler.setFormatter(file_formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(stream_formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

def item_rarity_test():
    Item.get_level()


def item_name_test():
    Item.get_fantasy_name()
    Item.get_fantasy_name(0)
    Item.get_fantasy_name(10, [], [])


def item_skew_multiplier_test():
    Item.get_skew_multiplier()
    Item.get_skew_multiplier(10000)


def item_get_attr_detr_value_test():
    Item.zero_to_range(0)
    Item.zero_to_range(1)
    Item.zero_to_range(10000)


def item_balance_test_test():
    Item.test_item_balance('weapon')
    Item.test_item_balance('armour')


def weapon_generation_test():
    Weapon.get_random_weapon()
    Weapon.get_random_weapon(0)
    Weapon.get_random_weapon(-1)
    Weapon.get_random_weapon(10000)
    for weapon_type in Weapon.weapon_types:
        Weapon.get_random_weapon(None, weapon_type)


def armour_generation_test():
    Armour.get_random_armour()
    Armour.get_random_armour(0)
    Armour.get_random_armour(-1)
    Armour.get_random_armour(10000)
    for armour_type in Armour.armour_types:
        Armour.get_random_armour(None, armour_type)

    for armour_material in Armour.armour_materials:
        Armour.get_random_armour(None, None, armour_material)


def enemy_generation_test():
    EnemyHumanoid.get_random_enemy()
    EnemyHumanoid.get_random_enemy(0)
    EnemyHumanoid.get_random_enemy(-1)
    EnemyHumanoid.get_random_enemy(10000)
    for enemy_type in EnemyHumanoid.enemy_list:
        EnemyHumanoid.get_random_enemy(None, enemy_type)
    for enemy_class in EnemyHumanoid.enemy_class_list:
        EnemyHumanoid.get_random_enemy(None, None, enemy_class)


def run_tests():
    item_rarity_test()
    item_name_test()
    item_skew_multiplier_test()
    item_get_attr_detr_value_test()
    # item_balance_test_test()
    weapon_generation_test()
    armour_generation_test()
    enemy_generation_test()