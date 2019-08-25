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
    LOOPED     = 0
    QUIET      = 1
    IMMEDIATE  = 2      # Delayed sounds are commonly undesirable
    BRIEF      = 3      # Punchy sounds, good for rapid fire
    NEW        = 4
    PAINFUL    = 5      # Eardrum-piercing sounds
    NAVI       = 6      # Navi sounds (hand chosen)
    HPLOW      = 7      # Low HP sounds (hand chosen)
    HOVERBOOT  = 8      # Hover boot sounds (hand chosen)
    NIGHTFALL  = 9      # Nightfall sounds (hand chosen)
    MENUSELECT = 10     # Menu selection sounds (hand chosen, could use some more)
    MENUMOVE   = 11     # Menu movement sounds  (hand chosen, could use some more)
    HORSE      = 12     # Horse neigh sounds (hand chosen)
    INC_NE     = 20     # Incompatible with NAVI_ENEMY? (Verify)
                        # I'm now thinking it has to do with a limit of concurrent sounds)

Sound = namedtuple('Sound',   'id      keyword                  label                        tags')
class Sounds(Enum):
    NONE               = Sound(0x0000, 'none',                  'None',                      [Tags.LOOPED, Tags.QUIET, Tags.IMMEDIATE, Tags.BRIEF, Tags.NEW, Tags.NAVI, Tags.NIGHTFALL, Tags.INC_NE])
    ARMOS_GROAN        = Sound(0x3848, 'armos',                 'Armos',                     [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    BARK               = Sound(0x28D8, 'bark',                  'Bark',                      [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    BOMB_BOUNCE        = Sound(0x282F, 'bomb-bounce',           'Bomb Bounce',               [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    BOOTS_HOVER        = Sound(0x08C9, 'hover-boots',           'Hover Boots',               [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    BOOTS_IRON         = Sound(0x080D, 'iron-boots',            'Iron Boots',                [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    BOTTLE_CORK        = Sound(0x286C, 'bottle-cork',           'Bottle Cork',               [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    BOW_TWANG          = Sound(0x1830, 'bow-twang',             'Bow Twang',                 [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    BUBBLE_LOL         = Sound(0x38CA, 'bubble-laugh',          'Bubble Laugh',              [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    BONGO_HIGH         = Sound(0x3951, 'bongo-bongo-high',      'Bongo Bongo High',          [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    BONGO_LOW          = Sound(0x3950, 'bongo-bongo-low',       'Bongo Bongo Low',           [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    CARROT_REFILL      = Sound(0x4845, 'carrot-refill',         'Carrot Refill',             [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    CARTOON_FALL       = Sound(0x28A0, 'cartoon-fall',          'Cartoon Fall',              [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    CHANGE_ITEM        = Sound(0x0835, 'change-item',           'Change Item',               [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    CHEST_OPEN         = Sound(0x2820, 'chest-open',            'Chest Open',                [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    CHILD_CRINGE       = Sound(0x683A, 'child-cringe',          'Child Cringe',              [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    CHILD_GASP         = Sound(0x6836, 'child-gasp',            'Child Gasp',                [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    CHILD_HURT         = Sound(0x6825, 'child-hurt',            'Child Hurt',                [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    CHILD_OWO          = Sound(0x6823, 'child-owo',             'Child owo',                 [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    CHILD_PANT         = Sound(0x6829, 'child-pant',            'Child Pant',                [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    CHILD_SCREAM       = Sound(0x6828, 'child-scream',          'Child Scream',              [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    CRATE_EXPLODE      = Sound(0x2839, 'exploding-crate',       'Exploding Crate',           [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    CUCCO_CLUCK        = Sound(0x2812, 'cluck',                 'Cluck',                     [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    CUCCO_CROW         = Sound(0x2813, 'cockadoodledoo',        'Cockadoodledoo',            [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    CURSED_SCREAM      = Sound(0x6867, 'cursed-scream',         'Cursed Scream',             [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    CURSED_ATTACK      = Sound(0x6868, 'cursed-attack',         'Cursed Attack',             [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    DRAWBRIDGE_SET     = Sound(0x280E, 'drawbridge-set',        'Drawbridge Set',            [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    DUSK_HOWL          = Sound(0x28AE, 'dusk-howl',             'Dusk Howl',                 [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    DEKU_BABA_CHATTER  = Sound(0x3860, 'deku-baba',             'Deku Baba',                 [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    EPONA_CHILD        = Sound(0x2844, 'baby-epona',            'Baby Epona',                [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    EXPLOSION          = Sound(0x180E, 'explosion',             'Explosion',                 [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    FANFARE_MED        = Sound(0x4831, 'medium-fanfare',        'Medium Fanfare',            [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    FANFARE_SMALL      = Sound(0x4824, 'light-fanfare',         'Light Fanfare',             [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    FIELD_SHRUB        = Sound(0x2877, 'field-shrub',           'Field Shrub',               [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    FLARE_BOSS_LOL     = Sound(0x3981, 'flare-dancer-laugh',    'Flare Dancer Laugh',        [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    FLARE_BOSS_STARTLE = Sound(0x398B, 'flare-dancer-startled', 'Flare Dancer Startled',     [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    GANON_TENNIS       = Sound(0x39CA, 'ganondorf-teh',         'Ganondorf "Teh!"',          [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    GOHMA_LARVA_CROAK  = Sound(0x395D, 'gohma-larva-croak',     'Gohma Larva Croak',         [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    GOLD_SKULL_TOKEN   = Sound(0x4843, 'gold-skull-token',      'Gold Skull Token',          [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    GORON_WAKE         = Sound(0x38FC, 'goron-wake',            'Goron Wake',                [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    GREAT_FAIRY        = Sound(0x6858, 'great-fairy',           'Great Fairy',               [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    GUAY               = Sound(0x38B6, 'guay',                  'Guay',                      [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    GUNSHOT            = Sound(0x4835, 'gunshot',               'Gunshot',                   [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    HAMMER_BONK        = Sound(0x180A, 'hammer-bonk',           'Hammer Bonk',               [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    HORSE_NEIGH        = Sound(0x2805, 'horse-neigh',           'Horse Neigh',               [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    HORSE_TROT         = Sound(0x2804, 'horse-trot',            'Horse Trot',                [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    HP_LOW             = Sound(0x481B, 'low-health',            'Low Health',                [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    HP_RECOVER         = Sound(0x480B, 'recover-health',        'Recover Health',            [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    ICE_SHATTER        = Sound(0x0875, 'shattering-ice',        'Shattering Ice',            [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    INGO_WOOAH         = Sound(0x6854, 'ingo-wooah',            'Ingo "Wooah!"',             [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    IRON_KNUCKLE       = Sound(0x3929, 'iron-knuckle',          'Iron Knuckle',              [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    INGO_KAAH          = Sound(0x6855, 'kaah',                  'Kaah!',                     [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    MOBLIN_CLUB_GROUND = Sound(0x38EF, 'moblin-club-ground',    'Moblin Club Ground',        [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    MOBLIN_CLUB_SWING  = Sound(0x39E1, 'moblin-club-swing',     'Moblin Club Swing',         [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    MOO                = Sound(0x28DF, 'moo',                   'Moo',                       [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    NAVI_HELLO         = Sound(0x6844, 'navi-hello',            'Navi "Hello!"',             [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    NAVI_HEY           = Sound(0x685F, 'navi-hey',              'Navi "Hey!"',               [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    NAVI_RANDOM        = Sound(0x6843, 'navi-random',           'Navi Random',               [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    NOTIFICATION       = Sound(0x4820, 'notification',          'Notification',              [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    PHANTOM_GANON_LOL  = Sound(0x38B0, 'phantom-ganon-laugh',   'Phantom Ganon Laugh',       [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    PLANT_EXPLODE      = Sound(0x284E, 'plant-explode',         'Plant Explode',             [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    POE                = Sound(0x38EC, 'poe',                   'Poe',                       [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    POT_SHATTER        = Sound(0x2887, 'shattering-pot',        'Shattering Pot',            [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    REDEAD_MOAN        = Sound(0x38E4, 'redead-moan',           'Redead Moan',               [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    REDEAD_SCREAM      = Sound(0x38E5, 'redead-scream',         'Redead Scream',             [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    RIBBIT             = Sound(0x28B1, 'ribbit',                'Ribbit',                    [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    RUPEE              = Sound(0x4803, 'rupee',                 'Rupee',                     [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    RUPEE_SILVER       = Sound(0x28E8, 'silver-rupee',          'Silver Rupee',              [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    RUTO_CHILD_CRASH   = Sound(0x6860, 'ruto-crash',            'Ruto Crash',                [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    RUTO_CHILD_EXCITED = Sound(0x6861, 'ruto-excited',          'Ruto Excited',              [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    RUTO_CHILD_GIGGLE  = Sound(0x6863, 'ruto-giggle',           'Ruto Giggle',               [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    RUTO_CHILD_LIFT    = Sound(0x6864, 'ruto-lift',             'Ruto Lift',                 [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    RUTO_CHILD_THROWN  = Sound(0x6865, 'ruto-thrown',           'Ruto Thrown',               [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    RUTO_CHILD_WIGGLE  = Sound(0x6866, 'ruto-wiggle',           'Ruto Wiggle',               [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    SCRUB_BUSINESS     = Sound(0x3882, 'business-scrub',        'Business Scrub',            [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    SCRUB_NUTS_UP      = Sound(0x387C, 'scrub-emerge',          'Scrub Emerge',              [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    SHABOM_BOUNCE      = Sound(0x3948, 'shabom-bounce',         'Shabom Bounce',             [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    SHABOM_POP         = Sound(0x3949, 'shabom-pop',            'Shabom Pop',                [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    SHELLBLADE         = Sound(0x3849, 'shellblade',            'Shellblade',                [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    SKULLTULA          = Sound(0x39DA, 'skulltula',             'Skulltula',                 [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    SOFT_BEEP          = Sound(0x4804, 'soft-beep',             'Soft Beep',                 [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    SPIKE_TRAP         = Sound(0x38E9, 'spike-trap',            'Spike Trap',                [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    SPIT_NUT           = Sound(0x387E, 'spit-nut',              'Spit Nut',                  [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    STALCHILD_ATTACK   = Sound(0x3831, 'stalchild-attack',      'Stalchild Attack',          [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    STINGER_CRY        = Sound(0x39A3, 'stinger-squeak',        'Stinger Squeak',            [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    SWITCH             = Sound(0x2815, 'switch',                'Switch',                    [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    SWORD_BONK         = Sound(0x181A, 'sword-bonk',            'Sword Bonk',                [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    TAMBOURINE         = Sound(0x4842, 'tambourine',            'Tambourine',                [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    TARGETING_ENEMY    = Sound(0x4830, 'target-enemy',          'Target Enemy',              [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    TARGETING_NEUTRAL  = Sound(0x480C, 'target-neutral',        'Target Neutral',            [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    TALON_CRY          = Sound(0x6853, 'talon-cry',             'Talon Cry',                 [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    TALON_HMM          = Sound(0x6852, 'talon-hmm',             'Talon "Hmm"',               [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    TALON_SNORE        = Sound(0x6850, 'talon-snore',           'Talon Snore',               [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    TALON_WTF          = Sound(0x6851, 'talon-wtf',             'Talon Wtf',                 [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    THUNDER            = Sound(0x282E, 'thunder',               'Thunder',                   [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    TIMER              = Sound(0x481A, 'timer',                 'Timer',                     [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    TWINROVA_BICKER    = Sound(0x39E7, 'twinrova-bicker',       'Twinrova Bicker',           [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    WOLFOS_HOWL        = Sound(0x383C, 'wolfos-howl',           'Wolfos Howl',               [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    ZELDA_ADULT_GASP   = Sound(0x6879, 'adult-zelda-gasp',      'Adult Zelda Gasp',          [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])
    ZORA_KING          = Sound(0x687A, 'mweep',                 'Mweep!',                    [Tags.HPLOW, Tags.HOVERBOOT, Tags.MENUSELECT, Tags.MENUMOVE, Tags.HORSE])


# Sound pools
standard    = [s for s in Sounds if Tags.LOOPED not in s.value.tags]
looping     = [s for s in Sounds if Tags.LOOPED in s.value.tags]
no_painful  = [s for s in standard if Tags.PAINFUL not in s.value.tags]
navi        = [s for s in Sounds if Tags.NAVI in s.value.tags]
hp_low      = [s for s in Sounds if Tags.HPLOW in s.value.tags]
hover_boots = [s for s in Sounds if Tags.HOVERBOOT in s.value.tags]
nightfall   = [s for s in Sounds if Tags.NIGHTFALL in s.value.tags]
menu_select = [s for s in Sounds if Tags.MENUSELECT in s.value.tags]
menu_cursor = [s for s in Sounds if Tags.MENUMOVE in s.value.tags]
horse_neigh = [s for s in Sounds if Tags.HORSE in s.value.tags]


SoundHook = namedtuple('SoundHook', 'name pool locations')
class SoundHooks(Enum):
    NAVI_OVERWORLD  = SoundHook('Navi - Overworld', navi,        [0xAE7EF2, 0xC26C7E])
    NAVI_ENEMY      = SoundHook('Navi - Enemy',     navi,        [0xAE7EC6])
    HP_LOW          = SoundHook('Low Health',       hp_low,      [0xADBA1A])
    BOOTS_HOVER     = SoundHook('Hover Boots',      hover_boots, [0xBDBD8A])
    NIGHTFALL       = SoundHook('Nightfall',        nightfall,   [0xAD3466, 0xAD7A2E])
    MENU_SELECT     = SoundHook('Menu Select',      no_painful,  [
                        0xBA1BBE, 0xBA23CE, 0xBA2956, 0xBA321A, 0xBA72F6, 0xBA8106, 0xBA82EE,
                        0xBA9DAE, 0xBA9EAE, 0xBA9FD2, 0xBAE6D6])
    MENU_CURSOR     = SoundHook('Menu Cursor',      no_painful,  [
                        0xBA165E, 0xBA1C1A, 0xBA2406, 0xBA327E, 0xBA3936, 0xBA77C2, 0xBA7886,
                        0xBA7A06, 0xBA7A6E, 0xBA7AE6, 0xBA7D6A, 0xBA8186, 0xBA822E, 0xBA82A2,
                        0xBAA11E, 0xBAE7C6])
    HORSE_NEIGH     = SoundHook('Horse Neigh',      horse_neigh, [
                        0xC18832, 0xC18C32, 0xC19A7E, 0xC19CBE, 0xC1A1F2, 0xC1A3B6, 0xC1B08A,
                        0xC1B556, 0xC1C28A, 0xC1CC36, 0xC1EB4A, 0xC1F18E, 0xC6B136, 0xC6BBA2,
                        0xC1E93A, 0XC6B366, 0XC6B562])


#   # Some enemies have a different cutting sound, making this a bit weird
#   SWORD_SLASH     = SoundHook('Sword Slash',      standard,         [0xAC2942])


def get_patch_dict():
    return {s.value.keyword: s.value.id for s in Sounds}


def get_hook_pool(sound_hook, earsafeonly = "FALSE"):
    if earsafeonly == "TRUE":
        list = [s for s in sound_hook.value.pool if Tags.PAINFUL not in s.value.tags]
        return list
    else:
        return sound_hook.value.pool


def get_setting_choices(sound_hook):
    pool     = sound_hook.value.pool
    choices  = {s.value.keyword: s.value.label for s in pool}
    result   = {
        #'default':           'Default',
        #'completely-random': 'Completely Random',
        #'random-ear-safe':   'Random Ear-Safe',
        #'random-choice':     'Random Choice',
        'none':              'None',
        **choices,
        }
    return result
