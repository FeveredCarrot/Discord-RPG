import logging
import random
import tkinter

logging.basicConfig(level=logging.INFO)


class Item:
    """Base representation of a game object"""

    stat_skew_percent = 5
    boring_adjectives = ('boring', 'uninteresting', 'unworthy', 'absolutely awful', 'tasteless', 'peasant\'s', 'poorly crafted', 'unfit')
    vowels = ('a', 'e', 'i', 'o', 'u')
    consonants = ('w', 'r', 't', 'p', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'c', 'v', 'b', 'n', 'm')

    def __init__(self, name, item_stats):
        self.name = name
        self.item_values = item_stats

        if 'total_value' in item_stats:
            self.total_value = item_stats['rarity'] * 50

    def __repr__(self):
        return self.item_values['name']

    @staticmethod
    def get_random_consonant():
        return Item.consonants[random.randint(0, len(Item.consonants) - 1)]

    @staticmethod
    def get_random_vowel():
        return Item.vowels[random.randint(0, len(Item.vowels) - 1)]

    @staticmethod
    def get_fantasy_name(name_length):
        """Returns a name using a combination of vowels and consonants"""

        if random.randint(0, 1) == 1:
            fantasy_name = Item.get_random_consonant()
            fantasy_name += Item.get_random_vowel()
        else:
            fantasy_name = Item.get_random_vowel()

        i = 0
        while i < name_length:
            fantasy_name += Item.get_random_consonant()
            fantasy_name += Item.get_random_vowel()
            i += 1

        if random.randint(0, 1) == 1:
            fantasy_name += Item.get_random_consonant()

        return str.capitalize(fantasy_name)

    @staticmethod
    def get_skew_multiplier(percent=stat_skew_percent):
        """Takes a percent value and returns a multiplier used to randomly skew the stats of items"""
        return 1 + (random.uniform(-percent, percent) / 100)

    @staticmethod
    def get_attribute_determiner_value(rng):
        return random.uniform(0, rng)

    @staticmethod
    def test_item_balance(item_classification, item_type=None, sample_size=1000):
        """Returns comparisons of the average stats of items for balance purposes"""
        do_not_compare = []
        item_type_list = []
        item_list = []

        if item_classification == 'weapon':
            item_type_list = Weapon.weapon_types
        elif item_classification == 'armour':
            item_type_list = Armour.armour_materials

        print('Generating Items')
        i = 0
        while i < sample_size:
            if item_classification == 'weapon':
                item_list.append(Weapon.get_random_weapon(None, item_type))
            elif item_classification == 'armour':
                item_list.append(Armour.get_random_armour(None, None, item_type))
            else:
                raise Exception(item_classification + ' is not a valid type of item! try \"weapon\" or \"armour\"')
                continue
            i += 1
        """we made a list of rng items, lets sort and compare this info"""

        separated_items = {}
        """separated_items is a dict with keys as the item_type string and values that are lists which include all items of that item type"""
        if item_type:
            separated_items = {item_type: item_list}
        else:
            for item_type in item_type_list:
                separated_items[item_type] = []
                for item in item_list:
                    if item.item_stats['item_type'] == item_type:
                        separated_items[item_type].append(item)

        all_item_averages = {}
        """all_item_averages is a dict with keys being the item type and values being another dict with keys being stat names and values being the average value for that stat"""
        for item_type in separated_items:
            print('Getting average stats for ' + item_type)
            item_stat_averages = {}
            num_of_items = 0

            for item in separated_items[item_type]:
                item_stats = item.item_stats

                for stat in item_stats:
                    if (type(item_stats[stat]) is int or type(item_stats[stat]) is float) and stat not in do_not_compare:
                        if stat not in item_stat_averages:
                            item_stat_averages[stat] = 0
                        item_stat_averages[stat] += item_stats[stat]
                num_of_items += 1

            for stat in item_stat_averages:
                item_stat_averages[stat] /= num_of_items
                item_stat_averages[stat] = round(item_stat_averages[stat], 2)

            if item_classification == 'weapon':
                item_stat_averages['dmg_per_ap'] = round(item_stat_averages['total_dmg'] / item_stat_averages['ap'], 2)
            all_item_averages[item_type] = item_stat_averages

        cleaned_data_string = '\n'
        for item_type in all_item_averages:
            item_stats = all_item_averages[item_type]
            cleaned_data_string += '-- average values for ' + item_type + ' --\n'
            for stat in item_stats:
                cleaned_data_string += stat + ' -- ' + str(item_stats[stat]) + '\n'
            cleaned_data_string += '\n'
        return cleaned_data_string


