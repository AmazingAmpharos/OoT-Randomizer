# OoTRandomizer

This is a randomizer for _The Legend of Zelda: Ocarina of Time_ for the Nintendo 64.

# Installation

It is strongly suggested users get the latest release from here: https://github.com/AmazingAmpharos/OoT-Randomizer/releases .
Simply download the .msi installer and run it if you have a Windows machine.

If you do not have Windows or you simply wish to run the script raw, clone this repository and either run '''Gui.py''' for a
graphical interface or '''OoTRandomizer.py''' for the command line version. Both require Python 3.5+.

This randomizer requires The Legend of Zelda: Ocarina of Time version 1.0 NTSC-US version. This randomizer includes an in-built decompressor, but if
the user wishes a pre-decompressed ROM may be supplied as input. Please be sure your input ROM filename is either a .n64 or .z64 file. For users
playing via any means other than on real N64 hardware, the use of the "Compress patched ROM" flag is strongly encouraged as uncompressed ROMs are
impossible to inject for the Virtual Console and have random crashing problems on all emulators.

For general use, the recommended emulator is RetroArch; it has been shown to work with minimal issues. Bizhawk and Mupen64plus are generally good choices
too. If you want to play on Project 64 for whatever reason, you can but you will need to set the rando to use 8 MB of RAM and will want to play with the
cheat code 8109C58A 0000 to partially fix Project 64's tragically poor handling of OoT's pause menu. Project 64 also has one particular crash that only
happens for some unknown settings configurations; we cannot support this. I cannot emphasize enough that it is a discouraged emulator to use.

# General Description

This program takes _The Legend of Zelda: Ocarina of Time_ and randomizes the locations of the items for a more dynamic play experience.
Proper logic is used to ensure every seed is possible to complete without the use of glitches and will be safe from the possibility of softlocks
with any possible usage of keys in dungeons.

The items that randomize currently are all items within chests including those in grottos, items given as rewards by NPCs including from minigames and
Deku Scrub Salesmen, the items given by freestanding Pieces of Heart, Heart Containers, and Keys, and the items obtained when getting the Bottle and the
Fire Arrows at Lake Hylia or the Ocarina of Time from the Castle Town moat. All dungeons will always have the same number of Maps, Compasses, Small Keys,
and Boss Keys they had in the original game, but which chests within those dungeons have those things is random. The item pool will contain a Biggoron Sword
that will not interfere with Medigoron's sale of the Giant's Knife (which is always vanilla), and a randomly selected adult trading quest item other than the
Odd Potion will be somewhere in the item pool.

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

To be more clear about which NPC items are shuffled, it's only the one time permanent item rewards for the most part like NPCs who originally gave Pieces of Heart
or inventory items. The only exception is that even though in vanilla the reward for 40 Gold Skulltulla Tokens was just 10 Bombchus that is still a randomized reward
in randomizer (but the 200 rupees for all 100 Gold Skulltulla Tokens is not randomized so the most tokens that could be required to complete a seed is 50). As a mercy
to the player, the Ocarina Memory Game in the Lost Woods will start on the final round as that minigame was very long originally, the three day wait on the Claim Check
is removed, Bombchu Bowling will have a fixed sequence of prizes that is of maximum convenience to the player, Dampe's Gravedigging Tour will always be won on the first
dig, and the fishing minigame is made much simpler (8 lb fish for child now, 10 lb for adult). Additionally, any NPC who gives a trading quest item either for the child
or for the adult other than Anju's initial gift as an adult does not have a randomized reward.

A special note is needed for the six Great Fairy Fountains scattered across Hyrule. All six of these fountains now give random item rewards, and the magic and life
upgrades can now be found as normal items scattered around the world. Happy hunting!

The Ocarina songs are shuffled in a pool amongst themselves, and each learn spot will still have the original conditions it has always had. These conditions may not
have all been obvious, but here are some high points. Saria will teach her song after completing the events in the Castle Courtyard. The warp songs can mostly only
be learned by an adult, but the location for Requiem of Spirit is available for even a child if the Desert Colossus can be reached. The location for the Prelude of
Light requires the Forest Medallion, and the location for the Nocturne of Shadow requires the Forest Medallion, Fire Medallion, and Water Medallions. This can be
changed with a setting.

Speaking of Medallions, each boss in the eight main dungeons will drop a random Spiritual Stone or Medallion, and instead of the Light Medallion being granted by the
now removed "becoming an adult" cutscene, the player will start every seed with a random Spiritual Stone or Medallion. The pedestal in which the Spiritual Stones
rest in the Temple of Time has hint text pointing to the locations of the Spiritual Stones and Medallions. A child will be able to read hints for the Spiritual
Stones while an adult will be able to read hints for the Medallions. This information and some other relevant dungeon based info can be seen in the pause menu by
holding the "A" button on the c-item menu.

To be very clear on this point, while the rewards for up to 50 Gold Skulltulla Tokens are randomized, the tokens themselves are not.

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
simply result in the player having one extra Small Key. Certain settings configurations will disable this behavior.

To be clear about the logic rules of what can be where, the randomizer will ensure a glitchless path through the seed will exist, but the randomizer will not prevent
the use of glitches for those players who enjoy that sort of thing though we offer no guarantees that all glitches will have identical behavior to the original game.
Glitchless can still mean that clever or unintuitive strategies may be required involving the use of things like Hover Boots, the Hookshot, or Scarecrow's Song that
may not have been important options in the original game. The Lens of Truth is guaranteed available and useable before completion of the Treasure Chest Game is required
or before walking through any invisible objects or opening any invisible chests is required with the exception of the one invisible wall that is required to enter
the Bottom of the Well as the original game required passing that invisible wall to reach the Lens of Truth.

