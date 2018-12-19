# SOUNDS.PY
#
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
    LOOPED    = 0
    QUIET     = 1
    IMMEDIATE = 2       # Delayed sounds are commonly undesirable
    BRIEF     = 3       # Punchy sounds, good for rapid fire
    NEW       = 4
    PAINFUL   = 5       # Eardrum-piercing sounds
    INC_NE    = 20      # Incompatible with NAVI_ENEMY? (Verify)
                        # I'm now thinking it has to do with a limit of concurrent sounds)


Sound = namedtuple('Sound',   'id      keyword                  label                        tags')
class Sounds(Enum):
    NONE               = Sound(0x0000, 'none',                  'None',                      [])
    CUCCO_CLUCK        = Sound(0x2812, 'cluck',                 'Cluck',                     [Tags.BRIEF])
    RUPEE              = Sound(0x4803, 'rupee',                 'Rupee',                     [Tags.PAINFUL])
    SOFT_BEEP          = Sound(0x4804, 'soft-beep',             'Soft Beep',                 [])
    HP_RECOVER         = Sound(0x480B, 'recover-health',        'Recover Health',            [])
    TIMER              = Sound(0x481A, 'timer',                 'Timer',                     [Tags.INC_NE])
    HP_LOW             = Sound(0x481B, 'low-health',            'Low Health',                [Tags.INC_NE])
    NOTIFICATION       = Sound(0x4820, 'notification',          'Notification',              [])
    TAMBOURINE         = Sound(0x4842, 'tambourine',            'Tambourine',                [Tags.QUIET])
    CARROT_REFILL      = Sound(0x4845, 'carrot-refill',         'Carrot Refill',             [])
    ZELDA_ADULT_GASP   = Sound(0x6879, 'adult-zelda-gasp',      'Adult Zelda Gasp',          [])
    ZORA_KING          = Sound(0x687A, 'mweep',                 'Mweep!',                    [Tags.BRIEF])
    ICE_SHATTER        = Sound(0x0875, 'shattering-ice',        'Shattering Ice',            [])
    EXPLOSION          = Sound(0x180E, 'explosion',             'Explosion',                 [])
    CRATE_EXPLODE      = Sound(0x2839, 'exploding-crate',       'Exploding Crate',           [])
    GREAT_FAIRY        = Sound(0x6858, 'great-fairy',           'Great Fairy',               [Tags.PAINFUL])
    MOO                = Sound(0x28DF, 'moo',                   'Moo',                       [])
    BARK               = Sound(0x28D8, 'bark',                  'Bark',                      [Tags.BRIEF])
    RIBBIT             = Sound(0x28B1, 'ribbit',                'Ribbit',                    [])
    POT_SHATTER        = Sound(0x2887, 'shattering-pot',        'Shattering Pot',            [])
    CUCCO_CROW         = Sound(0x2813, 'cockadoodledoo',        'Cockadoodledoo',            [])
    EPONA              = Sound(0x2805, 'epona',                 'Epona',                     [])
    SKULLTULA          = Sound(0x39DA, 'skulltula',             'Skulltula',                 [Tags.BRIEF])
    REDEAD_SCREAM      = Sound(0x38E5, 'redead-scream',         'Redead Scream',             [Tags.PAINFUL])
    POE                = Sound(0x38EC, 'poe',                   'Poe',                       [])
    DUSK_HOWL          = Sound(0x28AE, 'dusk-howl',             'Dusk Howl',                 [])
    SCRUB_BUSINESS     = Sound(0x3882, 'business-scrub',        'Business Scrub',            [])
    GUAY               = Sound(0x38B6, 'guay',                  'Guay',                      [Tags.BRIEF])
    NAVI_HELLO         = Sound(0x6844, 'navi-hello',            'Navi "Hello!"',             [])
    NAVI_RANDOM        = Sound(0x6843, 'navi-random',           'Navi Random',               [])
    NAVI_HEY           = Sound(0x685F, 'navi-hey',              'Navi "Hey!"',               [])
    BOOTS_IRON         = Sound(0x080D, 'iron-boots',            'Iron Boots',                [Tags.BRIEF, Tags.QUIET])
    HAMMER_BONK        = Sound(0x180A, 'hammer-bonk',           'Hammer Bonk',               [])
    SWORD_BONK         = Sound(0x181A, 'sword-bonk',            'Sword Bonk',                [])
    BOW_TWANG          = Sound(0x1830, 'bow-twang',             'Bow Twang',                 [])
    HORSE_TROT         = Sound(0x2804, 'horse-trot',            'Horse Trot',                [])
    DRAWBRIDGE_SET     = Sound(0x280E, 'drawbridge-set',        'Drawbridge Set',            [])
    SWITCH             = Sound(0x2815, 'switch',                'Switch',                    [])
    BOMB_BOUNCE        = Sound(0x282F, 'bomb-bounce',           'Bomb Bounce',               [Tags.QUIET])
    BONGO_LOW          = Sound(0x3950, 'bongo-bongo-low',       'Bongo Bongo Low',           [Tags.QUIET])
    # New (for the most part)
    ARMOS_GROAN        = Sound(0x3848, 'armos',                 'Armos',                     [])
    BOOTS_HOVER        = Sound(0x08C9, 'hover-boots',           'Hover Boots',               [Tags.LOOPED])
    BOTTLE_CORK        = Sound(0x286C, 'bottle-cork',           'Bottle Cork',               [Tags.IMMEDIATE, Tags.BRIEF, Tags.QUIET])
    BUBBLE_LOL         = Sound(0x38CA, 'bubble-laugh',          'Bubble Laugh',              [])
    BONGO_HIGH         = Sound(0x3951, 'bongo-bongo-high',      'Bongo Bongo High',          [])
    CARTOON_FALL       = Sound(0x28A0, 'cartoon-fall',          'Cartoon Fall',              [])
    CHANGE_ITEM        = Sound(0x0835, 'change-item',           'Change Item',               [Tags.IMMEDIATE, Tags.BRIEF])
    CHEST_OPEN         = Sound(0x2820, 'chest-open',            'Chest Open',                [])
    CHILD_CRINGE       = Sound(0x683A, 'child-cringe',          'Child Cringe',              [Tags.IMMEDIATE])
    CHILD_GASP         = Sound(0x6836, 'child-gasp',            'Child Gasp',                [])
    CHILD_HURT         = Sound(0x6825, 'child-hurt',            'Child Hurt',                [])
    CHILD_OWO          = Sound(0x6823, 'child-owo',             'Child owo',                 [])
    CHILD_PANT         = Sound(0x6829, 'child-pant',            'Child Pant',                [Tags.IMMEDIATE])
    CHILD_SCREAM       = Sound(0x6828, 'child-scream',          'Child Scream',              [Tags.IMMEDIATE])
    CURSED_SCREAM      = Sound(0x6867, 'cursed-scream',         'Cursed Scream',             [])
    CURSED_ATTACK      = Sound(0x6868, 'cursed-attack',         'Cursed Attack',             [Tags.IMMEDIATE])
    DEKU_BABA_CHATTER  = Sound(0x3860, 'deku-baba',             'Deku Baba',                 [])
    EPONA_CHILD        = Sound(0x2844, 'baby-epona',            'Baby Epona',                [])
    FANFARE_MED        = Sound(0x4831, 'medium-fanfare',        'Medium Fanfare',            [])
    FANFARE_SMALL      = Sound(0x4824, 'light-fanfare',         'Light Fanfare',             [])
    FIELD_SHRUB        = Sound(0x2877, 'field-shrub',           'Field Shrub',               [])
    FLARE_BOSS_LOL     = Sound(0x3981, 'flare-dancer-laugh',    'Flare Dancer Laugh',        [Tags.IMMEDIATE])
    FLARE_BOSS_STARTLE = Sound(0x398B, 'flare-dancer-startled', 'Flare Dancer Startled',     [])
    GANON_TENNIS       = Sound(0x39CA, 'ganondorf-teh',         'Ganondorf "Teh!"',          [])
    GOHMA_LARVA_CROAK  = Sound(0x395D, 'gohma-larva-croak',     'Gohma Larva Croak',         [])
    GOLD_SKULL_TOKEN   = Sound(0x4843, 'gold-skull-token',      'Gold Skull Token',          [])
    GORON_WAKE         = Sound(0x38FC, 'goron-wake',            'Goron Wake',                [])
    GUNSHOT            = Sound(0x4835, 'gunshot',               'Gunshot',                   [])
    IRON_KNUCKLE       = Sound(0x3929, 'iron-knuckle',          'Iron Knuckle',              [])
    MOBLIN_CLUB_GROUND = Sound(0x38EF, 'moblin-club-ground',    'Moblin Club Ground',        [])
    MOBLIN_CLUB_SWING  = Sound(0x39E1, 'moblin-club-swing',     'Moblin Club Swing',         [])
    PHANTOM_GANON_LOL  = Sound(0x38B0, 'phantom-ganon-laugh',   'Phantom Ganon Laugh',       [])
    PLANT_EXPLODE      = Sound(0x284E, 'plant-explode',         'Plant Explode',             [])
    REDEAD_MOAN        = Sound(0x38E4, 'redead-moan',           'Redead Moan',               [])
    RUPEE_SILVER       = Sound(0x28E8, 'silver-rupee',          'Silver Rupee',              [])
    RUTO_CHILD_CRASH   = Sound(0x6860, 'ruto-crash',            'Ruto Crash',                [])
    RUTO_CHILD_EXCITED = Sound(0x6861, 'ruto-excited',          'Ruto Excited',              [])
    RUTO_CHILD_GIGGLE  = Sound(0x6863, 'ruto-giggle',           'Ruto Giggle',               [])
    RUTO_CHILD_LIFT    = Sound(0x6864, 'ruto-lift',             'Ruto Lift',                 [])
    RUTO_CHILD_THROWN  = Sound(0x6865, 'ruto-thrown',           'Ruto Thrown',               [])
    RUTO_CHILD_WIGGLE  = Sound(0x6866, 'ruto-wiggle',           'Ruto Wiggle',               [])
    SCRUB_NUTS_UP      = Sound(0x387C, 'scrub-emerge',          'Scrub Emerge',              [])
    SHABOM_BOUNCE      = Sound(0x3948, 'shabom-bounce',         'Shabom Bounce',             [Tags.IMMEDIATE])
    SHABOM_POP         = Sound(0x3949, 'shabom-pop',            'Shabom Pop',                [Tags.IMMEDIATE, Tags.BRIEF])
    SHELLBLADE         = Sound(0x3849, 'shellblade',            'Shellblade',                [])
    SPIKE_TRAP         = Sound(0x38E9, 'spike-trap',            'Spike Trap',                [Tags.LOOPED])
    SPIT_NUT           = Sound(0x387E, 'spit-nut',              'Spit Nut',                  [Tags.IMMEDIATE, Tags.BRIEF])
    STALCHILD_ATTACK   = Sound(0x3831, 'stalchild-attack',      'Stalchild Attack',          [])
    STINGER_CRY        = Sound(0x39A3, 'stinger-squeak',        'Stinger Squeak',            [Tags.PAINFUL])
    TARGETING_ENEMY    = Sound(0x4830, 'target-enemy',          'Target Enemy',              [])
    TARGETING_NEUTRAL  = Sound(0x480C, 'target-neutral',        'Target Neutral',            [])
    TALON_CRY          = Sound(0x6853, 'talon-cry',             'Talon Cry',                 [])
    TALON_HMM          = Sound(0x6852, 'talon-hmm',             'Talon "Hmm"',               [])
    TALON_SNORE        = Sound(0x6850, 'talon-snore',           'Talon Snore',               [])
    TALON_WTF          = Sound(0x6851, 'talon-wtf',             'Talon Wtf',                 [])
    THUNDER            = Sound(0x282E, 'thunder',               'Thunder',                   [])
    TWINROVA_BICKER    = Sound(0x39E7, 'twinrova-bicker',       'Twinrova Bicker',           [Tags.LOOPED])
    WOLFOS_HOWL        = Sound(0x383C, 'wolfos-howl',           'Wolfos Howl',               [])
    INGO_WOOAH         = Sound(0x6854, 'ingo-wooah',            'Ingo "Wooah!"',             [])
    MAN_KAAH           = Sound(0x6855, 'man-kaah',              'Man "Kaah!"',               [])
    HORSE_NEIGH        = Sound(0x2805, 'horse-neigh',           'Horse Neigh',               [])


