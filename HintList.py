class Hint(object):
    name = ""
    text = ""
    type = ""

    def __init__(self, name, text, type):
        self.name = name
        self.text = text
        self.type = type

def getHint(string):
    ret = Hint
    for hint in hintTable:
        if string == hint:
            text, type = hintTable[hint]
            ret = Hint(hint, text, type)
            break
        else:
            text, type = hintTable['useless']
            ret = Hint(hint, text, type)
    return ret

def getHintGroup(string):
    ret = []
    for hint in hintTable:
        text, type = hintTable[hint]
        if type == string:
            ret.append(Hint(hint, text, type))
    return ret

#table of hints, format is (name, hint text, type of hint) there are special characters that are read for certain in game commands:
#^ is a box break
#& is a new line
#@ will print the player name
hintTable = {'Hammer':                                                (" the dragon smasher.", 'item'),
             'Magic Meter':                                           (" pixie dust.", 'item'),
             'Progressive Hookshot':                                  (" Dampe's Keepsake.", 'item'),
             'Progressive Strength Upgrade':                          (" power gloves.", 'item'),
             'Hover Boots':                                           (" butter boots.", 'item'),
             'Master Sword':                                          (" evil's bane.", 'item'),
             'Mirror Shield':                                         (" the reflective rampart.", 'item'),
             'Forest Medallion':                                      (" the forest's power.", 'item'),
             'Fire Medallion':                                        (" fire's power.", 'item'),
             'Water Medallion':                                       (" water's power.", 'item'),
             'Shadow Medallion':                                      (" shadow's power.", 'item'),
             'Spirit Medallion':                                      (" spirit's power.", 'item'),
             'Light Medallion':                                       (" light's power.", 'item'),
             'Goron Ruby':                                            (" the Goron's treasure.", 'item'),
             'Kokiri Emerald':                                        (" the Kokiri's gift.", 'item'),
             'Zora Sapphire':                                         (" an engagement gift.", 'item'),
             'Farores Wind':                                          (" teleportation.", 'item'),
             'Nayrus Love':                                           (" a safe space.", 'item'),
             'Ice Arrows':                                            (" the refrigerator rocket.", 'item'),
             'Lens of Truth':                                         (" the perjurless porthole.", 'item'),
             'Dins Fire':                                             (" an inferno.", 'item'),
             'Fairy Ocarina':                                         (" a brown flute.", 'item'),
             'Goron Tunic':                                           (" ruby robes.", 'item'),
             'Zora Tunic':                                            (" a sapphire suit.", 'item'),
             'Iron Boots':                                            (" sink shoes.", 'item'),
             'Zeldas Letter':                                         (" a signed banana.", 'item'),
             'Zeldas Lullaby':                                        (" a song of royal slumber.", 'item'),
             'Nocturne of Shadow':                                    (" a song of spooky spirits.", 'item'),
             'Bow':                                                   (" an archery enabler.", 'item'),
             'Bomb Bag':                                              (" an explosive container.", 'item'),
             'Sarias Song':                                           (" a song of dancing gorons.", 'item'),
             'Song of Time':                                          (" a song 7 years long.", 'item'),
             'Song of Storms':                                        (" Rain Dance.", 'item'),
             'Minuet of Forest':                                      (" the song of tall trees.", 'item'),
             'Requiem of Spirit':                                     (" a song of sandy statues.", 'item'),
             'Slingshot':                                             (" a seed shooter.", 'item'),
             'Boomerang':                                             (" a banana.", 'item'),
             'Fire Arrows':                                           (" the furnace firearm.", 'item'),
             'Ocarina of Time':                                       (" blue flute.", 'item'),
             'Bottle':                                                (" a fairy prison.", 'item'),
             'Bottle with Letter':                                    (" a call for help.", 'item'),
             'Bottle with Milk':                                      (" vitamin D.", 'item'),
             'Progressive Scale':                                     (" Zora Flippers.", 'item'),
             'Stone of Agony':                                        (" an empty chest.", 'item'),
             'Eponas Song':                                           (" an equestrian etude.", 'item'),
             'Epona':                                                 (" a horse.", 'item'),
             'Gerudo Membership Card':                                (" a GT subscription.", 'item'),
             'Progressive Wallet':                                    (" a mo' money holder.", 'item'),
             'Bolero of Fire':                                        (" a song of lethal lava.", 'item'),
             'Suns Song':                                             (" Sunny Day.", 'item'),
             'Deku Shield':                                           (" a wooden ward.", 'item'),
             'Hylian Shield':                                         (" a steel safeguard.", 'item'),
             'Deku Stick Capacity':                                   (" a bundle of sticks.", 'item'),
             'Deku Nut Capacity':                                     (" more nuts.", 'item'),
             'Prelude of Light':                                      (" a luminous prologue melody.", 'item'),
             'Serenade of Water':                                     (" a song of a damp ditch.", 'item'),
             'Heart Container':                                       (" a lot of love.", 'item'),
             'Piece of Heart':                                        (" love.", 'item'),
             'Recovery Heart':                                        (" a free heal.", 'item'),
             'Rupee (1)':                                             (" rare riches.", 'item'),
             'Rupees (5)':                                            (" a common coin.", 'item'),
             'Rupees (20)':                                           (" couch cash.", 'item'),
             'Rupees (50)':                                           (" big bucks.", 'item'),
             'Rupees (200)':                                          (" a juicy jackpot.", 'item'),
             'Light Arrows':                                          (" the shining shot.", 'item'),
             'Kokiri Sword':                                          (" a butter knife.", 'item'),
             'Map':                                                   (" a dungeon atlas.", 'item'),
             'Compass':                                               (" a treasure tracker.", 'item'),
             'BossKey':                                               (" a master of unlocking.", 'item'),
             'SmallKey':                                              (" a tool for unlocking.", 'item'),
             'useless':                                               (" something worthless.", 'item'),
             'Arrows (5)':                                            (" danger darts.", 'item'),
             'Arrows (10)':                                           (" danger darts.", 'item'),
             'Arrows (30)':                                           (" danger darts.", 'item'),
             'Bombs (5)':                                             (" explosives.", 'item'),
             'Bombs (10)':                                            (" explosives.", 'item'),
             'Bombs (20)':                                            (" lots-o-explosives.", 'item'),
             'Ice Trap':                                              (" a gift from Ganon.", 'item'),
             'Magic Bean':                                            (" wizardly legumes.", 'item'),
             'Bombchus (5)':                                          (" mice bombs.", 'item'),
             'Bombchus (10)':                                         (" mice bombs.", 'item'),
             'Bombchus (20)':                                         (" mice bombs.", 'item'),
             'Deku Nuts (5)':                                         (" some nuts.", 'item'),
             'Deku Nuts (10)':                                        (" lots-o-nuts.", 'item'),
                                                                       #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx handy marker for how long one line should be in a text box
             '10 Big Poes':                                           ("They say that 10 Big Poes leads&to", 'alwaysLocation'),
             'Deku Theater Mask of Truth':                            ("They say that the Mask of Truth&yields", 'alwaysLocation'),
             '30 Gold Skulltulla Reward':                             ("They say that slaying 30 Gold&Skulltullas reveals", 'alwaysLocation'),
             '40 Gold Skulltulla Reward':                             ("They say that slaying 40 Gold&Skulltullas reveals", 'alwaysLocation'),
             '50 Gold Skulltulla Reward':                             ("They say that slaying 50 Gold&Skulltullas reveals", 'alwaysLocation'),
             'Child Fishing':                                         ("They say that fishing in youth&bestows", 'alwaysLocation'),
             'Adult Fishing':                                         ("They say that fishing in maturity&bestows", 'alwaysLocation'),
             'Song from Ocarina of Time':                             ("They say the Ocarina of Time&teaches", 'alwaysLocation'),
             '20 Gold Skulltulla Reward':                             ("They say that slaying 20 Gold&Skulltullas reveals", 'location'),
             'Hyrule Castle Fairy Reward':                            ("They say that Hyrule Castle's Great&Fairy holds", 'location'),
             'Zoras Fountain Fairy Reward':                           ("They say that The Fairy of Zora&Fountain hides", 'location'),
             'Desert Colossus Fairy Reward':                          ("They say the Great Fairy near The&Colossus holds", 'location'),
             'Treasure Chest Game':                                   ("They say that gambling&grants", 'location'),
             'Darunias Joy':                                          ("They say that Darunia's dance leads&to", 'location'),
             'Frog Ocarina Game':                                     ("They say The Frogs of Zora River&hold", 'location'),
             'Horseback Archery 1500 Points':                         ("They say that mastery of horseback&archery grants", 'location'),
             'Lake Hylia Sun':                                        ("They say staring into the sun&grants", 'location'),
             'Heart Piece Grave Chest':                               ("They say there's a hidden location&where the Sun's Song&spawns", 'location'),
             'Goron City Leftmost Maze Chest':                        ("They say in Goron City the hammer&unlocks", 'location'),
             'Chest Above King Dodongo':                              ("They say that the chest above the&Infernal Dinosaur&contains", 'location'),
             'Forest Temple Floormaster Chest':                       ("Deep in the forest, shadows guard a&chest containing", 'location'),
             'Fire Temple Scarecrow Chest':                           ("They say high in the Fire Temple,&Pierre hid", 'location'),
             'Fire Temple Megaton Hammer Chest':                      ("They say that the highest&chest in the crater&holds", 'location'),
             'Water Temple River Chest':                              ("They say deep under the lake&beyond the currents&hides", 'location'),
             'Water Temple Boss Key Chest':                           ("Deep under the lake,&the gilded chest&contains", 'location'),
             'Gerudo Training Grounds Underwater Silver Rupee Chest': ("They say those who seek&sunken silver rupees will&find", 'location'),
             'Gerudo Training Grounds Maze Path Final Chest':         ("They say that past all the locked&doors is", 'location'),
             'Bottom of the Well Defeat Boss':                        ("They say that Dead Hand&holds", 'location'),
             'Silver Gauntlets Chest':                                ("They say that upon&the Colossus's southern edge&is", 'location'),
             'Mirror Shield Chest':                                   ("They say that upon&the Colossus's northern edge&is", 'location'),
             'Shadow Temple Hidden Floormaster Chest':                ("They say in a maze&guarded by shadows&hides", 'location'),
             'Haunted Wasteland Structure Chest':                     ("They say that deep in the Wasteland&is", 'location'),
             'Composer Grave Chest':                                  ("They say that the Composer Brothers&hid", 'location'),
             'Song from Composer Grave':                              ("They say that the Composer Brothers&wrote", 'location'),
             'Song at Windmill':                                      ("They say that Guru-guru is driven&mad by", 'location'),
             'Sheik Forest Song':                                     ("They say that deep&in the forest Sheik&teaches", 'location'),
             'Sheik at Temple':                                       ("They say that Sheik&waits at a monument to time to&teach", 'location'),
             'Sheik in Crater':                                       ("They say that the craters melody&is", 'location'),
             'Sheik in Ice Cavern':                                   ("They say that the&frozen cavern echoes&with", 'location'),
             'Sheik in Kakariko':                                     ("They say that a&ravaged village mourns&with", 'location'),
             'Sheik at Colossus':                                     ("They say that a hero ventures&beyond the Wasteland to&learn", 'location'),
                                                                       #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx handy marker for how long one line should be in a text box
             '1001':                                                  ("Ganondorf 2020!", 'junkHint'),
             '1002':                                                  ("They say that monarchy is a&terrible system of governance.", 'junkHint'),
             '1003':                                                  ("They say that Zelda is a poor&leader.", 'junkHint'),
             '1004':                                                  ("These hints can be quite useful.&This is an exception.", 'junkHint'),
             '1005':                                                  ("The Stone of Agony is in your&inventory.", 'junkHint'),
             '1006':                                                  ("They say that all the Zora drowned&in Wind Waker.", 'junkHint'),
             '1007':                                                  ("They say that PJ64 is a terrible&emulator.", 'junkHint'),
             '1008':                                                  ("'Member when Ganon was a blue pig?^I 'member.", 'junkHint'),
             '1009':                                                  ("One who does not have Triforce&can't go in.", 'junkHint'),
             '1010':                                                  ("Save your future,&end the Happy Mask Salesmen.", 'junkHint'),
             '1011':                                                  ("Early Agony equals likely&troll seed.", 'junkHint'),
             '1012':                                                  ("I'm stoned. Get it?", 'junkHint'),
             '1013':                                                  ("Hoot! Hoot! Would you like me to&repeat that?", 'junkHint'),
             '1014':                                                  ("Gorons are stupid.&They eat rocks.", 'junkHint'),
             '1015':                                                  ("They say that Lon Lon Ranch&prospered under Ingo.", 'junkHint'),
             '1016':                                                  ("The single rupee is a&unique item.", 'junkHint'),
             '1017':                                                  ("Without Lens of Truth, the&Treasure Chest Mini-Game&is a 1 out of 32 chance.^Good luck!", 'junkHint'),
             '1018':                                                  ("Use bombs wisely.", 'junkHint'),
             '1019':                                                  ("Bomchus are not considered&in logic.", 'junkHint'),
             '1021':                                                  ("I found you faker!", 'junkHint'),
             '1022':                                                  ("You're comparing&yourself to me?^Ha! You're not even good&enough to be my fake.", 'junkHint'),
             '1023':                                                  ("I'll make you eat those words.", 'junkHint'),
             '1024':                                                  ("What happened to Sheik?", 'junkHint'),
             '1025':                                                  ("L2P @.", 'junkHint'),
             '1026':                                                  ("I heard @ isn't&very good at Zelda.", 'junkHint'),
             '1027':                                                  ("I'm Lunk from Pennsylvania.", 'junkHint'),
             '1028':                                                  ("I bet you'd like to&have more bombs.", 'junkHint'),
             '1029':                                                  ("When all else fails&use Fire.", 'junkHint'),
             '1030':                                                  ("Here's a hint @.&Don't be bad.", 'junkHint'),
             '1031':                                                  ("Game Over.&Return of Ganon.", 'junkHint'),
             '1032':                                                  ("May the way of the Hero&lead to the Triforce.", 'junkHint'),
             '1033':                                                  ("Can't find an item?&Scan an Amiibo.", 'junkHint'),
             '1034':                                                  ("They say this game has&just a few glitches.", 'junkHint'),
             '1035':                                                  ("BRRING BRRING This is Ulrira.&Wrong number?", 'junkHint'),
             '1036':                                                  ("Tingle Tingle Kooloo Limpah", 'junkHint'),
             '1037':                                                  ("L is real 2041", 'junkHint'),
             '1038':                                                  ("They say that Ganondorf will&appear in the next Mario Tennis.", 'junkHint'),
             '1039':                                                  ("Medigoron sells the earliest&Breath of the Wild demo.", 'junkHint'),
             '1040':                                                  ("There's a reason why I am special&inquisitor!", 'junkHint'),
             '1041':                                                  ("You were almost a @&sandwich.", 'junkHint'),
             '1042':                                                  ("I'm a helpful hint Gossip Stone!^See I'm helping.", 'junkHint')}

class RewardHint(object):
    name = ""
    text = ""

    def __init__(self, name, text):
        self.name = name
        self.text = text

#table of reward hints, format is ('name': "hint text"):
#^ is a box break, #& is a new line
rewardHints = {'Queen Gohma':   (" is in a talking tree."),
               'King Dodongo':  (" is in a mountain cave."),
               'Barinade':      (" is in a fish's belly."),
               'Phantom Ganon': (" is in a deep forest."),
               'Volvagia':      (" is in a volcano."),
               'Morpha':        (" is under a vast lake."),
               'Twinrova':      (" is in a desert temple."),
               'Bongo Bongo':   (" is in an ancient tomb."),
               'Pocket':        (" is in your pocket."),
               'Child':         ("Whoever seeks the three Spiritual&Stones should travel to these&locations:"),
               'Adult':         ("Whoever seeks the six Medallions&should travel to these locations:")}