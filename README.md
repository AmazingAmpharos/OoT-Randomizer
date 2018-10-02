# OoTRandomizer

This is a randomizer for _The Legend of Zelda: Ocarina of Time_ for the Nintendo
64.

# Installation

It is strongly suggested users get the latest release from here:
https://github.com/AmazingAmpharos/OoT-Randomizer/releases.
For Windows machines, simply download the .msi installer and run it.

If you are not running Windows or simply wish to run the script raw, clone this
repository and either run _Gui.py_ for a graphical interface or
_OoTRandomizer.py_ for the command line version. Both require Python 3.5+.

This randomizer requires The Legend of Zelda: Ocarina of Time version 1.0
NTSC-US. It includes an in-built decompressor, but if you wish a previously
decompressed ROM may be used as well. Please be sure your input ROM is either a
.n64 or .z64 file. For users playing via means other than on real N64 hardware,
 use of the "Compress patched ROM" option is strongly encouraged, as
uncompressed ROMs are impossible to inject for the Virtual Console and tend to
crash randomly on all emulators.

For general use, the recommended emulator is RetroArch; it has been shown to
work with minimal issues. Bizhawk and Mupen64plus are generally good choices
too. If you would like to play on Project 64 for whatever reason, you can, but
you will need to set the rando to use 8 MB of RAM and will want to play with the
cheat code `8109C58A 0000` to partially fix Project 64's tragically poor
handling of OoT's pause menu. Project 64 also has one particular crash that only
happens for some unknown settings configurations; we cannot support this. I
cannot emphasize enough that its use is discouraged for the purposes of this
project.

# General Description

This program takes _The Legend of Zelda: Ocarina of Time_ and randomizes the
locations of the items for a more dynamic play experience. Proper logic is used
to ensure every seed is possible to complete without the use of glitches and
will be safe from the possibility of softlocks with any possible usage of keys
in dungeons.

The items randomized currently include all items held within chests (including
those in grottos); special one-time items given as rewards by NPCs; upgrades
purchased from Deku Scrub Salesmen; freestanding Pieces of Heart, Heart
Containers, and Keys; the Ocarina of Time, Fire Arrows, and the bottle beneath
Lake Hylia. All dungeons will contain the same number of Maps, Compasses, Small
Keys, and Boss Keys as they had in the original game, but the chests which
contain them will be randomized.

The item pool will include a Biggoron's Sword that will not interfere with
Medigoron's sale of the Giant's Knife (which is always vanilla), and a randomly
selected adult trading quest item other than the Odd Potion will be somewhere in
the item pool.

Certain types of items are now "progressive", meaning that regardless of the
order the player encounters these items, they will function as a series of
upgrades akin to the natural progression of these items in vanilla playthroughs.

The following item types will be progressive upgrades:
* Hookshot, Longshot
* Bomb Bag, Big Bomb Bag, Biggest Bomb Bag
* Goron Bracelet, Silver Gauntlets, Gold Gauntlets
* Slingshot, Big Bullet Bag, Biggest Bullet Bag
* Bow, Big Quiver, Biggest Quiver
* Silver Scale, Gold Scale
* Adult Wallet, Giant's Wallet
* Deku Stick Capacity
* Deku Nut Capacity
* Magic Meter, Double Magic

To elaborate upon which NPC items are shuffled: it's generally the one-time
permanent item rewards, like Pieces of Heart or inventory items that were
originally given by NPCs. The only exception to this rule is the reward for 40
Gold Skulltulla Tokens, only 10 Bombchus in vanilla. This is still a randomized
reward (but the 200 rupees for all 100 Gold Skulltulla Tokens is not randomized
so the most tokens that could be required to complete a seed is 50).