class Weapon(Item):

    dmg_type_list = ('blunt_dmg', 'slash_dmg', 'puncture_dmg', 'electric_dmg', 'fire_dmg', 'magic_dmg', 'true_dmg')
    weapon_types = ('sword', 'axe', 'mace', 'spear', 'halberd', 'rapier', 'greatsword', 'dagger', 'caestus', 'bow', 'glaive')

    def __init__(self, name, weapon_stats):
        super().__init__(name, weapon_stats)

        self.item_stats = weapon_stats

        self.item_stats['total_dmg'] = 0
        for dmg_type in weapon_stats:
            if dmg_type in Weapon.dmg_type_list:
                """Check if dmg_type is a damage type instead of something like ap or weight"""
                self.item_stats['total_dmg'] += weapon_stats[dmg_type]

        self.useful_dmg_values = {}
        for dmg_type in self.item_stats:
            if dmg_type in Weapon.dmg_type_list:
                """Check if dmg_type is a damage type instead of something like ap or weight"""
                if self.item_stats[dmg_type] != 0:
                    self.useful_dmg_values[dmg_type] = str(self.item_stats[dmg_type])

        self.total_value = self.item_stats['total_dmg'] * weapon_stats['rarity']

    def __repr__(self):
        weapon_stat_string = 'Dmg per AP value -- ' + str(round(self.item_stats['total_dmg'] / self.item_stats['ap'], 2)) + ' | Level ' + str(round(self.item_stats['rarity'], 2)) + ' -- ' + self.name + '\n'
        for dmg_type in self.useful_dmg_values:
            weapon_stat_string += dmg_type + ' -- ' + str(self.useful_dmg_values[dmg_type]) + '\n'

        return weapon_stat_string

    @staticmethod
    def get_weapon_values(rarity=None, weapon_type=None):
        if not rarity:
            rarity = random.randint(1, 10)
        if not weapon_type:
            weapon_type = Weapon.weapon_types[random.randint(0, len(Weapon.weapon_types) - 1)]

        ap_scalar = 0.15
        rarity_scaling_exponential = pow(rarity, 2)
        ap_scaling_exponential = pow(rarity, 1)

        if weapon_type == 'sword':
            weapon_stats = {
                                    'ap': 45 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 0.8 * Item.get_skew_multiplier(20),
                                    'weight': 3 * Item.get_skew_multiplier(20),
                                    'requires_ammo': False,
                                    'blunt_dmg': 5 * rarity_scaling_exponential - 70,
                                    'slash_dmg': 20 * rarity_scaling_exponential,
                                    'puncture_dmg': 5 * rarity_scaling_exponential - 65,
                                    'electric_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'fire_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'magic_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'true_dmg': 10 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(8))
            }
        elif weapon_type == 'axe':
            weapon_stats = {
                                    'ap': 45 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 0.6 * Item.get_skew_multiplier(40),
                                    'weight': 3 * Item.get_skew_multiplier(20),
                                    'requires_ammo': False,
                                    'blunt_dmg': 4 * rarity_scaling_exponential - 20,
                                    'slash_dmg': 20 * rarity_scaling_exponential,
                                    'puncture_dmg': 5 * rarity_scaling_exponential - 15,
                                    'electric_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'fire_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'magic_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'true_dmg': 10 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(8))
            }
        elif weapon_type == 'mace':
            weapon_stats = {
                                    'ap': 45 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 0.7 * Item.get_skew_multiplier(20),
                                    'weight': 2.5 * Item.get_skew_multiplier(10),
                                    'requires_ammo': False,
                                    'blunt_dmg': 20 * rarity_scaling_exponential,
                                    'slash_dmg': 5 * rarity_scaling_exponential - 100,
                                    'puncture_dmg': 5 * rarity_scaling_exponential - 80,
                                    'electric_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'fire_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'magic_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'true_dmg': 10 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(12))
            }
        elif weapon_type == 'spear':
            weapon_stats = {
                                    'ap': 45 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 2.1 * Item.get_skew_multiplier(15),
                                    'weight': 3 * Item.get_skew_multiplier(20),
                                    'requires_ammo': False,
                                    'blunt_dmg': 0,
                                    'slash_dmg': 5 * rarity_scaling_exponential - 80,
                                    'puncture_dmg': 20 * rarity_scaling_exponential,
                                    'electric_dmg': 7 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'fire_dmg': 11 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'magic_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'true_dmg': 13 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(4))
            }
        elif weapon_type == 'halberd':
            weapon_stats = {
                                    'ap': 75 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 1.65 * Item.get_skew_multiplier(10),
                                    'weight': 5 * Item.get_skew_multiplier(20),
                                    'requires_ammo': False,
                                    'blunt_dmg': 5 * rarity_scaling_exponential - 100,
                                    'slash_dmg': 17 * rarity_scaling_exponential,
                                    'puncture_dmg': 17 * rarity_scaling_exponential,
                                    'electric_dmg': 15 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'fire_dmg': 13 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'magic_dmg': 13 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'true_dmg': 13 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(16))

            }
        elif weapon_type == 'rapier':
            weapon_stats = {
                                    'ap': 20 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 1.15 * Item.get_skew_multiplier(10),
                                    'weight': 2 * Item.get_skew_multiplier(10),
                                    'requires_ammo': False,
                                    'blunt_dmg': 5 * rarity_scaling_exponential - 200,
                                    'slash_dmg': 4 * rarity_scaling_exponential,
                                    'puncture_dmg': 8 * rarity_scaling_exponential,
                                    'electric_dmg': 3 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'fire_dmg': 3 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'magic_dmg': 3 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'true_dmg': 5 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(4))

            }
        elif weapon_type == 'greatsword':
            weapon_stats = {
                                    'ap': 90 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 1.65 * Item.get_skew_multiplier(10),
                                    'weight': 5 * Item.get_skew_multiplier(10),
                                    'requires_ammo': False,
                                    'blunt_dmg': 15 * rarity_scaling_exponential - 20,
                                    'slash_dmg': 40 * rarity_scaling_exponential,
                                    'puncture_dmg': 10 * rarity_scaling_exponential - 50,
                                    'electric_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'fire_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'magic_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'true_dmg': 10 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(12))

            }
        elif weapon_type == 'dagger':
            weapon_stats = {
                                    'ap': 7 * ap_scaling_exponential * ap_scalar * 2 + 1,
                                    'range': 0.385 * Item.get_skew_multiplier(70),
                                    'weight': 0.5 * Item.get_skew_multiplier(50),
                                    'requires_ammo': False,
                                    'blunt_dmg': 1 * rarity_scaling_exponential - 100,
                                    'slash_dmg': 6 * rarity_scaling_exponential,
                                    'puncture_dmg': 6 * rarity_scaling_exponential,
                                    'electric_dmg': 2 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'fire_dmg': 2 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'magic_dmg': 2 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'true_dmg': 10 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(4))

            }
        elif weapon_type == 'caestus':
            weapon_stats = {
                                    'ap': 4 * ap_scaling_exponential * ap_scalar * 2 + 1,
                                    'range': 0.1 * Item.get_skew_multiplier(10),
                                    'weight': 0.3 * Item.get_skew_multiplier(10),
                                    'requires_ammo': False,
                                    'blunt_dmg': 4 * rarity_scaling_exponential,
                                    'slash_dmg': 2 * rarity_scaling_exponential - 100,
                                    'puncture_dmg': 3 * rarity_scaling_exponential - 50,
                                    'electric_dmg': 5 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'fire_dmg': 5 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'magic_dmg': 5 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'true_dmg': 3 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(8))

            }
        elif weapon_type == 'bow':
            weapon_stats = {
                                    'ap': 45 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 140 * Item.get_skew_multiplier(20),
                                    'weight': 2 * Item.get_skew_multiplier(10),
                                    'requires_ammo': True,
                                    'blunt_dmg': 2 * rarity_scaling_exponential - 150,
                                    'slash_dmg': 5 * rarity_scaling_exponential - 100,
                                    'puncture_dmg': 15 * rarity_scaling_exponential,
                                    'electric_dmg': 5 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'fire_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'magic_dmg': 5 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'true_dmg': 5 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(8))
            }
        elif weapon_type == 'glaive':
            weapon_stats = {
                                    'ap': 55 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 2.4 * Item.get_skew_multiplier(10),
                                    'weight': 5 * Item.get_skew_multiplier(10),
                                    'requires_ammo': False,
                                    'blunt_dmg': 5 * rarity_scaling_exponential - 100,
                                    'slash_dmg': 20 * rarity_scaling_exponential,
                                    'puncture_dmg': 5 * rarity_scaling_exponential,
                                    'electric_dmg': 15 * rarity_scaling_exponential - (rarity_scaling_exponential * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'fire_dmg': 13 * rarity_scaling_exponential - (rarity_scaling_exponential * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'magic_dmg': 13 * rarity_scaling_exponential - (rarity_scaling_exponential * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'true_dmg': 13 * rarity_scaling_exponential - (rarity_scaling_exponential * 150 * Weapon.get_attribute_determiner_value(16))
            }
        else:
            raise Exception('not a valid weapon type!')

        for dmg_type in weapon_stats:

            skew_multiplier = Weapon.get_skew_multiplier()

            if dmg_type in Weapon.dmg_type_list:
                """Check if dmg_type is a damage type instead of something like ap or weight"""
                weapon_stats[dmg_type] = weapon_stats[dmg_type] * skew_multiplier
                weapon_stats[dmg_type] = int(weapon_stats[dmg_type])

            if weapon_stats[dmg_type] < 0:
                weapon_stats[dmg_type] = 0

        weapon_stats['weight'] = round(weapon_stats['weight'], 1)
        weapon_stats['range'] = round(weapon_stats['range'], 2)

        weapon_stats['rarity'] = rarity
        weapon_stats['item_type'] = weapon_type

        return weapon_stats

    @classmethod
    def get_random_weapon(cls, rarity=None, weapon_type=None):
        """Returns a randomized weapon with the option to specify its rarity and type"""

        if not rarity:
            rarity = random.randint(1, 10)
        if not weapon_type:
            weapon_type = Weapon.weapon_types[random.randint(0, len(Weapon.weapon_types) - 1)]

        rarity_scaling_exponential = pow(rarity, 2)
        weapon_name = weapon_type
        weapon_stats = Weapon.get_weapon_values(rarity, weapon_type)

        total_dmg = 0
        for dmg_type in weapon_stats:
            if dmg_type in Weapon.dmg_type_list:
                """Check if dmg_type is a damage type instead of something like ap or weight"""
                total_dmg += weapon_stats[dmg_type]

        dmg_per_ap = total_dmg / weapon_stats['ap']

        for dmg_type in weapon_stats:
            if dmg_type in Weapon.dmg_type_list:
                """Check if dmg_type is a damage type instead of something like ap or weight"""
                if weapon_stats[dmg_type] * (rarity / 2) / weapon_stats['ap'] > .5:
                    adjectives = ['']
                    if dmg_type == 'blunt_dmg':
                        adjectives = ('crushing', 'bone-breaking', 'head-squashing', 'bludgeoning', 'crippling', 'gut-wrenching', 'heavy')

                    elif dmg_type == 'slash_dmg':
                        adjectives = ('slicing', 'slashing', 'bleeding', 'serrated', 'head-chopping', 'decapitating', 'cutting-edge', 'dismembering', 'sharp')

                    elif dmg_type == 'puncture_dmg':
                        adjectives = ('piercing', 'puncturing', 'poking', 'impaling', 'stabbing', 'skewering', 'hole-making', 'pointy')

                    elif dmg_type == 'electric_dmg':
                        adjectives = ('electrifying', 'shocking', 'heart-stopping', 'sparking', 'thunderous', 'jolting', 'zapping')

                    elif dmg_type == 'fire_dmg':
                        adjectives = ('burning', 'fiery', 'blistering', 'scorching', 'searing', 'red-hot', 'flaming')

                    elif dmg_type == 'magic_dmg':
                        adjectives = ('magical', 'enchanted', 'mystical', 'spellbound', 'spectral', 'otherworldly', 'encanted')

                    elif dmg_type == 'true_dmg':
                        adjectives = ('armour-ignoring', 'disemboweling', 'murderous', 'intimidating', 'legendary', 'killer', 'precise')

                    weapon_name = adjectives[random.randint(0, len(adjectives) - 1)] + ' ' + weapon_name

        if dmg_per_ap < 5:
            weapon_name = Item.boring_adjectives[random.randint(0, len(Item.boring_adjectives) - 1)] + ' ' + weapon_name

        if dmg_per_ap > rarity_scaling_exponential * 4.5 / rarity and rarity > 2.5:
            fantasy_name = Item.get_fantasy_name(random.randint(1, 4))
            weapon_titles = [' of ' + fantasy_name,
                             ' from the land of ' + fantasy_name,
                             ', crafted by the talented ' + fantasy_name,
                             ', infused with ' + fantasy_name,
                             ', feared by the ' + fantasy_name,
                             ', slayer of the ' + fantasy_name,
                             ' of the faraway plains of ' + fantasy_name,
                             ' from the swamp of ' + fantasy_name,
                             ', wielded by the great ' + fantasy_name,
                             ' excavated from the tombs of ' + fantasy_name,
                             ', winner of the ' + fantasy_name + ' war',
                             ', born from the depths of ' + fantasy_name,
                             ', originating from the deserts of ' + fantasy_name,
                             ' - \"The ' + weapon_type + ' of all ' + weapon_type + 's\"',
                             ' - One ' + weapon_type + ' to rule them all.'
                             ]
            weapon_name += weapon_titles[random.randint(0, len(weapon_titles) - 1)]

        return cls(weapon_name, weapon_stats)


class Armour(Item):

    armour_resistance_types = ('general_resistance', 'blunt_dmg_resistance', 'slash_dmg_resistance', 'puncture_dmg_resistance', 'electric_dmg_resistance', 'fire_dmg_resistance', 'magic_dmg_resistance')
    armour_multiplier_types = ('general_dmg_multiplier', 'blunt_dmg_multiplier', 'slash_dmg_multiplier', 'puncture_dmg_multiplier', 'electric_dmg_multiplier', 'fire_dmg_multiplier', 'magic_dmg_multiplier')
    armour_types = ('helmet', 'chestpiece', 'arm guards', 'gloves', 'leggings')
    armour_materials = ('cloth', 'leather', 'chainmail', 'bronze', 'iron', 'steel')

    def __init__(self, name, armour_values):

        super().__init__(name, armour_values)
        self.name = name
        self.item_stats = armour_values

        self.useful_resistances = {}
        self.useful_multipliers = {}

        for value in self.item_stats:
            if value in Armour.armour_resistance_types:
                if self.item_stats[value] != 0:
                    self.useful_resistances[value] = str(self.item_stats[value])
            elif value in Armour.armour_multiplier_types:
                if self.item_stats[value] > 1:
                    self.useful_multipliers[value] = str(self.item_stats[value])

    def __repr__(self):
        armour_stat_string = ''
        for resistance_type in self.useful_resistances:
            armour_stat_string += resistance_type + ' -- ' + self.useful_resistances[resistance_type] + '\n'
        # armour_stat_string += '\n'
        for multiplier_type in self.useful_multipliers:
            armour_stat_string += multiplier_type + ' -- ' + self.useful_multipliers[multiplier_type] + '\n'

        return 'Armour Value -- ' + str(self.item_stats['total_value']) + ' | Level ' + str(round(self.item_stats['rarity'], 2)) + ' -- ' + self.name + '\n' + armour_stat_string

    @staticmethod
    def get_armour_values(rarity=None, armour_type=None, armour_material=None):
        if not rarity:
            rarity = random.randint(1, 10)
        if not armour_type:
            armour_type = Armour.armour_types[random.randint(0, len(Armour.armour_types) - 1)]
        if not armour_material:
            armour_material = Armour.armour_materials[random.randint(0, len(Armour.armour_materials) - 1)]
        weight_modifier = 0
        rarity_scaling_exponential = pow(rarity, 1.6)

        if armour_type == 'helmet':
            weight_modifier = random.uniform(0.2, 0.3)
        elif armour_type == 'chestpiece':
            weight_modifier = random.uniform(0.9, 1.1)
        elif armour_type == 'arm guards':
            weight_modifier = random.uniform(0.15, 0.25)
        elif armour_type == 'gloves':
            weight_modifier = random.uniform(0.1, 0.15)
        elif armour_type == 'leggings':
            weight_modifier = random.uniform(0.7, 0.8)

        if armour_material == 'cloth':
            armour_stats = {
                            'weight': weight_modifier * 8,
                            'general_resistance': rarity_scaling_exponential * 0.5 - 100,
                            'blunt_dmg_resistance': rarity_scaling_exponential * 3,
                            'slash_dmg_resistance': rarity_scaling_exponential * 1 - 10,
                            'puncture_dmg_resistance': rarity_scaling_exponential * 1 - 10,
                            'electric_dmg_resistance': rarity_scaling_exponential * 5 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(4)),
                            'fire_dmg_resistance': 0,
                            'magic_dmg_resistance': rarity_scaling_exponential * 5 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(2)),
                            'general_dmg_multiplier': 0,
                            'blunt_dmg_multiplier': 0,
                            'slash_dmg_multiplier': 0,
                            'puncture_dmg_multiplier': 0,
                            'electric_dmg_multiplier': 3 - (Item.get_attribute_determiner_value(30)),
                            'fire_dmg_multiplier': 3 - (Item.get_attribute_determiner_value(10)),
                            'magic_dmg_multiplier': 3 - (Item.get_attribute_determiner_value(20))
            }
        elif armour_material == 'leather':
            armour_stats = {
                            'weight': weight_modifier * 12,
                            'general_resistance': rarity_scaling_exponential * 0.3 - 100,
                            'blunt_dmg_resistance': rarity_scaling_exponential * 5,
                            'slash_dmg_resistance': rarity_scaling_exponential * 1.5 - 10,
                            'puncture_dmg_resistance': rarity_scaling_exponential * 1.3 - 10,
                            'electric_dmg_resistance': rarity_scaling_exponential * 5 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(4)),
                            'fire_dmg_resistance': 0,
                            'magic_dmg_resistance': rarity_scaling_exponential * 5 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(2)),
                            'general_dmg_multiplier': 0,
                            'blunt_dmg_multiplier': 0,
                            'slash_dmg_multiplier': 0,
                            'puncture_dmg_multiplier': 0,
                            'electric_dmg_multiplier': 3 - (Item.get_attribute_determiner_value(30)),
                            'fire_dmg_multiplier': 3 - (Item.get_attribute_determiner_value(12)),
                            'magic_dmg_multiplier': 3 - (Item.get_attribute_determiner_value(20))
            }
        elif armour_material == 'chainmail':
            armour_stats = {
                            'weight': weight_modifier * 20,
                            'general_resistance': rarity_scaling_exponential * 0.5 - 100,
                            'blunt_dmg_resistance': rarity_scaling_exponential * 2,
                            'slash_dmg_resistance': rarity_scaling_exponential * 5,
                            'puncture_dmg_resistance': rarity_scaling_exponential * 1 - 10,
                            'electric_dmg_resistance': rarity_scaling_exponential * 2 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(4)),
                            'fire_dmg_resistance': rarity_scaling_exponential * 2 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(4)),
                            'magic_dmg_resistance': rarity_scaling_exponential * 2 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(4)),
                            'general_dmg_multiplier': 0,
                            'blunt_dmg_multiplier': 0,
                            'slash_dmg_multiplier': 0,
                            'puncture_dmg_multiplier': 0,
                            'electric_dmg_multiplier':  3 - (Item.get_attribute_determiner_value(10)),
                            'fire_dmg_multiplier':  3 - (Item.get_attribute_determiner_value(20)),
                            'magic_dmg_multiplier':  3 - (Item.get_attribute_determiner_value(20))
            }
        elif armour_material == 'bronze':
            armour_stats = {
                            'weight': weight_modifier * 30,
                            'general_resistance': rarity_scaling_exponential * 0.5 - 100,
                            'blunt_dmg_resistance': rarity_scaling_exponential * 1 - 10,
                            'slash_dmg_resistance': rarity_scaling_exponential * 10,
                            'puncture_dmg_resistance': rarity_scaling_exponential * 5,
                            'electric_dmg_resistance': 0,
                            'fire_dmg_resistance': rarity_scaling_exponential * 2 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(4)),
                            'magic_dmg_resistance': 0,
                            'general_dmg_multiplier': 0,
                            'blunt_dmg_multiplier': 0,
                            'slash_dmg_multiplier': 0,
                            'puncture_dmg_multiplier': 0,
                            'electric_dmg_multiplier':  3 - (Item.get_attribute_determiner_value(5)),
                            'fire_dmg_multiplier':  3 - (Item.get_attribute_determiner_value(30)),
                            'magic_dmg_multiplier':  3 - (Item.get_attribute_determiner_value(10))
            }
        elif armour_material == 'iron':
            armour_stats = {
                            'weight': weight_modifier * 40,
                            'general_resistance': rarity_scaling_exponential * 0.5 - 100,
                            'blunt_dmg_resistance': rarity_scaling_exponential * 2 - 10,
                            'slash_dmg_resistance': rarity_scaling_exponential * 13,
                            'puncture_dmg_resistance': rarity_scaling_exponential * 7,
                            'electric_dmg_resistance': 0,
                            'fire_dmg_resistance': rarity_scaling_exponential * 2 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(3)),
                            'magic_dmg_resistance': 0,
                            'general_dmg_multiplier': 0,
                            'blunt_dmg_multiplier': 0,
                            'slash_dmg_multiplier': 0,
                            'puncture_dmg_multiplier': 0,
                            'electric_dmg_multiplier':  3 - (Item.get_attribute_determiner_value(4)),
                            'fire_dmg_multiplier':  3 - (Item.get_attribute_determiner_value(30)),
                            'magic_dmg_multiplier':  3 - (Item.get_attribute_determiner_value(10))
            }
        elif armour_material == 'steel':
            armour_stats = {
                            'weight': weight_modifier * 50,
                            'general_resistance': rarity_scaling_exponential * 0.5 - 100,
                            'blunt_dmg_resistance': rarity_scaling_exponential * 3 - 10,
                            'slash_dmg_resistance': rarity_scaling_exponential * 15,
                            'puncture_dmg_resistance': rarity_scaling_exponential * 10,
                            'electric_dmg_resistance': 0,
                            'fire_dmg_resistance': rarity_scaling_exponential * 2 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(3)),
                            'magic_dmg_resistance': 0,
                            'general_dmg_multiplier': 0,
                            'blunt_dmg_multiplier': 0,
                            'slash_dmg_multiplier': 0,
                            'puncture_dmg_multiplier': 0,
                            'electric_dmg_multiplier':  3 - (Item.get_attribute_determiner_value(5)),
                            'fire_dmg_multiplier':  3 - (Item.get_attribute_determiner_value(30)),
                            'magic_dmg_multiplier':  3 - (Item.get_attribute_determiner_value(8))
            }
        else:
            raise Exception('Not a valid armour material!')

        total_protection = 0
        total_multiplier = 1
        for value in armour_stats:

            skew_multiplier = Item.get_skew_multiplier()
            armour_stats[value] = armour_stats[value] * weight_modifier

            if value in Armour.armour_resistance_types or value in Armour.armour_multiplier_types:
                armour_stats[value] = armour_stats[value] * skew_multiplier
                armour_stats[value] = int(armour_stats[value])

            if armour_stats[value] < 0:
                armour_stats[value] = 0
            if value in Armour.armour_resistance_types:
                total_protection += armour_stats[value]

            if value in Armour.armour_multiplier_types:
                armour_stats[value] = round(armour_stats[value] * skew_multiplier, 1)

                if armour_stats[value] < 1:
                    armour_stats[value] = 1

                total_multiplier *= armour_stats[value]

        total_value = int(total_protection * (1 / total_multiplier))

        armour_stats['total_value'] = total_value
        armour_stats['rarity'] = rarity
        armour_stats['item_type'] = armour_material
        armour_stats['weight'] = round(armour_stats['weight'], 1)
        armour_stats['weight_modifier'] = weight_modifier

        return armour_stats

    @classmethod
    def get_random_armour(cls, rarity=None, armour_type=None, armour_material=None):
        if not rarity:
            rarity = random.randint(1, 10)
        if not armour_type:
            armour_type = Armour.armour_types[random.randint(0, len(Armour.armour_types) - 1)]
        if not armour_material:
            armour_material = Armour.armour_materials[random.randint(0, len(Armour.armour_materials) - 1)]

        armour_stats = Armour.get_armour_values(rarity, armour_type, armour_material)
        armour_name = armour_material + ' ' + armour_type
        armour_stats['ap'] = 10
        rarity_scaling_exponential = pow(rarity, 1.6)

        for resistance_type in armour_stats:
            if resistance_type in Armour.armour_resistance_types:
                if armour_stats[resistance_type] * (rarity / 2) > 5:
                    adjectives = ['']
                    if resistance_type == 'blunt_dmg_resistance':
                        adjectives = ['hardy', 'cushioning', 'heavy', 'dent-resistant', 'shock-absorbing']

                    elif resistance_type == 'slash_dmg_resistance':
                        adjectives = ['hard', 'scratch-resistant', 'hardened', 'tempered']

                    elif resistance_type == 'puncture_dmg_resistance':
                        adjectives = ['impenetrable', 'thick', 'deflecting', 'puncture-resistant']

                    elif resistance_type == 'electric_dmg_resistance':
                        adjectives = ['grounded', 'rubbery', 'electron-absorbing', 'lightning-reflecting']

                    elif resistance_type == 'fire_dmg_resistance':
                        adjectives = ['heat-treated', 'unburnable', 'heat-absorbing', 'fire-resistant']

                    elif resistance_type == 'magic_dmg_resistance':
                        adjectives = ['blessed', 'encanted', 'magical', 'dark']

                    armour_name = adjectives[random.randint(0, len(adjectives) - 1)] + ' ' + armour_name

        if (armour_stats['total_value'] / armour_stats['weight_modifier']) < 10:
            # print(total_value / weight_modifier)
            armour_name = Item.boring_adjectives[random.randint(0, len(Item.boring_adjectives) - 1)] + ' ' + armour_name

        if (armour_stats['total_value'] / armour_stats['weight_modifier']) / rarity > rarity_scaling_exponential * 4 / rarity and rarity > 2.5:
            fantasy_name = Item.get_fantasy_name(random.randint(1, 4))
            armour_titles = [' of ' + fantasy_name,
                             ' from the land of ' + fantasy_name,
                             ', crafted by the talented ' + fantasy_name,
                             ', infused with ' + fantasy_name,
                             ', feared by the ' + fantasy_name,
                             ', protector of the ' + fantasy_name,
                             ' of the faraway plains of ' + fantasy_name,
                             ' from the swamp of ' + fantasy_name,
                             ', worn by the great ' + fantasy_name,
                             ' excavated from the tombs of ' + fantasy_name,
                             ', born from the depths of ' + fantasy_name,
                             ', originating from the deserts of ' + fantasy_name
                             ]
            armour_name += armour_titles[random.randint(0, len(armour_titles) - 1)]

        return cls(armour_name, armour_stats)


i = 1
while i <= 10:
    print(Weapon.get_random_weapon(i))
    i += 1

i = 1
while i <= 10:
    print(Armour.get_random_armour(i))
    i += 1

print(Item.test_item_balance('armour', None, 20000))
print(Item.test_item_balance('weapon', None, 20000))