One last detail is that the menu is now more like the Majora's Mask menu in that the player can move the cursor through empty spaces. This fixes a major problem from
the original game in that certain combinations of items would create menu shapes that would be impossible to fully menu through. Unfortunately, as of this 3.0 release,
this functionality does not apply to the "equipment" screen which can rarely create some tricky situations. Usually these can be solved by purchasing a Deku Shield and
a Hylian Shield.

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
-In a few places, out of sight Song of Time blocks can be summoned. The lava room in Gerudo Training Grounds, the beginning of Ganon's Castle Shadow Trial, and the last
hallway with a caged Goron in Fire Temple are the main cases.
-Adult Link can fully clear Dodongo's Cavern. He can even skip the first section by virtue of being tall.  
-In the Forest Temple, you can reach the room with the Floormaster (vanilla) or Redead (MQ) early by using Hover Boots in the block push room.  
-In the Fire Temple, you can reach the Boss Key door from the beginning with Hover Boots.  
-In the Water Temple, you can from the start with the water down jump to the middle platform level, very carefully aim the Hookshot to the target above, and pull yourself
to the highest level of the central platform. Then a very well spaced rolling jump can reach the water changing station to raise the water to the highest level. If you
make poor key choices in Water Temple, this may be what you need to do to untangle the situation.  
-In the Water Temple, Hover Boots can be used to reach the vanilla Boss Key chest without going through the room that requires Bombs and block pushing. Hover Boots can
also be used in this temple to avoid the Longshot requirement for the middle level chest that requires the Bow.  
-In the Shadow Temple, you can avoid the need for the Longshot in the room with the invisible spikes by backflipping onto the chest for extra height.  
-In the Shadow Temple, you can Hookshot the ladder to avoid pushing the block to get on the boat.  
-In the Shadow Temple, a combination of the scarecrow and the Longshot can be used to reach Bongo Bongo without needing the Bow.  
-In the Spirit Temple, the child can obtain the vanilla Map chest with Deku Sticks. No fire magic is needed.  
-In the Spirit Temple, you can collect the silver rupees without Hover Boots by jumping directly onto the rolling boulder or with a jump slash.  
-In the Spirit Temple, you can use the Longshot to cross from the hand with the Mirror Shield in vanilla to the other hand.  
-In Ganon's Castle Spirit Trial, the web can be burned with a precise shot through the torch by a normal arrow. Fire Arrows are not required.  
-While we guarantee tunics for Fire Temple and Water Temple, you can possibly force yourself to do without if you seriously let a Like Like eat the tunic and
then do not recover the tunic. It is almost always possible to do without, but it can make things really difficult on you.  
-Several Gold Skulltulla Tokens can be reached by clever/precise uses of jump slashes and spin attacks (possibly magic spin attacks).  

# Known issues

Sadly for this 3.0 release a few known issues exist. These will hopefully be addressed in future versions.

-The fishing minigame sometimes refuses to allow you to catch fish when playing specifically on Bizhawk. Save and quit (NOT savestate) and return to fix the issue.  
-Draining the Bottom of the Well with Song of Storms sometimes crashes on specific configurations of Project 64. We aren't sure of the exact story, but this bug is
easily avoided by playing on a different emulator and probably also avoidable by changing your settings and maybe graphics plug-in.  
-Executing the collection delay glitch on various NPCs may have unpredictable and undesirable consequences. In particular this can be devastating with Biggoron;
it is strongly suggested the player save before turning in the Claim Check.  
-Saving and quitting on the very first frame after becomming an adult when you would trigger the Light Arrow cutscene can have undesired consequences. Just don't
do that.  
-The equipment screen still cannot be easily navigated with all item configurations which can be especially problematic if the Biggoron Sword is found very early
or if shields cannot be easily purchased thanks to shopsanity. Getting the Master Sword and buying as many shields as you can is a good way to mitigate these issues.

# Settings

The OoT Randomizer has many different settings users can choose to customize their play experience. Here's a fully detailed list!

# ROM Options

## Base Rom

Specify the input ROM that will be used by the randomizer. Please be sure it is OoT US v1.0.

## Output Directory

Specify where the output ROM will be written on your computer.

## Create Spoiler Log

Decide whether to output a text file detailing where every item can be found and the sequence of play that will lead to seed completion. Selecting this option will
create a different item configuration than using otherwise identical settings without printing a log; this is intended to prevent cheating in race environments.

## Compress Rom

Decide the format of the output ROM. Compressed is generally recommended for most users; this is necessary for injection into a .wad for use on the Virtual Console,
and all known N64 emulators have significant crashing problems with uncompressed ROMs. Real N64 hardware doesn't care so generation time can be improved by using
the uncompressed option if you are playing on a real N64 with a flash cart. You can also choose not to output a ROM at all; this is useful if you just want to look
at spoiler logs.

## Default Targeting Option

This option specifies whether Z-targeting will default to "Switch" or "Hold" style. Either way, this can still be changed in-game as per usual.

## Multi-World Generation

This option allows for multiple worlds to be generated to be used in co-op play. Each player will get a different ROM designed to work in conjunction with another
to allow two players to work together to complete the game. Synchronization can be achieved on Bizhawk via the following script:

https://github.com/TestRunnerSRL/bizhawk-co-op

### Player Count

Use this to specify how many players will be participating in this co-op playthrough.

### Player ID

Use this to specify which player number you are in particular. Each participant in the co-op should choose a different number starting with 1.

## Setting String

This is an 18 character string that specifies the totality of other gameplay relevant (non-cosmetic) settings used throughout the randomizer. This string can be shared
between players and then the "Import Settings String" button can be pressed to automatically change all settings to match another player.

## Seed

This is a string representing the particular configuration of items that will occur in your seed; the purpose is to combine a seed string with an identical settings
string such that the randomizer will be able to generate the same game for multiple players. If this field is left blank, a random seed will be chosen.

# Main Rules

## Open Forest

Mido does not need to see a sword and shield to reach the Deku Tree and the Kokiri boy blocking the exit to the forest is gone. If this flag is not set, it is
guaranteed that the Deku Tree can be completed without leaving the forest. This means that within the forest or the Deku Tree itself it will be possible to find
the Kokiri Sword, Deku Shield for sale, and the Slingshot.

## Open Kakariko Gate

The gate leading up Death Mountain from Kakariko Village is open from the beginning of the game. Normally this requires Zelda's Letter to open. This allows more
diverse routing early in the game and prevents very long walks in seeds with the Weird Egg shuffled. Two things are important to note. Showing Zelda's Letter to
the guard is still required to begin the Happy Mask sidequest and to receive a discount on purchasing Hylian Shields. The gate is simply gone for an adult no
matter what.

## Open Door of Time

The Door of Time is open from the beginning of the game. The Song of Time is still potentially useful to move Song of Time blocks, play songs for the frogs on Zora
River, or for other such uses. If this flag is not used, the Door of Time must be opened to become an adult as in the original game, but all that is needed to open
the Door of Time is the Song of Time and any ocarina. The Ocarina of Time in particular and the Spiritual Stones have nothing to do with this.

