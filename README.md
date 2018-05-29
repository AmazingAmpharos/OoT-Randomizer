# OoTRandomizer

This is a randomizer for _The Legend of Zelda: Ocarina of Time_ for the Nintendo 64.

# Installation

Clone this repository and then run ```OoTRandomizer.py``` (requires Python 3).

Alternatively, run ```Gui.py``` for a simple graphical user interface.

For releases, a Windows standalone executable is available for users without Python 3.

This randomizer requires The Legend of Zelda: Ocarina of Time version 1.0 NTSC-US version. Upon first being run, the randomizer will automatically
create a decompressed version of this ROM that can be used for input for slightly faster seed generation times. Please be sure your input ROM filename
is either a .n64 or .z64 file. For users playing via any means other than on real N64 hardware, the use of the "Compress patched ROM" flag is strongly
encouraged as uncompressed ROMs are impossible to inject for the Virtual Console and have random crashing problems on all emulators.

For general use, the recommended emulators are Bizhawk and Mupen64plus. If you want to play on Project 64 for whatever reason, you can but
you will need to set the rando to use 8 MB of RAM and will want to play with the cheat code 8109C58A 0000 to partially fix Project 64's tragically
poor handling of OoT's pause menu. As of this 1.0 release, there are suspected crashing issues specifically with Project 64. I cannot emphasize enough
that it is a discouraged emulator to use.

# General Description

This program takes _The Legend of Zelda: Ocarina of Time_ and randomizes the locations of the items for a more dynamic play experience.
Proper logic is used to ensure every seed is possible to complete without the use of glitches and will be safe from the possibility of softlocks
with any possible usage of keys in dungeons.

The items that randomize currently are all items within chests, items given as rewards by NPCs including from minigames and Deku Scrub salesmen, and
the items obtained when getting the Bottle and the Fire Arrows at Lake Hylia. Due to technical limitations, chests in "generic" grottos are not randomized,
but chests in unique grottos are (one in Kakariko, one in the Sacred Forest Meadow). All dungeons will always have the same number of Maps, Compasses,
Small Keys, and Boss Keys they had in the original game, but which chests within those dungeons have those things is random. The item pool will contain a
Biggoron Sword that will not interfere with Medigoron's sale of the Giant's Knife (which is always vanilla), and a randomly selected adult trading quest item
other than the Odd Potion will be somewhere in the item pool.

Certain types of items are now "progressive", meaning that no matter what order the player encounters these items they will function as a series of upgrades.
The following item types will be progressive chains:

-Hookshot to Longshot
-Bomb Bag to Big Bomb Bag to Biggest Bomb Bag
-Goron Bracelet to Silver Gauntlets to Gold Gauntlets
-Slingshot to Big Bullet Bag to Biggest Bullet Bag
-Bow to Big Quiver to Biggest Quiver
-Silver Scale to Gold Scale
-Adult Wallet to Giant's Wallet
-Deku Stick Capacity Upgrades
-Deku Nut Capacity Upgrades
-Magic Meter to Double Magic

To be more clear about which NPC items are shuffled, it's NPCs who directly give you the item (so not the freestanding Pieces of Heart you can get from Dampe),
and it's only the one time permanent item rewards for the most part like NPCs who originally gave Pieces of Heart or inventory items. The only exception is that
even though in vanilla the reward for 40 Gold Skulltulla Tokens was just 10 Bombchus that is still a randomized reward in randomizer (but the 200 rupees for all
100 Gold Skulltulla Tokens is not randomized so the most tokens that could be required to complete a seed is 50). As a mercy to the player, the Ocarina Memory Game
in the Lost Woods will start on the final round as that minigame was very long originally, the three day wait on the Claim Check is removed, and Bombchu Bowling will
have a fixed sequence of prizes that is of maximum convenience to the player. Additionally, any NPC who gives a trading quest item either for the child or for the
adult other than Anju's initial gift as an adult does not have a randomized reward, and as a design decision, the Fairy Ocarina and Ocarina of Time are not randomized.

A special note is needed for the six Great Fairy Fountains scattered across Hyrule. These six fountains are randomized amongst themselves, and while they all still
require Zelda's Lullaby to utilize, none of them require a Magic Meter to obtain the reward. The two that give variations on the Magic Meter in vanilla are modeled
as progressives; the first the player uses will give a Magic Meter and the magic spin attack while the second will give the Double Magic upgrade.

