import random
import items


class Creature(items.Item):
    def __init__(self, stats, level, inventory):
        self.level = level
        self.inventory = inventory

        self.hp = stats['hp']
        self.height = stats['height']
        self.weight = stats['weight']
        self.speed = stats['speed']
        self.maxap = stats['maxap']
        self.ap = 0


    @property
    def stat_dict(self):
        stats = {
            'hp': self.hp,
            'height': self.height,
            'weight': self.weight,
            'speed': self.speed,
            'ap': self.ap
        }
        return stats

    def apply_stats(self, stats):
        self.hp = stats['hp']
        self.height = stats['height']
        self.weight = stats['weight']
        self.speed = stats['speed']
        self.ap = stats['ap']


class Humanoid(Creature):
    """Base humanoid class"""
    def __init__(self, stats, name, level, inventory):
        super().__init__(stats, level, inventory)
        self.name = name

        self.hp = stats['hp']
        self.arm_length = stats['arm_length']
        self.speed = stats['speed']
        self.weapon_slots = stats['weapon_slots']
        self.armour_slots = stats['armour_slots']

    @property
    def stat_dict(self):
        stats = {
            'hp': self.hp,
            'height': self.height,
            'weight': self.weight,
            'arm_length': self.weight,
            'speed': self.speed,
            'weapon_slots': self.weapon_slots,
            'armour_slots': self.armour_slots,
        }
        return stats

    def apply_stats(self, stats):
        super().apply_stats(stats)
        self.arm_length = stats['arm_length']
        self.weapon_slots = stats['weapon_slots']
        self.armour_slots = stats['armour_slots']

    def equip_armour(self, armour=None):
        if not armour:
            armour = items.Armour.get_armour_set()
        if type(armour) != list:
            armour = list(armour)

        for armour_part in armour:
            armour_type = armour_part.item_stats['armour_type']
            self.armour_slots[armour_type] = armour_part

    def attack(self, weapon, target):
        pass


class Player(Humanoid):
    """Representation of a player"""
    def __init__(self, player_stats, name, level, inventory, skills):
        super().__init__(player_stats, name, level, inventory)

        self.skills = skills