## Gerudo Fortress

### Default Behavior

Gerudo Fortress will work the same way it did in the original game. All four carpenters must be rescued in order for the Gerudo woman who gives the Gerudo Card to
appear and for the Gerudo to stop being hostile. Rescuing a carpenter requires having a Gerudo Fortress Small Key and defeating the corresponding guard.

### Rescue One Carpenter

Only the bottom left carpenter must be rescued to complete Gerudo Fortress. Only one Gerudo Fortress Small Key will exist because of this.

### Start with Gerudo Card

The player will start with the Gerudo Card from the beginning of the game. The carpenters will be pre-rescued, and the bridge to Gerudo Fortress as an adult will
be repaired from the beginning. The Gerudo Card is the requirement in the randomizer to enter Gerudo Training Grounds so it will be an accessible area from the
moment adulthood is available.

## Rainbow Bridge Requirement

This determines the condition under which the rainbow bridge to Ganon's Castle will spawn.

### All Dungeons

The rainbow bridge spawn requires all medallions and spiritual stones to be in the player's possession.

### All Medallions

All six of the medallions are required to open Ganon's Castle.

### Vanilla

The rainbow bridge spawns under the same conditions it did in the original game, possession of the Light Arrows and having viewed the Zelda cutscene. This
cutscene in the Temple of Time is triggered by possessing the Shadow and Spirit Medallions.

### Open

The rainbow bridge is always present.

## Random Number of Ganon's Trials

A random number of trials within Ganon's Castle from 0 to 6 will be chosen, and individual trials will be randomly disabled as necessary to match this number.
Alternatively, a specific number of trials can be specified with the slider below. If a number of trials other than 0 or 6 is chosen and hints are enabled,
hints will be added to the hint pool informing the player which trials are present (if 1 to 3 trials) or which are missing (if 4 or 5 trials).

## All Locations Reachable

This option will set the logic to try to ensure Link can reach every item location in the game with the exception of "key for key" item locations (a single
item spot behind a locked door containing the key to open the door). If this option is not used, the logic will allow some items to be in impossible locations
so long as the set of reachable items is sufficient to complete the game.

## Bombchus are considered in logic

This option fundamentally changes how the Bombchu items found around the world function. With this option on, Bombchus are a progression item and operate as
a form of progressive item. The first Bombchu pack found will be worth 20 Bombchus and subsequent packs will be worth 10 or 5 Bombchus. Finding Bombchus will
be considered as logical progression, and having found any Bombchus will be the condition to play Bombchu Bowling or buy Bombchu items from shops. This flag
will also add Bombchu (5) buyable items to the shops in Kokiri Forest, Castle Town Bazaar, and Kakariko Bazaar. With this option off, randomly found Bombchu
items are not considered as logical progression, randomly found Bombchus will have specific denominations based on the values from the original game, and
finding a Bomb Bag is what enables playing Bombchu Bowling and buying Bombchus from shops which will not have their inventories edited.

## Dungeons have one major item

This option places one "major item" and one only in each of the dungeons. For the purpose of the randomizer, the dungeons are defined as the eight dungeons that
contain either Medallions or Spiritual Stones as well as Bottom of the Well, Ice Cavern, Gerudo Training Grounds, and Ganon's Castle. The major items are any
item usable with a c-button that is not simply a form of ammo (Bombchus are major only if "Bombchus are considered in logic" is on), songs, Mirror Shield, swords,
tunics, boots, Double Defense, Magic Meter/Double Magic, Bullet Bags, Quivers, Bomb Bags, Strength Upgrades, Scales, Wallets, and the Stone of Agony. To be
clear, this means that rupees, ammo, Deku Stick and Deku Nut ammo expansions, Pieces of Heart, Heart Containers, Gold Skulltulla Tokens, Maps, Compasses,
Small Keys, Boss Keys, Deku Shields, Hylian Shields, and Ice Traps are not considered major items.

## Dungeon Quest

This option specifies the form dungeons will take. The item pool will be updated to reflect the items originally found in the dungeons used.

### Vanilla

Dungeons will have the same internal layout as they did in the original The Legend of Zelda: Ocarina of Time.

### Master Quest

Dungeons will have the internal layouts found in The Legend of Zelda: Ocarina of Time Master Quest.

### Mixed

Dungeons will each have a random internal layout chosen between the vanilla and Master Quest forms.

## Shuffle Kokiri Sword

This flag adds the Kokiri Sword to the shuffle. With it off, the Kokiri Sword will always be found in its original chest in the Kokiri Forest.

## Shuffle Weird Egg

This flag adds the Weird Egg given by child Malon to the shuffle. With this flag on, child Malon will give a random item and the Weird Egg must be located
to do the events at Hyrule Castle with Zelda and Impa. These events block interacting with Talon and Malon at Lon Lon Ranch as a child as well as Saria in
Sacred Forest Meadow.

## Shuffle Ocarinas

This flag adds both the Fairy Ocarina and the Ocarina of Time to the shuffle. The ocarinas are a progressive item; the first found will always be the Fairy
Ocarina with the second being the Ocarina of Time even though the two are functionally identical. Without this flag on, leaving the Kokiri Forest to the
Lost Woods bridge as a child will always grant one Ocarina and the other is always available at the gate of Castle Town as a child when all three Spiritual
Stones are in the player's possession.

## Shuffle Songs with Items

This flag adds the 12 standard ocarina songs to the shuffle as normal items. With this flag on, the spots that contained songs in the original game will
simply give Link a random item, and the songs can be found as items freely. Without this flag on, songs are still randomized but only between each other.
In either case, the Scarecrow's Song is not affected; it is still obtained by interacting with Bonooru at Lake Hylia first as a kid and then as an adult.

## Shuffle Gerudo Card

This flag shuffles the Gerudo Card into the general item pool. In the randomizer, this is required to gain access to Gerudo Training Grounds, but it does
not have any impact on the hostility of the Gerudo in Gerudo Fortress who still check for the carpenter rescue events. Without this flag, the Gerudo
Card is always given by the Gerudo woman who spawns after the final carpenter is rescued. If Gerudo Fortress is cleared from the beginning of the game,
the player starts the game with the Gerudo Card and this setting is voided.

