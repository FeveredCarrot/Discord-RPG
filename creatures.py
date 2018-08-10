import logging
import random
import items
from game import GameObject
from game import Vector2

logger = logging.getLogger(__name__)
if __name__ == '__main__':
    logger.setLevel(logging.INFO)
logger.propagate = True

stream_formatter = logging.Formatter('%(levelname)s:%(message)s')
file_formatter = logging.Formatter('%(levelno)s:%(asctime)s:%(message)s')

file_handler = logging.FileHandler('bot.log')
file_handler.setFormatter(file_formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(stream_formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


class Creature(GameObject):
    """Representation of a living entity"""
    def __init__(self, stats, name, level, inventory, position=None):
        super().__init__(position)
        self.name = name
        self.level = level
        self.inventory = inventory

        self.hp = stats['hp']
        self.height = stats['height']
        self.weight = stats['weight']
        self.carry_capacity = stats['carry_capacity']
        self.speed = stats['speed']
        self.max_ap = stats['max_ap']
        self.ap = self.max_ap

    @property
    def stat_dict(self):
        stats = {
            'hp': self.hp,
            'height': self.height,
            'carry_capacity': self.carry_capacity,
            'weight': self.weight,
            'speed': self.speed,
            'ap': self.ap,
            'max_ap': self.max_ap
        }
        return stats

    @stat_dict.setter
    def stat_dict(self, stats):
        self.hp = stats['hp']
        self.height = stats['height']
        self.weight = stats['weight']
        self.carry_capacity = stats['carry_capacity']
        self.speed = stats['speed']
        self.max_ap = stats['max_ap']
        self.ap = stats['ap']

    @property
    def inventory_value(self):
        inventory_value = 0
        for item in self.inventory:
            inventory_value += item.item_stats['total_value']
        return inventory_value

    @property
    def inventory_weight(self):
        inventory_weight = 0
        for item in self.inventory:
            inventory_weight += item.item_stats['weight']
        return inventory_weight

    @property
    def power_level(self):
        return int(self.hp * self.max_ap * (self.speed / 10) * self.inventory_value)

    @staticmethod
    def power_sort_key(creature):
        return creature.power_level

    def add_to_inventory(self, item):
        """
        Adds an item to the creature's inventory.
        Returns True if successful, returns False if there is no room in inventory
        """
        if item.item_stats['weight'] <= self.carry_capacity - self.inventory_weight:
            self.inventory.append(item)
            del item
            return True
        else:
            logger.debug(f'Creature cannot hold {item.name}')
            return False

    @classmethod
    def generate_enemies(cls, level=None, total_enemies=None, enemy_distribution=None):
        """
        TODO: Include enemy creatures, add enemy type modifiers
        Generates a list of enemies

        level: The average level of the enemies
        total_enemies: total power level of the enemies
        enemy_distribution: higher value means higher level but fewer number of enemies

        """
        if not level:
            level = GameObject.get_level() * 10

        if not total_enemies:
            total_enemies = (level**2 * GameObject.get_level()**2 * 0.1) - (GameObject.get_level()**2)

        if not enemy_distribution:
            enemy_distribution = random.uniform(0.5, 2)

        enemy_list = []
        enemy_tries = 0
        while total_enemies > level and enemy_tries < 100:
            enemy_level = (level / 10) * (enemy_distribution - GameObject.zero_to_range(enemy_distribution / 2))
            enemy_instance = EnemyHumanoid.get_random_enemy(enemy_level)

            total_enemies -= enemy_instance.power_level
            if total_enemies < 50:
                total_enemies += enemy_instance.power_level
                enemy_distribution -= 0.1
            else:
                enemy_list.append(enemy_instance)
            total_enemies = int(total_enemies)

            enemy_tries += 1

        return enemy_list

    def attack(self, weapon, target):
        """
        TODO: Finish
        """
        if type(target) != Creature:
            raise Exception('Invalid Target Type. Target must inherit from creature!')
        if type(weapon) != items.Weapon:
            raise Exception('Invalid weapon. Weapon must be Weapon or inherit from Weapon')

        dmg_to_resistance_dict = {}         # keys are dmg_type, values are resistance_type
        dmg_to_multiplier_dict = {}         # keys are dmg_type, values are dmg multiplier
        i = 0
        while i < len(items.Armour.armour_resistance_types) - 1:
            dmg_to_resistance_dict[items.Weapon.dmg_type_list[i]] = items.Armour.armour_resistance_types[i]
            dmg_to_multiplier_dict[items.Weapon.dmg_type_list[i]] = items.Armour.armour_multiplier_types[i]

        total_dmg = 0
        for dmg_type in dmg_to_resistance_dict:
            damage_dealt = (weapon.item_stats[dmg_type] - target.combined_armour_stats[dmg_to_resistance_dict[dmg_type]]) * target.combined_armour_stats[dmg_to_multiplier_dict[dmg_type]]
            target.hp -= damage_dealt
            total_dmg += damage_dealt
            logger.info(f'{self.name} dealt {damage_dealt} {dmg_type} to {target.name}')
        logger.info(f'Total damage: {total_dmg}')


class Humanoid(Creature):
    """Representation of a humanoid creature"""
    def __init__(self, stats, name, level, inventory):
        super().__init__(stats, name, level, inventory)
        
        self.arm_length = stats['arm_length']
        self.weapon_slots = stats['weapon_slots']
        self.armour_slots = stats['armour_slots']

    def __str__(self):
        player_string = f'{self.name} \n{self.stat_dict}'
        return player_string

    def json_readable(self):
        item_list = []
        for item in self.inventory:
            item_list.append(item.json_readable())

        stats = self.stat_dict
        for slot in self.stat_dict['weapon_slots']:
            if self.stat_dict['weapon_slots'][slot] and type(self.stat_dict['weapon_slots'][slot]) is items.Weapon:
                self.stat_dict['weapon_slots'][slot] = self.stat_dict["weapon_slots"][slot].json_readable()

        for slot in self.stat_dict['armour_slots']:
            if self.stat_dict['armour_slots'][slot] and type(self.stat_dict['armour_slots'][slot]) is items.Armour:
                self.stat_dict['armour_slots'][slot] = self.stat_dict['armour_slots'][slot].json_readable()

        return {
            'stats': stats,
            'name': self.name,
            'level': self.level,
            'inventory': item_list
        }

    def describe(self, info_level):
        """
        Returns a string describing the player.
        Info level is a float from 0 to 1 which changes how detailed the description is.
        """
        description_string = f'{self.name}'
        if info_level < 0.2:
            description_string += f''

    @property
    def stat_dict(self):
        stats = {
            'arm_length': self.arm_length,
            'speed': self.speed,
            'weapon_slots': self.weapon_slots,
            'armour_slots': self.armour_slots,
        }
        return {**stats, **super().stat_dict}

    @stat_dict.setter
    def stat_dict(self, stats):
        super().stat_dict = stats
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

    @property
    def combined_armour_stats(self):
        total_armour_stats = {}
        for slot in self.armour_slots:

            armour_piece = self.armour_slots[slot]
            for armour_stat in armour_piece.item_stats:
                total_armour_stats[armour_stat] += armour_piece.item_stats[armour_stat]

        return total_armour_stats

    @property
    def combined_armour_value(self):
        combined_armour_value = 0
        for slot in self.armour_slots:

            armour_piece = self.armour_slots[slot]
            if armour_piece:
                if type(armour_piece) is dict:
                    logger.debug('Armour is dict for some reason')
                    armour_piece = items.Armour.load_from_save(armour_piece)
                combined_armour_value += armour_piece.item_stats['total_value']

        return combined_armour_value

    @property
    def combined_weapon_value(self):
        combined_weapon_value = 0
        for slot in self.weapon_slots:

            weapon = self.weapon_slots[slot]
            if weapon:
                if type(weapon) is dict:
                    logger.debug('Weapon is dict for some reason')
                    weapon = items.Weapon.load_from_save(weapon)
                combined_weapon_value += weapon.item_stats['total_value']

        return combined_weapon_value

    @property
    def power_level(self):
        return int(self.hp + self.level + self.inventory_value + self.combined_armour_value + self.combined_weapon_value + self.max_ap + self.arm_length + self.speed * 2)


class Player(Humanoid):
    """Representation of a player"""
    def __init__(self, stats, name, level, inventory, player_id, skills):
        super().__init__(stats, name, level, inventory)

        self.player_id = player_id
        self.skills = skills
        self.player_class = stats['player_class']

    @property
    def stat_dict(self):
        stats = {
            'player_id': self.player_id,
            'skills': self.skills,
            'player_class': self.player_class
        }
        return {**stats, **super().stat_dict}

    @stat_dict.setter
    def stat_dict(self, stats):
        super().stat_dict = stats
        self.player_id = stats['player_id']
        self.skills = stats['skills']
        self.player_class = stats['player_class']

    @classmethod
    def load_from_save(cls, attribute_dict):
        item_list = []
        for item_dict in attribute_dict['inventory']:
            item_list.append(items.Item.load_from_save(item_dict))

        for slot in attribute_dict['stats']['weapon_slots']:
            if attribute_dict['stats']['weapon_slots'][slot]:
                attribute_dict['stats']['weapon_slots'][slot] = items.Weapon.load_from_save(attribute_dict['stats']['weapon_slots'][slot])

        for slot in attribute_dict['stats']['armour_slots']:
            if attribute_dict['stats']['armour_slots'][slot]:
                attribute_dict['stats']['armour_slots'][slot] = items.Armour.load_from_save(attribute_dict['stats']['armour_slots'][slot])

        return cls(
            attribute_dict['stats'],
            attribute_dict['name'],
            attribute_dict['level'],
            item_list,
            attribute_dict['stats']['player_id'],
            attribute_dict['stats']['skills']
        )


class EnemyHumanoid(Humanoid):
    """Representation of an enemy"""
    hp_modifier = 1
    ap_modifier = 5

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
        'brawler',
        'viking'
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

        self.skill = enemy_stats['skill']
        self.aggression = enemy_stats['aggression']
        self.courage = enemy_stats['courage']
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
                enemy_stat_string += f'Level ' \
                                     f'{str(int(armour_slots[armour].item_stats["rarity"] * 10))} ' \
                                     f'{armour_slots[armour].name},\n'
        enemy_stat_string += '\n'

        for stat in self.stat_dict:
            if type(self.stat_dict[stat]) == int or type(self.stat_dict[stat]) == float:
                enemy_stat_string += f'{stat} -- {str(self.stat_dict[stat])}\n'

        return enemy_stat_string

    @property
    def stat_dict(self):
        stats = {
            'skill': self.skill,
            'aggression': self.aggression,
            'courage': self.courage,
            'weapon_slots': self.weapon_slots,
            'armour_slots': self.armour_slots,
            'enemy_type': self.enemy_type,
            'enemy_class': self.enemy_class
        }
        return {**stats, **super().stat_dict}

    @stat_dict.setter
    def stat_dict(self, stats):
        super().stat_dict = stats
        self.skill = stats['skill']
        self.aggression = stats['aggression']
        self.courage = stats['courage']
        self.weapon_slots = stats['weapon_slots']
        self.armour_slots = stats['armour_slots']
        self.enemy_type = stats['enemy_type']
        self.enemy_class = stats['enemy_class']

    @classmethod
    def load_from_save(cls, attribute_dict):
        logger.debug(f'Loading enemy from save...')
        item_list = []
        for item_dict in attribute_dict['inventory']:
            item_list.append(items.Item.load_from_save(item_dict))

        for slot in attribute_dict['stats']['weapon_slots']:
            if attribute_dict['stats']['weapon_slots'][slot]:
                attribute_dict['stats']['weapon_slots'][slot] = items.Weapon.load_from_save(attribute_dict['stats']['weapon_slots'][slot])

        for slot in attribute_dict['stats']['armour_slots']:
            if attribute_dict['stats']['armour_slots'][slot]:
                attribute_dict['stats']['armour_slots'][slot] = items.Armour.load_from_save(attribute_dict['stats']['armour_slots'][slot])

        return cls(
            attribute_dict['stats'],
            attribute_dict['name'],
            attribute_dict['level'],
            item_list,
        )

    @classmethod
    def get_random_enemy(cls, level=None, enemy_type=None, enemy_class=None):
        if not level:
            level = items.Item.get_level()
        if not enemy_type:
            enemy_type = cls.enemy_list[random.randint(0, len(cls.enemy_list) - 1)]
        if not enemy_class:
            enemy_class = cls.enemy_class_list[random.randint(0, len(cls.enemy_class_list) - 1)]

        if level < 0.1:
            level = 0.1
            logger.debug('Enemy has level less than 1')

        inventory = []

        level_scale = pow(level, 2)

        if enemy_type == 'goblin':
            enemy_stats = {
                'hp': 75 * level_scale + 10,
                'height': 1.05 * items.Item.get_skew_multiplier(10),
                'weight': 80 * items.Item.get_skew_multiplier(20),
                'speed': 0.25,
                'skill': 20,
                'aggression': 65,
                'courage': 50,
                'max_ap': 80,
                'carry_capacity': 50 * level + 5
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
                'speed': 0.15,
                'skill': 30,
                'aggression': 65,
                'courage': 70,
                'max_ap': 100,
                'carry_capacity': 150 * level + 5
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
                'max_ap': 90,
                'carry_capacity': 100 * level + 5
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
                'max_ap': 50,
                'carry_capacity': 80 * level + 5
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
                'max_ap': 65,
                'carry_capacity': 65 * level + 5
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
                'max_ap': 110,
                'carry_capacity': 100 * (level / 10) + 5
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
            available_weapons = list(set(available_weapons + ['sword', 'axe', 'mace', 'greatsword', 'halberd', 'spear', 'glaive', 'katana', 'nodachi']))
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

        elif enemy_class == 'viking':
            available_weapons += ['axe']
            available_armours = ['leather', 'chainmail', 'wooden', 'iron']
            enemy_stats['courage'] *= 1.1
            enemy_stats['aggression'] *= 1.1
            enemy_stats['skill'] *= 0.9
            armour_consistency *= 0.7

        else:
            raise Exception(enemy_class + ' is not a valid class type!')

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
        enemy_stats['height'] = round(enemy_stats['height'], 2)
        enemy_stats['arm_length'] = round(enemy_stats['height'] * (2/5) * items.Item.get_skew_multiplier(10), 2)
        enemy_stats['hp'] = int(enemy_stats['hp'])
        enemy_stats['weight'] = round(enemy_stats['weight'], 1)
        enemy_stats['carry_capacity'] = int(enemy_stats['carry_capacity'])
        enemy_stats['max_hp'] = enemy_stats['hp']
        enemy_stats['max_ap'] = int(enemy_stats['max_ap'] * cls.ap_modifier * (level / 10) + 10)
        level = int(level * 10)

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
    # TODO Add enemy creatures
    def __init__(self, enemy_stats, level, inventory):
        super().__init__(enemy_stats, level, inventory)

    enemy_creature_list = (
        'slime',
        'giant spider')

    legendary_creature_list = ()
