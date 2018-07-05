#!/usr/bin/env python3
from argparse import Namespace
from glob import glob
import json
import random
import os
import shutil
from tkinter import Scale, Checkbutton, OptionMenu, Toplevel, LabelFrame, Radiobutton, PhotoImage, Tk, BOTH, LEFT, RIGHT, BOTTOM, TOP, StringVar, IntVar, Frame, Label, W, E, X, N, S, NW, Entry, Spinbox, Button, filedialog, messagebox, ttk, HORIZONTAL
from urllib.parse import urlparse
from urllib.request import urlopen

from GuiUtils import ToolTips, set_icon, BackgroundTaskProgress
from Main import main
from Utils import is_bundled, local_path, output_path, open_file
from Rom import get_tunic_color_options, get_navi_color_options
from Settings import Settings, setting_infos, __version__ as ESVersion


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
                if info.gui_params and 'options' in info.gui_params:
                    for gui_text,gui_value in info.gui_params['options'].items(): 
                        if gui_value == value:
                            guivar.set( gui_text )
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
            result[name] = None
            continue
        guivar = guivars[name]
        # checkbox
        if info.type == bool:
            result[name] = bool(guivar.get())
        # dropdown/radiobox
        if info.type == str:
            if info.gui_params and 'options' in info.gui_params:
                result[name] = info.gui_params['options'][guivar.get()]
            else:
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
    frames = {}

    mainWindow = Tk()
    mainWindow.wm_title("OoT Randomizer %s" % ESVersion)

    set_icon(mainWindow)

    notebook = ttk.Notebook(mainWindow)
    frames['rom_tab'] = ttk.Frame(notebook)
    frames['rules_tab'] = ttk.Frame(notebook)
    frames['logic_tab'] = ttk.Frame(notebook)
    frames['other_tab'] = ttk.Frame(notebook)
    frames['aesthetic_tab'] = ttk.Frame(notebook)
    adjustWindow = ttk.Frame(notebook)
    customWindow = ttk.Frame(notebook)
    notebook.add(frames['rom_tab'], text='ROM Options')
    notebook.add(frames['rules_tab'], text='Main Rules')
    notebook.add(frames['logic_tab'], text='Detailed Logic')
    notebook.add(frames['other_tab'], text='Other')
    notebook.add(frames['aesthetic_tab'], text='Aesthetics')

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
        # setup orientation
        side = TOP
        anchor = W
        if "horizontal" in data and data["horizontal"]:
            side = LEFT
            anchor = N
        # add the radio buttons
        for option in data["options"]:
            radio_button = Radiobutton(lable_frame, text=option["description"], value=option["value"], variable=radio_var,
                                       justify=LEFT, wraplength=data["wraplength"])
            radio_button.pack(expand=True, side=side, anchor=anchor)
        # return the frame so it can be packed, and the var so it can be used
        return (lable_frame, radio_var)

    #######################
    # randomizer controls #
    #######################

    # hold the results of the user's decisions here
    guivars = {}

    # hierarchy
    ############

    #Rules Tab
    frames['open']   = LabelFrame(frames['rules_tab'], text='Open',   labelanchor=NW)
    frames['logic']  = LabelFrame(frames['rules_tab'], text='Logic',  labelanchor=NW)

    # Logic tab
    frames['rewards'] = LabelFrame(frames['logic_tab'], text='Remove Specific Locations', labelanchor=NW)
    frames['tricks']  = LabelFrame(frames['logic_tab'], text='Specific expected tricks', labelanchor=NW)

    #Other Tab
    frames['convenience'] = LabelFrame(frames['other_tab'], text='Speed Ups', labelanchor=NW)
    frames['other']       = LabelFrame(frames['other_tab'], text='Misc',      labelanchor=NW)

    #Aesthetics tab
    frames['tuniccolor'] = LabelFrame(frames['aesthetic_tab'], text='Tunic Color', labelanchor=NW)
    frames['navicolor']       = LabelFrame(frames['aesthetic_tab'], text='Navi Color',  labelanchor=NW)
    frames['lowhp']      = LabelFrame(frames['aesthetic_tab'], text='Low HP SFX',  labelanchor=NW)


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


    # pack the hierarchy

    frames['open'].pack(  fill=BOTH, expand=True, anchor=N, side=LEFT, pady=(5,1) )
    frames['logic'].pack( fill=BOTH, expand=True, anchor=N, side=LEFT, pady=(5,1) )

    # Logic tab
    frames['rewards'].pack(fill=BOTH, expand=True, anchor=N, side=LEFT, pady=(5,1) )
    frames['tricks'].pack( fill=BOTH, expand=True, anchor=N, side=LEFT, pady=(5,1) )

    #Other Tab
    frames['convenience'].pack(fill=BOTH, expand=True, anchor=N, side=LEFT, pady=(5,1) )
    frames['other'].pack(      fill=BOTH, expand=True, anchor=N, side=LEFT, pady=(5,1) )

    #Aesthetics tab
    frames['navicolor'].pack( fill=BOTH, expand=True, anchor=N, side=RIGHT, pady=(5,1) )
    frames['tuniccolor'].pack(fill=BOTH, expand=True, anchor=W, side=TOP, pady=(5,1) )
    frames['lowhp'].pack(     fill=BOTH, expand=True, anchor=W, side=BOTTOM, pady=(5,1) )

    
    notebook.pack(fill=BOTH, expand=True, padx=5, pady=5)


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
    else:
        # try to load saved settings
        try:
            with open('settings.sav') as f:
                settings = Settings( json.load(f) )
                settings.update_seed("")
                settings_to_guivars(settings, guivars)
        except:
            pass

    mainWindow.mainloop()

    # save settings on close
    with open('settings.sav', 'w') as outfile:
        settings = guivars_to_settings(guivars)
        json.dump(settings.__dict__, outfile)

if __name__ == '__main__':
    guiMain()