## Shuffle Deku Salescrubs

This flag makes every Deku Scrub Salesman in the world sell a random item instead of only the three that sold permanent upgrades in the original game.
Using this flag adds the various low tier items the other scrubs sold to the item pool for the most part; the potion refills are replaced with Recovery
Hearts for Red Potions and blue rupees for Green Potions. For each Deku Scrub that sold arrows/seeds depending on age, there will be a 75% chance of
adding a 30 arrow item and a 25% chance of adding a 30 seed item to the pool. While the text will not update, if this flag is used the price of every
Deku Scrub Salesman's item will be reduced to 10 rupees, and once the purchase is made that particular Deku Scrub Salesman will disappear forever.

## Shopsanity

This setting randomizes the items sold in shops. When it is used, all shop items are randomly re-arranged among all 8 of the original game's shops.
This setting causes the Bombchu Shop to be open from the very beginning of the game, and this setting considers the two shops in adult Kakariko
Village to be distinct shops from the two similar shops in child Castle Town; however, the shops in Kokiri Forest, Goron City, and Zora Domain are
the same shops as both ages. This setting overrides the "Bombchus considered in logic" editing of the shop item pool.

### Off

This disables the Shopsanity feature.

### Shuffled Shops (0 Items)

This causes all of the Shopsanity features described above.

### Shuffled Shops (1-4 Items)

This not only causes all of the Shopsanity features described above, but it also adds 1-4 (depending on the exact setting) items from the general
item pool into shops to buy for randomly chosen amounts of money. Lower value shop items are removed to make room for this, and low value junk items
are added to the item pool to fill the extra empty chests this will implicitly create. Using this feature will also replace several of the rupee
items found throughout the seed with higher value rupees and will add a third Wallet upgrade, the "Tycoon's Wallet", to the item pool which can hold
up to 999 rupees. The items from the general item pool added to shops will always be on the far left of the shop inventories, and these items can
always be bought if the player has enough rupees even if they are explosives without an appropriate container or a tunic as a child.

### Shuffled Shops (Random Items)

This is similar to the 1-4 items variant but gives each shop a random number of new items from 0-4. Each shop can have a different amount of unique
items with this setting.

## Shuffle Dungeon Items

This setting allows the player to decide the natural distribution of dungeon items. Dungeon items can be found confined to their original dungeons,
spread freely throughout the world, or prevented from existing completely. Items that are prevented from existing completely will be replaced in the
item pool with an assortment of various low tier junk items. This feature can be specified for Maps/Compasses, Small Keys, and Boss Keys independently.
If Small Keys or Boss Keys are prevented from existing, this will also remove all locks those keys would be used for from existing as well. If Small Keys
are left in their original dungeons and the Fire Temple is not in the form of Master Quest, the locked door in the first room that leads to the normal
location of the Boss Key will be removed.

## Maps and Compasses give information

This setting, only available if Maps and Compasses are spread across the world, disables the pedestal in the Temple of Time from giving information about
the location of the Medallions and Spiritual Stones. Instead, the Compass from each of the eight eligible dungeons will tell the player which dungeon has
which reward. If the dungeon quest is set to mixed, each of the ten Maps will tell the player whether any given dungeon is in the vanilla or Master Quest
form. The Compasses from Bottom of the Well and Ice Cavern do not give any information.

## Remove Ganon's Door Boss locked

This setting removes the Boss Key lock from Ganon's Tower. This removes the need to locate the Ganon's Tower Boss Key to finish the game.

## Tokensanity

This setting shuffles the Gold Skulltulla item drops into the general pool of locations. The player can choose only to include Gold Skulltullas
found in dungeons for a more mild version of this setting.

# Detailed Logic

## Maximum expected Skulltulla tokens

This setting can be used to reduce the number of Gold Skulltulla Tokens that may be required to finish the game.

## No Nighttime Skulltullas without Sun's Song

This setting causes the logic to expect the player to have an ocarina and the Sun's Song to get Gold Skulltulla locations that are only found at
nighttime.

## No Big Poes

This setting will guarantee that the Big Poe vendor will not have an important item.

## No Child Fishing

This setting will guarantee that the reward from child fishing is not an important item. This is mostly recommended if the player simply must play
on Bizhawk.

## No Adult Fishing

This setting will guarantee that the reward from adult fishing is not an important item. This is mostly recommended if the player simply must play
on Bizhawk.

## No Skull Mask reward

This setting will guarantee that the item obtained from showing the Skull Mask in the Deku Theater is not an important item.

## No Mask of Truth reward

This setting will guarantee that the item obtained from showing the Mask of Truth in the Deku Theater is not an important item.

## No 1500 Horseback Archery

This setting will guarantee that the item obtained from scoring 1500 points at the horseback archery challenge at Gerudo Fortress is not an
important item.

## No Lost Woods Memory Game

This setting will guarantee that the item obtained from winning the ocarina memory game in the Lost Woods is not an important item.

## No Racing Dampe a second time

This setting will guarantee that the item obtained from finishing with a sub-minute time in the second Dampe race is not an important item.

## No Biggoron reward

This setting will guarantee that the item obtained from showing the Claim Check to Biggoron is not an important item.

## Adult Trade sequence

This pair of settings can be used to specify the earliest and latest items that can be allowed to randomly show up in the general item pool.
Only one item will be in the item pool regardless of this setting; this can merely be used to limit the range of possibilities.

## Require minor tricks

This setting allows a huge number of minor tricks to be allowed by the logic. Here is a complete list:

-A precise jumpslash with either a Deku Stick or the Kokiri Sword can be used to reach a Gold Skulltulla on some vines in standad Deku Tree.  
-The Bow can be used to knock down the stairs in Dodongo's Cavern with two well timed shots.  
-The vines in Forest Temple leading to where the well drain switch is in the standard form can be barely reached with the standard Hookshot.  
-A Bombchu from the ground level can be used to hit the switch to bypass the block pushing puzzle in Forest Temple MQ.  
-A rusted switch under a Song of Time block in the standard Fire Temple can be hit by using Hammer into the block.  
-The location with the Boss Key chest in Fire Temple MQ can be reached without the Bow with very particular use of Din's Fire.  
-The upper levels of the old boulder maze in Fire Temple MQ can be reached without explosives by using the Hammer through a wall.  
-In the standard Spirit Temple, the bridge on child side can be lowered with a carefully timed Bombchu.  
-The frozen switch in Spirit Temple MQ can be hit without a fire source by using the Bow and Song of Time very cleverly.  
-The chest in the basement of the standard Bottom of the Well can be reached with only a Strength Upgrade by using a jump slash with a lit
Deku Stick to access the bomb flowers in the basement.  
-The first room of the Spirit Trail in Ganon's Castle MQ can be cleared without the Bow by using a Hammer jump slash to hit the rusted switch
through the thrones.  
-The Gold Skulltulla in adult Kokiri Forest can be reached without the Hookshot by using Hover Boots off one of the roots.  
-The child can reach the chest on Death Mountain trail with just the Goron Bracelet by backwalking with the Bomb Flower intended to open
Dodongo's Cavern and throwing the Bomb Flower at the wall very quickly.  
-Gerudo Fortress can be cleared without any items other than those needed for access. The logic normally guarantees one of the Bow, Hookshot, or
Hover Boots to help navigate the "kitchen".  

Using this setting will also pre-set all of the lower logic flags to a reasonable configuration to match the trick level. These can then be
edited as the player desires if the given configuration isn't desired.

## Man on Roof without Hookshot

This allows the logic to consider a trick in which the player does a sidehop off the tall tower in Kakariko Village to reach the man on the
rooftop with no items.

## Child Deadhand without Kokiri Sword

This allows the logic to consider defeating the Deadhand in Bottom of the Well with Deku Sticks. This is not hard with use of the power crouch
stab glitch, but consistently landing actual jump slashes on his unusual hitbox is pretty difficult and using normal slashes consumes 9 Deku Sticks.

## Dodongo's Cavern spike trap room jump without Hover Boots

This allows the logic to consider that the adult can make a particularly useful jump in Dodongo's Cavern to reach the area with the Bomb Bag chest early.
Due to the precision of the jump, normally the logic expects Hover Boots to complete this path.

## Windmill PoH as adult with nothing

This allows the logic to consider a jump the adult can make in the windmill to reach the Piece of Heart within with no items. The jump requires leaping
from an object on which it is not obvious Link is allowed to stand and has counterintuitive timing so it is not in standard logic.

## Crater's bean PoH with Hover Boots

This allows the logic to consider using Hover Boots to reach the Piece of Heart atop the volcano in Death Mountain Crater. The path involves walking up a
very steep slope that is not visibly walkable so it is not in normal logic.

## Zora's Domain entry with Cucco

This allows the logic to consider using a Cucco on Zora River to enter Zora's Domain as a child without playing Zelda's Lullaby. It requires slipping behind
the waterfall trickily from the left side.

## Zora's Domain entry with Hover Boots

This allows the logic to consider this similar trick to the above except as an adult with Hover Boots. This is actually a lot more difficult even though it can
be done from either side of the waterfall.

## Fewer Tunic Requirements

This relaxes the tunic requirements by the logic somewhat. Normally the logic expects a Goron Tunic to enter Fire Temple or complete the Fire Trial in Ganon's Castle
and a Zora Tunic to enter Water Temple, collect the underwater silver rupees in Gerudo Training Grounds, or obtain the Piece of Heart at the bottom of the frozen Zora's
Fountain. With this flag set, the Goron Tunic will not be required to actually enter Fire Temple, only to fight Volvagia or to reach the upper floors. The Zora Tunic
requirements are removed completely except to reach the chest at the bottom of the central pillar in Water Temple.

## Lens of Truth

This setting alters the expectations about interacting with invisible objects without the Lens of Truth.

### Required everywhere

This setting requires the Lens of Truth to interact with any invisible object except for whatever was required in the original game to obtain the Lens of Truth.

### Wasteland and Chest Minigame

This setting expects the Lens of Truth to be used only to cross the Haunted Wasteland and to win the Treasure Chest Minigame in Castle Town at night.

### Only Chest Minigame

This setting expects the Lens of Truth to be used only to win the Treasure Chest Minigame in Castle Town at night.

# Other

## Skip Tower Collapse Sequence

This setting causes defeating Ganondorf to skip directly to the Ganon fight without the need to do the collapsing Ganon's Tower sequence.

## Skip Interior Castle Guard Stealth Sequence

This setting causes entering the crawlspace at Hyrule Castle to deposit the player directly into the Castle Courtyard, bypassing the guard
evasion sequence.

## Skip Epona Race

This setting causes Epona to be stolen from Ingo from the start of the game, only requiring Epona's Song and an ocarina as an adult to summon.

## Fast Chest Cutscenes

This setting causes all chests to open with a quick animation. If this setting is off, certain important items will trigger the slow opening animation.

## Random Big Poe Target Count

This setting causes the number of Big Poes that must be turned into the vendor to obtain his item to be random from 1-10. Alternatively, the number
of Big Poes requires can be selected manually with the slider below. Note that Big Poes can be found as pre-stocked Bottle contents, and the logic
can expect using them if the required number is sufficiently low.

## Start with Scarecrow's Song

This flag causes Pierre the Scarecrow to be available to summon for the adult from the beginning of the game. The box below can be used to
specify the particular desired Scarecrow's Song. This song must be exactly eight notes long and must contain at least two different notes.

## Randomize ocarina song notes

This flag randomizes the particular notes in the 12 standard ocarina songs. This can predictably be pretty obnoxious. In general, the patterns chosen
for the top row songs will be simpler than the patterns chosen for warp songs.

## Chest size matches contents

This flag causes keys, Ice Traps, and items flagged as progression items to appear in large treasure chests while other items will be in small treasure chests.
This means that players can choose to skip small treasure chests since they will only contain handy, not essential, items.

## Clearer hints

This flag changes the text of Gossip Stone hints to be overwhelmingly explicit. This is helpful for players who do not have English as their first language,
but the hints will be less "fun" and less like the sorts of things that would be said in the original game.

## Gossip Stones

This flag changes the behavior of Gossip Stones to give hints to players. The hints will be distributed as such:

