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
             'Bottle':                                                (" fairy prison.", 'item'),
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
             'Prelude of Light':                                      (" a luminous intros melody.", 'item'),
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
             'Boss Key':                                              (" a master of unlocking.", 'item'),
             'Small Key':                                             (" a tool for unlocking.", 'item'),
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
             '10 Big Poes':                                           ("They say 10 Big Poes leads&to", 'alwaysLocation'),
             'Deku Theater Mask of Truth':                            ("They say the Mask of Truth&yields", 'alwaysLocation'),
             '30 Gold Skulltulla Reward':                             ("Slay 30 Gold Skulltullas to&find", 'alwaysLocation'),
             '40 Gold Skulltulla Reward':                             ("Slay 40 Gold Skulltullas to&find", 'alwaysLocation'),
             '50 Gold Skulltulla Reward':                             ("Slay 50 Gold Skulltullas to&find", 'alwaysLocation'),
             'Child Fishing':                                         ("At the fishing hole, when young,&is", 'alwaysLocation'),
             'Adult Fishing':                                         ("At the fishing hole, when mature,&is", 'alwaysLocation'),
             'Song from Ocarina of Time':                             ("They say the Ocarina of Time&has", 'alwaysLocation'),
             '20 Gold Skulltulla Reward':                             ("Slay 20 Gold Skulltullas to&find", 'location'),
             'Hyrule Castle Fairy Reward':                            ("At the Castle Great Fairy&is", 'location'),
             'Zoras Fountain Fairy Reward':                           ("At the Zora Great Fairy&is", 'location'),
             'Desert Colossus Fairy Reward':                          ("At the Desert Great Fairy&is", 'location'),
             'Treasure Chest Game':                                   ("They say gambling&grants", 'location'),
             'Darunias Joy':                                          ("They say Darunia's dance leads&to", 'location'),
             'Frog Ocarina Game':                                     ("They say the frogs&hold", 'location'),
             'Horseback Archery 1500 Points':                         ("Mastery of horseback archery&grants", 'location'),
             'Lake Hylia Sun':                                        ("Staring into the sun&grants", 'location'),
             'Heart Piece Grave Chest':                               ("They say the Sun's Song&spawns", 'location'),
             'Goron City Leftmost Maze Chest':                        ("At Goron City the hammer&unlocks", 'location'),
             'Chest Above King Dodongo':                              ("Above the Infernal Dinosaur&is", 'location'),
             'Forest Temple Floormaster Chest':                       ("Behind forest shadows&is", 'location'),
             'Fire Temple Scarecrow Chest':                           ("In the Fire Temple, Pierre&hides", 'location'),
             'Fire Temple Megaton Hammer Chest':                      ("A gilded chest in the crater&holds", 'location'),
             'Water Temple River Chest':                              ("Under the lake past currents&hides", 'location'),
             'Water Temple Boss Key Chest':                           ("Under the lake, the gilded chest&is", 'location'),
             'Gerudo Training Grounds Underwater Silver Rupee Chest': ("They say training underwater&grants", 'location'),
             'Gerudo Training Grounds Maze Path Final Chest':         ("Past all the locked doors&is", 'location'),
             'Bottom of the Well Defeat Boss':                        ("The say Dead Hand&holds", 'location'),
             'Bottom of the Well Underwater Left Chest':              ("A watery prison holds", 'location'),
             'Silver Gauntlets Chest':                                ("Upon the Colossus's southern edge&is", 'location'),
             'Mirror Shield Chest':                                   ("Upon the Colossus's northern edge&is", 'location'),
             'Shadow Temple Hidden Floormaster Chest':                ("A shadow in the maze&hides", 'location'),
             'Haunted Wasteland Structure Chest':                     ("They say deep in the Wasteland&is", 'location'),
             'Composer Grave Chest':                                  ("The Composer Brothers&hid", 'location'),
             'Song from Composer Grave':                              ("The Composer Brothers&wrote", 'location'),
             'Song at Windmill':                                      ("Guru-guru is driven mad&by", 'location'),
             'Sheik Forest Song':                                     ("In the forest Sheik&teaches", 'location'),
             'Sheik at Temple':                                       ("Sheik waits with time to&teach", 'location'),
             'Sheik in Crater':                                       ("The craters melody&is", 'location'),
             'Sheik in Ice Cavern':                                   ("The frozen cavern&echoes", 'location'),
             'Sheik in Kakariko':                                     ("The stormy village&plays", 'location'),
             'Sheik at Colossus':                                     ("Trek past the Wasteland to&learn", 'location'),
             '1001':                                                  ("Ganondorf 2020!", 'junkHint'),
             '1002':                                                  ("They say that monarchy is a&terrible system of governance.", 'junkHint'),
             '1003':                                                  ("They say that Zelda is a poor&leader.", 'junkHint'),
             '1004':                                                  ("These hints can be quite useful.&This is an exception.", 'junkHint'),
             '1005':                                                  ("The Stone of Agony is in your&inventory.", 'junkHint'),
             '1006':                                                  ("They say that all the Zora drowned&in Wind Waker.", 'junkHint'),
             '1007':                                                  ("They say that PJ64 is a terrible&emulator.", 'junkHint'),
             '1008':                                                  ("'Member when Ganon was a blue pig.^I 'member.", 'junkHint'),
             '1009':                                                  ("One who does not have Triforce&can't go in.", 'junkHint'),
             '1010':                                                  ("Save your future,&end the Happy Mask Salesmen.", 'junkHint'),
             '1011':                                                  ("Early Agony equals likely&troll seed.", 'junkHint'),
             '1012':                                                  ("I'm stoned. Get it?", 'junkHint'),
             '1013':                                                  ("Hoot! Hoot! Would you like me to&repeat that?", 'junkHint'),
             '1014':                                                  ("Gorons are stupid.&They eat rocks.", 'junkHint'),
             '1015':                                                  ("They say that Lon Lon Ranch&prospered under Ingo.", 'junkHint'),
             '1016':                                                  ("The single rupee is a&unique item.", 'junkHint'),
             '1017':                                                  ("Without Lens, Treasure Chest Game&is a 1 of 32 chance. GL!", 'junkHint'),
             '1018':                                                  ("Use bombs wisely.", 'junkHint'),
             '1019':                                                  ("Bomchus are not considered&in logic.", 'junkHint'),
             '1021':                                                  ("I found you faker!", 'junkHint'),
             '1022':                                                  ("You're comparing&yourself to me.", 'junkHint'),
             '1023':                                                  ("Ha! You're not even good&enough to be my fake.", 'junkHint'),
             '1024':                                                  ("I'll make you eay those words.", 'junkHint'),
             '1025':                                                  ("What happened to Sheik?", 'junkHint'),
             '1026':                                                  ("L2P @.", 'junkHint'),
             '1027':                                                  ("I heard @ isn't&very good at Zelda.", 'junkHint'),
             '1028':                                                  ("I'm Lunk from Pennsylvania.", 'junkHint')}

                        
             
             
             
             
             
             
             
             
             
             
             
             
                     
                     
                                                    
