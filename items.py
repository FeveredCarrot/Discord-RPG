import random
# import tkinter


class Item:
    # Base representation of a game object

    stat_skew_percent = 10
    boring_adjectives = ('boring', 'uninteresting', 'unworthy', 'absolutely awful', 'tasteless', 'peasant\'s', 'poorly crafted', 'unfit', 'terrible')
    vowels = ('a', 'e', 'i', 'o', 'u')
    consonants = ('w', 'r', 't', 'p', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'c', 'v', 'b', 'n', 'm', '-')
    japanese_letters = ('a', 'i', 'u', 'e', 'o', 'ya', 'yu', 'yo', 'n',
                        'ka', 'ki', 'ku', 'ke', 'ko', 'kya', 'kyu', 'kyo',
                        'sa', 'shi', 'su', 'se', 'so', 'sha', 'shu', 'sho',
                        'ta', 'chi', 'tsu', 'te', 'to', 'cha', 'chu', 'cho',
                        'na', 'ni', 'nu', 'ne', 'no', 'nya', 'nyu', 'nyo',
                        'ha', 'hi', 'fu', 'he', 'ho', 'hya', 'hyu', 'hyo',
                        'ma', 'mi', 'mu', 'me', 'mo', 'mya', 'myu', 'myo',
                        'ra', 'ri', 'ru', 're', 'ro', 'rya', 'ryu', 'ryo',
                        'wa', 'wi', 'we', 'wo'
                        'ga', 'gi', 'gu', 'ge', 'go', 'gya', 'gyu', 'gyo',
                        'za', 'ji', 'zu', 'ze', 'zo', 'ja', 'ju', 'jo',
                        'da', 'de', 'do'
                        'ba', 'bi', 'bu', 'be', 'bo', 'bya', 'byu', 'byo',
                        'pa', 'pi', 'pu', 'pe', 'po', 'pya', 'pyu', 'pyo')

    def __init__(self, name, item_stat_dict):
        self.name = name
        self.item_stat_dict = item_stat_dict

        if 'total_value' in item_stat_dict:
            self.total_value = item_stat_dict['rarity'] * 50

    def __repr__(self):
        return self.item_stat_dict['name']

    @staticmethod
    def get_item_rarity():
        random_number = random.uniform(0, 10)
        return 4*(0.1919 * random_number - 0.608)**3 + 1
        # return (0.214 * random_number)**3.02 + 0.1

    @staticmethod
    def get_random_consonant(consonant_list=None):
        if not consonant_list:
            consonant_list = Item.consonants
        return consonant_list[random.randint(0, len(consonant_list) - 1)]

    @staticmethod
    def get_random_vowel(vowel_list=None):
        if not vowel_list:
            vowel_list = Item.consonants
        return vowel_list[random.randint(0, len(vowel_list) - 1)]

    @staticmethod
    def get_fantasy_name(name_length, vowel_list=None, consonant_list=None):
        # Returns a name using a combination of vowels and consonants
        if not vowel_list:
            vowel_list = Item.vowels
        if not consonant_list:
            consonant_list = Item.consonants

        if random.randint(0, 1) == 1:
            fantasy_name = Item.get_random_consonant(consonant_list)
            fantasy_name += Item.get_random_vowel(vowel_list)
        else:
            fantasy_name = Item.get_random_vowel(vowel_list)

        i = 0
        while i < name_length - 1:
            fantasy_name += Item.get_random_consonant(consonant_list)
            fantasy_name += Item.get_random_vowel(vowel_list)
            i += 1

        if random.randint(0, 1) == 1:
            fantasy_name += Item.get_random_consonant(consonant_list)

        return str.capitalize(fantasy_name)


    @staticmethod
    def get_skew_multiplier(percent=stat_skew_percent):
        return 1 + (random.uniform(-percent, percent) / 100)

    @staticmethod
    def get_attribute_determiner_value(rng):
        return random.uniform(0, rng)

    @staticmethod
    def test_item_balance(item_classification, item_type=None, sample_size=1000):
        # Returns comparisons of the average stats of items for balance purposes
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
        # we made a list of rng items, lets sort and compare this info

        separated_items = {}
        # separated_items is a dict with keys as the item_type string and values that are lists which include all items of that item type
        if item_type:
            separated_items = {item_type: item_list}
        else:
            for item_type in item_type_list:
                separated_items[item_type] = []
                for item in item_list:
                    if item.item_stats['item_type'] == item_type:
                        separated_items[item_type].append(item)

        all_item_averages = {}
        # all_item_averages is a dict with keys being the item type and values being another dict with keys being stat names and values being the average value for that stat
        for item_type in separated_items:
            # Loop through each item type
            print('Getting average stats for ' + item_type)
            item_stat_averages = {}
            num_of_items = 0

            for item in separated_items[item_type]:
                # Loop through each item of the item type
                item_stats = item.item_stats

                for stat in item_stats:
                    # Loop through each item stat in the item
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
    weapon_types = ('sword', 'axe', 'mace', 'spear', 'halberd', 'rapier', 'greatsword', 'dagger', 'caestus', 'bow', 'glaive', 'katana', 'nodachi', 'wand', 'wizard staff', 'quarterstaff', 'warhammer')
    japanese_weapons = ('katana', 'nodachi')

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

    def __str__(self):
        weapon_stat_string = 'Level ' + str(int(self.item_stats['rarity'] * 10)) + ' -- ' + self.name + '\n'
        for dmg_type in self.useful_dmg_values:
            weapon_stat_string += dmg_type + ' -- ' + str(self.useful_dmg_values[dmg_type]) + '\n'
        return weapon_stat_string

    def __repr__(self):
        weapon_stat_string = self.__str__()
        '| Dmg per AP value -- ' + str(round(self.item_stats['total_dmg'] / self.item_stats['ap'], 1) + ' ' + weapon_stat_string)
        return weapon_stat_string

    @staticmethod
    def get_weapon_values(rarity=None, weapon_type=None):
        if not rarity:
            rarity = random.uniform(1, 10)
        if not weapon_type:
            weapon_type = Weapon.weapon_types[random.randint(0, len(Weapon.weapon_types) - 1)]

        ap_scalar = 0.15
        rarity_scaling_exponential = rarity**2
        ap_scaling_exponential = rarity**1

        if weapon_type == 'sword':
            weapon_stats = {
                                    'ap': 45 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 0.8 * Item.get_skew_multiplier(20),
                                    'weight': 3 * Item.get_skew_multiplier(20),
                                    'ammo_type': None,
                                    'one_handed': True,
                                    'throw_dmg_multiplier': 0.5,
                                    'blunt_dmg': 5 * rarity_scaling_exponential - 70,
                                    'slash_dmg': 20 * rarity_scaling_exponential + 3,
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
                                    'ammo_type': None,
                                    'one_handed': True,
                                    'throw_dmg_multiplier': 1.1,
                                    'blunt_dmg': 4 * rarity_scaling_exponential - 20,
                                    'slash_dmg': 20 * rarity_scaling_exponential + 3,
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
                                    'ammo_type': None,
                                    'one_handed': True,
                                    'throw_dmg_multiplier': 0.5,
                                    'blunt_dmg': 20 * rarity_scaling_exponential + 3,
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
                                    'ammo_type': None,
                                    'one_handed': False,
                                    'throw_dmg_multiplier': 2,
                                    'blunt_dmg': 0,
                                    'slash_dmg': 5 * rarity_scaling_exponential - 80,
                                    'puncture_dmg': 20 * rarity_scaling_exponential + 3,
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
                                    'ammo_type': None,
                                    'one_handed': False,
                                    'throw_dmg_multiplier': 0.2,
                                    'blunt_dmg': 5 * rarity_scaling_exponential - 100,
                                    'slash_dmg': 17 * rarity_scaling_exponential + 5,
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
                                    'ammo_type': None,
                                    'one_handed': True,
                                    'throw_dmg_multiplier': 0.5,
                                    'blunt_dmg': 5 * rarity_scaling_exponential - 200,
                                    'slash_dmg': 4 * rarity_scaling_exponential + 1,
                                    'puncture_dmg': 8 * rarity_scaling_exponential + 2,
                                    'electric_dmg': 3 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'fire_dmg': 3 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'magic_dmg': 3 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'true_dmg': 5 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(4))

            }
        elif weapon_type == 'greatsword':
            weapon_stats = {
                                    'ap': 100 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 1.65 * Item.get_skew_multiplier(10),
                                    'weight': 5 * Item.get_skew_multiplier(10),
                                    'ammo_type': None,
                                    'one_handed': False,
                                    'throw_dmg_multiplier': 0.8,
                                    'blunt_dmg': 15 * rarity_scaling_exponential - 20,
                                    'slash_dmg': 40 * rarity_scaling_exponential + 5,
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
                                    'ammo_type': None,
                                    'one_handed': True,
                                    'throw_dmg_multiplier': 1.2,
                                    'blunt_dmg': 1 * rarity_scaling_exponential - 100,
                                    'slash_dmg': 6 * rarity_scaling_exponential + 1,
                                    'puncture_dmg': 5 * rarity_scaling_exponential + 1,
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
                                    'ammo_type': None,
                                    'one_handed': False,
                                    'throw_dmg_multiplier': 0.1,
                                    'blunt_dmg': 4 * rarity_scaling_exponential + 1,
                                    'slash_dmg': 2 * rarity_scaling_exponential - 100,
                                    'puncture_dmg': 2 * rarity_scaling_exponential - 50,
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
                                    'ammo_type': 'arrow',
                                    'one_handed': False,
                                    'throw_dmg_multiplier': 0.1,
                                    'blunt_dmg': 2 * rarity_scaling_exponential - 150,
                                    'slash_dmg': 5 * rarity_scaling_exponential - 100,
                                    'puncture_dmg': 15 * rarity_scaling_exponential + 3,
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
                                    'ammo_type': None,
                                    'one_handed': False,
                                    'throw_dmg_multiplier': 0.9,
                                    'blunt_dmg': 5 * rarity_scaling_exponential - 100,
                                    'slash_dmg': 20 * rarity_scaling_exponential + 4,
                                    'puncture_dmg': 5 * rarity_scaling_exponential + 1,
                                    'electric_dmg': 15 * rarity_scaling_exponential - (rarity_scaling_exponential * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'fire_dmg': 13 * rarity_scaling_exponential - (rarity_scaling_exponential * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'magic_dmg': 13 * rarity_scaling_exponential - (rarity_scaling_exponential * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'true_dmg': 13 * rarity_scaling_exponential - (rarity_scaling_exponential * 150 * Weapon.get_attribute_determiner_value(16))
            }
        elif weapon_type == 'katana':
            weapon_stats = {
                                    'ap': 30 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 0.7 * Item.get_skew_multiplier(20),
                                    'weight': 3 * Item.get_skew_multiplier(20),
                                    'ammo_type': None,
                                    'one_handed': True,
                                    'throw_dmg_multiplier': 0.7,
                                    'blunt_dmg': 3 * rarity_scaling_exponential - 70,
                                    'slash_dmg': 13 * rarity_scaling_exponential + 3,
                                    'puncture_dmg': 5 * rarity_scaling_exponential - 65,
                                    'electric_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'fire_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'magic_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'true_dmg': 10 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(8))
            }
        elif weapon_type == 'nodachi':
            weapon_stats = {
                                    'ap': 80 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 0.9 * Item.get_skew_multiplier(10),
                                    'weight': 4 * Item.get_skew_multiplier(10),
                                    'ammo_type': None,
                                    'one_handed': False,
                                    'throw_dmg_multiplier': 0.8,
                                    'blunt_dmg': 3 * rarity_scaling_exponential - 20,
                                    'slash_dmg': 40 * rarity_scaling_exponential + 5,
                                    'puncture_dmg': 10 * rarity_scaling_exponential - 50,
                                    'electric_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'fire_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'magic_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'true_dmg': 10 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(12))
            }
        elif weapon_type == 'wand':
            weapon_stats = {
                                    'ap': 20 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 20 * Item.get_skew_multiplier(10),
                                    'weight': 1 * Item.get_skew_multiplier(10),
                                    'ammo_type': 'mana',
                                    'one_handed': True,
                                    'throw_dmg_multiplier': 0.1,
                                    'blunt_dmg': 0,
                                    'slash_dmg': 0,
                                    'puncture_dmg': 0,
                                    'electric_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'fire_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'magic_dmg': 5 * rarity_scaling_exponential + 3,
                                    'true_dmg': 10 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(12))
            }
        elif weapon_type == 'wizard staff':
            weapon_stats = {
                                    'ap': 40 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 30 * Item.get_skew_multiplier(10),
                                    'weight': 10 * Item.get_skew_multiplier(10),
                                    'ammo_type': 'mana',
                                    'one_handed': False,
                                    'throw_dmg_multiplier': 0.1,
                                    'blunt_dmg': 0,
                                    'slash_dmg': 0,
                                    'puncture_dmg': 0,
                                    'electric_dmg': 20 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'fire_dmg': 20 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'magic_dmg': 10 * rarity_scaling_exponential + 5,
                                    'true_dmg': 10 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(12))
            }
        elif weapon_type == 'quarterstaff':
            weapon_stats = {
                                    'ap': 20 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 2 * Item.get_skew_multiplier(10),
                                    'weight': 7 * Item.get_skew_multiplier(10),
                                    'ammo_type': 'mana',
                                    'one_handed': False,
                                    'throw_dmg_multiplier': 0.1,
                                    'blunt_dmg': 8 * rarity_scaling_exponential + 3,
                                    'slash_dmg': 1 * rarity_scaling_exponential - 20,
                                    'puncture_dmg': 3 * rarity_scaling_exponential - 20,
                                    'electric_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'fire_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'magic_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(8)),
                                    'true_dmg': 10 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(12))
            }
        elif weapon_type == 'warhammer':
            weapon_stats = {
                                    'ap': 100 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 1.5 * Item.get_skew_multiplier(20),
                                    'weight': 10 * Item.get_skew_multiplier(10),
                                    'ammo_type': None,
                                    'one_handed': False,
                                    'throw_dmg_multiplier': 1.2,
                                    'blunt_dmg': 45 * rarity_scaling_exponential + 7,
                                    'slash_dmg': 10 * rarity_scaling_exponential - 50,
                                    'puncture_dmg': 10 * rarity_scaling_exponential - 50,
                                    'electric_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'fire_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'magic_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'true_dmg': 10 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(12))
            }
        # Below are unlisted weapon types for use with special enemies/bosses
        elif weapon_type == 'goop':
            weapon_stats = {
                                    'ap': 30 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 2.5 * Item.get_skew_multiplier(10),
                                    'weight': 1 * Item.get_skew_multiplier(10),
                                    'ammo_type': None,
                                    'one_handed': False,
                                    'throw_dmg_multiplier': 2,
                                    'blunt_dmg': 3 * rarity_scaling_exponential + 2,
                                    'slash_dmg': 3 * rarity_scaling_exponential - 20,
                                    'puncture_dmg': 10 * rarity_scaling_exponential - 50,
                                    'electric_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'fire_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(8)),
                                    'magic_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'true_dmg': 10 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(12))
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
        # Returns a randomized weapon with the option to specify its rarity and type

        if not rarity:
            # rarity = random.uniform(1, 10)
            rarity = Item.get_item_rarity()
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
                        adjectives = ('piercing', 'puncturing', 'poking', 'impaling', 'stabbing', 'skewering', 'hole-making', 'pointy', 'spiky')

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
            if weapon_type in Weapon.japanese_weapons or random.uniform(0, 1) > 0.8:
                fantasy_name = Item.get_fantasy_name(random.randint(2, 4), Item.japanese_letters, Item.japanese_letters)
            else:
                fantasy_name = Item.get_fantasy_name(random.randint(1, 3))
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
    armour_materials = ('cloth', 'leather', 'wooden', 'chainmail', 'bronze', 'iron', 'steel')

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
        weapon_stat_string = self.__str__()
        return 'Armour Value -- ' + str(self.item_stats['total_value']) + ' | ' + weapon_stat_string

    def __str__(self):
        armour_stat_string = ''
        for resistance_type in self.useful_resistances:
            armour_stat_string += resistance_type + ' -- ' + self.useful_resistances[resistance_type] + '\n'
        # armour_stat_string += '\n'
        for multiplier_type in self.useful_multipliers:
            armour_stat_string += multiplier_type + ' -- ' + self.useful_multipliers[multiplier_type] + '\n'

        return 'Level ' + str(int(self.item_stats['rarity'] * 10)) + ' -- ' + self.name + '\n' + armour_stat_string

    @staticmethod
    def get_armour_values(rarity=None, armour_type=None, armour_material=None):
        if not rarity:
            rarity = Item.get_item_rarity()
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
                            'blunt_dmg_resistance': rarity_scaling_exponential * 3 + 5,
                            'slash_dmg_resistance': rarity_scaling_exponential * 1 - 3,
                            'puncture_dmg_resistance': rarity_scaling_exponential * 1 - 3,
                            'electric_dmg_resistance': rarity_scaling_exponential * 5 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(4)),
                            'fire_dmg_resistance': 0,
                            'magic_dmg_resistance': rarity_scaling_exponential * 5 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(2)),
                            'general_dmg_multiplier': 1,
                            'blunt_dmg_multiplier': 1,
                            'slash_dmg_multiplier': 1,
                            'puncture_dmg_multiplier': 1,
                            'electric_dmg_multiplier': 3 - (Item.get_attribute_determiner_value(30)),
                            'fire_dmg_multiplier': 3 - (Item.get_attribute_determiner_value(10)),
                            'magic_dmg_multiplier': 3 - (Item.get_attribute_determiner_value(20))
            }
        elif armour_material == 'leather':
            armour_stats = {
                            'weight': weight_modifier * 12,
                            'general_resistance': rarity_scaling_exponential * 0.3 - 100,
                            'blunt_dmg_resistance': rarity_scaling_exponential * 5 + 7,
                            'slash_dmg_resistance': rarity_scaling_exponential * 1.5 - 3,
                            'puncture_dmg_resistance': rarity_scaling_exponential * 1.3 - 3,
                            'electric_dmg_resistance': rarity_scaling_exponential * 5 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(4)),
                            'fire_dmg_resistance': 0,
                            'magic_dmg_resistance': rarity_scaling_exponential * 5 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(2)),
                            'general_dmg_multiplier': 1,
                            'blunt_dmg_multiplier': 1,
                            'slash_dmg_multiplier': 1,
                            'puncture_dmg_multiplier': 1,
                            'electric_dmg_multiplier': 3 - (Item.get_attribute_determiner_value(30)),
                            'fire_dmg_multiplier': 3 - (Item.get_attribute_determiner_value(12)),
                            'magic_dmg_multiplier': 3 - (Item.get_attribute_determiner_value(20))
            }
        elif armour_material == 'wooden':
            armour_stats = {
                            'weight': weight_modifier * 15,
                            'general_resistance': rarity_scaling_exponential * 0.3 - 100,
                            'blunt_dmg_resistance': rarity_scaling_exponential * 2 - 3,
                            'slash_dmg_resistance': rarity_scaling_exponential * 5 + 5,
                            'puncture_dmg_resistance': rarity_scaling_exponential * 3 - 3,
                            'electric_dmg_resistance': rarity_scaling_exponential * 5 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(4)),
                            'fire_dmg_resistance': 0,
                            'magic_dmg_resistance': rarity_scaling_exponential * 5 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(2)),
                            'general_dmg_multiplier': 1,
                            'blunt_dmg_multiplier': 1,
                            'slash_dmg_multiplier': 1,
                            'puncture_dmg_multiplier': 1,
                            'electric_dmg_multiplier': 3 - (Item.get_attribute_determiner_value(30)),
                            'fire_dmg_multiplier': 3 - (Item.get_attribute_determiner_value(8)),
                            'magic_dmg_multiplier': 3 - (Item.get_attribute_determiner_value(20))
            }
        elif armour_material == 'chainmail':
            armour_stats = {
                            'weight': weight_modifier * 20,
                            'general_resistance': rarity_scaling_exponential * 0.5 - 100,
                            'blunt_dmg_resistance': rarity_scaling_exponential * 2,
                            'slash_dmg_resistance': rarity_scaling_exponential * 5 + 10,
                            'puncture_dmg_resistance': rarity_scaling_exponential * 1 - 3,
                            'electric_dmg_resistance': rarity_scaling_exponential * 2 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(4)),
                            'fire_dmg_resistance': rarity_scaling_exponential * 2 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(4)),
                            'magic_dmg_resistance': rarity_scaling_exponential * 2 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(4)),
                            'general_dmg_multiplier': 1,
                            'blunt_dmg_multiplier': 1,
                            'slash_dmg_multiplier': 1,
                            'puncture_dmg_multiplier': 1,
                            'electric_dmg_multiplier':  3 - (Item.get_attribute_determiner_value(10)),
                            'fire_dmg_multiplier':  3 - (Item.get_attribute_determiner_value(20)),
                            'magic_dmg_multiplier':  3 - (Item.get_attribute_determiner_value(20))
            }
        elif armour_material == 'bronze':
            armour_stats = {
                            'weight': weight_modifier * 30,
                            'general_resistance': rarity_scaling_exponential * 0.5 - 100,
                            'blunt_dmg_resistance': rarity_scaling_exponential * 1 - 3,
                            'slash_dmg_resistance': rarity_scaling_exponential * 10 + 10,
                            'puncture_dmg_resistance': rarity_scaling_exponential * 5 + 3,
                            'electric_dmg_resistance': 0,
                            'fire_dmg_resistance': rarity_scaling_exponential * 2 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(4)),
                            'magic_dmg_resistance': 1,
                            'general_dmg_multiplier': 1,
                            'blunt_dmg_multiplier': 1,
                            'slash_dmg_multiplier': 1,
                            'puncture_dmg_multiplier': 1,
                            'electric_dmg_multiplier':  3 - (Item.get_attribute_determiner_value(5)),
                            'fire_dmg_multiplier':  3 - (Item.get_attribute_determiner_value(30)),
                            'magic_dmg_multiplier':  3 - (Item.get_attribute_determiner_value(10))
            }
        elif armour_material == 'iron':
            armour_stats = {
                            'weight': weight_modifier * 40,
                            'general_resistance': rarity_scaling_exponential * 0.5 - 100,
                            'blunt_dmg_resistance': rarity_scaling_exponential * 2 - 3,
                            'slash_dmg_resistance': rarity_scaling_exponential * 13 + 10,
                            'puncture_dmg_resistance': rarity_scaling_exponential * 7 + 4,
                            'electric_dmg_resistance': 0,
                            'fire_dmg_resistance': rarity_scaling_exponential * 2 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(3)),
                            'magic_dmg_resistance': 1,
                            'general_dmg_multiplier': 1,
                            'blunt_dmg_multiplier': 1,
                            'slash_dmg_multiplier': 1,
                            'puncture_dmg_multiplier': 1,
                            'electric_dmg_multiplier':  3 - (Item.get_attribute_determiner_value(4)),
                            'fire_dmg_multiplier':  3 - (Item.get_attribute_determiner_value(30)),
                            'magic_dmg_multiplier':  3 - (Item.get_attribute_determiner_value(10))
            }
        elif armour_material == 'steel':
            armour_stats = {
                            'weight': weight_modifier * 50,
                            'general_resistance': rarity_scaling_exponential * 0.5 - 100,
                            'blunt_dmg_resistance': rarity_scaling_exponential * 3 - 3,
                            'slash_dmg_resistance': rarity_scaling_exponential * 15 + 10,
                            'puncture_dmg_resistance': rarity_scaling_exponential * 10 + 5,
                            'electric_dmg_resistance': 0,
                            'fire_dmg_resistance': rarity_scaling_exponential * 2 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(3)),
                            'magic_dmg_resistance': 1,
                            'general_dmg_multiplier': 1,
                            'blunt_dmg_multiplier': 1,
                            'slash_dmg_multiplier': 1,
                            'puncture_dmg_multiplier': 1,
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
        armour_stats['total_protection'] = total_protection
        armour_stats['rarity'] = rarity
        armour_stats['item_type'] = armour_material
        armour_stats['weight'] = round(armour_stats['weight'], 1)
        armour_stats['weight_modifier'] = weight_modifier

        return armour_stats

    @classmethod
    def get_random_armour(cls, rarity=None, armour_type=None, armour_material=None):
        if not rarity:
            rarity = Item.get_item_rarity()
        if not armour_type:
            armour_type = Armour.armour_types[random.randint(0, len(Armour.armour_types) - 1)]
        if not armour_material:
            armour_material = Armour.armour_materials[random.randint(0, len(Armour.armour_materials) - 1)]

        armour_stats = Armour.get_armour_values(rarity, armour_type, armour_material)
        armour_name = armour_material + ' ' + armour_type
        armour_stats['ap'] = 10
        armour_stats['armour_type'] = armour_type
        armour_stats['armour_material'] = armour_material
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
                        adjectives = ['impenetrable', 'thick', 'deflecting', 'puncture-resistant', 'thicc']

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
        print((armour_stats['total_value'] / armour_stats['weight_modifier']) / rarity**1.3)
        if (armour_stats['total_value'] / armour_stats['weight_modifier']) / rarity**1.3 > 21 and rarity > 2.5:
            if random.uniform(0, 1) > 0.8:
                fantasy_name = Item.get_fantasy_name(random.randint(1, 3), Item.japanese_letters, Item.japanese_letters)
            else:
                fantasy_name = Item.get_fantasy_name(random.randint(1, 3))
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
                             ', originating from the deserts of ' + fantasy_name,
                             ]
            armour_name += armour_titles[random.randint(0, len(armour_titles) - 1)]

        return cls(armour_name, armour_stats)

    @staticmethod
    def get_armour_set(rarity=None, armour_material=None, armour_material_list=None, consistency=None):
        if not rarity:
            rarity = Item.get_item_rarity()
        if not armour_material:
            armour_material = Armour.armour_materials[random.randint(0, len(Armour.armour_materials) - 1)]
        if not armour_material_list:
            armour_material_list = list(Armour.armour_materials)
        if not consistency:
            consistency = 1
        if type(armour_material_list) != list:
            armour_material_list = list(armour_material_list)
        armour_material_list.append('none')

        armour_set = []
        for armour_type in Armour.armour_types:
            rarity *= Item.get_skew_multiplier(10)
            if random.uniform(0, 1) > consistency:
                inconsistent_armour_material = armour_material_list[random.randint(0, len(armour_material_list) - 1)]
                if inconsistent_armour_material == 'none':
                    pass
                else:
                    armour_set.append(Armour.get_random_armour(rarity, armour_type, inconsistent_armour_material))
            else:
                armour_set.append(Armour.get_random_armour(rarity, armour_type, armour_material))

        return armour_set
