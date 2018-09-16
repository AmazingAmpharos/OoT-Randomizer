import random

class Hint(object):
    name = ""
    text = ""
    type = ""

    def __init__(self, name, text, type, choice=None):
        self.name = name
        self.type = type

        if isinstance(text, str):
            self.text = text
        else:
            if choice == None:
                self.text = random.choice(text)
            else:
                self.text = text[choice]


def getHint(name, world):
    hint = name
    if name not in hintTable:
        hint = 'KeyError'

    textOptions, clearText, type = hintTable[hint]
    if world.clearer_hints == True:
        if clearText == None:
            return Hint(name, textOptions, type, 0)
        return Hint(name, clearText, type)
    else:
        return Hint(name, textOptions, type)


def getHintGroup(group, world):
    ret = []
    for name in hintTable:
        hint = getHint(name, world)
        if hint.type == group and not (name in hintExclusions(world)):
            ret.append(hint)
    return ret


#table of hints, format is (name, hint text, clear hint text, type of hint) there are special characters that are read for certain in game commands:
# ^ is a box break
# & is a new line
# @ will print the player name
# # sets color to white (currently only used for dungeon reward hints).
hintTable = {
    'Hammer':                                                (["the dragon smasher", "a metallic crusher", "the WHAM! weapon"], "the Hammer", 'item'),
    'Magic Meter':                                           (["sorcery training", "a stamina scroll", "pixie dust"], "Magic", 'item'),
    'Double Defense':                                        (["a white outline", "sturdy hearts", "strengthened love"], "Double Defense", 'item'),
    'Progressive Hookshot':                                  (["Dampe's keepsake", "an arm extension", "a great chain"], "a Hookshot", 'item'),
    'Progressive Strength Upgrade':                          (["power gloves", "arm day results", "the heavy lifty"], "a Strength Upgrade", 'item'),
    'Hover Boots':                                           (["butter boots", "slippery shoes", "spacewalkers"], "the Hover Boots", 'item'),
    'Master Sword':                                          (["evil's bane"], "the Master Sword", 'item'),
    'Mirror Shield':                                         (["the reflective rampart", "Medusa's weakness", "a silvered surface"], "the Mirror Shield", 'item'),
    'Farores Wind':                                          (["teleportation", "relocation magic", "a warp spell", "green wind"], "Farore's Wind", 'item'),
    'Nayrus Love':                                           (["a safe space", "an impregnable aura", "a blue barrier"], "Nayru's Love", 'item'),
    'Ice Arrows':                                            (["the refrigerator rocket", "frostbite bolts", "cold darts", "freezing projectiles"], "the Ice Arrows", 'item'),
    'Lens of Truth':                                         (["a lie detector", "true sight", "a detective's tool"], "the Lens of Truth", 'item'),
    'Dins Fire':                                             (["an inferno", "a great heat wave", "a blast of hot air"], "Din's Fire", 'item'),
    'Ocarina':                                               (["a flute", "a source of music"], "an Ocarina", 'item'),
    'Fairy Ocarina':                                         (["a brown flute", "a forest instrument"], "the Fairy Ocarina", 'item'),
    'Goron Tunic':                                           (["ruby robes", "fireproof garbs", "mountain clothing"], "a Goron Tunic", 'item'),
    'Zora Tunic':                                            (["a sapphire suit", "a fishy outfit", "lake clothing"], "a Zora Tunic", 'item'),
    'Iron Boots':                                            (["sink shoes", "watery footwear", "noisy boots"], "the Iron Boots", 'item'),
    'Zeldas Letter':                                         (["an autograph", "royal stationery", "royal snail mail"], "Zelda's Letter", 'item'),
    'Zeldas Lullaby':                                        (["a song of royal slumber", "a triforce tune"], "Zelda's Lullaby", 'item'),
    'Nocturne of Shadow':                                    (["a song of spooky spirits", "a graveyard boogie", "a ghastly tune"], "the Nocturne of Shadow", 'item'),
    'Bow':                                                   (["an archery enabler", "a danger dart launcher"], "a Bow", 'item'),
    'Bomb Bag':                                              (["an explosive container", "kaboom storage"], "a Bomb Bag", 'item'),
    'Sarias Song':                                           (["a song of dancing Gorons", "a green girl's tune", "child's forest melody"], "Sarias Song", 'item'),
    'Song of Time':                                          (["a song 7 years long", "a tune to move blocks"], "the Song of Time", 'item'),
    'Song of Storms':                                        (["Rain Dance", "a thunderstorm melody", "the tune of windmills"], "the Song of Storms", 'item'),
    'Minuet of Forest':                                      (["the song of tall trees", "adult's forest melody", "a green warp song"], "the Minuet of Forest", 'item'),
    'Requiem of Spirit':                                     (["a song of sandy statues", "an orange warp song", "the tune of the desert"], "the Requiem of Spirit", 'item'),
    'Slingshot':                                             (["a seed shooter", "a rubberband", "a child's catapult"], "a Slingshot", 'item'),
    'Boomerang':                                             (["a banana", "a faithful curved stick"], "the Boomerang", 'item'),
    'Fire Arrows':                                           (["the furnace firearm", "flame darts", "burning projectiles"], "the Fire Arrows", 'item'),
    'Ocarina of Time':                                       (["a blue flute", "a royal instrument"], "the Ocarina of Time", 'item'),
    'Bottle':                                                (["a glass container", "an empty jar", "something to be filled"], "a Bottle", 'item'),
    'Bottle with Letter':                                    (["a call for help", "an SOS jar", "fishy stationery"], "Ruto's letter", 'item'),
    'Bottle with Milk':                                      (["cow juice", "a white liquid"], "a Milk Bottle", 'item'),
    'Bottle with Red Potion':                                (["a vitality vial", "a red liquid"], "a Red Bottle", 'item'),
    'Bottle with Green Potion':                              (["a magic mixture", "a green liquid"], "a Green Bottle", 'item'),
    'Bottle with Blue Potion':                               (["a cure-all antidote", "a blue liquid"], "a Blue Bottle", 'item'),
    'Bottle with Fairy':                                     (["an imprisoned fairy", "an extra life"], "a Fairy Bottle", 'item'),
    'Bottle with Fish':                                      (["an aquarium", "a contained sea beast"], "a Fish Bottle", 'item'),
    'Bottle with Blue Fire':                                 (["a conflagration canteen", "an icemelt jar"], "a Fire Bottle", 'item'),
    'Bottle with Bugs':                                      (["an insectarium", "skultula finders", "a Bug Bottle"], "bugs", 'item'),
    'Bottle with Poe':                                       (["a spooky ghost", "a face in the jar"], "a Poe Bottle", 'item'),
    'Progressive Scale':                                     (["vertical swim depth", "a dive enhancer"], "a Zora Scale", 'item'),
    'Stone of Agony':                                        (["a vibrating rock", "a clue finder"], "the Stone of Agony", 'item'),
    'Eponas Song':                                           (["an equestrian etude", "a ranch song"], "Epona's song", 'item'),
    'Epona':                                                 (["a horse", "a four legged friend"], "Epona", 'item'),
    'Gerudo Membership Card':                                (["a GT subscription", "a desert tribe's pass"], "the Gerudo Card", 'item'),
    'Progressive Wallet':                                    (["a mo' money holder", "a gem purse", "financial capacity"], "a Wallet", 'item'),
    'Bolero of Fire':                                        (["a song of lethal lava", "a red warp song", "a volcano tune", "a song of a red sea"], "the Bolero of Fire", 'item'),
    'Suns Song':                                             (["Sunny Day", "a time advancer", "a day/night melody", "the gibdo's bane"], "the Sun's Song", 'item'),
    'Deku Shield':                                           (["a wooden ward", "forest protection"], "a Deku Shield", 'item'),
    'Hylian Shield':                                         (["a steel safeguard", "a Hylian relic", "metallic protection"], "a Hylian Shield", 'item'),
    'Deku Stick Capacity':                                   (["a lumber rack", "more flammable twigs"], "a Stick Capacity Upgrade", 'item'),
    'Deku Nut Capacity':                                     (["more nuts", "flashbang storage"], "a Nut Capacity Upgrade", 'item'),
    'Prelude of Light':                                      (["a luminous prologue melody", "a yellow warp song", "the temple traveler"], "the Prelude of Light", 'item'),
    'Serenade of Water':                                     (["a song of a damp ditch", "a blue warp song", "the lake's tune"], "the Serenade of Water", 'item'),
    'Heart Container':                                       (["a lot of love", "a Valentine's gift", "a boss's organ"], "a Heart Container", 'item'),
    'Piece of Heart':                                        (["love", "a partial Valentine"], "a Heart Piece", 'item'),
    'Piece of Heart (Treasure Chest Game)':                  (["love", "a partial Valentine"], "a Heart Piece", 'item'),
    'Recovery Heart':                                        (["a free heal", "disappointing love"], "a Recovery Heart", 'item'),
    'Rupee (1)':                                             (["a unique coin", "a penny", "a tiny coin", "a green gem"], "a Green Rupee", 'item'),
    'Rupees (5)':                                            (["a common coin", "a blue gem"], "a Blue Rupee", 'item'),
    'Rupees (20)':                                           (["couch cash", "a red gem"], "a Red Rupees", 'item'),
    'Rupees (50)':                                           (["big bucks", "a purple gem", "wealth"], "a Purple Rupee", 'item'),
    'Rupees (200)':                                          (["a juicy jackpot", "a yellow gem", "great wealth"], "a Gold Rupee", 'item'),
    'Light Arrows':                                          (["the shining shot", "glowing darts", "Ganondorf's bane"], "the Light Arrows", 'item'),
    'Kokiri Sword':                                          (["a butter knife", "a tiny, sharp blade", "a child's blade"], "the Kokiri Sword", 'item'),
    'Biggoron Sword':                                        (["an unwieldy knife", "a two-handed blade"], "the Biggoron Sword", 'item'),
    'Pocket Egg':                                            (["a Cucco container", "a Cucco, eventually", "a fowl youth"], "the Pocket Egg", 'item'),
    'Weird Egg':                                             (["a chicken dilemma"], "the Weird Egg", 'item'),
    'Pocket Cucco':                                          (["a little clucker"], "the Pocket Cucco", 'item'),
    'Cojiro':                                                (["a cerulean capon"], "Cojiro", 'item'),
    'Odd Mushroom':                                          (["a powder ingredient"], "an Odd Mushroom", 'item'),
    'Odd Potion':                                            (["Granny's goodies"], "an Odd Potion", 'item'),
    'Poachers Saw':                                          (["a tree killer"], "the Poacher's Saw", 'item'),
    'Broken Sword':                                          (["a shattered slicer"], "the Broken Sword", 'item'),
    'Prescription':                                          (["a pill pamphlet", "a Doctor's slip"], "the Prescription", 'item'),
    'Eyeball Frog':                                          (["a perceiving polliwog"], "the Eyeball Frog", 'item'),
    'Eyedrops':                                              (["a vision vial"], "the Eyedrops", 'item'),
    'Claim Check':                                           (["a three day wait"], "the Claim check", 'item'),
    'Map':                                                   (["a dungeon atlas", "blueprints"], "a Map", 'item'),
    'Compass':                                               (["a treasure tracker", "a magnetic needle"], "a Compass", 'item'),
    'BossKey':                                               (["a master of unlocking", "a dungeon's final pass"], "a Boss Key", 'item'),
    'SmallKey':                                              (["a tool for unlocking", "a dungeon pass", "a lock remover", "a legal lockpick", "a portal opener"], "a Small Key", 'item'),
    'FortressSmallKey':                                      (["a get out of jail free card"], "a Jail Key", 'item'),
    'KeyError':                                              (["something mysterious", "an unknown treasure"], "An Error (Please Report This)", 'item'),
    'Arrows (5)':                                            (["a few danger darts", "a few piercing ammunition"], "Arrows", 'item'),
    'Arrows (10)':                                           (["some danger darts", "some piercing ammunition"], "Arrows", 'item'),
    'Arrows (30)':                                           (["plenty of danger darts", "plenty of piercing ammunition"], "Arrows", 'item'),
    'Bombs (5)':                                             (["a few explosives", "a few sparky boom balls", "a few fireworks"], "Bombs", 'item'),
    'Bombs (10)':                                            (["some explosives", "some sparky boom balls", "some fireworks"], "Bombs", 'item'),
    'Bombs (20)':                                            (["lots-o-explosives", "plenty of sparky boom balls", "plenty of fireworks"], "Bombs", 'item'),
    'Ice Trap':                                              (["a gift from Ganon", "a chilling discovery", "an icy blast", "an unwanted freeze", "a wintery surprise"], "an Ice Trap", 'item'),
    'Magic Bean':                                            (["wizardly legumes"], "a Magic Bean", 'item'),
    'Bombchus':                                              (["mice bombs", "remote mines", "proximity mice", "wall crawlers", "trail blazers"], "Bombchus", 'item'),
    'Bombchus (5)':                                          (["a few mice bombs", "a few remote mines", "a few proximity mice", "a few wall crawlers", "a few trail blazers"], "Bombchus", 'item'),
    'Bombchus (10)':                                         (["some mice bombs", "some remote mines", "some proximity mice", "some wall crawlers", "some trail blazers"], "Bombchus", 'item'),
    'Bombchus (20)':                                         (["plenty of mice bombs", "plenty of remote mines", "plenty of proximity mice", "plenty of wall crawlers", "plenty of trail blazers"], "Bombchus", 'item'),
    'Deku Nuts (5)':                                         (["some nuts", "some flashbangs", "some Sheik's ammo"], "some Deku Nuts", 'item'),
    'Deku Nuts (10)':                                        (["lots-o-nuts", "plenty of flashbangs", "plenty of Sheik's ammo"], "plenty of Deku Nuts", 'item'),
    'Gold Skulltulla Token':                                 (["proof of destruction", "an arachnid chip", "spider remains"], "a Golden Token", 'item'),

    '10 Big Poes':                                           (["They say that Big Poes leads to", "They say that ghost hunters will be rewarded with"], None, 'alwaysLocation'),
    'Deku Theater Mask of Truth':                            ("They say that the Mask of Truth yields", None, 'alwaysLocation'),
    '30 Gold Skulltulla Reward':                             ("They say that slaying 30 Gold Skulltulas reveals", None, 'alwaysLocation'),
    '40 Gold Skulltulla Reward':                             ("They say that slaying 40 Gold Skulltulas reveals", None, 'alwaysLocation'),
    '50 Gold Skulltulla Reward':                             ("They say that slaying 50 Gold Skulltulas reveals", None, 'alwaysLocation'),
    'Song from Ocarina of Time':                             ("They say the Ocarina of Time teaches", None, 'alwaysLocation'),
    'Biggoron':                                              ("They say that Biggoron crafts", None, 'alwaysLocation'),
    'Child Fishing':                                         ("They say that fishing in youth bestows", None, 'location'),
    'Adult Fishing':                                         ("They say that fishing in maturity bestows", None, 'location'),
    '20 Gold Skulltulla Reward':                             ("They say that slaying 20 Gold Skulltulas reveals", None, 'location'),
    'Treasure Chest Game':                                   (["They say that gambling grants", "They say there is a 1/32 chance to win"], "They say that the treasure chest game grants", 'location'),
    'Darunias Joy':                                          ("They say that Darunia's dance leads to", None, 'location'),
    'Frog Ocarina Game':                                     (["They say The Frogs of Zora River hold", "They say that the musical amphibians have found"], None, 'location'),
    'Horseback Archery 1500 Points':                         ("They say that mastery of horseback archery grants", "They say that 1500 in horseback archery grants", 'location'),
    'Lake Hylia Sun':                                        (["They say staring into the sun grants", "They say that acts of solar aggression are punished with"], "They say that shooting the sun grants", 'location'),
    'Heart Piece Grave Chest':                               ("They say that in a grave the Sun's Song spawns", None, 'location'),
    'Goron City Leftmost Maze Chest':                        ("They say in Goron City the hammer unlocks", None, 'location'),
    'Chest Above King Dodongo':                              ("They say that the chest above the Infernal Dinosaur contains",  "They say that the chest above King Dodongo contains", 'location'),
    'Forest Temple Floormaster Chest':                       ("Deep in the forest, shadows guard a chest containing", "They say that a Floormaster in Forest Temple guards", 'location'),
    'Fire Temple Scarecrow Chest':                           ("They say high in the Fire Temple, Pierre hid", None, 'location'),
    'Fire Temple Megaton Hammer Chest':                      ("They say high in the Fire Temple, Fire Dancers hid", None, 'location'),
    'Water Temple River Chest':                              ("They say deep under the lake, beyond the currents, hides", "The say that the Water Temple River Chest holds", 'location'),
    'Water Temple Boss Key Chest':                           ("Deep under the lake, the gilded chest contains", "The say that the Water Temple Gold Chest holds", 'location'),
    'Gerudo Training Grounds Underwater Silver Rupee Chest': ("They say those who seek sunken silver rupees will find", None, 'location'),
    'Gerudo Training Grounds Maze Path Final Chest':         ("They say that past all the locked doors is", None, 'location'),
    'Bottom of the Well Defeat Boss':                        (["They say that Dead Hand holds", "They say that draining the water reveals a monster guarding"], None, 'location'),
    'Silver Gauntlets Chest':                                ("They say that upon the Colossus's right hand is", "They say that upon the Colossus's child hand is", 'location'),
    'Mirror Shield Chest':                                   ("They say that upon the Colossus's left hand is", "They say that upon the Colossus's adult hand is", 'location'),
    'Shadow Temple Hidden Floormaster Chest':                (["They say that shadows in an invisible maze guard", "They say that after a free boat ride comes"], "They say that a Floormaster in Shadow Temple guards", 'location'),
    'Haunted Wasteland Structure Chest':                     (["They say that deep in the Wasteland is", "They say that beneath the sands lies"], None, 'location'),
    'Composer Grave Chest':                                  (["They say that in the Composers' Grave, darkness hides", "They say that the Composer Brothers hid"], None, 'location'),
    'Song from Composer Grave':                              (["They say that in the Composers' Grave, Redead guard", "They say that the Composer Brothers wrote"], None, 'location'),
    'Song at Windmill':                                      (["They say the windmill echoes with", "They say that Guru-guru is driven mad by"], None, 'location'),
    'Sheik Forest Song':                                     ("They say that deep in the forest Sheik teaches", None, 'location'),
    'Sheik at Temple':                                       ("They say that Sheik waits at a monument to time to teach", None, 'location'),
    'Sheik in Crater':                                       ("They say that the crater's melody is", None, 'location'),
    'Sheik in Ice Cavern':                                   ("They say that the frozen cavern echoes with", None, 'location'),
    'Sheik in Kakariko':                                     ("They say that a ravaged village mourns with", None, 'location'),
    'Sheik at Colossus':                                     ("They say that a hero ventures beyond the Wasteland to learn", None, 'location'),
    'Zoras Fountain Bottom Freestanding PoH':                ("They say under the icy waters lies", None, 'location'),
    'Colossus Freestanding PoH':                             ("They say that riding a beanstalk in the desert leads to", None, 'location'),
    'DM Crater Volcano Freestanding PoH':                    ("They say that riding a beanstalk in the crater leads to", None, 'location'),
    'Goron City Pot Freestanding PoH':                       ("They say that spinning Goron pottery contains", None, 'location'),

    '1001':                                                  ("Ganondorf 2020!", None, 'junkHint'),
    '1002':                                                  ("They say that monarchy is a terrible system of governance.", None, 'junkHint'),
    '1003':                                                  ("They say that Zelda is a poor leader.", None, 'junkHint'),
    '1004':                                                  ("These hints can be quite useful. This is an exception.", None, 'junkHint'),
    '1006':                                                  ("They say that all the Zora drowned in Wind Waker.", None, 'junkHint'),
    '1007':                                                  ("They say that PJ64 is a terrible emulator.", None, 'junkHint'),
    '1008':                                                  ("'Member when Ganon was a blue pig?^I 'member.", None, 'junkHint'),
    '1009':                                                  ("One who does not have Triforce can't go in.", None, 'junkHint'),
    '1010':                                                  ("Save your future, end the Happy Mask Salesman.", None, 'junkHint'),
    '1012':                                                  ("I'm stoned. Get it?", None, 'junkHint'),
    '1013':                                                  ("Hoot! Hoot! Would you like me to repeat that?", None, 'junkHint'),
    '1014':                                                  ("Gorons are stupid. They eat rocks.", None, 'junkHint'),
    '1015':                                                  ("They say that Lon Lon Ranch prospered under Ingo.", None, 'junkHint'),
    '1016':                                                  ("The single rupee is a unique item.", None, 'junkHint'),
    '1017':                                                  ("Without the Lens of Truth, the Treasure Chest Mini-Game is a 1 out of 32 chance.^Good luck!", None, 'junkHint'),
    '1018':                                                  ("Use bombs wisely.", None, 'junkHint'),
    '1021':                                                  ("I found you, faker!", None, 'junkHint'),
    '1022':                                                  ("You're comparing yourself to me?^Ha! You're not even good enough to be my fake.", None, 'junkHint'),
    '1023':                                                  ("I'll make you eat those words.", None, 'junkHint'),
    '1024':                                                  ("What happened to Sheik?", None, 'junkHint'),
    '1025':                                                  ("L2P @.", None, 'junkHint'),
    '1026':                                                  ("I heard @ isn't very good at Zelda.", None, 'junkHint'),
    '1027':                                                  ("I'm Lonk from Pennsylvania.", None, 'junkHint'),
    '1028':                                                  ("I bet you'd like to have more bombs.", None, 'junkHint'),
    '1029':                                                  ("When all else fails, use Fire.", None, 'junkHint'),
    '1030':                                                  ("Here's a hint, @. Don't be bad.", None, 'junkHint'),
    '1031':                                                  ("Game Over. Return of Ganon.", None, 'junkHint'),
    '1032':                                                  ("May the way of the Hero lead to the Triforce.", None, 'junkHint'),
    '1033':                                                  ("Can't find an item? Scan an Amiibo.", None, 'junkHint'),
    '1034':                                                  ("They say this game has just a few glitches.", None, 'junkHint'),
    '1035':                                                  ("BRRING BRRING This is Ulrira. Wrong number?", None, 'junkHint'),
    '1036':                                                  ("Tingle Tingle Kooloo Limpah", None, 'junkHint'),
    '1037':                                                  ("L is real 2041", None, 'junkHint'),
    '1038':                                                  ("They say that Ganondorf will appear in the next Mario Tennis.", None, 'junkHint'),
    '1039':                                                  ("Medigoron sells the earliest Breath of the Wild demo.", None, 'junkHint'),
    '1040':                                                  ("There's a reason why I am special inquisitor!", None, 'junkHint'),
    '1041':                                                  ("You were almost a @ sandwich.", None, 'junkHint'),
    '1042':                                                  ("I'm a helpful hint Gossip Stone!^See, I'm helping.", None, 'junkHint'),
    '1043':                                                  ("Dear @, please come to the castle. I've baked a cake for you.&&Yours truly, princess Zelda.", None, 'junkHint'),
    '1044':                                                  ("They say all toasters toast toast.", None, 'junkHint'),
    '1045':                                                  ("They say that Okami is the best Zelda game.", None, 'junkHint'),
    '1046':                                                  ("They say that quest guidance can be found at a talking rock.", None, 'junkHint'),
    '1047':                                                  ("They say that the final item you're looking for can be found somewhere in Hyrule", None, 'junkHint'),
                                                             #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx handy marker for how long one line should be in a text box
    'Deku Tree':                                             ("an ancient tree", "Deku Tree", 'dungeon'),
    'Dodongos Cavern':                                       ("an immense cavern", "Dodongo's Cavern", 'dungeon'),
    'Jabu Jabus Belly':                                      ("the belly of a deity", "Jabu Jabu's Belly", 'dungeon'),
    'Forest Temple':                                         ("a deep forest", "Forest Temple", 'dungeon'),
    'Fire Temple':                                           ("a high mountain", "Fire Temple", 'dungeon'),
    'Water Temple':                                          ("a vast lake", "Water Temple", 'dungeon'),
    'Shadow Temple':                                         ("the house of the dead", "Shadow Temple", 'dungeon'),
    'Spirit Temple':                                         ("the goddess of the sand", "Spirit Temple", 'dungeon'),
    'Ice Cavern':                                            ("a frozen maze", "Ice Cavern", 'dungeon'),
    'Bottom of the Well':                                    ("a shadow\'s prison", "Bottom of the Well", 'dungeon'),
    'Gerudo Training Grounds':                               ("the test of thieves", "Gerudo Training Grounds", 'dungeon'),
    'Ganons Castle':                                         ("a conquered citadel", "Ganon's Castle", 'dungeon'),
                                                             #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx handy marker for how long one line should be in a text box             
    'Queen Gohma':                                           ("One inside an #ancient tree#...^", "One in the #Deku Tree#...^", 'boss'),
    'King Dodongo':                                          ("One within an #immense cavern#...^", "One in #Dodongo's Cavern#...^", 'boss'),
    'Barinade':                                              ("One in the #belly of a deity#...^", "One in #Jabu Jabu's Belly#...^", 'boss'),
    'Phantom Ganon':                                         ("One in a #deep forest#...^", "One in the #Forest Temple#...^", 'boss'),
    'Volvagia':                                              ("One on a #high mountain#...^", "One in the #Fire Temple#...^", 'boss'),
    'Morpha':                                                ("One under a #vast lake#...^", "One in the #Water Temple#...^", 'boss'),
    'Bongo Bongo':                                           ("One within the #house of the dead#...^", "One in the #Shadow Temple#...^", 'boss'),
    'Twinrova':                                              ("One inside a #goddess of the sand#...^", "One in the #Spirit Temple#...^", 'boss'),
    'Links Pocket':                                          ("One in #@'s pocket#...^", "One #@ already has#...^", 'boss'),
    'Spiritual Stone Text Start':                            ("Ye who owns 3 Spiritual Stones...^", None, 'boss'),
    'Spiritual Stone Text End':                              ("Stand with the Ocarina of Time&and play the Song of Time.", None, 'boss'),
    'Medallion Text End':                                    ("Together with the Hero of Time,&the awakened ones will bind the&evil and return the light of peace&to the world.", None, 'boss'),
                                                            #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx handy marker for how long one line should be in a text box
    'Validation Line':                                       ("Hmph... Since you made it this far,&I'll let you know what glorious&prize of Ganon's you likely&missed out on in my tower.^Behold...^", None, 'validation line'),
    'Light Arrow Location':                                  ("Ha ha ha... You'll never beat me by&reflecting my lightning bolts&and unleashing the arrows from&", None, 'Light Arrow Location'),
    '2001':                                                  ("Oh! It's @.&I was expecting someone called&Sheik. Do you know what&happened to them?", None, 'ganonLine'), 
    '2002':                                                  ("I knew I shouldn't have put the key&on the other side of my door.", None, 'ganonLine'),
    '2003':                                                  ("Looks like it's time for a&round of tennis.", None, 'ganonLine'),
    '2004':                                                  ("You'll never deflect my bolts of&energy with your sword,&then shoot me with those Light&Arrows you happen to have.", None, 'ganonLine'),
    '2005':                                                  ("Why did I leave my trident&back in the desert?", None, 'ganonLine'),
    '2006':                                                  ("Zelda is probably going to do&something stupid, like send you&back to your own timeline.^So this is quite meaningless.&Do you really want&to save this moron?", None, 'ganonLine'),
    '2007':                                                  ("What about Zelda makes you think&she'd be a better ruler than I?^I saved Lon Lon Ranch,&fed the hungry,&and my castle floats.", None, 'ganonLine'),
    '2008':                                                  ("I've learned this spell,&it's really neat,&I'll keep it later&for your treat!", None, 'ganonLine'),
    '2009':                                                  ("Many tricks are up my sleeve,&to save yourself&you'd better leave!", None, 'ganonLine'),
    '2010':                                                  ("After what you did to&Koholint Island, how can&you call me the bad guy?", None, 'ganonLine'),
    '2011':                                                  ("Today, let's begin down&'The Hero is Defeated' timeline.", None, 'ganonLine'),
}

# exclusions from the list for custom logic

def hintExclusions(world):
    expected_skulltulas = world.logic_skulltulas
    exclusions = []
    if world.logic_no_trade_skull_mask:
        exclusions.append('Deku Theater Skull Mask')
    if world.logic_no_trade_mask_of_truth:
        exclusions.append('Deku Theater Mask of Truth')
    if world.logic_no_trade_biggoron:
        exclusions.append('Biggoron')
    if world.logic_no_child_fishing:
        exclusions.append('Child Fishing')
    if world.logic_no_adult_fishing:
        exclusions.append('Adult Fishing')
    if world.logic_no_big_poes:
        exclusions.append('10 Big Poes')
    if expected_skulltulas < 50:
        exclusions.append('50 Gold Skulltulla Reward')
    if expected_skulltulas < 40:
        exclusions.append('40 Gold Skulltulla Reward')
    if expected_skulltulas < 30:
        exclusions.append('30 Gold Skulltulla Reward')
    if expected_skulltulas < 20:
        exclusions.append('20 Gold Skulltulla Reward')
    if expected_skulltulas < 10:
        exclusions.append('10 Gold Skulltulla Reward')
    return exclusions