The Ocarina songs are shuffled in a pool amongst themselves, and each learn spot will still have the original conditions it has always had. These conditions may not
have all been obvious, but here are some high points. Saria will teach her song after completing the events in the Castle Courtyard. The warp songs can mostly only
be learned by an adult, but the location for Requiem of Spirit is available for even a child if the Desert Colossus can be reached. The location for the Prelude of
Light requires the Forest Medallion, and the location for the Nocturne of Shadow requires the Forest Medallion, Fire Medallion, and Water Medallions.

Speaking of Medallions, each boss in the eight main dungeons will drop a random Spiritual Stone or Medallion, and instead of the Light Medallion being granted by the
now removed "becoming an adult" cutscene, the player will start every seed with a random Spiritual Stone or Medallion. The pedestal in which the Spiritual Stones
rest in the Temple of Time has hint text pointing to the locations of the Spiritual Stones and Medallions. A child will be able to read hints for the Spiritual
Stones while an adult will be able to read hints for the Medallions.

To be very clear on this point, freestanding Pieces of Heart (those not in chests or given directly by NPCs) are not randomized, and while the rewards for up to 50
Gold Skulltulla Tokens are randomized, the tokens themselves are not.

As a service to the player in this very long game, many cutscenes have been greatly shortened or removed and text is as often as possible either omitted or sped up.
We have been as thorough as our exploration of the game and various technical limitations will allow to make the parts of the game where you're watching and reading
as short as possible to make as much of your time with this randomizer as possible actual gameplay. I'm sure someone somewhere will miss the owl's interjections; to
that person, I'm sorry I guess?

A few bugs or other undesirable behaviors in the original game have been fixed. Of note, obtaining the Poacher's Saw will no longer prevent the player from obtaining
the reward in the Deku Theater for showing the Mask of Truth, and becoming an adult will not automatically equip the child with the Kokiri Sword. Sheik will no longer
prevent the player from returning to childhood before obtaining the Forest Medallion. Princess Ruto will never disappear from Jabu Jabu's Belly, and the condition for
the Castle Courtyard being sealed off is now completing the events within as opposed to seeing the Ocarina of Time be thrown into the moat.

One small detail that is important to know is that the locked door in the Fire Temple leading to the section with the Boss Key Chest is removed. This was necessary
due to the original design of the Fire Temple assuming that the player could not possibly have the Hammer before unlocking the doors leading into the depths of the
dungeon. This is obviously not true in randomizer, and of all possible solutions to this problem, this seemed the least disruptive. A full clear of the Fire Temple will
simply result in the player having one extra Small Key.

To be clear about the logic rules of what can be where, the randomizer will ensure a glitchless path through the seed will exist, but the randomizer will not prevent
the use of glitches for those players who enjoy that sort of thing though we offer no guarantees that all glitches will have identical behavior to the original game.
Glitchless can still mean that clever or unintuitive strategies may be required involving the use of things like Hover Boots, the Hookshot, or Scarecrow's Song that
may not have been important options in the original game. The Lens of Truth is guaranteed available and useable before completion of the Treasure Chest Game is required
or before walking through any invisible objects or opening any invisible chests is required with the exception of the one invisible wall that is required to enter
the Bottom of the Well as the original game required passing that invisible wall to reach the Lens of Truth.

One last detail is that the menu is now more like the Majora's Mask menu in that the player can move the cursor through empty spaces. This fixes a major problem from
the original game in that certain combinations of items would create menu shapes that would be impossible to fully menu through.

# Quirks to Know

While all the details of gameplay can't be detailed here, I want to inform you of a few non-obvious game sequences that are likely to get you stuck and one little
glitch we can do nothing about.