-If the required number of trials is 1-3, a hint will be added for each trial that must be done. If the required number of trials is 4 or 5, a hint will be added
for each trial that can be skipped.  
-Hints will be added for every one of the "always" locations that is allowed to have a random possibly valuable item under the current settings. These hints
will tell the player what item is at each of these locations. These locations are the rewards for 30, 40, and 50 Gold Skulltulla Tokens, the item obtained from
Biggoron by showing the Claim Check, the item obtained from the Big Poe vendor, both the song and the item slots at the Ocarina of Time, and the item obtained
from showing the Mask of Truth at the Deku Theater.  
-Some hints will be given for items at a randomly selected number of other locations that are generally somewhat inconvenient to check. The total number of these
hints will be either 11 or 12 minus the number of always hints placed.  
-3 or 4 hints will be given naming a specific non-dungeon specific item that can be found in a randomly chosen dungeon.  
-1 to 4 hints will be given naming a specific item found in a specific overworld region. Which part of this range is used is determined in part by how many
trial hints are given.  
-4 to 6 hints will be given naming what region specific progression items other than Gold Skulltulla Tokens can be found.  
-3 or 4 hints will be given naming specific regions that are "on the way of the hero" and thus contain at least one required progression item.  
-All remaining hints (33 total unique Gossip Stones exist) will be filled with non-information junk hints.  

This setting allows the player to specify which item is required to interact with the Gossip Stones. The Stone of Agony is the default option as it gives a
fairly purposeless vanilla item a use and allows both kid and adult to interact with the Gossip Stones. The default Mask of Truth can be used, but this has
the downside that the Mask of Truth can only be obtained with all Spiritual Stones which tends to make the hints not useful, and using the Mask of Truth
requires being a child which is another big downside. There is also an option for the information to just be free for those wanting an easier mode.

## Text Shuffle

This setting allows all the text in the game to be shuffled. This is mostly for comedy and is not intended to be a serious gameplay option.

### No text shuffled

Leave the text alone.

### Shuffled except Hints and Keys

Shuffle all text other than the useful text giving the player information.

### All text shuffled

Shuffle all text even to the player's mechanical disadvantage.

## Difficulty

This setting allows the player to tweak the item pool to make a somewhat harder experience.

### Normal

Leave the item pool alone.

### Hard

Heart Containers, Double Defense, and the second Magic Upgrade are replaced with junk items.

### Very Hard

In addition to the items from Hard, Pieces of Heart and Nayru's Love are also replaced with junk items.

### OHKO

In addition to the item changes from Very Hard, Link dies in one hit. Ice Traps are replaced with Recovery Hearts.

# Cosmetics

## Background Music

### Normal

Do not alter the background music.

### No Music

Disable background music. Sound effects will still play. This may be desired by players who like to listen to their own music.

### Random

Background music is shuffled so that different tracks may play in different areas. This may be silly.

## Kokiri Tunic Color

This determines the color of Link's default Kokiri Tunic. This only affects the color when he's wearing it, not the color of the icon in the menu.

### Most Colors

Simply get the particular color selected. Available colors are Kokiri Green, Goron Red, Zora Blue, Black, White, Purple, Yellow, Orange, Pink, Gray,
Brown, Gold, Silver, Beige, Teal, Royal Blue, Sonic Blue, Blood Red, Blood Orange, NES Green, Dark Green, and Lumen.

### Random Choice

Choose a random color from the set of pre-made colors.

### Completely Random

Generate a random color with numerically random RGB values.

### Custom Color

A special interface will pop up that will allow the user to choose any color from a diverse color wheel or input a desired RGB value.

## Goron Tunic Color

This determines the color of Link's Goron Tunic. This only affects the color when he's wearing it, not the color of the icon in the menu or when
holding it up after acquiring it. The options are identical to those for the Kokiri Tunic.

## Zora Tunic Color

This determines the color of Link's Zora Tunic. This only affects the color when he's wearing it, not the color of the icon in the menu or when
holding it up after acquiring it. The options are identical to those for the Kokiri Tunic.

## Low Health SFX

This determines which sound effect to play repeatedly when Link is very low on health. Several of these options are designed to be potentially
more pleasant to listen to while a few are designed to be more amusing.

### Particular Sounds

Set this particular sound for the heart beep. Available choices are Default, Softer Beep, Rupee, Timer, Tamborine, Recovery Heart, Carrot Refill,
Navi - Hey!, Zelda - Gasp, Cluck, and Mweep!. The last of these is indeed the sound a king might make when moving... very slowly.

### Random Choice

Play a random SFX from the list of choices.

### None

Disable low health heart beeps altogether.

## Navi Color

These options can be used to set Navi's color in a variety of contexts. The lists of pre-set colors here is different, but the same types of options
exist as for choosing tunic colors.

## Navi Hint

This option sets the SFX that will play when Navi is ready to give a hint. The options are very similar to the Low Health SFX.

## Navi Enemy Target

This option sets the SFX that will play when Navi targets an enemy. The options are very similar to the Low Health SFX.

# Command Line Options

```
-h, --help            
```

Show the help message and exit.

```
--check_version
```

Check for the latest version number online (default: False)

```
--checked_version CHECKED_VERSION
```

Check for the specified version number instead of a number from online.

```
--rom ROM
```

Path to a The Legend of Zelda: Ocarina of Time NTSC-US v1.0 ROM. (default: ZOOTDEC.z64)

```
--output_dir OUTPUT_DIR
```

Path to output directory for rom generation.

```
--seed SEED           
```

Define seed number to generate. (default: None)

```
--count COUNT         
```

Set the count option (default: None)

```
--world_count WORLD_COUNT       
```

Use to create a multi-world generation for co-op seeds. World count is the number of players.
Warning: Increasing the world count will drastically increase generation time. (default: 1)

```
--player_num PLAYER_NUM       
```

Use to select world to generate when there are multiple worlds. (default: 1)

```
--create_spoiler      
```

Output a Spoiler File (default: False)

```
--compress_rom [{True,False,None}]
```

Create a compressed version of the output rom file.
True: Compresses. Improves stability. Will take longer to generate
False: Uncompressed. Unstable on emulator. Faster generation
None: No ROM Output. Creates spoiler log only (default: True)

```
--open_forest
```

Set whether Kokiri children obstruct your path at the beginning of the game. (default: False)

```
--open_kakariko
```

The gate in Kakariko Village to Death Mountain Trail is always open, instead of needing Zelda's Letter. (default: False)

```
--open_door_of_time
```

Set whether the Door of Time is open from the beginning of the game. (default: False)

```
--gerudo_fortress [{normal,fast,open}]
```

Select how much of Gerudo Fortress is required. (default: normal)