# Sound pools
standard   = [s for s in Sounds if Tags.LOOPED not in s.value.tags]
looping    = [s for s in Sounds if Tags.LOOPED in s.value.tags]
immediate  = [s for s in standard if Tags.IMMEDIATE in s.value.tags]
no_painful = [s for s in standard if Tags.PAINFUL not in s.value.tags]

# Selected by hand (very much a WIP)
navi = [
        Sounds.SPIT_NUT,
        Sounds.CURSED_SCREAM,
        Sounds.TALON_CRY,
        Sounds.BOW_TWANG,
        Sounds.BOTTLE_CORK,
        Sounds.GANON_TENNIS,
        Sounds.STALCHILD_ATTACK,
        Sounds.FANFARE_SMALL,
        Sounds.STALCHILD_ATTACK,
        Sounds.MAN_KAAH,
        Sounds.HORSE_NEIGH,
        ]
hp_low = [
        Sounds.RIBBIT,
        Sounds.BONGO_LOW,
        Sounds.CURSED_SCREAM,
        Sounds.TAMBOURINE,
        Sounds.RUTO_CHILD_CRASH,
        Sounds.SHABOM_BOUNCE,
        Sounds.CARROT_REFILL,
        Sounds.MOBLIN_CLUB_GROUND,
        ]