-The condition to open the Door of Time is merely playing the Song of Time; the Spiritual Stones are not required. If you enter the Temple of Time via the Prelude
of Light, playing the Song of Time will create a glitchy cutscene and will not open the door (but you're safe to exit and re-enter and open it properly).  
-The condition to spawn the Ocarina of Time and learn that song is the three Spiritual Stones. The condition to learn a song from Sheik in the Temple of Time is
possessing the Forest Medallion. The condition to learn a song from Sheik in Kakariko is possessing Forest, Fire, and Water Medallions.  
-The running man in Hyrule Field only spawns if you have all three Spiritual Stones.  
-Skull Kid will only buy the Skull Mask if you have played Saria's Song for him.  
-The center of Death Mountain Crater as an adult can be reached from the summit as an adult by going around to the left with Hover Boots or by jumping down to the right
and using a combination of the Longshot and Scarecrow's Song. This allows access to Sheik and the Fire Temple without a Bomb Bag.  
-A sword must be equipped to play the fishing minigame. A Slingshot is not required for child target shooting, but the adult does need the Bow.  
-Other than those minigames, the child can do anything that would seem to require the sword with Deku Sticks. You can buy as many as you want in the Kokiri Forest shop.  
-In the randomizer, possessing the Bomb Bag is the requirement to get bomb drops, buy bombs or Bombchus, or play Bombchu Bowling.  
-Only the Hookshot, not the Longshot, is needed to do everything on the rooftops of Kakariko.  
-Grottos can be opened with either Bombs or the Hammer.  
-The boulder maze in Goron City can be solved with the Hammer or partially with Bombs as is obvious, but less obvious is that it can be fully solved with Silver Gauntlets.  
-The large colored blocks only encountered by the adult require Goron Bracelet to push.  
-Adult Link can fully clear Dodongo's Cavern. He can even skip the first section by virtue of being tall.  
-In the Forest Temple, you can reach the room with the Floormaster early by using Hover Boots in the block push room.  
-In the Fire Temple, you can reach the Boss Key door from the beginning with Hover Boots.  
-In the Water Temple, you can from the start with the water down jump to the middle platform level, very carefully aim the Hookshot to the target above, and pull yourself
to the highest level of the central platform. Then a very well spaced rolling jump can reach the water changing station to raise the water to the highest level. If you
make poor key choices in Water Temple, this may be what you need to do to untangle the situation.  
-In the Water Temple, Hover Boots can be used to reach the vanilla Boss Key chest without going through the room that requires Bombs and block pushing. Hover Boots can
also be used in this temple to avoid the Longshot requirement for the middle level chest that requires the Bow.  
-In the Shadow Temple, you can avoid the need for the Longshot in the room with the invisible spikes by backflipping onto the chest for extra height.  
-In the Spirit Temple, you can collect the silver rupees without Hover Boots by jumping directly onto the rolling boulder or with a jump slash.  
-In the Spirit Temple, you can use the Longshot to cross from the hand with the Mirror Shield in vanilla to the other hand.  
-While we guarantee tunics for Fire Temple and Water Temple, you can possibly force yourself to do without if you seriously let a Like Like eat the tunic and
then do not recover the tunic. It is almost always possible to do without, but it can make things really difficult on you.  
-Several Gold Skulltulla Tokens can be reached by clever/precise uses of jump slashes and spin attacks (possibly magic spin attacks).  

# Known issues

Sadly for this 1.0 release a few known issues exist. These will hopefully be addressed in future versions.

-The fishing minigame sometimes refuses to allow you to catch fish when playing specifically on Bizhawk. Save and quit (NOT savestate) and return to fix the issue.  
-Draining the Bottom of the Well with Song of Storms sometimes crashes on specific versions of Project 64. We aren't sure of the exact story, but this bug is easily
avoided by playing on a different emulator.  
-If the large rolling Goron in Goron City as a child has the same item as Link the Goron and the larger Goron's item is obtained first, Link the Goron will not give
his item. This mostly results in items like Piece of Heart being rendered unobtainable, but if a progressive lands in both of these spots, it could make an impossible
seed. The fix will simply be too complex to put in the 1.0 version, but this will be fixed soon.  
-Buying the Giant's Knife may be risky in 1.0. This needs more investigation.  
-Learning a warp song from Malon will break her script and cause Link to be unable to use the Ocarina until he leaves the current screen. Trying to switch which button
the Ocarina is on and use it in this situation can softlock the game. This will probably be very, very hard to fix; just don't try to get cute and live with the limitation
for now please.  
-Learning a warp song from Guru-Guru in the Windmill also breaks his script, but there are no known significant consequences.  
-Learning Sun's Song can warp Link out of the current cutscene in somewhat inconvenient ways. None of this should prevent completion of the seed, but it can be annoying.   
-There's a funny bug where sometimes obtaining Biggoron Sword displays a second erroneous text box. This has no gameplay consequence.  
-There's a reported but currently unconfirmed on modern code issue where somehow the child becomes erroneously equipped with Biggoron Sword. This should not be a disadvantage.
-Executing the collection delay glitch on various NPCs may have unpredictable and undesirable consequences.  
-The text for the Happy Mask Salesman is kinda wonky. Some of it is still slow, and one line flows out of the box. This should not impede your ability to play the game.  
-The Gorons return to Goron City based on possessing the Fire Medallion and not based on clearing Fire Temple currently. They don't really do anything, but it may weird you
out a bit.  
-Mido blocks you and complains about the Deku Tree being dead based on possession of the Kokiri Emerald and not on whether you've cleared Deku Tree currently. Just talk to him
to make him go away.  

# Settings

## Rainbow Bridge

This determines the condition under which the rainbow bridge to Ganon's Castle will spawn.

### Medallions

All six of the medallions are required to open Ganon's Castle.

### Vanilla

The rainbow bridge spawns under the same conditions it did in the original game, possession of the Light Arrows and having viewed the Zelda cutscene.

### All Dungeons

The rainbow bridge spawn requires all medallions and spiritual stones to be in the player's possession.

### Open

The rainbow bridge is always present.

## Create Spoiler Log

Output a Spoiler File.

## Do not Create Patched Rom

If set, will not produce a patched rom as output. Useful in conjunction with the spoiler log option to batch
generate spoilers for statistical analysis.

## Compress patched Rom

If set, the randomizer will additionally output a compressed ROM using Grant Man's bundled compressor. This compressor is the fastest
compressor out there and tuned specifically for this game, but in order to achieve its incredibly high speed, it does utilize every last bit
of CPU your computer will give it so your computer will slow to a crawl otherwise during the couple of minutes this will take.

## Open Forest

Mido does not need to see a sword and shield to reach the Deku Tree and the Kokiri boy blocking the exit to the forest is gone.
If this flag is not set, it is guaranteed that the Deku Tree can be completed without leaving the forest.

## Open Door of Time

The Door of Time is open from the beginning of the game. The Song of Time is only useful to move Song of Time blocks.

## Place Dungeon Items

If not set, Compasses and Maps are removed from the dungeon item pools and replaced by five rupee chests that may end up anywhere in the world.
This may lead to different amount of itempool items being placed in a dungeon than you are used to.

## Only Ensure Seed Beatable

If set, will only ensure that Ganon can be defeated, but not necessarily that all locations are reachable.

## Gossip Stone Hints with Stone of Agony

If set, the 32 Gossip Stones scattered across Hyrule will have various hints informing the player of which items are in various inconvenient locations. The
Stone of Agony is the condition to be able to talk to the Gossip Stones in this mode instead of the Mask of Truth out of mercy to the player. The nine locations
we regarded as the most generally inconvenient for all medallions play will always have hints, those hints will appear in two places, and the logic will guarantee
access to the Stone of Agony before those places must be checked. Those places are the rewards for 30, 40, and 50 Gold Skulltullas, both rewards from the fishing
minigame, the song from the Ocarina of Time, the item from showing the Mask of Truth in the Deku Theater, the item for defeating 10 Big Poes, and the item for
redeeming the Claim Check with Biggoron. There will be seven other hints that only exist once for other somewhat inconvenient places for which there is no
guarantee of Stone of Agony access, and there will be seven other sorts of remarks from the Gossip Stones in the hint pool that may bring a smile to your face but
will not provide you with unique information for your quest. The unreachable Gossip Stone in the Kokiri Forest is included in this 32 Gossip Stone hint shuffle as
well so be aware that one instance of a hint will seem to effectively vanish every seed.

## Seed

Can be used to set a seed number to generate. Using the same seed with same settings on the same version of the randomizer will always yield an identical output.

## Count

Use to batch generate multiple seeds with same settings. If a seed number is provided, it will be used for the first seed, then used to derive the next seed (i.e. generating 10 seeds with the same seed number given will produce the same 10 (different) roms each time).

# Command Line Options

```
-h, --help            
```

Show the help message and exit.

```
--create_spoiler      
```

Output a Spoiler File (default: False)

```
--bridge [{medallions,vanilla,dungeons,open}]
```

Select the condition to spawn the Rainbow Bridge to Ganon's Castle. (default: medallions)

```
--rom ROM
```

Path to a The Legend of Zelda: Ocarina of Time NTSC-US v1.0 ROM. (default: ZELOOTROMDEC.z64)

```
--loglevel [{error,info,warning,debug}]
```

Select level of logging for output. (default: info)

```
--seed SEED           
```

Define seed number to generate. (default: None)

```
--count COUNT         
```

Set the count option (default: None)

```
--open_forest
```

Set whether Kokiri children obstruct your path at the beginning of the game. (default: False)

```
--open_door_of_time
```

Set whether the Door of Time is open from the beginning of the game. (default: False)

```
--nodungeonitems
```

If set, Compasses and Maps are removed from the dungeon item pools and replaced by five rupee chests that may end up anywhere in the world.
This may lead to different amount of itempool items being placed in a dungeon than you are used to. (default: False)

```
--beatableonly
```

Enables the "Only Ensure Seed Beatable" option (default: False)

```
--hints
```

Gossip Stones provide helpful hints about which items are in inconvenient locations if the Stone of Agony is in the player's inventory. (default: False)

```
--suppress_rom
```

Enables the "Do not Create Patched Rom" option. (default: False)

```
--compress_rom
```

Create a compressed version of the output ROM file. (default: False)

```
--gui
```

Open the graphical user interface. Preloads selections with set command line parameters.