```
--bridge [{medallions,vanilla,dungeons,open}]
```

Select the condition to spawn the Rainbow Bridge to Ganon's Castle. (default: medallions)

```
--all_reachable
```

Enables the "Only Ensure Seed Beatable" option (default: False)

```
--all_reachable
```

Enables the "Only Ensure Seed Beatable" option (default: False)

```
--bombchus_in_logic
```

Changes how the logic considers Bombchus and other Bombchu related mechanics (default: False)

```
--one_item_per_dungeon
```

Each dungeon will have exactly one major item. (default: False)

```
--trials_random
```

Sets the number of trials that must be cleared in Ganon's Castle to a random value (default: False)

```
--trials [{0,1,2,3,4,5,6}]
```

Sets the number of trials that must be cleared in Ganon's Castle (default: 6)

```
--no_escape_sequence
```

Removes the tower collapse sequence after defeating Ganondorf (default: False)

```
--no_guard_stealth
```

Removes the guard evasion sequence in Hyrule Castle (default: False)

```
--no_epona_race
```

Removes the need to race Ingo to acquire Epona (default: False)

```
--fast_chests
```

Causes all chests to open with a fast animation (default: False)

```
--big_poe_count_random
```

Sets the number of Big Poes that must be sold to the vendor for an item to a random value (default: False)

```
--big_poe_count [{1,2,3,4,5,6,7,8,9,10}]
```

Sets the number of Big Poes that must be sold to the vendor for an item (default: 10)

```
--free_scarecrow
```

Start the game with the Scarecrow's Song activated and Pierre possible for the adult to summon (default: False)

```
--scarecrow_song [SCARECROW_SONG]
```

Set Scarecrow's Song if --free_scarecrow is used. Valid notes: A, U, L, R, D (default: DAAAAAAA)

```
--shuffle_kokiri_sword
```

Include the Kokiri Sword as a randomized item (default: False)

```
--shuffle_weird_egg
```

Include the Weird Egg as a randomized item (default: False)

```
--shuffle_ocarinas
```

Include the two ocarinas as randomized items (default: False)

```
--shuffle_song_items
```

Treat the ocarina songs as normal items and shuffle them into the general item pool (default: False)

```
--shuffle_gerudo_card
```

Include the Gerudo Card to access Gerudo Training Grounds as a randomized item (default: False)

```
--shuffle_scrubs
```

Include all Deku Scrub Salesmen as randomized item locations (default: False)

```
--shopsanity [{off,0,1,2,3,4,random}]
```

Randomize shop items and add the chosen number of items from the general item pool to shop inventories (default: off)

```
--shuffle_mapcompass [{remove,dungeon,keysanity}]
```

Choose the locations Maps and Compasses can be found (default: dungeon)

```
--shuffle_smallkeys [{remove,dungeon,keysanity}]
```

Choose the locations Small Keys can be found (default: dungeon)

```
--shuffle_bosskeys [{remove,dungeon,keysanity}]
```

Choose the locations Boss Keys can be found (default: dungeon)

```
--enhance_map_compass
```

Change the functionality of the Map and Compass to give information about their dungeons. Requires --shuffle_mappcompass keysanity (default: False)

```
--unlocked_ganondorf
```

Remove the Boss Key door leading to Ganondorf (default: False)

```
--tokensanity [{off,dungeons,all}]
```

Include the chosen Gold Skulltulla Token locations in the item shuffle (default: off)

```
--quest [{vanilla,master,mixed}]
```

Choose the internal layout of the dungeons (default: vanilla)

```
--logic_skulltulas [{0,10,20,30,40,50}]
```

Choose the maximum number of Gold Skulltulla Tokens that could be required (default: 50)

```
--logic_no_night_tokens_without_suns_song
```

Change logic to expect Sun's Song to defeat nighttime Gold Skulltullas (default: False)

```
--logic_no_big_poes
```

Prevent the Big Poe vendor from having a required item (default: False)

```
--logic_no_child_fishing
```

Prevent the prize from fishing as a child from being a required item (default: False)

```
--logic_no_adult_fishing
```

Prevent the prize from fishing as an adult from being a required item (default: False)

```
--logic_no_trade_skull_mask
```

Prevent the item obtained by showing the Skull Mask at the Deku Theater from being a required item (default: False)

```
--logic_no_trade_mask_of_truth
```

Prevent the item obtained by showing the Mask of Truth at the Deku Theater from being a required item (default: False)

```
--logic_no_1500_archery
```

Prevent the item obtained by scoring 1500 points at horseback archery from being a required item (default: False)

```
--logic_no_memory_game
```

Prevent the item obtained by completing the ocarina memory game in the Lost Woods from being a required item (default: False)

```
--logic_no_second_dampe_race
```

Prevent the prize won by finishing the second Dampe race in under 1 minute from being a required item (default: False)

```
--logic_no_trade_biggoron
```

Prevent the item obtained by showing the Claim Check to Biggoron from being a required item (default: False)

```
--logic_earliest_adult_trade [{pocket_egg,pocket_cucco,cojiro,odd_mushroom,poachers_saw,broken_sword,prescription,eyeball_frog,eyedrops,claim_check}]
```

Set the earliest item in the adult trade sequence that can be found in the item pool (default: pocket_egg)

```
--logic_latest_adult_trade [{pocket_egg,pocket_cucco,cojiro,odd_mushroom,poachers_saw,broken_sword,prescription,eyeball_frog,eyedrops,claim_check}]
```

Set the latest item in the adult trade sequence that can be found in the item pool (default: claim_check)

```
--logic_tricks
```

Enable the logic to consider a large number of minor tricks (default: False)

```
--logic_man_on_roof
```

Enable the logic to consider the trick to reach the man on the roof in Kakariko Village with a sidehop from the tower (default: False)

```
--logic_child_deadhand
```

Enable the logic to consider the child defeating Deadhand with only Deku Sticks (default: False)

```
--logic_dc_jump
```

Enable the logic to consider the trick to bypass the second Lizalfos fight room in Dodongo's Cavern as an adult with a simple jump (default: False)

```
--logic_windmill_poh
```

Enable the logic to consider the trick to reach the Piece of Heart in the windmill as an adult with nothing (default: False)

```
--logic_crater_bean_poh_with_hovers
```

Enable the logic to consider the trick to reach the Piece of Heart on the volcano in Death Mountain Crater with Hover Boots (default: False)