As a mercy to the player the following changes are in place:
* The Ocarina memory game in the Lost Woods will start on the final round.
* The three day wait on the Claim Check is removed.
* Bombchu Bowling will have a fixed sequence of prizes that is of maximum
convenience to the player.
* Dampe's Gravedigging Tour will always reveal a Piece of Heart upon the first
try.
* The fishing minigame is made much simpler (8 lb fish for child now, 10 lb for
adult).
* Additionally, any NPC who gives a trading quest item either for the child
or for the adult other than Anju's initial gift as an adult does not have a
randomized reward.

A special note is needed for the six Great Fairy Fountains scattered across
Hyrule. All six of these fountains now give random item rewards, and the magic
and life upgrades can now be found as normal items scattered around the world.
Happy hunting!

The Ocarina songs are shuffled in a pool amongst themselves, and each song
location will still have the original conditions it has always had. The
conditions for these events to occur may not have all been obvious, but here are
some high points. Saria will teach her song after the player meets Zelda in the
Castle Courtyard. Most of the warp songs can only be learned as an adult, but
the location for Requiem of Spirit is available for even a child if the Desert
Colossus can be reached. The location for the Prelude of Light requires the
Forest Medallion, and the location for the Nocturne of Shadow requires the
Forest Medallion, Fire Medallion, and Water Medallions. This can be changed with
a setting.

Speaking of Medallions, each boss in the eight main dungeons will drop a random
Spiritual Stone or Medallion, and instead of the Light Medallion being granted
by the now removed "becoming an adult" cutscene, the player will start every
seed with a random Spiritual Stone or Medallion. The pedestal in which the
Spiritual Stones rest in the Temple of Time has hint text pointing to the
locations of the Spiritual Stones and Medallions. A child will be able to read
hints for the Spiritual Stones, while an adult will be able to read hints for
the Medallions. This information and some other relevant dungeon based info can
be seen in the pause menu by holding the "A" button on the C-item menu.

To be very clear on this point, while the rewards for up to 50 Gold Skulltulla
Tokens are randomized, the tokens themselves are not.

As a service to the player in this very long game, many cutscenes have been
greatly shortened or removed entirely, and text is as often as possible either
omitted or sped up. We have been as thorough as our exploration of the game and
various technical limitations will allow to reduce the time you spend sitting
through cutscenes and dialog, so as to maximize the time you spend with this
randomizer actually playing the game. I'm sure someone somewhere will miss the
owl's interjections; to that person, I'm sorry I guess?

A few bugs or other undesirable behaviors in the original game have been fixed.
Of note, obtaining the Poacher's Saw will no longer prevent the player from
obtaining the reward in the Deku Theater for showing the Mask of Truth, and
becoming an adult will not automatically equip the child with the Kokiri Sword.
Sheik will no longer prevent the player from returning to childhood before
obtaining the Forest Medallion. Princess Ruto will never disappear from Jabu
Jabu's Belly, and the condition for the Castle Courtyard being sealed off is now
completing the events within as opposed to Zelda fleeing the castle.

One small detail that is important to know is that the locked door in the Fire
Temple leading to the section with the Boss Key Chest is removed. This was
necessary due to the original design of the Fire Temple assuming that the player
could not possibly have the Hammer before unlocking the doors leading into the
depths of the dungeon. This is obviously not true in randomizer, and of all
possible solutions to this problem, this seemed the least disruptive. A full
clear of the Fire Temple will simply result in the player having one extra Small
Key. Certain settings will disable this behavior.

To further explain the logic that determines what items can be placed where: the
randomizer will always ensure that a glitchless path exists, but it will not
prevent the use of glitches for players who enjoy that sort of thing. However,
we offer no guarantees that glitches will have the same behavior they had in the
original game. Glitchless can still mean that clever or unintuitive strategies
are required that involve the use of things like Hover Boots, the Hookshot, or
Scarecrow's Song that may not have been necessary in the original game. The Lens
of Truth is guaranteed to be available before you are expected to complete the
Treasure Chest Game or open any invisible chests or walk through any false
walls, with the exception of the false wall required to enter the Bottom of the
Well, since it was the original game's expectation that the player would cross
it before reaching the Lens of Truth.

