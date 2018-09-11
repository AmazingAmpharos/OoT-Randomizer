# MMRandomizer

This is a randomizer for _The Legend of Zelda: Majora's Mask_ for the Nintendo 64. This program is currently not functional. I'm hoping that it will at least be able to generate spoiler logs by the end of the month. If you'd like to help out in any way, feel free to join the discord where we are coordinating things: https://discord.gg/2xpZYQq or submit a pull request, and somebody will probably merge it soon TM

# General Description

This program takes _The Legend of Zelda: Majora's Mask_ and randomizes the locations of the items for a more dynamic play experience.
Proper logic is used to ensure every seed is possible to complete without the use of glitches and will be safe from the possibility of softlocks
with any possible usage of keys in dungeons.

The items that randomize currently are all items within chests, items given as rewards by NPCs. All dungeons will always have the same number of Maps, Compasses, Small Keys, and Boss Keys they had in the original game, but which chests within those dungeons have those things is random. The item pool will contain all Stray Fairies that are placed in chests. Stray Fairies not found within a chest will be shuffled among themselves.

Certain types of items are now "progressive", meaning that no matter what order the player encounters these items they will function as a series of upgrades.
The following item types will be progressive chains:

-Bomb Bag to Big Bomb Bag to Biggest Bomb Bag
-Bow to Big Quiver to Biggest Quiver
-Adult Wallet to Giant's Wallet
-Magic Meter to Double Magic

The Ocarina songs are shuffled in a pool amongst themselves, and each learn spot will still have the original conditions it has always had. These conditions may not have all been obvious, but here are some high points (later).

Freestanding Pieces of Heart (those not in chests or given directly by NPCs) are not randomized yet, but the logic will pretend they are until any part of this actually hacks the ROM.

As this randomizer progresses, the aim will be to add an option to remove the most time wasting of cutscenes.

The randomizer will ensure a glitchless path through the seed will exist, but the randomizer will not prevent the use of glitches for those players who enjoy that sort of thing though we offer no guarantees that all glitches will have identical behavior to the original game. Glitchless can still mean that clever or unintuitive strategies may be required.


# Settings

## Moon Entry

This determines the condition under which the moon meadows will open for exploration. Entry will occur upon playing Oath to Order on the top of the Clock Tower.

### Open

Oath to Order is all that is required to enter the moon meadows.

### Vanilla

The moon meadows are reached under the same conditions they were in the original game, possession of all four boss remains.

### All Masks

Entering the moon meadows requires all 20 non transformation masks to be in the player's possession.

## Give Ocarina of Time

Skip needing to do the entire first part of the game up until obtaining the Ocarina of Time.

## Initial Form

Change which Link you start the game as. Except for when starting as human Link, learning the Song of Healing will award you the mask of the form you started in and return you to your human form. Note that changing to another transformation mask before finding the Song of Healing will leave you unable to return to this form. This by extension means that the Song of Healing will never be found in a location which requires you to use your initial form to obtain.

### Vanilla

Everything proceeds as it did in the original game. Link gets bullied by Skull Kid and human Link chases his horse until being transformed a Deku to do the rest.

### Human

Opening plays as usual until Link confronts the Skull Kid, and Skull Kid's magic has no effect, and then you spawn in the Clock Tower as human Link.

### Deku

The game now starts with the Deku consuming ritual cutscene and you proceed as a Deku child.

### Goron

It might be a future consideration to find a way to spawn at Darmani's Grave, however, for now we'll stick with the more realistic situation of Goron Link spawning in the Clock Tower.

### Zora

Similarly, we could have Zora Link start in Great Bay, but we'll stick with spawning in the Clock Tower.

### Randomize

Game will start as any of the four Links inside the Clock Tower.


## Stray Fairy Shuffle

There are five Great Fairy Fountains scattered across Termina. These five fountains are randomized amongst themselves. The two that give variations on the Magic Meter in vanilla are modelled as progressives; the first Great Fairy the player activates will give a Magic Meter while the second will give the Double Magic upgrade. With the Great Fairy Sword being in the pool, one of the Great Fairies will hold an item as a reward. Talking to the Great Fairy with the Great Fairy Mask will reveal which reward is given by that Great Fairy.

Stray Fairies can be found floating around in each of the four main dungeons. There are 15 found in each of these dungeons which can be returned to the nearby Great Fairy Fountain for a prize. Which prize is awarded at a given fountain is randomized, but stray fairies must be returned to their appropriate fountain to claim the reward.

There are two different types of stray fairies, which can each be randomized differently. Freestanding Stray Fairies will always stay in the location they were found in their dungeon, but which fountain they belong to can be different. Chest Stray Fairies however can be placed in any chest in the game (I hope. No part of this theory has been tested, but Stone Tower will get a whole lot more interesting if this works). There's going to tweaking since with this system, I've already run into corner cases that break the system

## Stray Fairy Shuffle

### Home Dungeon

All Stray Fairies will be from the same fountain that shares its name with the dungeon it's found in.

### Random Dungeon

All Stray Fairies within a particular dungeon will belong to the same fairy fountain.

### Random

Any Freestanding Stray Fairy can be found in any dungeon.

## Chest Stray Fairy Locations

### All in Dungeon

Every Chest Stray Fairy will be found within dungeons according to the conditions for Stray Fairy Shuffle.

### Partially Randomized

Specify a minimum number of Stray Fairies to be randomized in with the non dungeon chests. This number might be exceeded if Random Dungeon is selected for Stray Fairy Shuffle.

### Anywhere

Can be found in any chest in the game (barring technical limitations)

