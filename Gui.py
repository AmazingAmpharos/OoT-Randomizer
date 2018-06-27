#!/usr/bin/env python3
from argparse import Namespace
from glob import glob
import json
import random
import os
import shutil
from tkinter import Checkbutton, OptionMenu, Toplevel, LabelFrame, Radiobutton, PhotoImage, Tk, BOTH, LEFT, RIGHT, BOTTOM, TOP, StringVar, IntVar, Frame, Label, W, E, X, N, S, NW, Entry, Spinbox, Button, filedialog, messagebox, ttk
from urllib.parse import urlparse
from urllib.request import urlopen

from GuiUtils import ToolTips, set_icon, BackgroundTaskProgress
from Main import main, __version__ as ESVersion
from Utils import is_bundled, local_path, output_path, open_file
from Rom import get_tunic_color_options, get_navi_color_options
from Settings import Settings, setting_infos


def settings_to_guivars(settings, guivars):
    for info in setting_infos:
        name = info.name
        if name not in guivars:
            continue
        guivar = guivars[name]
        value = settings.__dict__[name]
        # checkbox
        if info.type == bool:
            guivar.set( int(value) )
        # dropdown/radiobox
        if info.type == str:
            if value is None:
                guivar.set( "" )
            else:
                guivar.set( value )
        # text field for a number...
        if info.type == int:
            if value is None:
                guivar.set( str(1) )
            else:
                guivar.set( str(value) )

def guivars_to_settings(guivars):
    result = {}
    for info in setting_infos:
        name = info.name
        if name not in guivars:
            result[name] = none
            continue
        guivar = guivars[name]
        # checkbox
        if info.type == bool:
            result[name] = bool(guivar.get())
        # dropdown/radiobox
        if info.type == str:
            result[name] = guivar.get()
        # text field for a number...
        if info.type == int:
            result[name] = int( guivar.get() )
    if result['seed'] == "":
        result['seed'] = None
    if result['count'] == 1:
        result['count'] = None

    return Settings(result)