One last detail to note is that the pause menu now controls like the one in
Majora's Mask, meaning that the cursor will cross through empty spaces. This
fixes a major problem from the original game wherein having certain combinations
of items results in menu shapes that would be impossible to fully navigate.
Unfortunately, as of this 3.0 release, this functionality does not apply to the
Equipment Subscreen which can rarely create some tricky situations. Usually
these can be resolved simply by purchasing a Deku Shield and a Hylian Shield.

# Quirks to Be Aware of

While all the details of gameplay can't be explained here, I want to inform you
of a few non-obvious game sequences that are likely to get you stuck and one
little glitch we can do nothing about.

* The condition to open the Door of Time is merely playing the Song of Time; the
Spiritual Stones are not actually required. If you enter the Temple of Time via
the Prelude of Light, playing the Song of Time will create a glitchy cutscene
and will not open the door (but you're safe to exit, re-enter, and open it
properly from there).
* To get the Ocarina of Time at the drawbridge you must collect the three
Spiritual Stones.
* For Sheik to teach you the song in the Temple of Time you must possess the
Forest Medallion.
* For Sheik to teach you the song in Kakariko Village you must possess the
Forest, Fire, and Water Medallions.
* The running man in Hyrule Field only appears once you have all three Spiritual
Stones (He starts from the stream northwest).
* Skull Kid will only buy the Skull Mask if you have played Saria's Song for
him.
* The center of Death Mountain Crater can be reached from the summit as an adult
by going around to the left with Hover Boots or by jumping down to the right and
using a combination of the Longshot and Scarecrow's Song. This allows access to
Sheik and the Fire Temple without a Bomb Bag.
* A sword must be equipped to play the fishing minigame.
* The Slingshot is not required to play at the Shooting Gallery as a child, but
you will need the Bow in order to play as an adult.
* The child can do anything that would seem to require the sword with Deku
Sticks. You can buy as many as you want in the Kokiri Forest shop.
* In the randomizer, possessing the Bomb Bag is the requirement for finding bomb
drops, purchasing Bombs or Bombchus, and playing at the Bombchu Bowling Alley.
* Only the Hookshot, not the Longshot, is needed to do everything on the
rooftops of Kakariko.
* Grottos can be opened with either Bombs or the Hammer.
* The boulder maze in Goron City can be solved partially with Bombs and fully
with just the Hammer, but less obvious is that it can be fully solved
using only the Silver Gauntlets.
* Even though Link doesn't appear to be wearing it as an adult, the Goron
Bracelet is needed to push large colored blocks such as the ones in the Forest
Temple.
* In a few places, out of sight Song of Time blocks can be summoned. The lava
room in Gerudo Training Grounds, the Anubis room the adult portion of the Spirit
Temple, the beginning of the Shadow Trial in Ganon's Castle, and the last
hallway with a caged Goron in Fire Temple are the main cases.
* Adult Link can fully clear Dodongo's Cavern. He can even skip the first
section by virtue of being tall.
* In the Forest Temple, you can reach the room with the Floormaster (vanilla) or
Redead (MQ) early by using Hover Boots in the block push room.
* In the Fire Temple, you can reach the Boss Key door from the beginning with
Hover Boots.
* Starting in the Water Temple with the water lowered, you can jump down to the
middle platform level. From there you can very carefully aim your Hookshot to
the target above, pulling yourself to the highest level of the central platform.
Finally, with a very well-spaced rolling jump, you can reach the platform to
raise the water to the highest level. If you manage your keys poorly in the
temple this may be what you need to do to untangle the situation.
* In the Water Temple, you can use the Hover boots to bypass the room that
requires Bombs and pushing large blocks, in order to reach the vanilla Boss Key
chest. You can also use them to avoid the Longshot requirement on the middle
level chest that requires the Bow.
* In the Shadow Temple, you can avoid the need for the Longshot in the room with
the invisible spikes by backflipping onto the chest for extra height.
* In the Shadow Temple, you can hookshot directly onto the ladder by the boat to
avoid having to push the large block.
* In the Shadow Temple, a combination of the Scarecrow's Song and the Longshot
can be used to reach Bongo Bongo without the Bow.
* In the Spirit Temple, you can activate the vanilla Map chest with only a lit
Deku Stick. Fire magic is not needed.
* In the Spirit Temple, you can collect the silver rupees without Hover Boots by
jumping directly onto the rolling boulder or using a jump slash.
* From the opposite hand of the Desert Colossus, you can use the Longshot to
reach what is the Silver Guantlets chest in vanilla.
* In the Spirit Trial of Ganon's Castle, the web can be burned with a precise
shot of an arrow through the torch. Fire Arrows are not required.
* While we guarantee the tunics to be available before Fire Temple and Water
Temple, you can possibly trap yourself into going without if you seriously let a
Like Like eat your tunic without then recovering it. It is almost always
possible to go without, but it can make things really difficult for you.
* Several Gold Skulltulla Tokens can be reached by clever/precise uses of jump
slashes and spin attacks (possibly Great Spins).

