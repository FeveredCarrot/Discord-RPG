import logging
import random

logging.basicConfig(level=logging.INFO)


class Item:

    stat_skew_percent = 0
    boring_adjectives = ['boring', 'uninteresting', 'unworthy', 'absolutely awful', 'tasteless', 'peasant\'s', 'poorly crafted', 'unfit']
    vowels = ['a', 'e', 'i', 'o', 'u']
    consonants = ['w', 'r', 't', 'p', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'c', 'v', 'b', 'n', 'm']

    def __init__(self, name, ap, rarity, weight):
        self.name = name
        self.ap = ap
        self.rarity = rarity
        self.weight = weight
        self.value = rarity * 50

    def __repr__(self):
        return self.name

    @staticmethod
    def get_random_consonant():
        return Item.consonants[random.randint(0, len(Item.consonants) - 1)]

    @staticmethod
    def get_random_vowel():
        return Item.vowels[random.randint(0, len(Item.vowels) - 1)]

    @staticmethod
    def get_fantasy_name(name_length):

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
        return 1 + (random.uniform(-percent, percent) / 100)

    @staticmethod
    def get_attribute_determiner_value(rng):
        return random.uniform(0, rng)


class Weapon(Item):

    weapon_types = ['sword', 'axe', 'mace', 'spear', 'halberd', 'rapier', 'greatsword', 'dagger', 'caestus', 'bow', 'glaive']

    def __init__(self, name, ap, rarity, weight, weapon_type, weapon_range, blunt_dmg, slash_dmg, puncture_dmg, electric_dmg, fire_dmg, magic_dmg, true_dmg):
        super().__init__(name, ap, rarity, weight)

        self.weapon_type = weapon_type
        self.weapon_range = weapon_range
        self.blunt_dmg = blunt_dmg
        self.slash_dmg = slash_dmg
        self.puncture_dmg = puncture_dmg
        self.electric_dmg = electric_dmg
        self.fire_dmg = fire_dmg
        self.magic_dmg = magic_dmg
        self.true_dmg = true_dmg
        self.total_dmg = blunt_dmg + slash_dmg + puncture_dmg + electric_dmg + fire_dmg + magic_dmg + true_dmg
        self.value = self.total_dmg * rarity




    # @classmethod
    # def create_weapon(cls, name, ap, rarity, weight, blunt_dmg, slash_dmg, puncture_dmg, electric_dmg, fire_dmg, magic_dmg, true_dmg):
    #     return cls(name, ap, rarity, weight, blunt_dmg, slash_dmg, puncture_dmg, electric_dmg, fire_dmg, magic_dmg, true_dmg)

    @classmethod
    def get_random_weapon(cls, rarity=random.randint(1, 10), weapon_type=None):
        if not weapon_type:
            weapon_type = Weapon.weapon_types[random.randint(0, len(Weapon.weapon_types) - 1)]
            # ('weapon type is ' + weapon_type)

        weapon_name = weapon_type
        ap_scalar = 0.15
        rarity_scaling_exponential = pow(rarity, 2)
        ap_scaling_exponential = pow(rarity, 1)

        if weapon_type == 'sword':
            weapon_type_modifiers = {
                                    'ap': 40 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 0.8 * Item.get_skew_multiplier(20),
                                    'weight': 3 * Item.get_skew_multiplier(20),
                                    'blunt_dmg': 5 * rarity_scaling_exponential - 70,
                                    'slash_dmg': 20 * rarity_scaling_exponential,
                                    'puncture_dmg': 5 * rarity_scaling_exponential - 65,
                                    'electric_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'fire_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'magic_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'true_dmg': 10 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(8))
            }
        elif weapon_type == 'axe':
            weapon_type_modifiers = {
                                    'ap': 40 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 0.6 * Item.get_skew_multiplier(40),
                                    'weight': 3 * Item.get_skew_multiplier(20),
                                    'blunt_dmg': 5 * rarity_scaling_exponential - 20,
                                    'slash_dmg': 20 * rarity_scaling_exponential,
                                    'puncture_dmg': 5 * rarity_scaling_exponential - 15,
                                    'electric_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'fire_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'magic_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'true_dmg': 10 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(8))
            }
        elif weapon_type == 'mace':
            weapon_type_modifiers = {
                                    'ap': 40 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 0.7 * Item.get_skew_multiplier(20),
                                    'weight': 2.5 * Item.get_skew_multiplier(10),
                                    'blunt_dmg': 23 * rarity_scaling_exponential,
                                    'slash_dmg': 5 * rarity_scaling_exponential - 100,
                                    'puncture_dmg': 5 * rarity_scaling_exponential - 80,
                                    'electric_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'fire_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'magic_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'true_dmg': 10 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(12))
            }
        elif weapon_type == 'spear':
            weapon_type_modifiers = {
                                    'ap': 45 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 2.1 * Item.get_skew_multiplier(15),
                                    'weight': 3 * Item.get_skew_multiplier(20),
                                    'blunt_dmg': 0,
                                    'slash_dmg': 5 * rarity_scaling_exponential - 80,
                                    'puncture_dmg': 25 * rarity_scaling_exponential,
                                    'electric_dmg': 7 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'fire_dmg': 11 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'magic_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'true_dmg': 13 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(4))
            }
        elif weapon_type == 'halberd':
            weapon_type_modifiers = {
                                    'ap': 70 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 1.65 * Item.get_skew_multiplier(10),
                                    'weight': 5 * Item.get_skew_multiplier(20),
                                    'blunt_dmg': 5 * rarity_scaling_exponential - 100,
                                    'slash_dmg': 17 * rarity_scaling_exponential,
                                    'puncture_dmg': 17 * rarity_scaling_exponential,
                                    'electric_dmg': 15 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'fire_dmg': 13 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'magic_dmg': 13 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'true_dmg': 13 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(16))

            }
        elif weapon_type == 'rapier':
            weapon_type_modifiers = {
                                    'ap': 20 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 1.15 * Item.get_skew_multiplier(10),
                                    'weight': 2 * Item.get_skew_multiplier(10),
                                    'blunt_dmg': 5 * rarity_scaling_exponential - 200,
                                    'slash_dmg': 4 * rarity_scaling_exponential,
                                    'puncture_dmg': 8 * rarity_scaling_exponential,
                                    'electric_dmg': 3 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'fire_dmg': 3 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'magic_dmg': 3 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'true_dmg': 5 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(4))

            }
        elif weapon_type == 'greatsword':
            weapon_type_modifiers = {
                                    'ap': 80 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 1.65 * Item.get_skew_multiplier(10),
                                    'weight': 5 * Item.get_skew_multiplier(10),
                                    'blunt_dmg': 15 * rarity_scaling_exponential - 20,
                                    'slash_dmg': 40 * rarity_scaling_exponential,
                                    'puncture_dmg': 10 * rarity_scaling_exponential - 50,
                                    'electric_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'fire_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'magic_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'true_dmg': 10 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(12))

            }
        elif weapon_type == 'dagger':
            weapon_type_modifiers = {
                                    'ap': 7 * ap_scaling_exponential * ap_scalar * 2 + 1,
                                    'range': 0.385 * Item.get_skew_multiplier(70),
                                    'weight': 0.5 * Item.get_skew_multiplier(50),
                                    'blunt_dmg': 1 * rarity_scaling_exponential - 100,
                                    'slash_dmg': 4 * rarity_scaling_exponential,
                                    'puncture_dmg': 2 * rarity_scaling_exponential,
                                    'electric_dmg': 2 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'fire_dmg': 2 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'magic_dmg': 2 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'true_dmg': 10 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(4))

            }
        elif weapon_type == 'caestus':
            weapon_type_modifiers = {
                                    'ap': 4 * ap_scaling_exponential * ap_scalar * 2 + 1,
                                    'range': 0.1 * Item.get_skew_multiplier(10),
                                    'weight': 0.3 * Item.get_skew_multiplier(10),
                                    'blunt_dmg': 5 * rarity_scaling_exponential,
                                    'slash_dmg': 3 * rarity_scaling_exponential - 100,
                                    'puncture_dmg': 3 * rarity_scaling_exponential - 50,
                                    'electric_dmg': 5 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'fire_dmg': 5 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'magic_dmg': 5 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'true_dmg': 3 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(8))

            }
        elif weapon_type == 'bow':
            weapon_type_modifiers = {
                                    'ap': 40 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 140 * Item.get_skew_multiplier(20),
                                    'weight': 2 * Item.get_skew_multiplier(10),
                                    'blunt_dmg': 2 * rarity_scaling_exponential - 150,
                                    'slash_dmg': 5 * rarity_scaling_exponential - 100,
                                    'puncture_dmg': 20 * rarity_scaling_exponential,
                                    'electric_dmg': 5 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'fire_dmg': 10 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'magic_dmg': 5 * rarity_scaling_exponential - (rarity * 100 * Weapon.get_attribute_determiner_value(3)),
                                    'true_dmg': 5 * rarity_scaling_exponential - (rarity * 150 * Weapon.get_attribute_determiner_value(8))


            }
        elif weapon_type == 'glaive':
            weapon_type_modifiers = {
                                    'ap': 65 * ap_scaling_exponential * ap_scalar + 1,
                                    'range': 2.4 * Item.get_skew_multiplier(10),
                                    'weight': 5 * Item.get_skew_multiplier(10),
                                    'blunt_dmg': 5 * rarity_scaling_exponential - 100,
                                    'slash_dmg': 20 * rarity_scaling_exponential,
                                    'puncture_dmg': 5 * rarity_scaling_exponential,
                                    'electric_dmg': 15 * rarity_scaling_exponential - (rarity_scaling_exponential * 100 * Weapon.get_attribute_determiner_value(4)),
                                    'fire_dmg': 13 * rarity_scaling_exponential - (rarity_scaling_exponential * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'magic_dmg': 13 * rarity_scaling_exponential - (rarity_scaling_exponential * 100 * Weapon.get_attribute_determiner_value(2)),
                                    'true_dmg': 13 * rarity_scaling_exponential - (rarity_scaling_exponential * 150 * Weapon.get_attribute_determiner_value(16))


            }
        else:
            print('not a valid weapon type!')
            pass

        total_dmg = 0
        for dmg_type in weapon_type_modifiers:

            skew_multiplier = Weapon.get_skew_multiplier()

            if dmg_type is not 'range' and dmg_type is not 'weight':
                weapon_type_modifiers[dmg_type] = weapon_type_modifiers[dmg_type] * skew_multiplier
                weapon_type_modifiers[dmg_type] = int(weapon_type_modifiers[dmg_type])

            if weapon_type_modifiers[dmg_type] < 0:
                weapon_type_modifiers[dmg_type] = 0
            if dmg_type is not 'ap' and dmg_type is not 'range' and dmg_type is not 'weight':
                total_dmg += weapon_type_modifiers[dmg_type]

        weapon_type_modifiers['weight'] = round(weapon_type_modifiers['weight'], 1)
        weapon_type_modifiers['range'] = round(weapon_type_modifiers['range'], 2)

        dmg_per_ap = total_dmg / weapon_type_modifiers['ap']

        for dmg_type in weapon_type_modifiers:
            if weapon_type_modifiers[dmg_type] * (rarity / 2) / weapon_type_modifiers['ap'] > .5:
                adjectives = ['']
                if dmg_type == 'blunt_dmg':
                    adjectives = ['crushing', 'bone-breaking', 'head-squashing', 'bludgeoning', 'crippling', 'gut-wrenching', 'heavy']

                elif dmg_type == 'slash_dmg':
                    adjectives = ['slicing', 'slashing', 'bleeding', 'serrated', 'head-chopping', 'decapitating', 'cutting-edge', 'dismembering', 'sharp']

                elif dmg_type == 'puncture_dmg':
                    adjectives = ['piercing', 'puncturing', 'poking', 'impaling', 'stabbing', 'skewering', 'hole-making', 'pointy']

                elif dmg_type == 'electric_dmg':
                    adjectives = ['electrifying', 'shocking', 'heart-stopping', 'sparking', 'thunderous', 'jolting', 'zapping']

                elif dmg_type == 'fire_dmg':
                    adjectives = ['burning', 'fiery', 'blistering', 'scorching', 'searing', 'red-hot', 'flaming']

                elif dmg_type == 'magic_dmg':
                    adjectives = ['magical', 'enchanted', 'mystical', 'spellbound', 'spectral', 'otherworldly', 'encanted']

                elif dmg_type == 'true_dmg':
                    adjectives = ['armour-ignoring', 'disemboweling', 'murderous', 'intimidating', 'legendary', 'killer', 'precise']

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

        print('Dmg per AP value -- ' + str(round(total_dmg / weapon_type_modifiers['ap'], 2)) + ' | Level ' + str(round(rarity, 2)) + ' -- ' + weapon_name + ' -- ' + str(weapon_type_modifiers) + '\n')
        return cls(
            weapon_name,
            weapon_type_modifiers['ap'],
            rarity,
            weapon_type_modifiers['weight'],
            weapon_type,
            weapon_type_modifiers['range'],
            weapon_type_modifiers['blunt_dmg'],
            weapon_type_modifiers['slash_dmg'],
            weapon_type_modifiers['puncture_dmg'],
            weapon_type_modifiers['electric_dmg'],
            weapon_type_modifiers['fire_dmg'],
            weapon_type_modifiers['magic_dmg'],
            weapon_type_modifiers['true_dmg']
                   )


class Armour(Item):

    armour_types = ['helmet', 'chestpiece', 'arm guards', 'gloves', 'leggings']
    armour_materials = ['cloth', 'leather', 'chainmail', 'bronze', 'iron' 'steel']
    armour_materials = ['cloth', 'leather', 'chainmail']

    def __init__(self,
                 name,
                 ap,
                 rarity,
                 weight,
                 armour_type,
                 blunt_dmg_resistance,
                 slash_dmg_resistance,
                 puncture_dmg_resistance,
                 electric_dmg_resistance,
                 fire_dmg_resistance,
                 magic_dmg_resistance,
                 blunt_dmg_multiplier,
                 slash_dmg_multiplier,
                 puncture_dmg_multiplier,
                 electric_dmg_multiplier,
                 fire_dmg_multiplier,
                 magic_dmg_multiplier):

        super().__init__(name, ap, rarity, weight)
        self.name = name
        self.rarity = rarity
        self.weight = weight
        self.armour_type = armour_type
        self.blunt_dmg_resistance = blunt_dmg_resistance
        self.slash_dmg_resistance = slash_dmg_resistance
        self.puncture_dmg_resistance = puncture_dmg_resistance
        self.electric_dmg_resistance = electric_dmg_resistance
        self.fire_dmg_resistance = fire_dmg_resistance
        self.magic_dmg_resistance = magic_dmg_resistance
        self.blunt_dmg_multiplier = blunt_dmg_multiplier
        self.slash_dmg_multiplier = slash_dmg_multiplier
        self.puncture_dmg_multiplier = puncture_dmg_multiplier
        self.electric_dmg_multiplier = electric_dmg_multiplier
        self.fire_dmg_multiplier = fire_dmg_multiplier
        self.magic_dmg_multiplier = magic_dmg_multiplier

    @classmethod
    def get_random_armour(cls, rarity=random.randint(1, 10), armour_type=None, armour_material=None):

        if not armour_type:
            armour_type = Armour.armour_types[random.randint(0, len(Armour.armour_types) - 1)]
        if not armour_material:
            armour_material = Armour.armour_materials[random.randint(0, len(Armour.armour_materials) - 1)]

        armour_name = armour_material + ' ' + armour_type
        armour_values = {}
        armour_multipliers = {}
        weight_modifier = 0
        ap = 10
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
            armour_values = {
                            'weight': weight_modifier * 8,
                            'general_resistance': rarity_scaling_exponential * 0.5 - 100,
                            'blunt_dmg_resistance': rarity_scaling_exponential * 2,
                            'slash_dmg_resistance': rarity_scaling_exponential * 1 - 10,
                            'puncture_dmg_resistance': rarity_scaling_exponential * 1 - 10,
                            'electric_dmg_resistance': rarity_scaling_exponential * 5 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(4)),
                            'fire_dmg_resistance': 0,
                            'magic_dmg_resistance': rarity_scaling_exponential * 5 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(2)),

            }
            armour_multipliers = {
                                 'general_dmg_multiplier': 0,
                                 'blunt_dmg_multiplier': 0,
                                 'slash_dmg_multiplier': 0,
                                 'puncture_dmg_multiplier': 0,
                                 'electric_dmg_multiplier': rarity_scaling_exponential * 1 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(10)),
                                 'fire_dmg_multiplier': rarity_scaling_exponential * 2 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(2)),
                                 'magic_dmg_multiplier': rarity_scaling_exponential * 1 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(10))
            }
        elif armour_material == 'leather':
            armour_values = {
                            'weight': weight_modifier * 12,
                            'general_resistance': rarity_scaling_exponential * 0.3 - 100,
                            'blunt_dmg_resistance': rarity_scaling_exponential * 3,
                            'slash_dmg_resistance': rarity_scaling_exponential * 1.5 - 10,
                            'puncture_dmg_resistance': rarity_scaling_exponential * 1.3 - 10,
                            'electric_dmg_resistance': rarity_scaling_exponential * 5 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(4)),
                            'fire_dmg_resistance': 0,
                            'magic_dmg_resistance': rarity_scaling_exponential * 5 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(2)),

            }
            armour_multipliers = {
                                 'general_dmg_multiplier': 0,
                                 'blunt_dmg_multiplier': 0,
                                 'slash_dmg_multiplier': 0,
                                 'puncture_dmg_multiplier': 0,
                                 'electric_dmg_multiplier': rarity_scaling_exponential * 0.5 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(8)),
                                 'fire_dmg_multiplier': rarity_scaling_exponential * 1 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(4)),
                                 'magic_dmg_multiplier': rarity_scaling_exponential * 1 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(8))
            }
        elif armour_material == 'chainmail':
            armour_values = {
                            'weight': weight_modifier * 20,
                            'general_resistance': rarity_scaling_exponential * 0.5 - 100,
                            'blunt_dmg_resistance': rarity_scaling_exponential * 3,
                            'slash_dmg_resistance': rarity_scaling_exponential * 3 - 10,
                            'puncture_dmg_resistance': rarity_scaling_exponential * 1 - 10,
                            'electric_dmg_resistance': rarity_scaling_exponential * 2 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(4)),
                            'fire_dmg_resistance': rarity_scaling_exponential * 2 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(4)),
                            'magic_dmg_resistance': rarity_scaling_exponential * 2 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(4)),

            }
            armour_multipliers = {
                                 'general_dmg_multiplier': 0,
                                 'blunt_dmg_multiplier': 0,
                                 'slash_dmg_multiplier': 0,
                                 'puncture_dmg_multiplier': 0,
                                 'electric_dmg_multiplier':  0.5 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(3)),
                                 'fire_dmg_multiplier':  1 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(8)),
                                 'magic_dmg_multiplier':  1 - (rarity_scaling_exponential * 100 * Item.get_attribute_determiner_value(8))
            }
        else:
            print('Not a valid armour material!')
            pass

        total_protection = 0
        for protection_type in armour_values:

            armour_values[protection_type] = armour_values[protection_type] * weight_modifier
            skew_multiplier = Item.get_skew_multiplier()

            if protection_type is not 'ap_multiplier' and protection_type is not 'weight':
                armour_values[protection_type] = armour_values[protection_type] * skew_multiplier
                armour_values[protection_type] = int(armour_values[protection_type])

            if armour_values[protection_type] < 0:
                armour_values[protection_type] = 0
            if protection_type is not 'weight' and protection_type is not 'ap_multiplier' and protection_type is not 'weight':
                total_protection += armour_values[protection_type]

        total_multiplier = 0
        for multiplier in armour_multipliers:

            skew_multiplier = Item.get_skew_multiplier()
            armour_multipliers[multiplier] = armour_multipliers[multiplier] * skew_multiplier

            if armour_multipliers[multiplier] < 0:
                armour_multipliers[multiplier] = 0

            total_multiplier += armour_multipliers[multiplier]

        total_value = total_protection * (1 / (total_multiplier + 1))

        armour_values['weight'] = round(armour_values['weight'], 1)

        for protection_type in armour_values:
            if armour_values[protection_type] * (rarity / 2) > 5 and protection_type is not 'weight':
                adjectives = ['']
                if protection_type == 'blunt_dmg_resistance':
                    adjectives = ['hardy', 'cushioning', 'heavy', 'dent-resistant', 'shock-absorbing']

                elif protection_type == 'slash_dmg_resistance':
                    adjectives = ['hard', 'scratch-resistant', 'hardened', 'tempered']

                elif protection_type == 'puncture_dmg_resistance':
                    adjectives = ['impenetrable', 'thick', 'deflecting', 'puncture-resistant']

                elif protection_type == 'electric_dmg_resistance':
                    adjectives = ['grounded', 'rubbery', 'electron-absorbing', 'lightning-reflecting']

                elif protection_type == 'fire_dmg_resistance':
                    adjectives = ['heat-treated', 'unburnable', 'heat-absorbing', 'fire-resistant']

                elif protection_type == 'magic_dmg_resistance':
                    adjectives = ['blessed', 'encanted', 'magical', 'dark']

                armour_name = adjectives[random.randint(0, len(adjectives) - 1)] + ' ' + armour_name

        if (total_value / weight_modifier) < 10:
            armour_name = Item.boring_adjectives[random.randint(0, len(Item.boring_adjectives) - 1)] + ' ' + armour_name

        if (total_value / weight_modifier) / rarity > rarity_scaling_exponential * 4 / rarity and rarity > 2.5:
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

        print('Armour Value -- ' + str(total_value) + ' | Level ' + str(round(rarity, 2)) + ' -- ' + armour_name + ' -- ' + '\n\n' + str(armour_values) + '\n' + str(armour_multipliers) + '\n\n')
        return cls(armour_name,
                   ap,
                   rarity,
                   armour_values['weight'],
                   armour_type,
                   armour_values['blunt_dmg_resistance'],
                   armour_values['slash_dmg_resistance'],
                   armour_values['puncture_dmg_resistance'],
                   armour_values['electric_dmg_resistance'],
                   armour_values['fire_dmg_resistance'],
                   armour_values['magic_dmg_resistance'],
                   armour_multipliers['blunt_dmg_multiplier'],
                   armour_multipliers['slash_dmg_multiplier'],
                   armour_multipliers['puncture_dmg_multiplier'],
                   armour_multipliers['electric_dmg_multiplier'],
                   armour_multipliers['fire_dmg_multiplier'],
                   armour_multipliers['magic_dmg_multiplier'])


i = 1
while i <= 10:
    Weapon.get_random_weapon(i)
    i += 1

i = 1
while i <= 10:
    Armour.get_random_armour(i)
    i += 1
