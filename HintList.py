import random

class Hint(object):
    name = ""
    text = ""
    type = ""

    def __init__(self, name, text, type):
        self.name = name
        self.text = text
        self.type = type

def _getHint(name):
    textOptions, type = hintTable[name]
    # Because it doesn't make sense to offer random variants of some hints
    if isinstance(textOptions, str):
        return (textOptions, type)
    else:
        return (random.choice(textOptions), type)

def getHint(name):
    ret = Hint
    for hint in hintTable:
        if name == hint:
            text, type = _getHint(hint)
            ret = Hint(hint, text, type)
            break
        else:
            text, type = _getHint('KeyError')
            ret = Hint(hint, text, type)
    return ret

def getHintGroup(group, world):
    ret = []
    for hint in hintTable:
        text, type = _getHint(hint)
        if type == group and not (hint in hintExclusions(world)):
            ret.append(Hint(hint, text, type))
    return ret

#table of hints, format is (name, hint text, type of hint) there are special characters that are read for certain in game commands:
# ^ is a box break
# & is a new line
# @ will print the player name
# # sets color to white (currently only used for dungeon reward hints).
hintTable = {'Hammer':                                                (["the dragon smasher", "a metallic crusher", "the WHAM! weapon"], 'item'),
             'Magic Meter':                                           (["pixie dust", "ability fuel"], 'item'),
             'Double Defense':                                        (["a white outline", "sturdy hearts", "strengthened love"], 'item'),
             'Progressive Hookshot':                                  (["Dampe's keepsake", "an arm extension", "a great chain"], 'item'),
             'Progressive Strength Upgrade':                          (["power gloves", "arm day results", "heavy object lifters"], 'item'),
             'Hover Boots':                                           (["butter boots", "slippery shoes", "spacewalkers"], 'item'),
             'Master Sword':                                          (["evil's bane"], 'item'),
             'Mirror Shield':                                         (["the reflective rampart", "Medusa's weakness"], 'item'),
             'Farores Wind':                                          (["teleportation", "relocation magic", "a warp spell", "green wind"], 'item'),
             'Nayrus Love':                                           (["a safe space", "an impregnable aura"], 'item'),
             'Ice Arrows':                                            (["the refrigerator rocket", "frostbite bolts", "cold darts", "freezing projectiles"], 'item'),
             'Lens of Truth':                                         (["the perjureless porthole", "true sight", "a detective's tool"], 'item'),
             'Dins Fire':                                             (["an inferno", "a great heat wave", "a blast of hot air"], 'item'),
             'Ocarina':                                               (["a flute", "a source of music"], 'item'),
             'Fairy Ocarina':                                         (["a brown flute", "a forest instrument"], 'item'),
             'Goron Tunic':                                           (["ruby robes", "fireproof garbs", "mountain clothing"], 'item'),
             'Zora Tunic':                                            (["a sapphire suit", "a fishy outfit", "lake clothing"], 'item'),
             'Iron Boots':                                            (["sink shoes", "watery footwear", "noisy boots"], 'item'),
             'Zeldas Letter':                                         (["an autograph", "royal stationary", "royal snail mail"], 'item'),
             'Zeldas Lullaby':                                        (["a song of royal slumber", "a triforce tune"], 'item'),
             'Nocturne of Shadow':                                    (["a song of spooky spirits", "a graveyard boogie", "a ghastly tune"], 'item'),
             'Bow':                                                   (["an archery enabler", "a danger dart launcher"], 'item'),
             'Bomb Bag':                                              (["an explosive container", "kaboom storage"], 'item'),
             'Sarias Song':                                           (["a song of dancing Gorons", "a green girl's tune", "child's forest melody"], 'item'),
             'Song of Time':                                          (["a song 7 years long", "a tune to move blocks"], 'item'),
             'Song of Storms':                                        (["Rain Dance", "a thunderstorm melody", "the tune of windmills"], 'item'),
             'Minuet of Forest':                                      (["the song of tall trees", "adult's forest melody", "a green warp song"], 'item'),
             'Requiem of Spirit':                                     (["a song of sandy statues", "an orange warp song", "the tune of the desert"], 'item'),
             'Slingshot':                                             (["a seed shooter", "a child's catapult"], 'item'),
             'Boomerang':                                             (["a banana"], 'item'),
             'Fire Arrows':                                           (["flame darts", "burning projectiles"], 'item'),
             'Ocarina of Time':                                       (["a blue flute", "a royal instrument", "a paint-job"], 'item'),
             'Bottle':                                                (["a glass container", "an empty jar", "something to be filled"], 'item'),
             'Bottle with Letter':                                    (["a call for help", "an SOS jar", "a princess's glass"], 'item'),
             'Bottle with Milk':                                      (["cow juice", "a white liquid"], 'item'),
             'Bottle with Red Potion':                                (["a vitality vial", "a red liquid"], 'item'),
             'Bottle with Green Potion':                              (["a magic mixture", "a green liquid"], 'item'),
             'Bottle with Blue Potion':                               (["a cure-all antidote", "a blue liquid"], 'item'),
             'Bottle with Fairy':                                     (["an imprisoned pixie", "an extra life"], 'item'),
             'Bottle with Fish':                                      (["an aquarium", "a contained sea beast"], 'item'),
             'Bottle with Blue Fire':                                 (["a conflagration canteen", "an icemelt jar"], 'item'),
             'Bottle with Bugs':                                      (["a terrarium", "skultula finders", "a digging trio"], 'item'),
             'Bottle with Poe':                                       (["a spooky ghost", "a face in the jar"], 'item'),
             'Progressive Scale':                                     (["vertical swim depth", "a dive enhancer"], 'item'),
             'Stone of Agony':                                        (["an empty chest", "a vibrating rock", "a clue finder"], 'item'),
             'Eponas Song':                                           (["an equestrian etude", "a ranch song"], 'item'),
             'Epona':                                                 (["a horse", "a four legged friend"], 'item'),
             'Gerudo Membership Card':                                (["a GT subscription", "a desert tribe's pass"], 'item'),
             'Progressive Wallet':                                    (["a mo' money holder", "a gem purse", "financial capacity"], 'item'),
             'Bolero of Fire':                                        (["a song of lethal lava", "a red warp song", "a volcano tune", "a song of a red sea"], 'item'),
             'Suns Song':                                             (["Sunny Day", "a time advancer", "a day/night melody", "the gibdo's bane"], 'item'),
             'Deku Shield':                                           (["a wooden ward", "forest protection"], 'item'),
             'Hylian Shield':                                         (["a steel safeguard", "a Hylian relic", "metallic protection"], 'item'),
             'Deku Stick Capacity':                                   (["a bundle of sticks", "more flammable twigs"], 'item'),
             'Deku Nut Capacity':                                     (["more nuts", "flashbang storage"], 'item'),
             'Prelude of Light':                                      (["a luminous prologue melody", "a yellow warp song", "the temple traveler"], 'item'),
             'Serenade of Water':                                     (["a song of a damp ditch", "a blue warp song", "the lake's tune"], 'item'),
             'Heart Container':                                       (["a lot of love", "a Valentine's gift", "a boss's organ"], 'item'),
             'Piece of Heart':                                        (["love", "a partial Valentine"], 'item'),
             'Piece of Heart (Treasure Chest Game)':                  (["love", "a partial Valentine"], 'item'),
             'Recovery Heart':                                        (["a free heal", "disappointing love"], 'item'),
             'Rupee (1)':                                             (["a unique coin", "a penny", "a tiny coin", "a green gem"], 'item'),
             'Rupees (5)':                                            (["a common coin", "a blue gem"], 'item'),
             'Rupees (20)':                                           (["couch cash", "a red gem"], 'item'),
             'Rupees (50)':                                           (["big bucks", "a purple gem", "wealth"], 'item'),
             'Rupees (200)':                                          (["a juicy jackpot", "a yellow gem", "great wealth"], 'item'),
             'Light Arrows':                                          (["the shining shot", "glowing darts", "Ganondorf's bane"], 'item'),
             'Kokiri Sword':                                          (["a butter knife", "a child's blade"], 'item'),
             'Biggoron Sword':                                        (["a shield disabler", "a two-handed blade"], 'item'),
             'Pocket Egg':                                            (["a Cucco container", "a Cucco, eventually", "a fowl youth"], 'item'),
             'Weird Egg':                                             (["a strange gamete"], 'item'),
             'Pocket Cucco':                                          (["a little clucker"], 'item'),
             'Cojiro':                                                (["a cerulean capon"], 'item'),
             'Odd Mushroom':                                          (["a powder ingredient"], 'item'),
             'Odd Potion':                                            (["Granny's goodies"], 'item'),
             'Poachers Saw':                                          (["a tree killer"], 'item'),
             'Broken Sword':                                          (["a shattered slicer"], 'item'),
             'Prescription':                                          (["a pill pamphlet", "a Doctor's slip"], 'item'),
             'Eyeball Frog':                                          (["a perceiving polliwog"], 'item'),
             'Eyedrops':                                              (["a vision vial"], 'item'),
             'Claim Check':                                           (["a three day wait"], 'item'),
             'Map':                                                   (["a dungeon atlas"], 'item'),
             'Compass':                                               (["a treasure tracker"], 'item'),
             'BossKey':                                               (["a master of unlocking", "a dungeon's final pass"], 'item'),
             'SmallKey':                                              (["a tool for unlocking", "a dungeon pass", "a lock remover", "a more legal lockpick", "a portal opener"], 'item'),
             'FortressSmallKey':                                      (["a get out of jail free card"], 'item'),
             'KeyError':                                              (["something mysterious", "an unknown treasure"], 'item'),
             'Arrows (5)':                                            (["danger darts", "piercing ammunition", "a quiver's contents"], 'item'),
             'Arrows (10)':                                           (["danger darts", "piercing ammunition", "a quiver's contents"], 'item'),
             'Arrows (30)':                                           (["danger darts", "piercing ammunition", "a quiver's contents"], 'item'),
             'Bombs (5)':                                             (["explosives", "sparky boom balls"], 'item'),
             'Bombs (10)':                                            (["explosives", "sparky boom balls"], 'item'),
             'Bombs (20)':                                            (["lots-o-explosives", "sparky boom balls"], 'item'),
             'Ice Trap':                                              (["a gift from Ganon", "a chilling discovery", "an icy blast", "an unwanted freeze", "a wintery surprise"], 'item'),
             'Magic Bean':                                            (["wizardly legumes"], 'item'),
             'Bombchus':                                              (["mice bombs", "hot-headed friends"], 'item'),
             'Bombchus (5)':                                          (["mice bombs", "hot-headed friends"], 'item'),
             'Bombchus (10)':                                         (["mice bombs", "hot-headed friends"], 'item'),
             'Bombchus (20)':                                         (["mice bombs", "hot-headed friends"], 'item'),
             'Deku Nuts (5)':                                         (["some nuts", "some flashbangs", "Sheik's ammo"], 'item'),
             'Deku Nuts (10)':                                        (["lots-o-nuts", "lots of flashbangs", "Sheik's ammo"], 'item'),
             'Gold Skulltulla Token':                                 (["proof of destruction", "an arachnid chip", "spider remains"], 'item'),

             '10 Big Poes':                                           (["They say that Big Poes leads to", "They say that ghost hunters will be rewarded with"], 'alwaysLocation'),
             'Deku Theater Mask of Truth':                            ("They say that the Mask of Truth yields", 'alwaysLocation'),
             '30 Gold Skulltulla Reward':                             ("They say that slaying 30 Gold Skulltulas reveals", 'alwaysLocation'),
             '40 Gold Skulltulla Reward':                             ("They say that slaying 40 Gold Skulltulas reveals", 'alwaysLocation'),
             '50 Gold Skulltulla Reward':                             ("They say that slaying 50 Gold Skulltulas reveals", 'alwaysLocation'),
             'Song from Ocarina of Time':                             ("They say the Ocarina of Time teaches", 'alwaysLocation'),
             'Biggoron':                                              ("They say that Biggoron crafts", 'alwaysLocation'),
             'Child Fishing':                                         ("They say that fishing in youth bestows", 'location'),
             'Adult Fishing':                                         ("They say that fishing in maturity bestows", 'location'),
             '20 Gold Skulltulla Reward':                             ("They say that slaying 20 Gold Skulltulas reveals", 'location'),
             'Treasure Chest Game':                                   (["They say that gambling grants", "They say there is a 1/32 chance to win"], 'location'),
             'Darunias Joy':                                          ("They say that Darunia's dance leads to", 'location'),
             'Frog Ocarina Game':                                     (["They say The Frogs of Zora River hold", "They say that the musical amphibians have found"], 'location'),
             'Horseback Archery 1500 Points':                         ("They say that mastery of horseback archery grants", 'location'),
             'Lake Hylia Sun':                                        (["They say staring into the sun grants", "They say that acts of solar aggression are punished with"], 'location'),
             'Heart Piece Grave Chest':                               ("They say there's a hidden location where the Sun's Song spawns", 'location'),
             'Goron City Leftmost Maze Chest':                        ("They say in Goron City the hammer unlocks", 'location'),
             'Chest Above King Dodongo':                              ("They say that the chest above the Infernal Dinosaur contains", 'location'),
             'Forest Temple Floormaster Chest':                       ("Deep in the forest, shadows guard a chest containing", 'location'),
             'Fire Temple Scarecrow Chest':                           ("They say high in the Fire Temple, Pierre hid", 'location'),
             'Fire Temple Megaton Hammer Chest':                      (["They say that the highest chest in the crater holds"], 'location'),
             'Water Temple River Chest':                              ("They say deep under the lake, beyond the currents, hides", 'location'),
             'Water Temple Boss Key Chest':                           ("Deep under the lake, the gilded chest contains", 'location'),
             'Gerudo Training Grounds Underwater Silver Rupee Chest': ("They say those who seek sunken silver rupees will find", 'location'),
             'Gerudo Training Grounds Maze Path Final Chest':         ("They say that past all the locked doors is", 'location'),
             'Bottom of the Well Defeat Boss':                        (["They say that Dead Hand holds", "They say that draining the water reveals a monster guarding"], 'location'),
             'Silver Gauntlets Chest':                                ("They say that upon the Colossus's southern edge is", 'location'),
             'Mirror Shield Chest':                                   ("They say that upon the Colossus's northern edge is", 'location'),
             'Shadow Temple Hidden Floormaster Chest':                (["They say in a maze guarded by shadows hides", "They say that after a free boat ride comes"], 'location'),
             'Haunted Wasteland Structure Chest':                     (["They say that deep in the Wasteland is", "They say that beneath the sands lies"], 'location'),
             'Composer Grave Chest':                                  ("They say that the Composer Brothers hid", 'location'),
             'Song from Composer Grave':                              ("They say that the Composer Brothers wrote", 'location'),
             'Song at Windmill':                                      (["They say that Guru-guru is driven mad by", "They say the windmill echoes with"], 'location'),
             'Sheik Forest Song':                                     ("They say that deep in the forest Sheik teaches", 'location'),
             'Sheik at Temple':                                       ("They say that Sheik waits at a monument to time to teach", 'location'),
             'Sheik in Crater':                                       ("They say that the crater's melody is", 'location'),
             'Sheik in Ice Cavern':                                   ("They say that the frozen cavern echoes with", 'location'),
             'Sheik in Kakariko':                                     ("They say that a ravaged village mourns with", 'location'),
             'Sheik at Colossus':                                     ("They say that a hero ventures beyond the Wasteland to learn", 'location'),
             'Zoras Fountain Bottom Freestanding PoH':                ("They say under the icy waters lies", 'location'),
             'Colossus Freestanding PoH':                             ("They say that riding a beanstalk in the desert leads to", 'location'),
             'DM Crater Volcano Freestanding PoH':                    ("They say that riding a beanstalk in the crater leads to", 'location'),
             'Goron City Pot Freestanding PoH':                       ("They say that spinning Goron pottery contains", 'location'),

             '1001':                                                  ("Ganondorf 2020!", 'junkHint'),
             '1002':                                                  ("They say that monarchy is a terrible system of governance.", 'junkHint'),
             '1003':                                                  ("They say that Zelda is a poor leader.", 'junkHint'),
             '1004':                                                  ("These hints can be quite useful. This is an exception.", 'junkHint'),
             '1006':                                                  ("They say that all the Zora drowned in Wind Waker.", 'junkHint'),
             '1007':                                                  ("They say that PJ64 is a terrible emulator.", 'junkHint'),
             '1008':                                                  ("'Member when Ganon was a blue pig?^I 'member.", 'junkHint'),
             '1009':                                                  ("One who does not have Triforce can't go in.", 'junkHint'),
             '1010':                                                  ("Save your future, end the Happy Mask Salesman.", 'junkHint'),
             '1012':                                                  ("I'm stoned. Get it?", 'junkHint'),
             '1013':                                                  ("Hoot! Hoot! Would you like me to repeat that?", 'junkHint'),
             '1014':                                                  ("Gorons are stupid. They eat rocks.", 'junkHint'),
             '1015':                                                  ("They say that Lon Lon Ranch prospered under Ingo.", 'junkHint'),
             '1016':                                                  ("The single rupee is a unique item.", 'junkHint'),
             '1017':                                                  ("Without the Lens of Truth, the Treasure Chest Mini-Game is a 1 out of 32 chance.^Good luck!", 'junkHint'),
             '1018':                                                  ("Use bombs wisely.", 'junkHint'),
             '1021':                                                  ("I found you, faker!", 'junkHint'),
             '1022':                                                  ("You're comparing yourself to me?^Ha! You're not even good enough to be my fake.", 'junkHint'),
             '1023':                                                  ("I'll make you eat those words.", 'junkHint'),
             '1024':                                                  ("What happened to Sheik?", 'junkHint'),
             '1025':                                                  ("L2P @.", 'junkHint'),
             '1026':                                                  ("I heard @ isn't very good at Zelda.", 'junkHint'),
             '1027':                                                  ("I'm Lonk from Pennsylvania.", 'junkHint'),
             '1028':                                                  ("I bet you'd like to have more bombs.", 'junkHint'),
             '1029':                                                  ("When all else fails, use Fire.", 'junkHint'),
             '1030':                                                  ("Here's a hint, @. Don't be bad.", 'junkHint'),
             '1031':                                                  ("Game Over. Return of Ganon.", 'junkHint'),
             '1032':                                                  ("May the way of the Hero lead to the Triforce.", 'junkHint'),
             '1033':                                                  ("Can't find an item? Scan an Amiibo.", 'junkHint'),
             '1034':                                                  ("They say this game has just a few glitches.", 'junkHint'),
             '1035':                                                  ("BRRING BRRING This is Ulrira. Wrong number?", 'junkHint'),
             '1036':                                                  ("Tingle! Tingle! Kooloo, Limpah!", 'junkHint'),
             '1037':                                                  ("L is real 2041", 'junkHint'),
             '1038':                                                  ("They say that Ganondorf will appear in the next Mario Tennis.", 'junkHint'),
             '1039':                                                  ("Medigoron sells the earliest Breath of the Wild demo.", 'junkHint'),
             '1040':                                                  ("There's a reason why I am special inquisitor!", 'junkHint'),
             '1041':                                                  ("You were almost a @ sandwich.", 'junkHint'),
             '1042':                                                  ("I'm a helpful hint Gossip Stone!^See, I'm helping.", 'junkHint'),
             '1043':                                                  ("Dear @, please come to the castle. I've baked a cake for you.&&Yours truly, princess Zelda.", 'junkHint'),
             '1044':                                                  ("I like shorts! They're comfy and easy to wear!", 'junkHint'),
             '1044':                                                  ("They say all toasters toast toast.", 'junkHint'),
             '1045':                                                  ("They say that Okami is the best Zelda game.", 'junkHint'),
             '1046':                                                  ("They say that quest guidance can be found at a talking rock.", 'junkHint'),
             '1047':                                                  ("They say that victory can be found after the Ganon fight.", 'junkHint'),
             '1047':                                                  ("They say that the final item you're looking for can be found somewhere in Hyrule", 'junkHint'),
                                                                       #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx handy marker for how long one line should be in a text box
             'Deku Tree':                                             ("an ancient tree", 'dungeon'),
             'Dodongos Cavern':                                       ("an immense cavern", 'dungeon'),
             'Jabu Jabus Belly':                                      ("the belly of a deity", 'dungeon'),
             'Forest Temple':                                         ("a deep forest", 'dungeon'),
             'Fire Temple':                                           ("a high mountain", 'dungeon'),
             'Water Temple':                                          ("a vast lake", 'dungeon'),
             'Shadow Temple':                                         ("the house of the dead", 'dungeon'),
             'Spirit Temple':                                         ("the goddess of the sand", 'dungeon'),
             'Ice Cavern':                                            ("a frozen maze", 'dungeon'),
             'Bottom of the Well':                                    ("a shadow\'s prison", 'dungeon'),
             'Gerudo Training Grounds':                               ("the test of thieves", 'dungeon'),
             'Ganons Castle':                                         ("a conquered citadel", 'dungeon'),
                                                                       #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx handy marker for how long one line should be in a text box             
             'Queen Gohma':                                           ("One inside an #ancient tree#...^", 'boss'),
             'King Dodongo':                                          ("One within an #immense cavern#...^", 'boss'),
             'Barinade':                                              ("One in the #belly of a deity#...^", 'boss'),
             'Phantom Ganon':                                         ("One in a #deep forest#...^", 'boss'),
             'Volvagia':                                              ("One on a #high mountain#...^", 'boss'),
             'Morpha':                                                ("One under a #vast lake#...^", 'boss'),
             'Bongo Bongo':                                           ("One within the #house of the dead#...^", 'boss'),
             'Twinrova':                                              ("One inside a #goddess of the sand#...^", 'boss'),
             'Links Pocket':                                          ("One in #@'s pocket#...^", 'boss'),
             'Spiritual Stone Text Start':                            ("Ye who owns 3 Spiritual Stones...^", 'boss'),
             'Spiritual Stone Text End':                              ("Stand with the Ocarina of Time&and play the Song of Time.", 'boss'),
             'Medallion Text End':                                    ("Together with the Hero of Time,&the awakened ones will bind the&evil and return the light of peace&to the world.", 'boss'),
                                                                       #xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx handy marker for how long one line should be in a text box
             'Validation Line':                                       ("Hmph... Since you made it this far,&I'll let you know what glorious&prize of Ganon's you likely&missed out on in my tower.^Behold...^", 'validation line'),
             'Light Arrow Location':                                  ("Ha ha ha... You'll never beat me by&reflecting my lightning bolts&and unleashing the arrows from&", 'Light Arrow Location'),
             '2001':                                                  ("Oh! It's @.&I was expecting someone called&Sheik. Do you know what&happened to them?", 'ganonLine'), 
             '2002':                                                  ("I knew I shouldn't have put the key&on the other side of my door.", 'ganonLine'),
             '2003':                                                  ("Looks like it's time for a&round of tennis.", 'ganonLine'),
             '2004':                                                  ("You'll never deflect my bolts of&energy with your sword,&then shoot me with those Light&Arrows you happen to have.", 'ganonLine'),
             '2005':                                                  ("Why did I leave my trident&back in the desert?", 'ganonLine'),
             '2006':                                                  ("Zelda is probably going to do&something stupid, like send you&back to your own timeline.^So this is quite meaningless.&Do you really want&to save this moron?", 'ganonLine'),
             '2007':                                                  ("What about Zelda makes you think&she'd be a better ruler than I?^I saved Lon Lon Ranch,&fed the hungry,&and my castle floats.", 'ganonLine'),
             '2008':                                                  ("I've learned this spell,&it's really neat,&I'll keep it later&for your treat!", 'ganonLine'),
             '2009':                                                  ("Many tricks are up my sleeve,&to save yourself&you'd better leave!", 'ganonLine'),
             '2010':                                                  ("After what you did to&Koholint Island, how can&you call me the bad guy?", 'ganonLine'),
             '2011':                                                  ("Today, let's begin down&'The Hero is Defeated' timeline.", 'ganonLine'),
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