# Known issues

Sadly, for this 3.0 release a few known issues exist. These will hopefully be
addressed in future versions.

* The fishing minigame sometimes refuses to let you to catch fish, specifically
when playing on Bizhawk. Save and quit (DON'T savestate) and return to fix the
issue.
* Draining the well with the Song of Storms sometimes crashes with specific
configurations of Project 64. We aren't sure of the exact story, but this bug
is easily avoided by playing on a different emulator. If you must use Project
64, the crash is also probably avoidable by changing your settings and perhaps
your graphics plugin.
* Executing the collection delay glitch on various NPCs may have unpredictable
and undesirable consequences. In particular, this can be devastating with
Biggoron; it is strongly suggested you save before turning in the Claim Check.
* Saving and quitting on the very first frame after becoming an adult at a
point in the game when you would trigger the Light Arrow cutscene can have
undesired consequences. Just don't do that.
* The Equipment Subscreen still cannot be easily navigated with all item
configurations. This can be especially problematic if Biggoron's Sword is found
very early or if shields cannot be easily purchased thanks to shopsanity.
Getting the Master Sword and buying as many shields as you can is a good way to
mitigate these issues.

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

The Door of Time is open from the beginning of the game. The Song of Time is still potentially useful to move Song of Time blocks, play songs for the frogs on Zora's
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
Village to be distinct shops from the two similar shops in child Castle Town; however, the shops in Kokiri Forest, Goron City, and Zora's Domain are
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

* A precise jumpslash with either a Deku Stick or the Kokiri Sword can be used to reach a Gold Skulltulla on some vines in standad Deku Tree.
* The Bow can be used to knock down the stairs in Dodongo's Cavern with two well timed shots.
* The vines in Forest Temple leading to where the well drain switch is in the standard form can be barely reached with the standard Hookshot.
* A Bombchu from the ground level can be used to hit the switch to bypass the block pushing puzzle in Forest Temple MQ.
* A rusted switch under a Song of Time block in the standard Fire Temple can be hit by using Hammer into the block.
* The location with the Boss Key chest in Fire Temple MQ can be reached without the Bow with very particular use of Din's Fire.
* The upper levels of the old boulder maze in Fire Temple MQ can be reached without explosives by using the Hammer through a wall.
* In the standard Spirit Temple, the bridge on child side can be lowered with a carefully timed Bombchu.
* The frozen switch in Spirit Temple MQ can be hit without a fire source by using the Bow and Song of Time very cleverly.
* The chest in the basement of the standard Bottom of the Well can be reached with no additional items by using a jump slash with a lit
Deku Stick.
* The first room of the Spirit Trail in Ganon's Castle MQ can be cleared without the Bow by using a Hammer jump slash to hit the rusted switch
through the thrones.
* The Gold Skulltulla in adult Kokiri Forest can be reached without the Hookshot by using Hover Boots off one of the roots.
* The child can reach the chest on Death Mountain trail with just the Goron Bracelet by backwalking with the Bomb Flower intended to open
Dodongo's Cavern and throwing the Bomb Flower at the wall very quickly.
* Gerudo Fortress can be cleared without any items other than those needed for access. The logic normally guarantees one of the Bow, Hookshot, or
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

This allows the logic to consider using a Cucco on Zora's River to enter Zora's Domain as a child without playing Zelda's Lullaby. It requires slipping behind
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

* If the required number of trials is 1-3, a hint will be added for each trial that must be done. If the required number of trials is 4 or 5, a hint will be added
for each trial that can be skipped.
* Hints will be added for every one of the "always" locations that is allowed to have a random possibly valuable item under the current settings. These hints
will tell the player what item is at each of these locations. These locations are the rewards for 30, 40, and 50 Gold Skulltulla Tokens, the item obtained from
Biggoron by showing the Claim Check, the item obtained from the Big Poe vendor, both the song and the item slots at the Ocarina of Time, and the item obtained
from showing the Mask of Truth at the Deku Theater.
* Some hints will be given for items at a randomly selected number of other locations that are generally somewhat inconvenient to check. The total number of these
hints will be either 11 or 12 minus the number of always hints placed.
* 3 or 4 hints will be given naming a specific non-dungeon specific item that can be found in a randomly chosen dungeon.
* 1 to 4 hints will be given naming a specific item found in a specific overworld region. Which part of this range is used is determined in part by how many
trial hints are given.
* 4 to 6 hints will be given naming what region specific progression items other than Gold Skulltulla Tokens can be found.
* 3 or 4 hints will be given naming specific regions that are "on the way of the hero" and thus contain at least one required progression item.
* All remaining hints (33 total unique Gossip Stones exist) will be filled with non-information junk hints.

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
--create_spoiler      
```

Output a Spoiler File (default: False)

```
--bridge [{medallions,vanilla,dungeons,open}]
```

Select the condition to spawn the Rainbow Bridge to Ganon's Castle. (default: medallions)

```
--kokiricolor [{'Kokiri Green', 'Goron Red', 'Zora Blue', 'Black', 'White', 'Purple', 'Yellow', 'Orange', 'Pink', 'Gray', 'Brown', 'Gold', 'Silver', 'Beige', 'Teal', 'Royal Blue', 'Sonic Blue', 'Blood Red', 'Blood Orange', 'NES Green', 'Dark Green', 'Random', 'True Random'}]
```

Select the color of Link's Kokiri Tunic. (default: Kokiri Green)

```
--goroncolor [{'Kokiri Green', 'Goron Red', 'Zora Blue', 'Black', 'White', 'Purple', 'Yellow', 'Orange', 'Pink', 'Gray', 'Brown', 'Gold', 'Silver', 'Beige', 'Teal', 'Royal Blue', 'Sonic Blue', 'Blood Red', 'Blood Orange', 'NES Green', 'Dark Green', 'Random', 'True Random'}]
```

Select the color of Link's Goron Tunic. (default: Goron Red)

```
--zoracolor [{'Kokiri Green', 'Goron Red', 'Zora Blue', 'Black', 'White', 'Purple', 'Yellow', 'Orange', 'Pink', 'Gray', 'Brown', 'Gold', 'Silver', 'Beige', 'Teal', 'Royal Blue', 'Sonic Blue', 'Blood Red', 'Blood Orange', 'NES Green', 'Dark Green', 'Random', 'True Random'}]
```

Select the color of Link's Zora Tunic. (default: Zora Blue)

```
--healthSFX [{'Default', 'Softer Beep', 'Rupee', 'Timer', 'Tamborine', 'Recovery Heart', 'Carrot Refill', 'Navi - Hey!', 'Zelda - Gasp', 'Cluck', 'Mweep!', 'Random', 'None'}]
```

Select the sound effect that loops at low health. (default: Default)

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
--fast_ganon
```

Set whether most of Ganon's Castle can be skipped. (default: False)

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
