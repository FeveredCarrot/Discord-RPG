import random
import items


class Enemy:
    enemy_humanoid_list = ('goblin', 'ork', 'guard', 'bat person', 'skeleton')
    enemy_creature_list = ('slime', 'giant spider')
    enemy_list = enemy_humanoid_list + enemy_creature_list
    enemy_class_list = ('assassin', 'archer', 'knight', 'samurai', 'thug', 'mage', 'brawler')
    legendary_creature_list = ('moth man', 'sasquatch', 'yeti', 'skeleton king', 'demon bird')

    def __init__(self, name, level, hp, inventory, skills):
        self.name = name
        self.level = level
        self.hp = hp
        self.inventory = inventory
        self.skills = skills

    @staticmethod
    def get_enemy_values(level=None, enemy_type=None, enemy_class=None):
        if not level:
            level = items.Item.get_item_rarity()
        if not enemy_type:
            enemy_type = Enemy.enemy_humanoid_list[random.randint(0, len(Enemy.enemy_list) - 1)]
        if not enemy_class:
            enemy_class = Enemy.enemy_class_list[random.randint(0, len(Enemy.enemy_class_list) - 1)]

        inventory = []

        level_scale = pow(level, 2)

        if enemy_type == 'goblin':
            enemy_stats = {

            }
        elif enemy_type == 'ork':
            enemy_stats = {
                            'arm_length': 0.7 * items.Item.get_skew_multiplier(10),
                            'weight': 160 * items.Item.get_skew_multiplier(20),
                            'hp': 150 * level_scale,
                            'available_weapons': ['axe', 'sword', 'mace', 'greatsword', 'spear'],
                            'available_armours': items.Armour.armour_materials,
                            'is_humanoid': True
            }
        else:
            raise Exception(enemy_type + ' is not a valid enemy type!')

        if enemy_class == 'assassin':
            enemy_stats['available_weapons'] = ['dagger']
            enemy_stats['available_armours'] = ['cloth', 'leather', 'chainmail']
        elif enemy_class == 'archer':
            enemy_stats['available_weapons'] = ['bow']
            enemy_stats['available_armours'] = ['cloth', 'leather']
        elif enemy_class == 'knight':
            # converting a list to a set removes duplicates
            enemy_stats['available_weapons'] = list(set(enemy_stats['available_weapons'] + ['sword', 'axe', 'mace', 'greatsword', 'halberd', 'spear', 'glaive', 'katana', 'nodachi']))
            enemy_stats['available_armours'] = list(items.Armour.armour_materials)
        elif enemy_class == 'samurai':
            enemy_stats['available_weapons'] = ['katana', 'nodachi', 'quarterstaff', 'glaive']
            enemy_stats['available_armours'] = list(items.Armour.armour_materials)
        elif enemy_class == 'thug':
            enemy_stats['available_weapons'] += ['axe', 'dagger']
            enemy_stats['available_armours'] = ['cloth', 'leather', 'chainmail', 'bronze']
        elif enemy_class == 'mage':
            enemy_stats['available_weapons'] = ['wand', 'wizard staff']
            enemy_stats['available_armours'] = ['cloth', 'leather']
        elif enemy_class == 'brawler':
            enemy_stats['available_weapons'] = ['caestus']
            enemy_stats['available_armours'] = ['cloth', 'leather']
        else:
            raise Exception(enemy_class + ' is not a valid class type!')
        pass

        return enemy_stats

    @classmethod
    def get_random_enemy(cls, level=None, enemy_type=None, enemy_class=None):
        if not level:
            level = random.randint(1, 100)
        if not enemy_type:
            enemy_type = Enemy.enemy_humanoid_list[random.randint(0, len(Enemy.enemy_list) - 1)]
        if not enemy_class:
            enemy_class = Enemy.enemy_class_list[random.randint(0, len(Enemy.enemy_class_list) - 1)]

        enemy_name = enemy_type + ' ' + enemy_class
