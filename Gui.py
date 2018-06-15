#!/usr/bin/env python3
from argparse import Namespace
from glob import glob
import json
import random
import os
import shutil
from tkinter import Checkbutton, OptionMenu, Toplevel, LabelFrame, PhotoImage, Tk, LEFT, RIGHT, BOTTOM, TOP, StringVar, IntVar, Frame, Label, W, E, X, Entry, Spinbox, Button, filedialog, messagebox, ttk
from urllib.parse import urlparse
from urllib.request import urlopen

from GuiUtils import ToolTips, set_icon, BackgroundTaskProgress
from Main import main, __version__ as ESVersion
from Utils import is_bundled, local_path, output_path, open_file


def guiMain(args=None):
    mainWindow = Tk()
    mainWindow.wm_title("OoT Randomizer %s" % ESVersion)

    set_icon(mainWindow)

    notebook = ttk.Notebook(mainWindow)
    randomizerWindow = ttk.Frame(notebook)
    adjustWindow = ttk.Frame(notebook)
    customWindow = ttk.Frame(notebook)
    notebook.add(randomizerWindow, text='Randomize')
    notebook.pack()

    # Shared Controls

    farBottomFrame = Frame(mainWindow)

    def open_output():
        open_file(output_path(''))

    openOutputButton = Button(farBottomFrame, text='Open Output Directory', command=open_output)

    if os.path.exists(local_path('README.html')):
        def open_readme():
            open_file(local_path('README.html'))
        openReadmeButton = Button(farBottomFrame, text='Open Documentation', command=open_readme)
        openReadmeButton.pack(side=LEFT)

    farBottomFrame.pack(side=BOTTOM, fill=X, padx=5, pady=5)

    # randomizer controls

    topFrame = Frame(randomizerWindow)
    rightHalfFrame = Frame(topFrame)
    checkBoxFrame = Frame(rightHalfFrame)

    # refactoring repeated code for checkboxes...
    checkboxInfo = {
        "create_spoiler":    { "text": "Create Spoiler Log",               "default": "checked"   },
        "suppress_rom":      { "text": "Do not create patched Rom",        "default": "unchecked" },
        "compress_rom":      { "text": "Compress patched Rom",             "default": "checked"   },
        "open_forest":       { "text": "Open Forest",                      "default": "checked"   },
        "open_door_of_time": { "text": "Open Door of Time",                "default": "checked"   },
        "nodungeonitems":    { "text": "Removed Maps and Compasses",       "default": "checked"   },
        "beatableonly":      { "text": "Only ensure seed is beatable",     "default": "checked"   },
        "hints":             { "text": "Gossip Stones have useful hints",  "default": "checked"   },
        "always_hints":      { "text": "Gossip Stones can always be read", "default": "checked"   },
        "custom_logic":      { "text": "Use this fork's custom logic",     "default": "checked"   },
    }

    # create the checkboxes
    checkboxes = {} # this isn't used later currently, but I'm holding on to the pointers in case it matters later on
    checkboxVars = {}
    for var_name, info in checkboxInfo.items():
        # determine the initial value of the checkbox
        default_value = 1 if info["default"] == "checked" else 0
        # create a variable to access the box's state
        checkboxVars[var_name] = IntVar(value=default_value)
        # create the checkbox
        checkboxes[var_name] = Checkbutton(checkBoxFrame, text=info["text"], variable=checkboxVars[var_name])
        checkboxes[var_name].pack(expand=True, anchor=W)

    # createSpoilerVar = IntVar()
    # createSpoilerCheckbutton = Checkbutton(checkBoxFrame, text="Create Spoiler Log", variable=createSpoilerVar)
    # suppressRomVar = IntVar()
    # suppressRomCheckbutton = Checkbutton(checkBoxFrame, text="Do not create patched Rom", variable=suppressRomVar)
    # compressRomVar = IntVar()
    # compressRomCheckbutton = Checkbutton(checkBoxFrame, text="Compress patched Rom", variable=compressRomVar)
    # openForestVar = IntVar()
    # openForestCheckbutton = Checkbutton(checkBoxFrame, text="Open Forest", variable=openForestVar)
    # openDoorVar = IntVar()
    # openDoorCheckbutton = Checkbutton(checkBoxFrame, text="Open Door of Time", variable=openDoorVar)
    # dungeonItemsVar = IntVar()
    # dungeonItemsCheckbutton = Checkbutton(checkBoxFrame, text="Place Dungeon Items (Compasses/Maps)", onvalue=0, offvalue=1, variable=dungeonItemsVar)
    # beatableOnlyVar = IntVar()
    # beatableOnlyCheckbutton = Checkbutton(checkBoxFrame, text="Only ensure seed is beatable, not all items must be reachable", variable=beatableOnlyVar)
    # hintsVar = IntVar()
    # hintsCheckbutton = Checkbutton(checkBoxFrame, text="Gossip Stone Hints with Stone of Agony", variable=hintsVar)
    # alwaysHintsVar = IntVar()
    # alwaysHintsCheckbutton = Checkbutton(checkBoxFrame, text="Gossip Stone Always Respond", variable=alwaysHintsVar)
    # useCustomLogic = IntVar(value=1)
    # useCustomLogicCheckbutton = Checkbutton(checkBoxFrame, text="Use Custom Logic", variable=useCustomLogic)

    # createSpoilerCheckbutton.pack(expand=True, anchor=W)
    # suppressRomCheckbutton.pack(expand=True, anchor=W)
    # compressRomCheckbutton.pack(expand=True, anchor=W)
    # openForestCheckbutton.pack(expand=True, anchor=W)
    # openDoorCheckbutton.pack(expand=True, anchor=W)
    # dungeonItemsCheckbutton.pack(expand=True, anchor=W)
    # beatableOnlyCheckbutton.pack(expand=True, anchor=W)
    # hintsCheckbutton.pack(expand=True, anchor=W)
    # alwaysHintsCheckbutton.pack(expand=True, anchor=W)
    # useCustomLogicCheckbutton.pack(expand=True, anchor=W)

    fileDialogFrame = Frame(rightHalfFrame)

    romDialogFrame = Frame(fileDialogFrame)
    baseRomLabel = Label(romDialogFrame, text='Base Rom')
    romVar = StringVar()
    romEntry = Entry(romDialogFrame, textvariable=romVar)

    def RomSelect():
        rom = filedialog.askopenfilename(filetypes=[("Rom Files", (".z64", ".n64")), ("All Files", "*")])
        romVar.set(rom)
    romSelectButton = Button(romDialogFrame, text='Select Rom', command=RomSelect)

    baseRomLabel.pack(side=LEFT)
    romEntry.pack(side=LEFT)
    romSelectButton.pack(side=LEFT)

    romDialogFrame.pack()

    checkBoxFrame.pack()
    fileDialogFrame.pack()

    dropDownFrame = Frame(topFrame)


    bridgeFrame = Frame(dropDownFrame)
    bridgeVar = StringVar()
    bridgeVar.set('medallions')
    bridgeOptionMenu = OptionMenu(bridgeFrame, bridgeVar, 'medallions', 'vanilla', 'dungeons', 'open')
    bridgeOptionMenu.pack(side=RIGHT)
    bridgeLabel = Label(bridgeFrame, text='Rainbow Bridge Requirement')
    bridgeLabel.pack(side=LEFT)

    colorVars = []
    colorVars.append(StringVar())
    colorVars.append(StringVar())
    colorVars.append(StringVar())
    colorVars[0].set('Kokiri Green')
    colorVars[1].set('Goron Red')
    colorVars[2].set('Zora Blue')

    kokiriFrame = Frame(dropDownFrame)
    kokiriOptionMenu = OptionMenu(kokiriFrame, colorVars[0], 'Kokiri Green', 'Goron Red', 'Zora Blue', 'Black', 'White', 'Purple', 'Yellow', 'Orange', 'Pink', 'Gray', 'Brown', 'Gold', 'Silver', 'Beige', 'Teal', 'Royal Blue', 'Sonic Blue', 'Blood Red', 'Blood Orange', 'NES Green', 'Dark Green', 'Only', 'Random', 'True Random')
    kokiriOptionMenu.pack(side=RIGHT)
    kokiriLabel = Label(kokiriFrame, text='Kokiri Tunic Color')
    kokiriLabel.pack(side=LEFT)

    goronFrame = Frame(dropDownFrame)
    goronOptionMenu = OptionMenu(goronFrame, colorVars[1], 'Kokiri Green', 'Goron Red', 'Zora Blue', 'Black', 'White', 'Purple', 'Yellow', 'Orange', 'Pink', 'Gray', 'Brown', 'Gold', 'Silver', 'Beige', 'Teal', 'Royal Blue', 'Sonic Blue', 'Blood Red', 'Blood Orange', 'NES Green', 'Dark Green', 'Only', 'Random', 'True Random')
    goronOptionMenu.pack(side=RIGHT)
    goronLabel = Label(goronFrame, text='Goron Tunic Color')
    goronLabel.pack(side=LEFT)

    zoraFrame = Frame(dropDownFrame)
    zoraOptionMenu = OptionMenu(zoraFrame, colorVars[2], 'Kokiri Green', 'Goron Red', 'Zora Blue', 'Black', 'White', 'Purple', 'Yellow', 'Orange', 'Pink', 'Gray', 'Brown', 'Gold', 'Silver', 'Beige', 'Teal', 'Royal Blue', 'Sonic Blue', 'Blood Red', 'Blood Orange', 'NES Green', 'Dark Green', 'Only', 'Random', 'True Random')
    zoraOptionMenu.pack(side=RIGHT)
    zoraLabel = Label(zoraFrame, text='Zora Tunic Color')
    zoraLabel.pack(side=LEFT)

    lowHealthSFXVar = StringVar()
    lowHealthSFXVar.set('Default')
    
    lowHealthSFXFrame = Frame(dropDownFrame)
    lowHealthSFXOptionMenu = OptionMenu(lowHealthSFXFrame, lowHealthSFXVar, 'Default', 'Softer Beep', 'Rupee', 'Timer', 'Tamborine', 'Recovery Heart', 'Carrot Refill', 'Navi - Hey!', 'Zelda - Gasp', 'Cluck', 'Mweep!', 'Random', 'None')
    lowHealthSFXOptionMenu.pack(side=RIGHT)
    lowHealthSFXLabel = Label(lowHealthSFXFrame, text='Low Health SFX')
    lowHealthSFXLabel.pack(side=LEFT)
    
    bridgeFrame.pack(expand=True, anchor=E)
    kokiriFrame.pack(expand=True, anchor=E)
    goronFrame.pack(expand=True, anchor=E)
    zoraFrame.pack(expand=True, anchor=E)
    lowHealthSFXFrame.pack(expand=True, anchor=E)

    bottomFrame = Frame(randomizerWindow)

    seedLabel = Label(bottomFrame, text='Seed #')
    seedVar = StringVar()
    seedEntry = Entry(bottomFrame, textvariable=seedVar)
    countLabel = Label(bottomFrame, text='Count')
    countVar = StringVar()
    countSpinbox = Spinbox(bottomFrame, from_=1, to=100, textvariable=countVar)

    def generateRom():
        guiargs = Namespace
        guiargs.seed = int(seedVar.get()) if seedVar.get() else None
        guiargs.count = int(countVar.get()) if countVar.get() != '1' else None
        guiargs.bridge = bridgeVar.get()
        guiargs.kokiricolor = colorVars[0].get()
        guiargs.goroncolor = colorVars[1].get()
        guiargs.zoracolor = colorVars[2].get()
        guiargs.healthSFX = lowHealthSFXVar.get()
        guiargs.create_spoiler = bool(checkboxVars["create_spoiler"].get())
        guiargs.suppress_rom = bool(checkboxVars["suppress_rom"].get())
        guiargs.compress_rom = bool(checkboxVars["compress_rom"].get())
        guiargs.open_forest = bool(checkboxVars["open_forest"].get())
        guiargs.open_door_of_time = bool(checkboxVars["open_door_of_time"].get())
        guiargs.nodungeonitems = bool(checkboxVars["nodungeonitems"].get())
        guiargs.beatableonly = bool(checkboxVars["beatableonly"].get())
        guiargs.hints = bool(checkboxVars["hints"].get())
        guiargs.always_hints = bool(checkboxVars["always_hints"].get())
        guiargs.custom_logic = bool(checkboxVars["custom_logic"].get())
        guiargs.rom = romVar.get()
        try:
            if guiargs.count is not None:
                seed = guiargs.seed
                for _ in range(guiargs.count):
                    main(seed=seed, args=guiargs)
                    seed = random.randint(0, 999999999)
            else:
                main(seed=guiargs.seed, args=guiargs)
        except Exception as e:
            messagebox.showerror(title="Error while creating seed", message=str(e))
        else:
            messagebox.showinfo(title="Success", message="Rom patched successfully")

    generateButton = Button(bottomFrame, text='Generate Patched Rom', command=generateRom)

    seedLabel.pack(side=LEFT)
    seedEntry.pack(side=LEFT)
    countLabel.pack(side=LEFT, padx=(5, 0))
    countSpinbox.pack(side=LEFT)
    generateButton.pack(side=LEFT, padx=(5, 0))

    openOutputButton.pack(side=RIGHT)

    dropDownFrame.pack(side=LEFT)
    rightHalfFrame.pack(side=RIGHT)
    topFrame.pack(side=TOP)
    bottomFrame.pack(side=BOTTOM)

    if args is not None:
        # load values from commandline args
        checkboxVars["create_spoiler"].set(int(args.create_spoiler))
        checkboxVars["suppress_rom"].set(int(args.suppress_rom))
        checkboxVars["compress_rom"].set(int(args.compress_rom))
        checkboxVars["open_forest"].set(int(args.open_forest))
        checkboxVars["open_door_of_time"].set(int(args.open_door_of_time))
        checkboxVars["nodungeonitems"].set(int(args.nodungeonitems))
        checkboxVars["beatableonly"].set(int(args.beatableonly))
        checkboxVars["hints"].set(int(args.hints))
        checkboxVars["always_hints"].set(int(args.always_hints))
        checkboxVars["custom_logic"].set(int(args.custom_logic))
        if args.count:
            countVar.set(str(args.count))
        if args.seed:
            seedVar.set(str(args.seed))
        bridgeVar.set(args.bridge)
        colorVars.set([args.kokiricolor, args.goroncolor, args.zoracolor])
        lowHealthSFXVar.set(args.healthSFX)
        romVar.set(args.rom)

    mainWindow.mainloop()

if __name__ == '__main__':
    guiMain()