def guiMain(settings=None):
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
        "fast_ganon":        { "text": "Skip most of Ganon's Castle",      "group": "logic",  "default": "checked"   },
        "nodungeonitems":    { "text": "Remove Maps and Compasses",        "group": "logic",  "default": "checked"   },
        "beatableonly":      { "text": "Only ensure seed is beatable",     "group": "logic",  "default": "checked"   },
        "custom_logic":      { "text": "Use this fork's custom logic",     "group": "logic",  "default": "checked"   },
        "ocarina_songs":     { "text": "Randomize ocarina song notes",     "group": "other",  "default": "unchecked" },
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
    gerudo_fortress_data = {
        "name": "Gerudo Fortress",
        "options": [
            { "value": "normal", "description": "Default Behavior" },
            { "value": "fast",   "description": "Only rescue one carpenter" },
            { "value": "open",   "description": "Start with Gerudo Card" },
        ],
        "default": "fast",
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
    text_shuffle_data = {
        "name": "Text Shuffle",
        "options": [
            { "value": "none",         "description": "No text shuffle" },
            { "value": "except_hints", "description": "Text is shuffled (except hints)" },
            { "value": "complete",     "description": "Text is shuffled (completely)" },
        ],
        "default": "none",
        "wraplength": 240,
    }
    # dropdown info
    color_options = get_tunic_color_options()
    navi_options = get_navi_color_options()
    dropdownInfo = {
        "kokiricolor":   { "name": "Kokiri Tunic Color", "default": "Kokiri Green", "options": color_options, "row": "top" },
        "goroncolor":    { "name": "Goron Tunic Color",  "default": "Goron Red",    "options": color_options, "row": "top" },
        "zoracolor":     { "name": "Zora Tunic Color",   "default": "Zora Blue",    "options": color_options, "row": "top" },
        "healthSFX":     { "name": "Low Health SFX",     "default": "Default",      "options": ['Default', 'Softer Beep', 'Rupee', 'Timer', 'Tamborine', 'Recovery Heart', 'Carrot Refill', 'Navi - Hey!', 'Zelda - Gasp', 'Cluck', 'Mweep!', 'Random', 'None'], "row": "right" },
        "navicolordefault":   { "name": "Navi Idle",            "default": "White",      "options": navi_options, "row": "bottom" },
        "navicolorenemy":     { "name": "Navi Targeting Enemy", "default": "Yellow",     "options": navi_options, "row": "bottom" },
        "navicolornpc":       { "name": "Navi Targeting NPC",   "default": "Light Blue", "options": navi_options, "row": "bottom" },
        "navicolorprop":      { "name": "Navi Targeting Prop",  "default": "Green",      "options": navi_options, "row": "bottom" },
    }

    # hold the results of the user's decisions here
    guivars = {}

    # hierarchy
    ############

    checkAndRadioFrame = Frame(randomizerWindow)
    if True: # just indenting for hierarchy clarity
        leftSideChecks = Frame(checkAndRadioFrame)
        if True: # just indenting for hierarchy clarity
            outputOptionsFrame = LabelFrame(leftSideChecks, text='Output', labelanchor=NW)
            (textShuffleFrame, guivars['text_shuffle']) = MakeRadioList(leftSideChecks, text_shuffle_data)
        leftMiddleChecks = Frame(checkAndRadioFrame)
        if True: # just indenting for hierarchy clarity
            (rainbowBridgeFrame, guivars['bridge']) = MakeRadioList(leftMiddleChecks, bridge_requirements_data)
            (gerudoFrame, guivars['gerudo_fortress'])  = MakeRadioList(leftMiddleChecks, gerudo_fortress_data)
        logicOptionsFrame = LabelFrame(checkAndRadioFrame, text='Logic', labelanchor=NW)
        rightSideChecks = Frame(checkAndRadioFrame)
        if True: # just indenting for hierarchy clarity
            (hintsFrame, guivars['hints'])  = MakeRadioList(rightSideChecks, hint_options_data)
            otherOptionsFrame = LabelFrame(rightSideChecks, text='Other', labelanchor=NW)

    aestheticFrame = LabelFrame(randomizerWindow, text='Aesthetic', labelanchor=NW)
    if True: # just indenting for hierarchy clarity
        aestheticLeftFrame = Frame(aestheticFrame)
        if True: # just indenting for hierarchy clarity
            aestheticTopFrame = Frame(aestheticLeftFrame)
            aestheticBottomFrame = Frame(aestheticLeftFrame)
        aestheticRightFrame = Frame(aestheticFrame)

    settingsFrame = Frame(randomizerWindow)

    generateSeedFrame = Frame(randomizerWindow)

    # build gui
    ############

    # create the checkboxes
    checkboxes = {} # this isn't used later currently, but I'm holding on to the pointers in case it matters later on
    for var_name, info in checkboxInfo.items():
        # determine the initial value of the checkbox
        default_value = 1 if info["default"] == "checked" else 0
        # create a variable to access the box's state
        guivars[var_name] = IntVar(value=default_value)
        # create the checkbox
        parent = { 'output': outputOptionsFrame, 'logic': logicOptionsFrame, 'other': otherOptionsFrame}[info["group"]] # sorry, this is gross; I was reaching my limit
        checkboxes[var_name] = Checkbutton(parent, text=info["text"], variable=guivars[var_name])
        checkboxes[var_name].pack(expand=True, anchor=W)

    # create the dropdowns
    dropdownFrames = {}
    for var_name, info in dropdownInfo.items():
        # create the variable to store the user's decision
        guivars[var_name] = StringVar(value=info['default'])
        # create the option menu
        parent = { 'top': aestheticTopFrame, 'bottom': aestheticBottomFrame, 'right': aestheticRightFrame}[info["row"]]
        dropdownFrames[var_name] = Frame(parent)
        # dropdown = OptionMenu(dropdownFrames[var_name], guivars[var_name], *(info['options']))
        dropdown = ttk.Combobox(dropdownFrames[var_name], textvariable=guivars[var_name], values=info['options'], state='readonly')
        dropdown.pack(side=BOTTOM, anchor=W)
        # label the option
        label = Label(dropdownFrames[var_name], text=info['name'])
        label.pack(side=TOP, anchor=W)
        # pack the frame
        dropdownFrames[var_name].pack(expand=True, side=LEFT, anchor=N, padx=3, pady=3)

    # pack the hierarchy
    outputOptionsFrame.pack(fill=BOTH, expand=True, anchor=E, side=TOP, pady=5)
    textShuffleFrame.pack(fill=BOTH, expand=True, anchor=E, side=BOTTOM, pady=5)
    leftSideChecks.pack(fill=BOTH, expand=True, anchor=N, side=LEFT, padx=5)

    rainbowBridgeFrame.pack(fill=BOTH, expand=True, anchor=E, side=TOP, pady=5)
    gerudoFrame.pack(fill=BOTH, expand=True, anchor=E, side=BOTTOM, pady=5)
    leftMiddleChecks.pack(fill=BOTH, expand=True, anchor=N, side=LEFT, padx=5)

    logicOptionsFrame.pack(fill=BOTH, expand=True, anchor=N, side=LEFT, padx=5, pady=5)

    hintsFrame.pack(fill=BOTH, expand=True, anchor=E, side=TOP, pady=5)
    otherOptionsFrame.pack(fill=BOTH, expand=True, anchor=E, side=BOTTOM, pady=5)
    rightSideChecks.pack(fill=BOTH, expand=True, anchor=N, side=LEFT, padx=5)

    checkAndRadioFrame.pack(side=TOP, anchor=N)

    aestheticTopFrame.pack(expand=True, anchor=W, side=TOP)
    aestheticBottomFrame.pack(fill=BOTH, expand=True, anchor=W, side=BOTTOM, pady=5)
    aestheticRightFrame.pack(fill=BOTH, expand=True, anchor=N, side=RIGHT)
    aestheticLeftFrame.pack(fill=BOTH, expand=True, anchor=N, side=LEFT)
    aestheticFrame.pack(fill=BOTH, anchor=W, padx=5)



    # didn't refactor the rest, sorry

    settings_string_var = StringVar()
    settingsEntry = Entry(settingsFrame, textvariable=settings_string_var)

    def show_settings():
        settings = guivars_to_settings(guivars)
        settings_string_var.set( settings.get_settings_string() )

    def import_settings():
        try:
            settings = guivars_to_settings(guivars)
            text = settings_string_var.get().upper()
            settings.seed = guivars['seed'].get()
            settings.update_with_settings_string(text)
            settings_to_guivars(settings, guivars)
        except Exception as e:
            messagebox.showerror(title="Error", message="Invalid settings string")

    showSettingsButton = Button(settingsFrame, text='Show Settings String', command=show_settings)
    importSettingsButton = Button(settingsFrame, text='Import Settings String', command=import_settings)

    showSettingsButton.pack(side=LEFT, padx=(6,10))
    settingsEntry.pack(side=LEFT)
    importSettingsButton.pack(side=LEFT, padx=10)

    settingsFrame.pack(fill=BOTH, anchor=W, padx=5, pady=(10,0))


    fileDialogFrame = Frame(generateSeedFrame)

    romDialogFrame = Frame(fileDialogFrame)
    baseRomLabel = Label(romDialogFrame, text='Base Rom')
    guivars['rom'] = StringVar(value='ZOOTDEC.z64')
    romEntry = Entry(romDialogFrame, textvariable=guivars['rom'])

    def RomSelect():
        rom = filedialog.askopenfilename(filetypes=[("Rom Files", (".z64", ".n64")), ("All Files", "*")])
        guivars['rom'].set(rom)
    romSelectButton = Button(romDialogFrame, text='Select Rom', command=RomSelect)

    baseRomLabel.pack(side=LEFT)
    romEntry.pack(side=LEFT)
    romSelectButton.pack(side=LEFT)

    romDialogFrame.pack()

    fileDialogFrame.pack(side=LEFT, padx=5)


    seedLabel = Label(generateSeedFrame, text='Seed #')
    guivars['seed'] = StringVar()
    seedEntry = Entry(generateSeedFrame, textvariable=guivars['seed'])
    countLabel = Label(generateSeedFrame, text='Count')
    guivars['count'] = StringVar()
    countSpinbox = Spinbox(generateSeedFrame, from_=1, to=100, textvariable=guivars['count'])


    def generateRom():
        settings = guivars_to_settings(guivars)

        try:
            if settings.count is not None:
                orig_seed = settings.seed
                for i in range(settings.count):
                    settings.update_seed(orig_seed + '-' + str(i))
                    main(settings)
            else:
                main(settings)
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

    generateSeedFrame.pack(side=BOTTOM, anchor=W, padx=5, pady=10)

    if settings is not None:
        # load values from commandline args
        settings_to_guivars(settings, guivars)

    mainWindow.mainloop()

if __name__ == '__main__':
    guiMain()
