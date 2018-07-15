import logging
import random
import items

logging.basicConfig(level=logging.INFO)

class Enemy():

    enemy_types = ['slime', 'goblin', 'ork', 'guard', 'bat person', 'giant spider', 'skeleton']
    enemy_classes = ['assassin', 'archer', 'knight', 'thug', 'mage']
    legendary_creatures = ['moth man', 'sasquatch', 'yeti', 'skeleton king', 'demon bird']

    def __init__(self, name, hp, inventory, skills):
        self.name = name
        self.hp = hp
        self.inventory = inventory
        self.skills = skills

    def GetRandomEnemy(self, level, enemy_type):
        if not enemy_type:
            enemy_type = Enemy.enemy_types[random.randint(0, len(Enemy.enemy_types) - 1)]

        enemy_name = enemy_type


