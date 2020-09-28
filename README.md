# OoTRandomizer

This is a randomizer for _The Legend of Zelda: Ocarina of Time_ for the Nintendo 64.

* [Installation](#installation)
* [General Description](#general-description)
  * [Getting Stuck](#getting-stuck)
  * [Settings](#settings)
  * [Known Issues](#known-issues)
* [Changelog](#changelog)
  * [5.2](#52)
  * [5.1](#51)
  * [5.0](#50)
  * [4.0](#40)

## Installation

It is strongly suggested users use the web generator from here:

https://ootrandomizer.com

If you wish to run the script raw, clone this repository and either run ```Gui.py``` for a
graphical interface or ```OoTRandomizer.py``` for the command line version. They both require Python 3.6+. This will be fully featured,
but the seeds you generate will have different random factors than the bundled release.

This randomizer requires The Legend of Zelda: Ocarina of Time version ```1.0 NTSC-US```. This randomizer includes an in-built decompressor, but if
the user wishes a pre-decompressed ROM may be supplied as input. Please be sure your input ROM filename is either a .n64 or .z64 file. For users
playing via any means other than on real N64 hardware, the use of the "Compress patched ROM" flag is strongly encouraged as uncompressed ROMs are
impossible to inject for the Virtual Console and have random crashing problems on all emulators.

For general use, the recommended emulator is RetroArch; it has been shown to work with minimal issues. Bizhawk and Mupen64plus are generally good choices
too. If you want to play on Project 64 for whatever reason, you can, but you will need to set the rando to use 8 MB of RAM and will want to play with the
cheat code ```8109C58A 0000``` to partially fix Project 64's tragically poor handling of OoT's pause menu. Project 64 also has one particular crash that only
happens for some unknown settings configurations; we cannot support this. We cannot emphasize enough that it is a discouraged emulator to use.

## General Description

This program takes _The Legend of Zelda: Ocarina of Time_ and randomizes the locations of the items for a new, more dynamic play experience.
Proper logic is used to ensure every seed is possible to complete without the use of glitches and will be safe from the possibility of softlocks with any possible usage of keys in dungeons.

The randomizer will ensure a glitchless path through the seed will exist, but the randomizer will not prevent the use of glitches for those players who enjoy that sort of thing though we offer no guarantees that all glitches will have identical behavior to the original game.
Glitchless can still mean that clever or unintuitive strategies may be required involving the use of things like Hover Boots, the Hookshot, or other items that may not have been as important in the original game.

Each major dungeon will earn you a random Spiritual Stone or Medallion once completed.
The particular dungeons where these can be found, as well as other relevant dungeon information can be viewed in the pause menu by holding the "A" button on the C-Item Menu.

As a service to the player in this very long game, many cutscenes have been greatly shortened, and text is as often as possible either omitted or sped up. It is likely that someone somewhere will miss the owl's interjections; to that person, I'm sorry I guess?

### Getting Stuck

With a game the size of _Ocarina of Time_, it's quite easy for new Randomizer players to get stuck in certain situations with no apparent path to progressing. Before reporting an issue, please make sure to check out [our Logic wiki page](https://wiki.ootrandomizer.com/index.php?title=Logic).

### Settings

The OoT Randomizer offers many different settings to customize your play experience.
A comprehensive list can be found [here](https://wiki.ootrandomizer.com/index.php?title=Readme).

#### Plandomizer

"Plan"-domizer is a feature that gives some additional control over the seed generation using a separate distribution file. In such a file you can:
* Place items at specific locations or restrict items from being placed at specific locations.
* Add or remove items from the item pool.
* Select items to start with.
* Set specific dungeons to be vanilla vs Master Quest.
* Set which trials are required.
* Set any regular settings.

Caveat: Plandomizer settings will override most settings in the main OoTR generator settings, particularly list-based settings like enabled tricks or starting inventory. For example, if the Plandomizer distribution file contains an empty list of starting items, and the generator settings include additional starting equipment, the player will start with none of them instead. You will have to edit the Plandomizer file to change such settings, or **delete** completely the line in the Plandomizer file with the given setting to allow the main generator to alter the setting.

See [the Plandomizer wiki page](https://wiki.ootrandomizer.com/index.php?title=Plandomizer) for full details.

### Known issues

Unfortunately, a few known issues exist. These will hopefully be addressed in future versions.

* The fishing minigame sometimes refuses to allow you to catch fish when playing specifically on Bizhawk. Save and Hard Reset (NOT savestate) and return to fix the
issue. You should always Hard Reset to avoid this issue entirely.
* Draining the Bottom of the Well with Song of Storms sometimes crashes on specific configurations of Project 64. We aren't sure of the exact story, but this bug is
easily avoided by playing on a different emulator and probably also avoidable by changing your settings and maybe graphics plug-in.
* Executing the collection delay glitch on various NPCs may have unpredictable and undesirable consequences.
* Saving and quitting on the very first frame after becoming an adult when you would trigger the Light Arrow cutscene can have undesired consequences. Just don't
do that.
* This randomizer is based on the 1.0 version of _Ocarina of Time_, so some of its specific bugs remain. Some of these like "empty bomb" can be disadvantageous to the
player.

## Changelog

### Dev

#### New Features
* New setting `Skip Some Minigame Phases`
  * Allows getting both rewards for Horseback Archery and Dampé Race in a single go!
  * Replaces the `Skip First Dampé Race` setting.
* `Lens of Truth` setting has been removed and replaced with several independent tricks.
  * `Lensless Wasteland`: assumes you can navigate the Wasteland to the Colossus without the Lens of Truth.
  * `<Area> without Lens of Truth`: assumes you can complete the given area without the Lens of Truth. Note that MQ and Vanilla dungeons have separate tricks.
  * Shadow Temples are split into two separate areas for these tricks.
  * Glitchless logic now requires Lens (or an appropriate trick) for some checks, particularly in Shadow Temple.
  * Glitched logic may sometimes assume you can do something without lens regardless of trick settings.
* New setting `Kakariko Gate`
  * Allows configuring how the Kakariko Gate and the Happy Mask Shop will open.
  * Default (vanilla) behavior requires showing Zelda's Letter to the guard to open the gate and the shop.
  * You can configure the gate to be always open or to open automatically upon obtaining the Letter. Both of these options will also open the Happy Mask Shop upon obtaining the Letter.
* New setting `Complete Mask Quest`
  * Marks all the mask sales complete so that the shop has all masks available to borrow as soon as it opens.
* Updated setting `Shuffle Songs`
  * This now allows selecting from three options: shuffling in **song** locations (previously 'off'), shuffling in **anywhere** (previously 'on'), and shuffling in **dungeon** reward locations (new).
  * The dungeon reward locations are: the 9 boss heart containers, the Lens of Truth chest (BotW), the Ice Arrows chest (GTG), the song reward in Ice Cavern, and the song from Impa in Hyrule Castle.
  * In multiworld, as before, only the "anywhere" setting will allow songs to be placed in other players' worlds.
* New setting `Shuffle Medigoron & Carpet Salesman`
  * Adds the Giant's Knife and a pack of Bombchus to the pool while Medigoron and Carpet Salesman each sell a randomly placed item once for 200 rupees.
* New cosmetic setting `HUD Button Colors`
  * The buttons shown on the HUD can be colored to match the N64 or Gamecube color scheme, of OoT or MM.
  * Or you can randomize the button color scheme. (We'll try to keep the button text readable.)
* New cosmetic setting `Item Model Colors Match Cosmetics`
  * Freestanding models like heart containers, gauntlets, and heart/magic drops will match their respective color settings.
  * Tunics are not affected, in order to keep freestanding tunics recognizable.
* New tricks
  * `Dodongo's Cavern Vines GS from Below with Longshot` - use the Longshot to avoid the staircase.
  * `Forest Temple First Room GS with Difficult-to-Use Weapons` - use a sword or Deku Sticks to jumpslash, or Bombs as child.
  * `Spirit Temple Main Room Jump from Hands to Upper Ledges` - make a precise jump without Hookshot or Hover Boots.
  * `Water Temple Falling Platform Room GS with Boomerang` - use the Boomerang from the very edge of the platform.
  * `Death Mountain Trail Climb with Hover Boots` - get past the boulders without destroying them.
  * `Zora's Domain GS with No Additional Items` - use only a jumpslash.
  * `Ice Cavern Block Room GS with Hover Boots` - reach the GS with the Hover Boots to jumpslash it.
  * `Hyrule Castle Storms Grotto GS with Just Boomerang` - make a precise throw with the Boomerang to send it behind the wall.
  * `Water Temple Central Pillar GS with Iron Boots` - unlock the door on the middle level before raising the water.
  * `Water Temple Dragon Statue Switch from Above the Water as Adult` - trigger the switch from dry land, then use Iron Boots, any Scale, or a jump dive coming from the river.
  * `Water Temple Dragon Statue Switch from Above the Water as Child` - same but for child. The Scale dive is very precise.
  * `Goron City Grotto with Hookshot While Taking Damage` - brave the heat, but be quick.
  * `Dodongo's Cavern Two Scrub Room with Strength` - position a block correctly and adult can bring a bomb flower to the wall.
  * `Shadow Temple Falling Spikes GS with Hover Boots` - make a precise move to get on the falling spikes, then another precise move to grab the token.
* Removed tricks
  * `Water Temple Boss Key Chest with Iron Boots`
  * `Water Temple Dragon Statue with Bombchu` - superseded by the new Dragon Statue tricks.
* New "Hint Distribution" customization options
  * Old hardcoded hint distributions are now defined by json files in `data/Hints`.
  * Custom hint distributions can be added to this folder, or defined directly in Plando files.
  * Many locations that did not previously have item hints now have hints, in case a custom hint distribution makes use of them.
  * Using the hint distribution "Bingo" allows setting a "Bingosync URL" to build hints for the specific OoTR Bingo board. Otherwise it's a generic hint distribution for OoTR Bingo.
* Hint distributions can configure groups of stones to all have the same hint, and can also disable stones from receiving useful hints (give them junk hints instead).
* Tournament hint distribution changes <!-- keep updated if there are changes later -->
  * Temple of Time stones all provide the same hint.
  * Grotto stones are disabled and only provide junk hints.
  * Only "always" and "WotH" hints have duplicates now.
  * Number of unique hints of each type are now (not counting seed-dependent hint types like 'always' and 'trial'): 4 WotH, 0 barren, 4(remainder) sometimes.
* Added options to `Background Music` and `Fanfares` for randomly selecting only from [custom music](https://wiki.ootrandomizer.com/index.php?title=Readme#Custom_Music_and_Fanfares).
* Tricks can be filtered in the GUI using a new dropdown.

#### Bug Fixes
* Bunny Hood speed bonus now applies correctly in cases other than child running at full speed.
* Avoid crashing on some systems when using child items as adult.
* Ensure Ice Traps have valid models if they can be seen.
* Limit Kokiri Tunic RGB values in Glitched Logic to prevent Weirdshot crashes.
* Prevent Gerudo guards from throwing child Link in jail.
* Prevent an errant `@` from showing up in Triforce Hunt.
* Allow playthrough to collect a second 'Bottle with Letter' as its first empty bottle.
* Fix some issues with `Randomize Main Rules`:
  * Closed Forest implies starting as child.
  * Triforce Hunt won't accidentally place the Boss Key for Ganon's Castle.
* Fix a rare issue in ER with using time-passing regions to gain new access.
* Fix a rare issue where settings strings weren't allocated enough bits.
* The seed generator can now retry a few times in case of failure.
* Exclude a line from text shuffle so the Malon race is completable.
* Minor plandomizer fixes and improvements.
* Various logic fixes.

#### Other Changes
* Most locations and a few items have been renamed to improve spoiler output and standardize.
  * This will break settings and distribution files from previous versions that reference these locations and items.
* In-game hints overhaul.
* File 3 has been removed from generated ROMs to free up some space.
* The Zora Sapphire in Jabu Jabu's Big Octo room is now the actual dungeon reward.
* The number of Triforces available in Triforce Hunt now rounds to the nearest whole number instead of the nearest whole **even** number.
* Performance improvements to seed generation.
* Updated development n64 compilation process to use latest available toolchain.
* Changed some C code to support GCC 10 in development n64 compilation.
* Added decompressor source and updated Decompress binaries.
* OoTRandomizer.py returns an error code on failure to interact better with user scripting.
* Plandomizer distribution files are copied to the Output directory next to the Spoiler and Cosmetics logs.
* Mweep.

### 5.2

#### New Features
* Triforce Hunt
  * Collect some number of Triforce Pieces to beat the game instead of beating Ganon.
  * Multiworld Triforce counts are collective, so once the total is reached across all players everyone wins.
  * If enabled via randomizing main rules, the count is always 20.
* Separate Double Defense model
  * Now appears as a color-shifted version of the Heart Container, with a transparent interior and prominent gold border.
* Visual Stone of Agony indicator
  * When the player has the Stone of Agony, it will appear on-screen above the rupee count when the player is near a hidden grotto.
  * The icon vibrates based on proximity to the grotto entrance, similar to the rumble pak.
  * A real rumble pak is not required.
* Starting Inventory
  * A new tab in the GUI allows setting initial inventory, without having to create a Plandomizer file.
  * Items are divided into sections in the GUI based on category.
  * Trade quest items, Gerudo Membership Card, Scarecrow Song not included.
    * To start with the Gerudo Membership Card, set `Gerudo Fortress` to `Open Fortress` and disable `Shuffle Gerudo Card` ('Main Rules' tab).
    * To start with the Scarecrow Song, enable `Free Scarecrow's Song` ('Other' tab).

#### Updated Settings 
* Open Zora Fountain now has an open only adult option.
* Added a new setting `Ice Trap Appearance` to select whether ice traps appear as major items (the default), junk items, or anything. This appearance can affect chest size with `Chest Size Matches Contents` enabled.
* Removed settings `Start with Fast Travel`, `Start with Tycoon's Wallet`, `Start with Deku Equipment`.
  * These have been replaced with settings in the "Starting Inventory" tab.
* New settings `Start with Consumables` (enable to start with max Sticks, Nuts, and ammo), `Starting Hearts` (changes starting max health).
* New list settings `Starting Equipment` (swords, shields, strength, etc.), `Starting Items` (c-items), `Starting Songs` (songs).
* Logic now requires Stone of Agony to access any hidden grotto.
  * A new trick `Hidden Grottos without Stone of Agony` will bypass this.
  * Stone of Agony is now only considered a useless item (for barren areas) when this trick is on and Gossip Stones do not use it.
* Added a new trick `Goron City Spinning Pot PoH with Strength`, which allows stopping the Spinning Pot using a bomb flower.
* Hell Mode preset includes both the above tricks.
* Tricks enabled/disabled in a Plandomizer file now take precedence over Tricks in 'Detailed Logic', even if the Plandomizer file has an empty list.
  * An empty list means the seed will be beatable without any tricks.
  * If there's no `allowed_tricks` item in the file, the Detailed Logic tricks apply instead.
  * If there is an `allowed_tricks` list in the file, it will not be possible to disable any of the enabled tricks (or enabling more) without editing the file.

#### Other Changes
* Cosmetic heart color setting now applies in the file select screen.
* Cosmetic tunic color setting now applies to the icons in the pause menu.
* Non-Always Location hints cannot be placed for an area that already has a Foolish hint.
  * If the location hint is placed first, then it can still appear in a foolish hinted area, however in Tournament hint distribution the Foolish hints are placed first so that cannot happen.
* The location containing Light Arrows will be considered a hinted location if Ganondorf's hint can be reached without them.
* Ganondorf no longer hints at his Boss Key chest contents, except when Light Arrows don't exist (only possible in Triforce Hunt).
* Improved Entrance Randomizer hints.
* Updated Compressor. The GUI progress bar is now granular. If for some reason, the rom won't fit into 32MB, then the compressor will increase the output size.
* Revised some settings tooltips.
* Refactored Logic once again. It now uses helper json rules and rules can reference other rules.
* Disabled settings don't show up in the spoiler.
* Plando will now accept JSON lists for `item` in the location dictionary to randomly choose between for placement.
  * Attempts to not exceed item pool values until all the pool counts for the items in the list are reached.
* Plando locations are matched without regard to case.
* "Start with" settings are now handled by the Plando library.
* Further seed generation speed improvements.
* The main search algorithm was renamed Search (from Playthrough) to avoid confusion with the spoiler playthrough.
* General code cleanup and typo fixes.
* Added more Plando unittests.

#### Bug Fixes
* Minor stability fix in Plando.
* Spoilers for plando'd seeds now correctly show the tricks enabled for the seed.
* Plando no longer occasionally attempts to place an item on a location where it's not allowed.
* Plando starting items and items set in specific locations now count toward the pool allocation. (Starting items are replaced with junk.)
* Plando now refuses to place more than the maximum amount of bottles, adult trade items, shop items, or total non-junk items.
* Plando no longer places Ice Traps as Junk if `Ice Traps` is set to 'off'.
* Other various Plando bug fixes.
* Starting items for adult that auto-equip should do so correctly now. (Non-Kokiri Tunics won't autoequip at the moment.)
* Fixed two chests in MQ Shadow Temple that had swapped names in plando and spoilers.
* Removed (unnecessarily) duplicated/overlapping hints.
* Hints that should come in multiples (duplicates) no longer come in singletons in certain corner cases.
* Randomizing main rules now works correctly.
* Removed a misleading random "trials" value from the non-randomized settings in the spoiler.
* Fix seed values with spaces no longer working.
* Removed a mispasted option description from Gauntlets colors tooltips.
* Major armips fix should prevent some crashes in Dev builds. (Devs: required armips version >= 0.10.0-68-g8669ffd)
* Miscellaneous logic fixes.
* Other bug fixes.

### 5.1

#### New Features
* `Skip First Dampé Race` 
  * Allows getting both rewards in one race if the 60 second target is cleared
* Rupee Icon Color changes based on your current wallet upgrade

#### Updated Settings 
* Improve `Ear Safe` to be less painful
* `Tokensanity: Overworld Only` 
  * Shuffles Gold Skultulla Tokens in the overworld to compliment `Dungeons Only`
* Configurable Skulltula target for the Bridge Requirement
* `Randomize Main Rule Settings` still allows setting the `MQ Dungeon Count`
* `Always Guaranteed Hints` are now determined conditionally based on settings
* `Default Presets` are updated to better reflect first time beginner settings
  * The previous `Beginner Preset` is renamed to `Easy Preset`

#### Bug Fixes
* Improve stability of music related features
* Fix "...???" textboxes at the entrance of Great Fairies
* In the unlikely event `Tournament Hints` runs out of hints, the remaining hints are filled with more "Sometimes Good" hints. If those run out as well then it will fill with "Random Locations" hints.
* The `Gerudo Valley Crate PoH as Adult with Hover Boots` trick now properly takes OHKO into account.
* Minor GUI tweaks
* Improve error feedback in GUI and Rules JSON


### 5.0

#### New Features
* New Electron GUI
  * New GUI now utilizes both Python and Node to bring you an even better interface
  * Now requires Node (with NPM), in addition to the Python requirement
* Glitched Logic
  * New Logic Rules option that takes movement glitches into consideration
  * Check out the Wiki for more information
* Entrance Randomizer
  * Randomize entrances/loading zones
  * Entrances are connected bidirectionally, and only shuffled with other entrances of the same pool
  * Ability to randomize entrances (loading zones) among multiple pools:
    * `Dungeons Only`: All Dungeons except Ganon's Castle
    * `Simple Indoors`: Dungeons; as well as Houses, Great Fairies, all Open and Hidden Grottos (including small Fairy Fountains and the Lost Woods Stage), and Graves.
    * `All Indoors`: Dungeons and Simple Indoors, as well as Link’s House, the Temple of Time, the Windmill, and Dampé’s Grave.
    * `All Indoors & Overworld Entrances`: Almost all loading zones connecting overworld areas, including Owls
  * Deku Tree, Fire Temple, and Bottom of the Well dungeon entrances are accessible as both ages
* Starting Age Option
  * Can now start as child, adult, or random
* Plan-domizer
  * Create a custom seed by placing items, hints and/or entrances where you want them
  * Customize starting items, item pools, active trials and Master Quest dungeons
  * Plandomizer files match the spoiler log JSON format
* Additional Customization
  * Additional Background Music Sequences can now be provided to be shuffled in
  * Fanfares randomization
  * Customizable Heart, Magic Meter, and Gauntlet colors
  * Separate inner and outer Navi colors
* Added `Randomize Main Rules` option
* Cow Sanity
  * Playing Epona's Song for a cow for the first time gives a randomized item.
* Shuffle Magic Beans
  * A pack of 10 beans is shuffled into the pool and the Bean Salesman sells a random item once for 60 rupees.
* Cucco Count
  * The number of cuccos to be gathered for Anju can be reduced or randomized, and Anju will tell you in-game the target number to catch (similar to 10 Big Poes).
* Enable Useful Cutscenes prevents some useful cutscenes from being skipped
  * Re-enables Poes at Forest Temple, Darunia at Fire Temple, and Twinrova at Spirit Temple

#### Major Changes
* Seeds generation is significantly faster
* Major refactor of logic for performance and ER
* Spoiler log is now in JSON format
* Log files are produced in `Logs` during generation to record any errors.
* Major Logic Changes
  * Desert Colossus Hands are now logically part of Spirit Temple
  * Added the ability to enter drain the Lake Hylia water as Adult after beating Morpha using a new Gossip Stone near the Serenade Warp Pad. Entering Water Temple with Gold Scale and Longshot is now always in logic, however no locations are accessible without additional tricks, Keysanity/Keysy, or Iron Boots.
  * Disabled Locations will always hold Junk items (except song locations if songs are not shuffled with items)
* Gameplay Changes
  * Mechanically, Hot Rodder Goron no longer checks for Bomb Bag
  * Wearing Bunny Hood increases running speed to match backwalking speed
  * All Gerudo now check for Gerudo Membership Card instead of Carpenters being freed
    * This only affects when `Shuffle Gerudo Card` is enabled or in Entrance Randomizer
    * In the affected modes, a Gerudo is added behind the Wasteland gate who can open the gate
  * Removed RNG from Fishing Minigame
    * Note: The optimal strategy is to have the line stationary for the fish to bite
  * Can now cast Farore's Wind and play Warp Songs from within Gerudo Training Grounds and all of Ganon's Castle
* Hint Changes
  * Every generic grotto gossip stone has their own hint.
  * The "Very Strong" hint setting can now give multiple Foolish dungeon hints.
  * The “Tournament” hint setting was revised to utilize all 40 hint stones.
    * Increased to 5 WOTH hints (with a new maximum of 2 Dungeon regions hinted); increased to 3 Foolish hints; Skull Mask added to Tournament hints’ Always hints; 5 Sometimes hints; all hints in this distribution are duplicated onto two Gossip Stones.
* Cutscene Changes
  * Burning Kakariko Cutscene can be triggered when entering Kakariko Village from any entrance.
  * Speedup Owl Flying cutscenes to be almost instant.
  * Enable Useful Cutscenes setting added (see above in New Features)

#### Updated Settings 
* Filter added to `Location Exclusion` dropdown
* More tricks added to the `Enable Tricks` dropdown
* Shuffle Gerudo Card can now be enabled alongside Open Gerudo Fortress.
* Forest Options
  * `Closed Deku`: Open Forest except Mido still blocks the Deku Tree
* Dungeon Item Options
  * Added `Vanilla` placement option for small keys, boss keys and maps/compasses
* Ganon's Boss Key 
  * Split Ganon’s Boss Key settings from the rest of the Boss Keys setting
  * Added LACS options that place the key there.
    * This allows playing with open bridge while still requiring dungeon completion
  * This replaces the Remove Ganon’s Boss Door Lock option
* Plentiful Item Pool
  * Duplicate Ruto's Letter added to plentiful item pool
* With `Start With Max Rupees` option enabled, wallet upgrades items now fill to max rupees

#### Bug Fixes
* No longer able to buy Bombchus with only bomb bag when Bombchus in logic
* Dampé freestanding Piece of Heart no longer requires opening the chest
* Buying Piece of Heart/Heart Container fully heals Link
* Learning Sun's Song from Malon no longer causes a softlock
* Castle and Gerudo guards can no longer cause softlock when catching you
* Vanilla shop items have correct price in spoiler log with shopsanity enabled
* Fixed Song of Storms not being usable in Sacred Forest Meadow immediately after learning it
* Improved Bottled Fairy logic rules for OHKO in ER
* Fixed `Starting Time of Day` times to better reflect their descriptions with the in-game state
  * `Night` options will spawn Skulltulas
* Add compatibility support for Python 3.8
* Improved Spoiler Logs for Multiworlds with differing Random settings between worlds
* Lab Dive now completable even with Eyedrops in your possession
* Great Fairy cutscene no longer plays on additional visits for health and magic refills.
* Running Man can now fill a Tycoon’s wallet when buying the Bunny Hood from the player


### 4.0

#### New Features

* Quick boot equips
  * Use D-pad left to equip Iron Boots if they're in the inventory, or D-pad right to equip Hover Boots if they're in the inventory.
  * Press the button again to equip Kokiri Boots.
* Quick Ocarina
  * Use D-pad down to pull out the Ocarina.
* Freestanding models
  * All freestanding item locations now display the model of the item you will receive.
* Ice traps now work from any location.
  * In freestanding locations, appears as a random major item
  * In shops, appears as a random major item with a misspelling
* Various speedups
  * No Talon cutscene when he runs away
  * Skip "Caught By Gerudo" cutscene
  * Shorten cutscene when getting Bullet Bag from the Deku Scrub in Lost Woods
  * Fast pushing and pulling
    * All types of blocks
    * Spinnable mirrors in Spirit Temple
    * Truth spinner in Shadow Temple
    * Puzzle in basement of Forest Temple
  * Ocarina minigame shortened to the first round
    * 5 notes instead of 8
  * Jabu-Jabu's Belly elevator spawns in a more convenient position
  * Kakariko carpenter position is offset so he is no longer in your way during the cucco route.
  * Warp songs now have a normal transition with no cutscene.
  * Pause screen starts on Inventory Screen instead of Map Screen
* Gold Skulltula textbox displays current number obtained
* Poe salesman tells point limit without needing to sell
* Patch files added so that generated seeds can be distributed legally

#### New Options

* Master Quest dungeon slider
  * Selects a number of Master Quest dungeons to appear in the game
    * Ex: 0 - All dungeons will have their default designs.
    * Ex: 6 - Half of all dungeons will have Master Quest redesigns.
    * Ex: 12 - All dungeons will have Master Quest redesigns.
* Damage multiplier
  * Changes the amount of damage taken
  * OHKO: Link dies in one hit
* Item pool
  * Replaces difficulty
  * Changes the number of bonus items that are available in the game
    * Plentiful: Extra major items are added
    * Balanced: The original item pool
    * Scarce: Some excess items are removed, including health upgrades
    * Minimal: Most excess items are removed
* Start with max rupees
  * The player begins the game with 99 rupees.
* Start with Deku equipment
  * The player begins the game with 10 Deku sticks and 20 Deku nuts.
  * If playing without shopsanity, the player begins with a Deku shield equipped.
* Start with fast travel
  * The player begins the game with the Prelude of Light and Serenade of Water songs learned and the Farore's Wind spell in the inventory.
  * These three items increase Link's mobility around the map, but don't actually unlock any new items or areas.
* Start with Tycoon wallet
* Open Zora's Fountain
  * King Zora is moved to the side from the start of the game.
  * Ruto's Letter is removed from the item pool and replaced with an Empty Bottle.
* Randomize starting time of day
* Ice traps setting
    * Off: All ice traps are removed
    * Normal: Only ice traps from base pool are placed
    * Extra ice traps: Chance to add extra ice traps when junk items are added to the item pool
    * Ice trap mayhem: All junk items added will be ice traps
    * Ice trap onslaught: All junk items will be ice traps, including ones in the base pool
* New Cosmetics
  * Added options for Sword Trail colors
    * Can set the length of the trails
    * Can set the inner and outer colors
    * Can set color to "Rainbow"
  * Additional SFX options

#### Updated Features

* Hints distribution
    * Changes how many useful hints are available in the game
    * Useless: Has nothing but junk hints
    * Balanced: Gives you a mix of useless and useful hints. Hints will not be repeated
    * Strong: Has some duplicate hints and no junk hints
    * Very Strong: Has only very useful hints
    * Tournament: Similar to strong but has no variation in hint types
* Frogs Ocarina Game added to always hints
* Hints are only in logic once you are able to reach the location of the gossip stone by logic.
    * Hints ignore logic if inaccessible
* Foolish choice hint added
  * Regions that are a foolish choice will not have any required items no matter what route is taken in logic.
* Big Poes location does not require a hint if the count set to 3 or less.
* Add medallion icons to the Temple of Time altar hint
* Add a hint for 0/6 trials if trial count is random
* Scrub Shuffle now updates the Business Scrubs' textboxes with the updated price for buying their item.

#### Updated Options

* Chest size matches contents updated
  * Boss keys appear in gold chests
  * Small keys appear in small gold chests
* Free Scarecrow's Song changes
  * Pulling out ocarina near a spot where Pierre can spawn will do so.
* Rainbow Bridge changes
  * Spiritual Stones added as bridge requirement
  * 100 Gold Skulltula tokens added as bridge requirement
* Any location can now be excluded from being required.
* Various advanced tricks has been split into individual tricks to be selected.
* Choose sound effects ocarina uses when played

#### Bug Fixes

* Deku and Hylian shields from chests no longer become Blue Rupees.
* Force game language to be English even if a Japanese rom is supplied
* Door of Time now opens when entering Temple of Time from all spawns.
* Fix empty bomb glitch
* Move item cost to after Player in the spoiler log
* Add Wasteland Bombchu Salesman to spoiler log when required for first Bombchus
* Fix message text table is too long error when using settings that add a lot of text to the ROM
* Kokiri Sword no longer required for fishing as child
* Fix Biggoron Sword collection delay
* Twinrova phase 2 textbox fix
* Switches in Forest and Fire Temple lowered by 1 unit to make it easier to press them
* Equipment menu will now show the name of the item you have in the first column
* Hover Boots will no longer show up as adult in the first equipment menu slot if a Fairy Slingshot was not gotten before becoming adult.
* Ammo items now use the correct item fanfare.
* Fix chest size matches contents to work for all chests
* Removed key for key logic
* Removed unused locked door in Water Temple
* Scarecrow's Song should no longer cause softlocks when played in laggy areas.
* Text error messages no longer display the Pocket Egg text.
* Ice traps added back to OHKO as the softlock appears fixed
* Ganon now says "my castle" instead of "Ganon's Castle" for light arrow hint.
* Fix various typos in text
  * Gerudo's Fortress
  * Zora's River
  * Red Rupee
  * Textbox about Dampé's grave
* "Ganon's Tower" is now just "Ganon's Castle".
* Dampé's Gravedigging Tour reward correctly flags collection on pickup.
* Castle Moat Bridge no longer closes when playing the Zelda Escape cutscene.
* Various logic fixes

#### Multiworld Changes

* Maximum player count increased from 31 to 255
* Ice traps can now be sent to other worlds.
* Ganon now tells you the location of your Light Arrows, not the location of some Light Arrows that may exist in your world.
* Item placement rebalanced so that an item for another player can only be placed on a location that both players can reach in logic

#### Development Version Changes

* Output patch file
  * Creates a binary patch file instead of a ROM which allows sharing a seed without sharing copyright protected material
* Patch ROM from file
  * Applies a generated patch file to the base ROM and creates a randomizer ROM which allows sharing a seed without sharing copyright protected material
* Settings presets
  * Adds a functionality to save settings strings for future use
  * Several presets are already provided.
* Create settings log if spoiler log is disabled
* File names no longer include a settings string.
  * Instead display a shortened SHA-1 hash of the settings string
* Add option for converting settings to a string and back
  * Only convert the specified settings to a settings string
  * If a settings string is specified output the used settings instead
* Python 3.5 is no longer supported.
  * You must have Python 3.6 or higher installed to run the randomizer code.
* Add option to only apply cosmetic patch without generating world data
* CLI uses a specified settings file instead of taking in each option.
  * Uses settings.sav as default if it exists
  * Uses default settings if no settings file is provided and no settings.sav exists
* Version check is no longer a dialog
  * Appears in a frame in the main randomizer window
* Copy settings string button
* The cosmetic versioning has been added to the ROM. Some cosmetics are only applied if they are safe to do so.
* Added ability to set the output file name and added file creation logs
* Major refactor of code