hover_boots = [
        Sounds.BARK,
        Sounds.SHABOM_POP,
        Sounds.CARTOON_FALL,
        Sounds.ZORA_KING,
        Sounds.TAMBOURINE,
        ]
nightfall = [
        Sounds.CUCCO_CROW,
        Sounds.REDEAD_MOAN,
        Sounds.TALON_SNORE,
        Sounds.GREAT_FAIRY,
        Sounds.THUNDER,
        Sounds.MOO,
        Sounds.GOLD_SKULL_TOKEN,
        ]
# Too small, needs more thought
menu_select = [
        Sounds.CHILD_CRINGE,
        Sounds.CHANGE_ITEM,
        Sounds.BONGO_HIGH,
        ]
# Too small, needs more thought
menu_cursor = [
        Sounds.CHILD_SCREAM,
        Sounds.BOW_TWANG,
        Sounds.DEKU_BABA_CHATTER,
        Sounds.BONGO_LOW,
        ]
horse_neigh = [
        Sounds.MOO,
        Sounds.CHILD_SCREAM,
        Sounds.RUTO_CHILD_WIGGLE,
        Sounds.GREAT_FAIRY,
        Sounds.ARMOS_GROAN,
        Sounds.REDEAD_SCREAM,
        Sounds.STALCHILD_ATTACK,
        ]


