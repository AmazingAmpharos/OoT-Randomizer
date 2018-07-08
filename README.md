# OoTRandomizer

Documentation for the core features of the randomizer from which this was forked can be found here: <https://github.com/AmazingAmpharos/OoT-Randomizer/blob/master/README.md>

# Notable Changes on this fork

The following were added or majorly changed on this fork:

## GUI changes

- Seeds can be text instead of just numbers
- Can get, share, and import a settings string to quickly set seed-changing options
- Options are saved when closing the GUI and loaded when opening it
- Can set Output directory

## Optional Logic changes

A bunch of optional logic changes can be applied from the "Detailed Logic" tab:

- Number of maximum expected gold skulltula tokens can be set
- Some particularly annoying locations can be removed from logic. This only makes it so that getting the item at the location is never required, it does not mean the location's vanilla item is not shuffled into the pool. For example, checking "No Biggoron Reward" just means that you cannot be expected to complete the adult trade sequence, it does not mean that the Biggoron Sword cannot be found somewhere in the world.
- A handful of easy tricks (that require some knowledge) can be marked to be usable
- Lens of Truth requirements and expectations can be set

## Fast Ganon broken into components

What was once called `fast_ganon` is now broken into 3 separate options:

- `trials`: specify the number of trials you need to do to dispel the barrier on Ganon's Tower (0-6). The trials you need to complete will be selected randomly.
- `unlocked_ganondorf`: the boss key door in Ganon's Tower will be unlocked from the start.
- `no_escape_sequence`: the tower collapse escape sequence between the Ganondorf and Ganon fights will be skipped .

## Gerudo Fortress options

Options for speeding up carpenter rescue portion of Gerudo Fortress

- fast: Only the carpenter nearest to the prison Link is tossed into needs to be freed to obtain the Gerudo Card and get all of its benefits; the other three carpenters are freed from the start
- open: All carpenters are freed from the start, and you start with the Gerudo Card and all of its benefits (and thus the bridge across the valley is always built)

## Other Conveniences

Options to skip some sequences that only pad the time of completing the game without ever really changing between seeds have been added:

- `no_guard_stealth`: the stealth sequence between the crawlspace into Hyrule Castle and Zelda's courtyard will be skipped.
- `no_epona_race`: you can summon Epona with her song without racing Ingo.
- `only_one_big_poe`: the poe buyer will give the reward after selling 1 Big Poe instead of 10.
- `default_targeting`: set the default targeting mode to be either `switch` or `hold`.

## Bombchus

Bombchus are now considered in logic. That is, once you've found bombchus, you can be expected to use them as explosives, hit switches, etc. to make progress in the seed. In order to have this make sense, the following changes were made:

- The back alley bombchu shop will now stock bombchus once you have bombchus in your inventory (even if you have 0). All options in this shop no longer sell out, and the right shelf's bottom-left pack is a sale of 5 bombchus for 60 rupees. Thus, once you have found bombchus, you can always buy more.
- Bomchu Bowling is now playable only once you have bombchus in your inventory. This gives bombchus some unique power beyond the spirit trial, and also keeps them better self-contained (since you win bombchus from this mini-game).

As a note, if you have access to the Wasteland carpet salesman and have a wallet upgrade, you can buy bombchus from him to get your first pack.

## Malon Egg

The Weird Egg is shuffled into the pool. This means that Malon will give a random item and that you must find the Weird Egg (and hatch it) before being able to visit Zelda.

Regardless of whether of not you use this option, Malon has been sped up in the following ways:
- Malon will never appear in the Castle Market, instead she will be waiting by the vines from the start of the game
- You do not need to talk to Malon twice to get her item. She will give it by talking only once
- The condition for Malon to move to Lon Lon Ranch is now obtaining her item and Talon fleeing the castle (instead of just Talon fleeing the castle)
- At Lon Lon Ranch, you no longer need to speak to Malon multiple times before she will teach you her song. You can simply walk up to her and pull out your Ocarina.

## Keysanity

Dungeon items (maps, compasses, small keys, boss keys) are shuffled into the item pool at large.

This was actually mostly implemented, I just pulled the trigger...

## Changed hint system

The hint system has been changed to include different kinds of hints (such as saying a location has something good, but not saying what item it is, or saying a specific item is somewhere in a dungeon, instead of giving the specific location, and so on.) An option has been added to allow talking to gossip stones from the start. Yes, this makes the Stone of Agony completely useless.

## Text shuffle

You can shuffle most of the text in the game. This is hilarious, but can get really confusing when buying from shops and such, so make sure you really know what people are actually asking for.

## Ocarina song randomization

You can randomize the note pattern that is required to activate each song. The new songs will be properly taught to you when you learn them, and can always be checked on the quest status screen like normal.

## Navi color options

Similar to the tunic color options, you can change Navi's color for each of her different kinds of targets.

## Chest size matches contents

`correct_chest_sizes`: Major items will appear in a large chest and other items in small chests. There are a few places that cannot be correctly updated:
- Chests in Generic Grottos
- Chests summoned by Zelda's Lullaby
- Chests summoned by Sun's Song Triggered
- Chests summoned by a switch that do not fall