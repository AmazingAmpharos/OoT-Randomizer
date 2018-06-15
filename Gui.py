#!/usr/bin/env python3
from argparse import Namespace
from glob import glob
import json
import random
import os
import shutil
from tkinter import Checkbutton, OptionMenu, Toplevel, LabelFrame, Radiobutton, PhotoImage, Tk, LEFT, RIGHT, BOTTOM, TOP, StringVar, IntVar, Frame, Label, W, E, X, N, S, NW, Entry, Spinbox, Button, filedialog, messagebox, ttk
from urllib.parse import urlparse
from urllib.request import urlopen

from GuiUtils import ToolTips, set_icon, BackgroundTaskProgress
from Main import main, __version__ as ESVersion
from Utils import is_bundled, local_path, output_path, open_file
from Rom import get_tunic_color_options

def guiMain(args=None):
    mainWindow = Tk()
    mainWindow.wm_title("OoT Randomizer %s" % ESVersion)

    set_icon(mainWindow)

    notebook = ttk.Notebook(mainWindow)
    randomizerWindow = ttk.Frame(notebook)
    adjustWindow = ttk.Frame(notebook)
    customWindow = ttk.Frame(notebook)
    notebook.add(randomizerWindow, text='Randomize')

    # Shared Controls

    farTopFrame = Frame(mainWindow)

    def open_output():
        open_file(output_path(''))

    openOutputButton = Button(farTopFrame, text='Open Output Directory', command=open_output)

    if os.path.exists(local_path('README.html')):
        def open_readme():
            open_file(local_path('README.html'))
        openReadmeButton = Button(farTopFrame, text='Open Documentation', command=open_readme)
        openReadmeButton.pack(side=LEFT)

    farTopFrame.pack(side=TOP, fill=X, padx=5, pady=2)
    notebook.pack(padx=5, pady=5)

    # adds a LabelFrame containing a list of radio buttons based on the given data
    # returns the label_frame, and a variable associated with it
    def MakeRadioList(parent, data):
        # create a frame to hold the radio buttons
        lable_frame = LabelFrame(parent, text=data["name"], labelanchor=NW)
        # create a variable to hold the result of the user's decision
        radio_var = StringVar(value=data["default"]);
        # add the radio buttons
        for option in data["options"]:
            radio_button = Radiobutton(lable_frame, text=option["description"], value=option["value"], variable=radio_var,
                                       justify=LEFT, wraplength=data["wraplength"])
            radio_button.pack(side=TOP, anchor=W)
        # return the frame so it can be packed, and the var so it can be used
        return (lable_frame, radio_var)

    #######################
    # randomizer controls #
    #######################

    # data
    ########

    # checkboxes information
    checkboxInfo = {
        "create_spoiler":    { "text": "Create Spoiler Log",               "group": "output", "default": "checked"   },
        "suppress_rom":      { "text": "Do not create patched Rom",        "group": "output", "default": "unchecked" },
        "compress_rom":      { "text": "Compress patched Rom",             "group": "output", "default": "checked"   },
        "open_forest":       { "text": "Open Forest",                      "group": "logic",  "default": "checked"   },
        "open_door_of_time": { "text": "Open Door of Time",                "group": "logic",  "default": "checked"   },
        "nodungeonitems":    { "text": "Remove Maps and Compasses",        "group": "logic",  "default": "checked"   },
        "beatableonly":      { "text": "Only ensure seed is beatable",     "group": "logic",  "default": "checked"   },
        "custom_logic":      { "text": "Use this fork's custom logic",     "group": "logic",  "default": "checked"   },
    }
    # radio list has a name, a list of options, and a default option
    bridge_requirements_data = {
        "name": "Rainbow Bridge Requirement",
        "options": [
            { "value": "dungeons",   "description": "All dungeons" },
            { "value": "medallions", "description": "All medallions" },
            { "value": "vanilla",    "description": "Vanilla requirements" },
            { "value": "open",       "description": "Always open" },
        ],
        "default": "medallions",
        "wraplength": 180,
    }
    hint_options_data = {
        "name": "Gossip Stones",
        "options": [
            { "value": "none",   "description": "Default Behavior" },
            { "value": "mask",   "description": "Have useful hints; read with the Mask of Truth" },
            { "value": "agony",  "description": "Have useful hints; read with Stone of Agony" },
            { "value": "always", "description": "Have useful hints; can always be read" },
        ],
        "default": "always",
        "wraplength": 140,
    }
    # dropdown info
    color_options = get_tunic_color_options()
    dropdownInfo = {
        "kokiricolor": { "name": "Kokiri Tunic Color", "default": "Kokiri Green", "options": color_options },
        "goroncolor":  { "name": "Goron Tunic Color",  "default": "Goron Red",    "options": color_options },
        "zoracolor":   { "name": "Zora Tunic Color",   "default": "Zora Blue",    "options": color_options },
        "healthSFX":   { "name": "Low Health SFX",     "default": "Default",      "options": ['Default', 'Softer Beep', 'Rupee', 'Timer', 'Tamborine', 'Recovery Heart', 'Carrot Refill', 'Navi - Hey!', 'Zelda - Gasp', 'Cluck', 'Mweep!', 'Random', 'None'] },
    }

    # hold the results of the user's decisions here
    resultVars = {}

    # hierarchy
    ############

    checkAndRadioFrame = Frame(randomizerWindow)
    if True: # just indenting for hierarchy clarity
        outputOptionsFrame = LabelFrame(checkAndRadioFrame, text='Output', labelanchor=NW)
        logicOptionsFrame = LabelFrame(checkAndRadioFrame, text='Logic', labelanchor=NW)
        (rainbowBridgeFrame, resultVars['bridge']) = MakeRadioList(checkAndRadioFrame, bridge_requirements_data)
        (hintsFrame,         resultVars['hints'])  = MakeRadioList(checkAndRadioFrame, hint_options_data)

    aestheticFrame = LabelFrame(randomizerWindow, text='Aesthetic', labelanchor=NW)

    generateSeedFrame = Frame(randomizerWindow)

    # build gui
    ############

    # create the checkboxes
    checkboxes = {} # this isn't used later currently, but I'm holding on to the pointers in case it matters later on
    for var_name, info in checkboxInfo.items():
        # determine the initial value of the checkbox
        default_value = 1 if info["default"] == "checked" else 0
        # create a variable to access the box's state
        resultVars[var_name] = IntVar(value=default_value)
        # create the checkbox
        parent = { 'output': outputOptionsFrame, 'logic': logicOptionsFrame }[info["group"]] # sorry, this is gross; I was reaching my limit
        checkboxes[var_name] = Checkbutton(parent, text=info["text"], variable=resultVars[var_name])
        checkboxes[var_name].pack(expand=True, anchor=W)

    # create the dropdowns
    dropdownFrames = {}
    for var_name, info in dropdownInfo.items():
        # create the variable to store the user's decision
        resultVars[var_name] = StringVar(value=info['default'])
        # create the option menu
        dropdownFrames[var_name] = Frame(aestheticFrame)
        dropdown = OptionMenu(dropdownFrames[var_name], resultVars[var_name], *(info['options']))
        dropdown.pack(side=BOTTOM, anchor=E)
        # label the option
        label = Label(dropdownFrames[var_name], text=info['name'], width=18)
        label.pack(side=TOP, anchor=NW)
        # pack the frame
        dropdownFrames[var_name].pack(expand=True, side=LEFT, anchor=N)

    # pack the hierarchy
    outputOptionsFrame.pack(expand=True, anchor=N, side=LEFT, padx=5)
    logicOptionsFrame.pack(expand=True, anchor=N, side=LEFT, padx=5)
    rainbowBridgeFrame.pack(expand=True, anchor=N, side=LEFT, padx=5)
    hintsFrame.pack(expand=True, anchor=N, side=LEFT, padx=5)

    checkAndRadioFrame.pack(side=TOP, anchor=N)

    aestheticFrame.pack(anchor=W, padx=5)



    # didn't refactor the rest, sorry

    fileDialogFrame = Frame(generateSeedFrame)

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

    fileDialogFrame.pack(side=LEFT, padx=5)


    seedLabel = Label(generateSeedFrame, text='Seed #')
    seedVar = StringVar()
    seedEntry = Entry(generateSeedFrame, textvariable=seedVar)
    countLabel = Label(generateSeedFrame, text='Count')
    countVar = StringVar()
    countSpinbox = Spinbox(generateSeedFrame, from_=1, to=100, textvariable=countVar)

    def generateRom():
        guiargs = Namespace
        guiargs.seed = int(seedVar.get()) if seedVar.get() else None
        guiargs.count = int(countVar.get()) if countVar.get() != '1' else None
        guiargs.bridge = resultVars["bridge"].get()
        guiargs.kokiricolor = resultVars["kokiricolor"].get()
        guiargs.goroncolor = resultVars["goroncolor"].get()
        guiargs.zoracolor = resultVars["zoracolor"].get()
        guiargs.healthSFX = resultVars["healthSFX"].get()
        guiargs.create_spoiler = bool(resultVars["create_spoiler"].get())
        guiargs.suppress_rom = bool(resultVars["suppress_rom"].get())
        guiargs.compress_rom = bool(resultVars["compress_rom"].get())
        guiargs.open_forest = bool(resultVars["open_forest"].get())
        guiargs.open_door_of_time = bool(resultVars["open_door_of_time"].get())
        guiargs.nodungeonitems = bool(resultVars["nodungeonitems"].get())
        guiargs.beatableonly = bool(resultVars["beatableonly"].get())
        guiargs.custom_logic = bool(resultVars["custom_logic"].get())
        guiargs.hints = resultVars["hints"].get()
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

    generateButton = Button(generateSeedFrame, text='Generate Patched Rom', command=generateRom)

    seedLabel.pack(side=LEFT)
    seedEntry.pack(side=LEFT)
    countLabel.pack(side=LEFT, padx=(5, 0))
    countSpinbox.pack(side=LEFT)
    generateButton.pack(side=LEFT, padx=(5, 0))

    openOutputButton.pack(side=RIGHT)

    generateSeedFrame.pack(side=BOTTOM, anchor=S, padx=5, pady=10)

    if args is not None:
        # load values from commandline args
        resultVars["create_spoiler"].set(int(args.create_spoiler))
        resultVars["suppress_rom"].set(int(args.suppress_rom))
        resultVars["compress_rom"].set(int(args.compress_rom))
        resultVars["open_forest"].set(int(args.open_forest))
        resultVars["open_door_of_time"].set(int(args.open_door_of_time))
        resultVars["nodungeonitems"].set(int(args.nodungeonitems))
        resultVars["beatableonly"].set(int(args.beatableonly))
        resultVars["custom_logic"].set(int(args.custom_logic))
        resultVars["hints"].set(args.hints)
        if args.count:
            countVar.set(str(args.count))
        if args.seed:
            seedVar.set(str(args.seed))
        resultVars["bridge"].set(args.bridge)
        resultVars["kokiricolor"].set(args.kokiricolor)
        resultVars["goroncolor"].set(args.goroncolor)
        resultVars["zoracolor"].set(args.zoracolor)
        resultVars["healthSFX"].set(args.healthSFX)
        romVar.set(args.rom)

    mainWindow.mainloop()

if __name__ == '__main__':
    guiMain()
