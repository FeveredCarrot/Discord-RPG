import random
import items


class Enemy:
    # Representation of an enemy

    enemy_humanoid_list = ('goblin', 'ork', 'undead', 'bat person', 'skeleton', 'outlaw')
    enemy_humanoid_list = ('goblin', 'ork', 'outlaw')
    enemy_creature_list = ('slime', 'giant spider')
    enemy_list = enemy_humanoid_list + enemy_creature_list
    enemy_class_list = ('assassin', 'archer', 'knight', 'samurai', 'thug', 'mage', 'brawler')
    legendary_creature_list = ('moth man', 'sasquatch', 'yeti', 'skeleton king', 'demon bird', 'centurion')

    def __init__(self, enemy_stats, name, level, inventory, skills):
        self.enemy_stats = enemy_stats
        self.name = name
        self.level = level
        self.inventory = inventory
        self.skills = skills

    def __str__(self):
        enemy_stat_string = 'Level ' + str(self.level) + ' ' + self.enemy_stats['enemy_type'] + ' ' + self.enemy_stats['enemy_class'] + ' ' + self.name + '\n'
        if self.enemy_stats['weapon_slots']['right_hand'] and self.enemy_stats['weapon_slots']['left_hand']:
            enemy_stat_string += 'Dual wielding ' + self.enemy_stats['weapon_slots']['right_hand'].item_stats['item_type'] + 's:\n'
            enemy_stat_string += self.enemy_stats['weapon_slots']['right_hand'].name + '\n'
            enemy_stat_string += self.enemy_stats['weapon_slots']['left_hand'].name
        else:
            if self.enemy_stats['weapon_slots']['right_hand']:
                hand = 'right_hand'
            else:
                hand = 'left_hand'
            enemy_stat_string += 'Wielding a'
            if self.enemy_stats['weapon_slots'][hand]:
                if self.enemy_stats['weapon_slots'][hand].name[0] in items.Item.vowels:
                    enemy_stat_string += 'n'
                enemy_stat_string += ' ' + self.enemy_stats['weapon_slots'][hand].name
                if self.enemy_stats['weapon_slots'][hand].item_stats['one_handed']:
                    enemy_stat_string += ' in their ' + hand[:-5] + ' hand'

        enemy_stat_string += '\n\nWearing:\n'
        for armour in self.enemy_stats['armour_slots']:
            if self.enemy_stats['armour_slots'][armour]:
                enemy_stat_string += 'Level ' + str(int(self.enemy_stats['armour_slots'][armour].item_stats['rarity'] * 10)) + ' ' + self.enemy_stats['armour_slots'][armour].name + ',\n'
        enemy_stat_string += '\n'

        for stat in self.enemy_stats:
            if type(self.enemy_stats[stat]) == int or type(self.enemy_stats[stat]) == float:
                enemy_stat_string += stat + ' -- ' + str(self.enemy_stats[stat]) + '\n'
        return enemy_stat_string

    def equip_armour(self, armour=None):
        if not armour:
            armour = items.Armour.get_armour_set()
        if type(armour) != list:
            armour = list(armour)

        for armour_part in armour:
            armour_slot_dict = self.enemy_stats['armour_slots']
            armour_type = armour_part.item_stats['armour_type']
            armour_slot_dict[armour_type] = armour_part

        self.enemy_stats['armour_slots'] = armour_slot_dict

    @staticmethod
    def get_random_enemy(level=None, enemy_type=None, enemy_class=None):
        if not level:
            level = items.Item.get_item_rarity()
        if not enemy_type:
            enemy_type = Enemy.enemy_humanoid_list[random.randint(0, len(Enemy.enemy_humanoid_list) - 1)]
        if not enemy_class:
            enemy_class = Enemy.enemy_class_list[random.randint(0, len(Enemy.enemy_class_list) - 1)]

        inventory = []

        level_scale = pow(level, 2)

        if enemy_type == 'goblin':
            enemy_stats = {
                            'hp': 75 * level_scale + 10,
                            'enemy_type': 'goblin',
                            'arm_length': 0.3 * items.Item.get_skew_multiplier(10),
                            'weight': 80 * items.Item.get_skew_multiplier(20),
                            'is_humanoid': True,
                            'speed': 0.25,
                            'skill': 20,
                            'aggression': 65,
                            'courage': 50,
            }
            consonants = ['skr', 'skl', 'sl', 'jh', 'j\'r', 'j\'l', 'dr', 'dil', 'gr', 'gl', 'k', 'kr', 'kl']
            vowels = ['a', 'ah', 'e', 'eh', 'i', 'ih', 'u', 'uh', 'o', 'oh']
            armour_consistency = 0.5
            available_weapons = ['axe', 'sword', 'dagger', 'rapier', 'spear']
            available_armours = ['cloth', 'leather', 'chainmail', 'wooden']
        elif enemy_type == 'ork':
            enemy_stats = {
                            'hp': 150 * level_scale + 10,
                            'enemy_type': 'ork',
                            'arm_length': 0.7 * items.Item.get_skew_multiplier(10),
                            'weight': 175 * items.Item.get_skew_multiplier(20),
                            'is_humanoid': True,
                            'speed': 0.15,
                            'skill': 30,
                            'aggression': 65,
                            'courage': 70
            }
            consonants = ['skr', 'skl', 'sl', 'jh', 'j\'r', 'j\'l', 'dr', 'dil', 'gr', 'gl', 'k', 'kr', 'kl']
            vowels = ['a', 'ah', 'e', 'eh', 'i', 'ih', 'u', 'uh', 'o', 'oh']
            armour_consistency = 0.6
            available_weapons = ['axe', 'sword', 'mace', 'greatsword', 'spear', 'glaive', 'halberd']
            available_armours = list(items.Armour.armour_materials)
        elif enemy_type == 'outlaw':
            enemy_stats = {
                            'hp': 100 * level_scale + 10,
                            'enemy_type': 'outlaw',
                            'arm_length': 0.6 * items.Item.get_skew_multiplier(10),
                            'weight': 135 * items.Item.get_skew_multiplier(20),
                            'is_humanoid': True,
                            'speed': 0.2,
                            'skill': 50,
                            'aggression': 50,
                            'courage': 65
            }
            consonants = items.Item.consonants
            vowels = items.Item.vowels
            armour_consistency = 0.8
            available_weapons = list(items.Weapon.weapon_types)
            available_armours = list(items.Armour.armour_materials)
        else:
            raise Exception(enemy_type + ' is not a valid enemy type!')

        if enemy_class == 'assassin':
            enemy_stats['enemy_class'] = 'assassin'
            available_weapons = ['dagger']
            available_armours = ['cloth', 'leather', 'chainmail']
            enemy_stats['skill'] *= 1.2
        elif enemy_class == 'archer':
            enemy_stats['enemy_class'] = 'archer'
            available_weapons = ['bow']
            available_armours = ['cloth', 'leather']
            enemy_stats['aggression'] *= 0.8
        elif enemy_class == 'knight':
            enemy_stats['enemy_class'] = 'knight'
            # converting a list to a set removes duplicates
            available_weapons = list(set(available_weapons + ['sword', 'axe', 'mace', 'greatsword', 'halberd', 'spear', 'glaive', 'katana', 'nodachi']))
            available_armours = list(items.Armour.armour_materials)
            enemy_stats['courage'] *= 1.2
            enemy_stats['aggression'] *= 0.9
            enemy_stats['skill'] *= 1.1
            armour_consistency *= 1.2
        elif enemy_class == 'samurai':
            enemy_stats['enemy_class'] = 'samurai'
            consonants = items.Item.japanese_letters
            vowels = items.Item.japanese_letters
            available_weapons = ['katana', 'nodachi', 'quarterstaff', 'glaive']
            available_armours = list(items.Armour.armour_materials)
            enemy_stats['courage'] *= 1.1
            enemy_stats['aggression'] *= 0.9
            enemy_stats['skill'] *= 1.2
            armour_consistency *= 1.2
        elif enemy_class == 'thug':
            enemy_stats['enemy_class'] = 'thug'
            available_weapons += ['axe', 'dagger']
            available_armours = ['cloth', 'leather', 'chainmail', 'bronze']
            enemy_stats['courage'] *= 0.8
            enemy_stats['aggression'] *= 1.3
            enemy_stats['skill'] *= 0.8
            armour_consistency *= 0.9
        elif enemy_class == 'mage':
            enemy_stats['enemy_class'] = 'mage'
            available_weapons = ['wand', 'wizard staff']
            available_armours = ['cloth', 'leather']
        elif enemy_class == 'brawler':
            enemy_stats['enemy_class'] = 'brawler'
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

        armour_list = items.Armour.get_armour_set(level * items.Item.get_skew_multiplier(10),
                                                  armour_material,
                                                  available_armours,
                                                  armour_consistency)

        weapon_type = available_weapons[random.randint(0, len(available_weapons) - 1)]
        enemy_weapon = items.Weapon.get_random_weapon(level * items.Item.get_skew_multiplier(10), weapon_type)

        enemy_name = items.Item.get_fantasy_name(random.randint(0, 2), vowels, consonants)

        enemy_stats['injury'] = 0
        enemy_stats['fear'] = 0
        level = int(level * 10)
        enemy_stats['arm_length'] = round(enemy_stats['arm_length'], 2)
        enemy_stats['hp'] = int(enemy_stats['hp'])
        enemy_stats['weight'] = round(enemy_stats['weight'], 1)
        enemy_stats['max_hp'] = enemy_stats['hp']

        enemy_instance = Enemy(enemy_stats, enemy_name, level, inventory, None)
        enemy_instance.equip_armour(armour_list)

        if right_handed:
            enemy_instance.enemy_stats['weapon_slots']['right_hand'] = enemy_weapon
        else:
            enemy_instance.enemy_stats['weapon_slots']['left_hand'] = enemy_weapon

        if enemy_weapon.item_stats['one_handed']:
            if random.uniform(0, 1) > 0.8:
                if right_handed:
                    enemy_instance.enemy_stats['weapon_slots']['left_hand'] = items.Weapon.get_random_weapon((level / 10) * items.Item.get_skew_multiplier(10), weapon_type)
                else:
                    enemy_instance.enemy_stats['weapon_slots']['right_hand'] = items.Weapon.get_random_weapon((level / 10) * items.Item.get_skew_multiplier(10), weapon_type)

        return enemy_instance
