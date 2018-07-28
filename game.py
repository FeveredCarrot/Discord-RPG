import math
import random
import logging

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

class GameObject:
    stat_skew_percent = 10

    vowels = ('a', 'e', 'i', 'o', 'u')

    consonants = (
        'w', 'r', 't', 'p', 's', 'd', 'f', 'g', 'h',
        'j', 'k', 'l', 'z', 'c', 'v', 'b', 'n', 'm', '-'
    )

    japanese_letters = (
        'a', 'i', 'u', 'e', 'o', 'ya', 'yu', 'yo', 'n',
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
        'pa', 'pi', 'pu', 'pe', 'po', 'pya', 'pyu', 'pyo'
    )

    def __init__(self, position=None, adjectives=['shiny']):
        self.position = position
        self.adjectives = adjectives

    @staticmethod
    def get_random_consonant(consonant_list=None):
        """returns a random consonant"""
        if not consonant_list:
            consonant_list = GameObject.consonants
        return consonant_list[random.randint(0, len(consonant_list) - 1)]

    @staticmethod
    def get_random_vowel(vowel_list=None):
        """returns a random vowel"""
        if not vowel_list:
            vowel_list = GameObject.consonants
        return vowel_list[random.randint(0, len(vowel_list) - 1)]

    @staticmethod
    def get_fantasy_name(name_length=None, vowel_list=None, consonant_list=None):
        """Returns a name using a combination of vowels and consonants"""
        if not name_length:
            name_length = 2
        if not vowel_list:
            vowel_list = GameObject.vowels
        if not consonant_list:
            consonant_list = GameObject.consonants

        if random.randint(0, 1) == 1:
            fantasy_name = GameObject.get_random_consonant(consonant_list)
            fantasy_name += GameObject.get_random_vowel(vowel_list)
        else:
            fantasy_name = GameObject.get_random_vowel(vowel_list)

        i = 0
        while i < name_length - 1:
            fantasy_name += GameObject.get_random_consonant(consonant_list)
            fantasy_name += GameObject.get_random_vowel(vowel_list)
            i += 1

        if random.randint(0, 1) == 1:
            fantasy_name += GameObject.get_random_consonant(consonant_list)

        return str.capitalize(fantasy_name)

    @staticmethod
    def get_skew_multiplier(percent=stat_skew_percent):
        """Gets a multiplier to skew item stats"""
        return 1 + (random.uniform(-percent, percent) / 100)

    @staticmethod
    def zero_to_range(rng):
        """Gives a float from zero to the argument"""
        return random.uniform(0, rng)

    @staticmethod
    def rarity_sort_key(item):
        return item.item_stats['rarity']

    @staticmethod
    def value_sort_key(item):
        return item.total_value

    @staticmethod
    def get_level():
        """Returns a rarity value from 0.1 to 10 based on weighted chance"""
        random_number = random.uniform(0, 10)
        return 4*(0.1919 * random_number - 0.608)**3 + 1


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def magnitude(self):
        return math.sqrt(abs(self.x**2) + abs(self.y**2))

    def __str__(self):
        return str(self.to_list())

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return [self.x, self.y]

    def __add__(self, other):
        if type(other) == Vector2:
            return Vector2(
                self.x + other.x,
                self.y + other.y
            )
        elif type(other) == list:
            return Vector2(
                self.x + other[0],
                self.y + other[1]
            )
        elif type(GameObject):
            return Vector2(
                self.x + other.position.x,
                self.y + other.position.y
            )

    def __sub__(self, other):
        if type(other) == Vector2:
            return Vector2(
                self.x - other.x,
                self.y - other.y
            )
        elif type(other) == list:
            return Vector2(
                self.x - other[0],
                self.y - other[1]
            )
        elif type(GameObject):
            return Vector2(
                self.x - other.position.x,
                self.y - other.position.y
            )

    def __mul__(self, other):
        if type(other) == Vector2:
            return Vector2(
                self.x * other.x,
                self.y - other.y
            )
        elif type(other) == list:
            return Vector2(
                self.x * other[0],
                self.y * other[1]
            )
        elif type(GameObject):
            return Vector2(
                self.x * other.position.x,
                self.y * other.position.y
            )

    def __truediv__(self, other):
        if type(other) == Vector2:
            return Vector2(
                self.x / other.x,
                self.y / other.y
            )
        elif type(other) == list:
            return Vector2(
                self.x / other[0],
                self.y / other[1]
            )
        elif type(GameObject):
            return Vector2(
                self.x / other.position.x,
                self.y / other.position.y
            )