class EnemyHumanoid(Humanoid):
    """Representation of an enemy"""
    enemy_list = (
        'goblin',
        'ork',
        'outlaw',
        'skeleton',
        'undead',
        'bat person'
    )

    enemy_class_list = (
        'assassin',
        'archer',
        'knight',
        'samurai',
        'thug',
        'mage',
        'brawler'
    )

    legendary_humanoid_list = (
        'moth man',
        'sasquatch',
        'yeti',
        'skeleton king',
        'demon bird',
        'centurion'
    )

    def __init__(self, enemy_stats, name, level, inventory):
        super().__init__(enemy_stats, name, level, inventory)

        self.name = name
        self.speed = enemy_stats['speed']
        self.skill = enemy_stats['skill']
        self.aggression = enemy_stats['aggression']
        self.courage = enemy_stats['courage']
        self.weapon_slots = enemy_stats['weapon_slots']
        self.armour_slots = enemy_stats['armour_slots']
        self.enemy_type = enemy_stats['enemy_type']
        self.enemy_class = enemy_stats['enemy_class']

    def __str__(self):
        enemy_stat_string = f'Level {str(self.level)} {self.enemy_type} {self.enemy_class} {self.name} \n'
        if self.weapon_slots['right_hand'] and self.weapon_slots['left_hand']:
            enemy_stat_string += f'Dual wielding {self.weapon_slots["right_hand"].item_stats["item_type"]}s:\n'
            enemy_stat_string += self.weapon_slots['right_hand'].name + '\n'
            enemy_stat_string += self.weapon_slots['left_hand'].name
        else:
            if self.weapon_slots['right_hand']:
                hand = 'right_hand'
            else:
                hand = 'left_hand'
            enemy_stat_string += 'Wielding a'

            if self.weapon_slots[hand]:
                if self.weapon_slots[hand].name[0] in items.Item.vowels:
                    enemy_stat_string += 'n'

                enemy_stat_string += ' ' + self.weapon_slots[hand].name
                if self.weapon_slots[hand].item_stats['one_handed']:
                    enemy_stat_string += f' in their {hand[:-5]} hand'

        enemy_stat_string += '\n\nWearing:\n'
        armour_slots = self.armour_slots
        for armour in armour_slots:
            if armour_slots[armour]:
                enemy_stat_string += f'Level {str(int(armour_slots[armour].item_stats["rarity"] * 10))} {armour_slots[armour].name},\n'
        enemy_stat_string += '\n'

        for stat in self.stat_dict:
            if type(self.stat_dict[stat]) == int or type(self.stat_dict[stat]) == float:
                enemy_stat_string += f'{stat} -- {str(self.stat_dict[stat])}\n'
        return enemy_stat_string

    @property
    def stat_dict(self):
        stats = {
            'hp': self.hp,
            'height': self.height,
            'weight': self.weight,
            'arm_length': self.weight,
            'speed': self.speed,
            'skill': self.skill,
            'aggression': self.aggression,
            'courage': self.courage,
            'weapon_slots': self.weapon_slots,
            'armour_slots': self.armour_slots,
            'enemy_type': self.enemy_type,
            'enemy_class': self.enemy_class
        }
        return stats

    def apply_stats(self, stats):
        super().apply_stats(stats)
        self.skill = stats['skill']
        self.aggression = stats['aggression']
        self.courage = stats['courage']
        self.weapon_slots = stats['weapon_slots']
        self.armour_slots = stats['armour_slots']
        self.enemy_type = stats['enemy_type']
        self.enemy_class = stats['enemy_class']

    @classmethod
    def get_random_enemy(cls, level=None, enemy_type=None, enemy_class=None):
        if not level:
            level = items.Item.get_item_rarity()
        if not enemy_type:
            enemy_type = cls.enemy_list[random.randint(0, len(cls.enemy_list) - 1)]
        if not enemy_class:
            enemy_class = cls.enemy_class_list[random.randint(0, len(cls.enemy_class_list) - 1)]

        inventory = []

        level_scale = pow(level, 2)

        if enemy_type == 'goblin':
            enemy_stats = {
                'hp': 75 * level_scale + 10,
                'height': 1.05 * items.Item.get_skew_multiplier(10),
                'weight': 80 * items.Item.get_skew_multiplier(20),
                'is_humanoid': True,
                'speed': 0.25,
                'skill': 20,
                'aggression': 65,
                'courage': 50,
                'maxap': 80 * level_scale + 10
            }
            consonants = ['skr', 'skl', 'sl', 'jh', 'j\'r', 'j\'l', 'dr', 'dil', 'gr', 'gl', 'k', 'kr', 'kl']
            vowels = ['a', 'ah', 'e', 'eh', 'i', 'ih', 'u', 'uh', 'o', 'oh']
            armour_consistency = 0.5
            available_weapons = ['axe', 'sword', 'dagger', 'rapier', 'spear']
            available_armours = ['cloth', 'leather', 'chainmail', 'wooden']
        elif enemy_type == 'ork':
            enemy_stats = {
                'hp': 150 * level_scale + 10,
                'height': 2.2 * items.Item.get_skew_multiplier(20),
                'weight': 175 * items.Item.get_skew_multiplier(20),
                'is_humanoid': True,
                'speed': 0.15,
                'skill': 30,
                'aggression': 65,
                'courage': 70,
                'maxap': 100 * level_scale + 10
            }
            consonants = ['skr', 'skl', 'sl', 'jh', 'j\'r', 'j\'l', 'dr', 'dil', 'gr', 'gl', 'k', 'kr', 'kl']
            vowels = ['a', 'ah', 'e', 'eh', 'i', 'ih', 'u', 'uh', 'o', 'oh']
            armour_consistency = 0.6
            available_weapons = ['axe', 'sword', 'mace', 'greatsword', 'spear', 'glaive', 'halberd']
            available_armours = list(items.Armour.armour_materials)
        elif enemy_type == 'outlaw':
            enemy_stats = {
                'hp': 100 * level_scale + 10,
                'height': 1.7 * items.Item.get_skew_multiplier(20),
                'weight': 135 * items.Item.get_skew_multiplier(20),
                'speed': 0.2,
                'skill': 50,
                'aggression': 50,
                'courage': 65,
                'maxap': 90 * level_scale + 10
            }
            consonants = items.Item.consonants
            vowels = items.Item.vowels
            armour_consistency = 0.8
            available_weapons = list(items.Weapon.weapon_types)
            available_armours = list(items.Armour.armour_materials)
        elif enemy_type == 'undead':
            enemy_stats = {
                'hp': 120 * level_scale + 10,
                'height': 1.7 * items.Item.get_skew_multiplier(20),
                'weight': 100 * items.Item.get_skew_multiplier(20),
                'speed': 0.1,
                'skill': 20,
                'aggression': 80,
                'courage': 90,
                'maxap': 50 * level_scale + 10
            }
            consonants = ['gr', 'br', 'b', 'd', 'g', 'w']
            vowels = ['eeeh', 'yoo', 'yuuuh', 'e', 'ooooh', 'uuuhh', 'aaa', 'yaaa']
            armour_consistency = 0.7
            available_weapons = list(items.Weapon.weapon_types)
            available_armours = list(items.Armour.armour_materials)
        elif enemy_type == 'skeleton':
            enemy_stats = {
                'hp': 80 * level_scale + 10,
                'height': 1.7 * items.Item.get_skew_multiplier(20),
                'weight': 80 * items.Item.get_skew_multiplier(20),
                'speed': 0.2,
                'skill': 60,
                'aggression': 50,
                'courage': 80,
                'maxap': 65 * level_scale + 10
            }
            consonants = ['spook', 'doot', 'scare', 'jiggle', 'bones', 'rattle', 'grim', 's', 'ed', 'er']
            vowels = ['e', 'y', 'ya', 'e', 'o', 'oo']
            armour_consistency = 0.7
            available_weapons = list(items.Weapon.weapon_types)
            available_armours = list(items.Armour.armour_materials)
        elif enemy_type == 'bat person':
            enemy_stats = {
                'hp': 90 * level_scale + 10,
                'height': 1.8 * items.Item.get_skew_multiplier(20),
                'weight': 140 * items.Item.get_skew_multiplier(20),
                'speed': 0.4,
                'skill': 60,
                'aggression':  40,
                'courage': 40,
                'maxap': 110 * level_scale + 10
            }
            consonants = ['skr', 'r', 'kr', 'sh']
            vowels = ['aa', 'aaaa', 'ee', 'eeee', 'ii', 'iiii', 'rr', 'rrrr']
            armour_consistency = 0.7
            available_weapons = list(items.Weapon.weapon_types)
            available_armours = list(items.Armour.armour_materials)
        else:
            raise Exception(enemy_type + ' is not a valid enemy type!')

        if enemy_class == 'assassin':
            available_weapons = ['dagger']
            available_armours = ['cloth', 'leather', 'chainmail']
            enemy_stats['skill'] *= 1.2

        elif enemy_class == 'archer':
            enemy_stats['enemy_class'] = 'archer'
            available_weapons = ['bow']
            available_armours = ['cloth', 'leather']
            enemy_stats['aggression'] *= 0.8

        elif enemy_class == 'knight':
            # converting a list to a set removes duplicates
            available_weapons = list(set(available_weapons + ['sword', 'axe', 'mace', 'greatsword', 'halberd','spear', 'glaive', 'katana', 'nodachi']))
            available_armours = list(items.Armour.armour_materials)
            enemy_stats['courage'] *= 1.2
            enemy_stats['aggression'] *= 0.9
            enemy_stats['skill'] *= 1.1
            armour_consistency *= 1.2

        elif enemy_class == 'samurai':
            consonants = items.Item.japanese_letters
            vowels = items.Item.japanese_letters
            available_weapons = ['katana', 'nodachi', 'quarterstaff', 'glaive']
            available_armours = list(items.Armour.armour_materials)
            enemy_stats['courage'] *= 1.1
            enemy_stats['aggression'] *= 0.9
            enemy_stats['skill'] *= 1.2
            armour_consistency *= 1.2

        elif enemy_class == 'thug':
            available_weapons += ['axe', 'dagger']
            available_armours = ['cloth', 'leather', 'chainmail', 'bronze']
            enemy_stats['courage'] *= 0.8
            enemy_stats['aggression'] *= 1.3
            enemy_stats['skill'] *= 0.8
            armour_consistency *= 0.9

        elif enemy_class == 'mage':
            available_weapons = ['wand', 'wizard staff']
            available_armours = ['cloth', 'leather']

        elif enemy_class == 'brawler':
            available_weapons = ['caestus']
            available_armours = ['cloth', 'leather']
            enemy_stats['aggression'] *= 1.3

        else:
            raise Exception(enemy_class + ' is not a valid class type!')
        pass

        enemy_stats['weapon_slots'] = {'left_hand': None, 'right_hand': None}
        right_handed = True
        if random.uniform(0, 1) > 0.9:
            right_handed = False

        enemy_stats['armour_slots'] = {}
        for armour_type in items.Armour.armour_types:
            enemy_stats['armour_slots'][armour_type] = None
            armour_material = available_armours[random.randint(0, len(available_armours) - 1)]

        armour_list = items.Armour.get_armour_set(
            level * items.Item.get_skew_multiplier(10),
            armour_material,
            available_armours,
            armour_consistency
        )

        weapon_type = available_weapons[random.randint(0, len(available_weapons) - 1)]
        enemy_weapon = items.Weapon.get_random_weapon(level * items.Item.get_skew_multiplier(10), weapon_type)

        enemy_name = items.Item.get_fantasy_name(random.randint(2, 2), vowels, consonants)

        enemy_stats['enemy_type'] = enemy_type
        enemy_stats['enemy_class'] = enemy_class
        enemy_stats['injury'] = 0
        enemy_stats['fear'] = 0
        enemy_stats['courage'] = int(enemy_stats['courage'])
        enemy_stats['skill'] = int(enemy_stats['skill'])
        level = int(level * 10)
        enemy_stats['height'] = round(enemy_stats['height'], 2)
        enemy_stats['arm_length'] = round(enemy_stats['height'] * (2/5) * items.Item.get_skew_multiplier(10), 2)
        enemy_stats['hp'] = int(enemy_stats['hp'])
        enemy_stats['weight'] = round(enemy_stats['weight'], 1)
        enemy_stats['max_hp'] = enemy_stats['hp']

        enemy_instance = cls(enemy_stats, enemy_name, level, inventory)
        enemy_instance.equip_armour(armour_list)

        if right_handed:
            enemy_instance.weapon_slots['right_hand'] = enemy_weapon
        else:
            enemy_instance.weapon_slots['left_hand'] = enemy_weapon

        if enemy_weapon.item_stats['one_handed']:
            if random.uniform(0, 1) > 0.8:
                if right_handed:
                    enemy_instance.weapon_slots['left_hand'] = items.Weapon.get_random_weapon((level / 10) * items.Item.get_skew_multiplier(10), weapon_type)
                else:
                    enemy_instance.weapon_slots['right_hand'] = items.Weapon.get_random_weapon((level / 10) * items.Item.get_skew_multiplier(10), weapon_type)

        return enemy_instance


class EnemyCreature(Creature):
    def __init__(self, enemy_stats, level, inventory):
        super().__init__(enemy_stats, level, inventory)

    enemy_creature_list = (
        'slime',
        'giant spider')

    legendary_creature_list = ()