```
--logic_zora_with_cucco
```

Enable the logic to consider the trick to enter Zora's Domain as a child using a Cucco instead of playing Zelda's Lullaby (default: False)

```
--logic_zora_with_hovers
```

Enable the logic to consider the trick to enter Zora's Domain as an adult using Hover Boots instead of playing Zelda's Lullaby (default: False)

```
--logic_fewer_tunic_requirements
```

Reduce the number of locations for which the logic expects a tunic upgrade (default: False)

```
--logic_lens [{chest,chest-wasteland,all}]
```

Set which hidden objects the logic expects the Lens of Truth to be used on (default: all)

```
--ocarina_songs
```

Randomize the particular notes that must be played for each of the 12 standard ocarina songs (default: False)

```
--correct_chest_sizes
```

Set chest sizes based on contents (default: False)

```
--clearer_hints
```

Reword hints to be incredibly direct (default: False)

```
--hints [{none,mask,agony,always}]
```

Enable hints from Gossip Stones and select the condition to read them (default: agony)

```
--text_shuffle [{none,except_hints,complete}]
```

Shuffle the chosen text randomly (default: none)

```
--difficulty [{normal,hard,very_hard,ohko}]
```

Alter the item pool to increase difficulty. The ohko option also causes Link to die in one hit. (default: normal)

```
--default_targeting [{hold,switch}]
```

Set the default Z-targeting setting. It can still be changed in the game's options menu. (default: hold)

```
--background_music [{normal,off,random}]
```

Choose whether the game's background music will be left alone, disabled, or shuffled randomly. (default: normal)

```
--kokiricolor [{'Random Choice', 'Completely Random', 'Kokiri Green', 'Goron Red', 'Zora Blue', 'Black', 'White', 'Purple', 'Yellow', 'Orange', 'Pink', 'Gray', 'Brown', 'Gold', 'Silver', 'Beige', 'Teal', 'Royal Blue', 'Sonic Blue', 'Blood Red', 'Blood Orange', 'NES Green', 'Dark Green', 'Lumen'}]
```

Select the color of Link's Kokiri Tunic. (default: Kokiri Green)

```
--goroncolor [{'Random Choice', 'Completely Random', 'Kokiri Green', 'Goron Red', 'Zora Blue', 'Black', 'White', 'Purple', 'Yellow', 'Orange', 'Pink', 'Gray', 'Brown', 'Gold', 'Silver', 'Beige', 'Teal', 'Royal Blue', 'Sonic Blue', 'Blood Red', 'Blood Orange', 'NES Green', 'Dark Green', 'Lumen'}]
```

Select the color of Link's Goron Tunic. (default: Goron Red)

```
--zoracolor [{'Random Choice', 'Completely Random', 'Kokiri Green', 'Goron Red', 'Zora Blue', 'Black', 'White', 'Purple', 'Yellow', 'Orange', 'Pink', 'Gray', 'Brown', 'Gold', 'Silver', 'Beige', 'Teal', 'Royal Blue', 'Sonic Blue', 'Blood Red', 'Blood Orange', 'NES Green', 'Dark Green', 'Lumen'}]
```

Select the color of Link's Zora Tunic. (default: Zora Blue)

```
--navicolordefault [{'Random Choice', 'Completely Random', 'Gold', 'White', 'Green', 'Light Blue', 'Yellow', 'Red', 'Magenta', 'Black', 'Tatl', 'Tael', 'Fi', 'Ciela', 'Epona', 'Ezlo', 'King of Red Lions', 'Linebeck', 'Loftwing', 'Midna', 'Phantom Zelda'}]
```

Select the color of Navi in idle. (default: White)

```
--navicolorenemy [{'Random Choice', 'Completely Random', 'Gold', 'White', 'Green', 'Light Blue', 'Yellow', 'Red', 'Magenta', 'Black', 'Tatl', 'Tael', 'Fi', 'Ciela', 'Epona', 'Ezlo', 'King of Red Lions', 'Linebeck', 'Loftwing', 'Midna', 'Phantom Zelda'}]
```

Select the color of Navi when she is targeting an enemy. (default: Yellow)

```
--navicolornpc [{'Random Choice', 'Completely Random', 'Gold', 'White', 'Green', 'Light Blue', 'Yellow', 'Red', 'Magenta', 'Black', 'Tatl', 'Tael', 'Fi', 'Ciela', 'Epona', 'Ezlo', 'King of Red Lions', 'Linebeck', 'Loftwing', 'Midna', 'Phantom Zelda'}]
```

Select the color of Navi when she is targeting an NPC. (default: Light Blue)

```
--navicolorprop [{'Random Choice', 'Completely Random', 'Gold', 'White', 'Green', 'Light Blue', 'Yellow', 'Red', 'Magenta', 'Black', 'Tatl', 'Tael', 'Fi', 'Ciela', 'Epona', 'Ezlo', 'King of Red Lions', 'Linebeck', 'Loftwing', 'Midna', 'Phantom Zelda'}]
```

Select the color of Navi when she is targeting a prop. (default: Green)

```
--navisfxoverworld [{Default,Notification,Rupee,Timer,Tamborine,Recovery Heart,Carrot Refill,Navi - Hey!,Navi - Random,Zelda - Gasp,Cluck,Mweep!,Random,None}]
```

Select the sound effect that plays when Navi wishes to speak with the player. (default: Default)

```
--navisfxenemytarget [{Default,Notification,Rupee,Timer,Tamborine,Recovery Heart,Carrot Refill,Navi - Hey!,Navi - Random,Zelda - Gasp,Cluck,Mweep!,Random,None}]
```

Select the sound effect that plays when Navi targets an enemy. (default: Default)

```
--healthSFX [{'Default', 'Softer Beep', 'Rupee', 'Timer', 'Tamborine', 'Recovery Heart', 'Carrot Refill', 'Navi - Hey!', 'Zelda - Gasp', 'Cluck', 'Mweep!', 'Random', 'None'}]
```

Select the sound effect that loops at low health. (default: Default)

```
--gui
```

Open the graphical user interface. Preloads selections with set command line parameters.

```
--loglevel [{error,info,warning,debug}]
```

Select level of logging for output. (default: info)

```
--settings_string SETTINGS_STRING
```

Enter a settings string that will encode and override most individual settings.
