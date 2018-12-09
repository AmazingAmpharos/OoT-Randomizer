# SOUNDS.PY
#
# I'd like to introduce you to my son, Sounds.py.
# A data-oriented module created to avoid cluttering (and entangling) other,
# more important modules with sound data.
#
# Tags
# To easily fetch related sounds by their properties. This seems generally
# better than the alternative of defining long lists by hand. You still can, of
# course. Categorizing sounds with more useful tags will require some work. Do
# this as needed.
#
# Sounds
# These are a collection of data structures relating to sounds. Already I'm sure
# you get the picture.
#
# Sound Pools
# These are just groups of sounds, to be referenced by sfx settings. Could
# potentially merit enumerating later on. ¯\_(ツ)_/¯
#
# Sound Hooks
# These are intended to gear themselves toward configurable settings, rather
# than to document every location where a particular sound is used. For example,
# suppose we want a setting to override all of Link's vocalizations. The sound
# hook would contain a bunch of addresses, whether they share the same default
# value or not.

from enum import Enum
from collections import namedtuple


class Tags(Enum):
    LOOPED = 0
    #IMMEDIATE
    #BRIEF


Sound = namedtuple('Sound', 'id      keyword            label                 tags')
class Sounds(Enum):
    NONE             = Sound(0x0000, 'none',            'None',               [])
    CUCCO_CLUCK      = Sound(0x2812, 'cluck',           'Cluck',              [])
    RUPEE            = Sound(0x4803, 'rupee',           'Rupee',              [])
    SOFT_BEEP        = Sound(0x4804, 'soft-beep',       'Soft Beep',          [])
    HEART_RECOVERY   = Sound(0x480B, 'recovery-heart',  'Recovery Heart',     [])
    TIMER            = Sound(0x481A, 'timer',           'Timer',              [])
    HP_LOW           = Sound(0x481B, 'low-health',      'Low Health',         [])
    NOTIFICATION     = Sound(0x4820, 'notification',    'Notification',       [])
    TAMBOURINE       = Sound(0x4842, 'tambourine',      'Tambourine',         [])
    CARROT_REFILL    = Sound(0x4845, 'carrot-refill',   'Carrot Refill',      [])
    ZELDA_GASP       = Sound(0x6879, 'zelda-gasp',      'Zelda - Gasp',       [])
    ZORA_KING        = Sound(0x687A, 'mweep',           'Mweep!',             [])
    ICE_SHATTER      = Sound(0x0875, 'shattering-ice',  'Shattering Ice',     [])
    EXPLOSION        = Sound(0x180E, 'explosion',       'Explosion',          [])
    CRATE_EXPLODE    = Sound(0x2839, 'exploding-crate', 'Exploding Crate',    [])
    GREAT_FAIRY      = Sound(0x6858, 'great-fairy',     'Great Fairy',        [])
    MOO              = Sound(0x28DF, 'moo',             'Moo',                [])
    BARK             = Sound(0x28D8, 'bark',            'Bark',               [])
    RIBBIT           = Sound(0x28B1, 'ribbit',          'Ribbit',             [])
    POT_SHATTER      = Sound(0x2887, 'shattering-pot',  'Shattering Pot',     [])
    CUCCO_CROW       = Sound(0x2813, 'cockadoodledoo',  'Cockadoodledoo',     [])
    EPONA            = Sound(0x2805, 'epona',           'Epona',              [])
    SKULLTULA        = Sound(0x39DA, 'skulltula',       'Skulltula',          [])
    REDEAD           = Sound(0x38E5, 'redead',          'Redead',             [])
    POE              = Sound(0x38EC, 'poe',             'Poe',                [])
    RUTO             = Sound(0x6863, 'ruto',            'Princess Ruto',      [])
    HOWL             = Sound(0x28AE, 'howl',            'Howl',               [])
    SCRUB_BUSINESS   = Sound(0x3882, 'business-scrub',  'Business Scrub',     [])
    GUAY             = Sound(0x38B6, 'guay',            'Guay',               [])
    NAVI_HELLO       = Sound(0x6844, 'navi-hello',      'Navi - Hello!',      [])
    NAVI_RANDOM      = Sound(0x6843, 'navi-random',     'Navi - Random',      [])
    NAVI_HEY         = Sound(0x685F, 'navi-hey',        'Navi - Hey!',        [])
    BOOTS_IRON       = Sound(0x080D, 'iron-boots',      'Iron Boots',         [])
    HAMMER           = Sound(0x180A, 'hammer',          'Hammer',             [])
    SWORD_BOUNCE     = Sound(0x181A, 'sword-bounce',    'Sword Bounce',       [])
    BOW              = Sound(0x1830, 'bow',             'Bow',                [])
    HORSE_GALLOP     = Sound(0x2804, 'gallop',          'Gallop',             [])
    DRAWBRIDGE       = Sound(0x280E, 'drawbridge',      'Drawbridge',         [])
    SWITCH           = Sound(0x2815, 'switch',          'Switch',             [])
    BOMB_BOUNCE      = Sound(0x282F, 'bomb-bounce',     'Bomb Bounce',        [])
    BONGO            = Sound(0x3950, 'bongo-bongo',     'Bongo Bongo',        [])
    BOOTS_HOVER      = Sound(0x08C9, 'hover-boots',     'Hover Boots',        [Tags.LOOPED])
    TWINROVA_BICKER  = Sound(0x39E7, 'twinrova-bicker', 'Twinrova - Bicker',  [Tags.LOOPED])


# Sound pools
standard   = [enum for enum in Sounds if Tags.LOOPED not in enum.value.tags]
looping    = [enum for enum in Sounds if Tags.LOOPED in enum.value.tags]


SoundHook = namedtuple('SoundHook', 'pool locations')
class SoundHooks(Enum):
    NAVI_OVERWORLD  = SoundHook(standard, [0xAE7EF2, 0xC26C7E])
    NAVI_ENEMY      = SoundHook(standard, [0xAE7EC6])
    HP_LOW          = SoundHook(standard, [0xADBA1A])
    BOOTS_HOVER     = SoundHook(standard, [0xBDBD8A])


def get_patch_dict():
    keys   = [enum.value.keyword for enum in Sounds]
    values = [enum.value.id for enum in Sounds]
    return dict(zip(keys, values))


def get_hook_pool(sound_hook):
    return sound_hook.value.pool


def get_setting_choices(sound_hook):
    pool     = sound_hook.value.pool
    keywords = [enum.value.keyword for enum in pool]
    labels   = [enum.value.label for enum in pool]
    choices  = dict(zip(keywords, labels))
    result   = {
        'default': 'Default',
        'random':  'Random Choice',
        **choices,
        }
    return result