### Randomize Clock Town Stray Fairy

It might be possible to change which type of Stray Fairy is found in Clock Town. This could add a Freestanding Stray Fairy to the pool (Possibly two).


## Owl Statue Shuffle

If set, the warp points opened up by activating an owl statue will be randomized among themselves. For example, you could activate the owl statue in Clock Town, and using the Song of Soaring would be able to take you to Stone Tower since the Clock Town owl statue randomized to the Stone Tower warp point.

### Include Hidden Owl

If set along with Owl Statue Shuffle, this will make one of the warp locations hidden behind the aesthetic owl statue in West Clock Town. This means that one owl statue will not add a warp point to the list. Be careful, if this happens and you see no warp points on your map after playing the Song of Soaring, press A to select whatever the game selected for you. This is called Index Warping and if this feature ever gets off the ground, I might put the table in here. This wording is not optimal or accurate, and I'll fix it later.


## Gossip Stone Hints with Mask of Truth

If set, the Gossip Stones scattered across Termina will have various hints informing the player of which items are in various inconvenient locations. The Stone of Agony is the condition to be able to talk to the Gossip Stones in this mode instead of the Mask of Truth out of mercy to the player.

The locations we regarded as the most generally inconvenient for all medallions play will always have hints, those hints will appear in two places, and the logic will guarantee access to the Mask of Truth before those places must be checked.

There will be other hints that only exist once for other somewhat inconvenient places for which there is no guarantee of Mask of Truth access, and there will be other sorts of remarks from the Gossip Stones in the hint pool that may bring a smile to your face but will not provide you with unique information for your quest.


# Installation

Clone this repository and then run ```MMRandomizer.py``` (requires Python 3).

Alternatively, run ```Gui.py``` for a simple graphical user interface.

For releases, a Windows standalone executable is available for users without Python 3.

This randomizer requires The Legend of Zelda: Majora's Mask version 1.0. This will first support the NTSC-U version before eventually supporting NTSC-J and NTSC-E. Upon first being run, the randomizer will automatically create a decompressed version of this ROM that can be used for input for slightly faster seed generation times. Please be sure your input ROM filename is either a .n64 or .z64 file. For users playing via any means other than on real N64 hardware, the use of the "Compress patched ROM" flag is strongly encouraged as uncompressed ROMs are impossible to inject for the Virtual Console and have random crashing problems on all emulators.

For general use, the recommended emulators are Bizhawk and Mupen64plus. If you want to play on Project 64 for whatever reason, you can but you will need to set the rando to use 8 MB of RAM and will want to play with the cheat code 8109C58A 0000 to partially fix Project 64's tragically poor handling of OoT's pause menu. For the eventual release, there will probably still be0 suspected crashing issues specifically with Project 64. I cannot emphasize enough that it is a discouraged emulator to use.

# Quirks to Know

This will expand as this develops (obviously)

-In the randomizer, possessing the Bomb Bag is the requirement to get bomb drops, buy bombs or Bombchus.  

# Boring Settings

## Create Spoiler Log

Output a Spoiler File.

## Do not Create Patched Rom

If set, will not produce a patched rom as output. Useful in conjunction with the spoiler log option to batch generate spoilers for statistical analysis.

## Compress patched Rom

If set, the randomizer will additionally output a compressed ROM using Grant Man's bundled compressor. This compressor is the fastest compressor out there and tuned specifically for this game, but in order to achieve its incredibly high speed, it does utilize every last bit of CPU your computer will give it so your computer will slow to a crawl otherwise during the couple of minutes this will take.

## Place Dungeon Items

If not set, Compasses and Maps are removed from the dungeon item pools and replaced by five rupee chests that may end up anywhere in the world.
This may lead to different amount of itempool items being placed in a dungeon than you are used to.


## Only Ensure Seed Beatable

If set, will only ensure that Majora's Mask can be defeated, but not necessarily that all locations are reachable.


## Seed

Can be used to set a seed number to generate. Using the same seed with same settings on the same version of the randomizer will always yield an identical output.


## Count

Use to batch generate multiple seeds with same settings. If a seed number is provided, it will be used for the first seed, then used to derive the next seed (i.e. generating 10 seeds with the same seed number given will produce the same 10 (different) roms each time).


# Known issues

Sadly for this 0.0 readme design draft, I have plenty of ideas, so problems have yet to be identified. Have a grievance list.
-I don't know much N64 assembly level stuff, so making this playable is waaaaaaay further down the line. I intend to do most of this by testing spoiler logs until all the logic is in place. Once that monster is taken care of, then we'll get to the juicy payload. That said, if anybody wants to help out, let me know. I can be found around Twitch and Discord pretty frequently under this name.
-The Title Deeds and Kafei fetch quest items are bad, and unless I find a way to hack the menu, they may not get randomized even though they have some of the best potential. The fact that these items will overwrite each other is a problem.
-I'll go more into the Kafei subtleties later
-Thief Bird worst bird
-Gossip Stones will be counted, and the hints will be rewritten to make sense to Majora's Mask. Couples Mask and the Skulltula Houses are definite hints.


# Command Line Options

There will be more of these, but this fork is nowhere near prepared enough to figure out how to line up command args.

```
-h, --help            
```

Show the help message and exit.

```
--create_spoiler      
```

Output a Spoiler File (default: False)

```
--rom ROM
```

Path to a The Legend of Zelda: Majora's Mask NTSC-US v1.0 ROM. (default: ZELOOTROMDEC.z64)

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

Gossip Stones provide helpful hints about which items are in inconvenient locations if the Mask of Truth is in the player's inventory. (default: False)

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