SoundHook = namedtuple('SoundHook', 'name pool locations')
class SoundHooks(Enum):
    NAVI            = SoundHook('Navi',        navi,        [0xAE7EF2, 0xC26C7E, 0xAE7EC6])
    HP_LOW          = SoundHook('Low Health',  hp_low,      [0xADBA1A])
    BOOTS_HOVER     = SoundHook('Hover Boots', hover_boots, [0xBDBD8A])
    NIGHTFALL       = SoundHook('Nightfall',   nightfall,   [0xAD3466, 0xAD7A2E])
    MENU_SELECT     = SoundHook('Menu Select', no_painful, [
                        0xBA1BBE, 0xBA23CE, 0xBA2956, 0xBA321A, 0xBA72F6, 0xBA8106, 0xBA82EE,
                        0xBA9DAE, 0xBA9EAE, 0xBA9FD2, 0xBAE6D6])
    MENU_CURSOR     = SoundHook('Menu Cursor', no_painful, [
                        0xBA165E, 0xBA1C1A, 0xBA2406, 0xBA327E, 0xBA3936, 0xBA77C2, 0xBA7886,
                        0xBA7A06, 0xBA7A6E, 0xBA7AE6, 0xBA7D6A, 0xBA8186, 0xBA822E, 0xBA82A2,
                        0xBAA11E, 0xBAE7C6])
    HORSE_NEIGH     = SoundHook('Horse Neigh', horse_neigh, [
                        0xC18832, 0xC18C32, 0xC19A7E, 0xC19CBE, 0xC1A1F2, 0xC1A3B6, 0xC1B08A,
                        0xC1B556, 0xC1C28A, 0xC1CC36, 0xC1EB4A, 0xC1F18E, 0xC6B136, 0xC6BBA2])
#   # Merged these into one
#   NAVI_OVERWORLD  = SoundHook('Navi - Overworld', navi_overworld,   [0xAE7EF2, 0xC26C7E])
#   NAVI_ENEMY      = SoundHook('Navi - Enemy',     navi_enemy,       [0xAE7EC6])
#   # Redeads have a different cutting sound, making this a bit weird
#   SWORD_SLASH     = SoundHook('Sword Slash',      standard,         [0xAC2942])


def get_patch_dict():
    return {s.value.keyword: s.value.id for s in Sounds}


def get_hook_pool(sound_hook):
    return sound_hook.value.pool


def get_setting_choices(sound_hook):
    pool     = sound_hook.value.pool
    choices  = {s.value.keyword: s.value.label for s in pool}
    result   = {
        'default':           'Default',
        'completely-random': 'Completely Random',
        'random-choice':     'Random Choice',
        **choices,
        }
    return result
