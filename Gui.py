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
from Utils import is_bundled, local_path, default_output_path, open_file
from Rom import get_tunic_color_options, get_navi_color_options
from Settings import Settings, setting_infos
from version import __version__ as ESVersion


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


    # shared
    settingsFrame = Frame(mainWindow)
    settings_string_var = StringVar()
    settingsEntry = Entry(settingsFrame, textvariable=settings_string_var)

    def show_settings(event=None):
        settings = guivars_to_settings(guivars)
        settings_string_var.set( settings.get_settings_string() )

        # Update any dependencies
        for info in setting_infos:
            if info.gui_params and 'dependency' in info.gui_params:
                dep_met = True
                for dep_var, dep_val in info.gui_params['dependency'].items():
                    if guivars[dep_var].get() != dep_val:
                        dep_met = False

                if widgets[info.name].winfo_class() == 'Frame':
                    for child in widgets[info.name].winfo_children():
                        child.configure(state= 'normal' if dep_met else 'disabled')
                else:
                    widgets[info.name].config(state = 'normal' if dep_met else 'disabled')


    def import_settings(event=None):
        try:
            settings = guivars_to_settings(guivars)
            text = settings_string_var.get().upper()
            settings.seed = guivars['seed'].get()
            settings.update_with_settings_string(text)
            settings_to_guivars(settings, guivars)
        except Exception as e:
            messagebox.showerror(title="Error", message="Invalid settings string")

    label = Label(settingsFrame, text="Settings String")
    importSettingsButton = Button(settingsFrame, text='Import Settings String', command=import_settings)
    label.pack(side=LEFT, anchor=W, padx=5)
    settingsEntry.pack(side=LEFT, anchor=W)
    importSettingsButton.pack(side=LEFT, anchor=W, padx=5)



    fileDialogFrame = Frame(frames['rom_tab'])

    romDialogFrame = Frame(fileDialogFrame)
    baseRomLabel = Label(romDialogFrame, text='Base Rom')
    guivars['rom'] = StringVar(value='ZOOTDEC.z64')
    romEntry = Entry(romDialogFrame, textvariable=guivars['rom'], width=40)

    def RomSelect():
        rom = filedialog.askopenfilename(filetypes=[("Rom Files", (".z64", ".n64")), ("All Files", "*")])
        if rom != '':
            guivars['rom'].set(rom)
    romSelectButton = Button(romDialogFrame, text='Select Rom', command=RomSelect, width=10)

    baseRomLabel.pack(side=LEFT, padx=(40,0))
    romEntry.pack(side=LEFT, padx=3)
    romSelectButton.pack(side=LEFT)

    romDialogFrame.pack()

    fileDialogFrame.pack(side=TOP, anchor=W, padx=5, pady=(5,1))

    def open_output():
        open_file(output_path(''))
    
    def output_dir_select():
        rom = filedialog.askdirectory(initialdir = default_output_path(guivars['output_dir'].get()))
        if rom != '':
            guivars['output_dir'].set(rom)

    outputDialogFrame = Frame(frames['rom_tab'])
    outputDirLabel = Label(outputDialogFrame, text='Output Directory')
    guivars['output_dir'] = StringVar(value='')
    outputDirEntry = Entry(outputDialogFrame, textvariable=guivars['output_dir'], width=40)
    outputDirButton = Button(outputDialogFrame, text='Select Dir', command=output_dir_select, width=10)
    outputDirLabel.pack(side=LEFT, padx=(3,0))
    outputDirEntry.pack(side=LEFT, padx=3)
    outputDirButton.pack(side=LEFT)
    outputDialogFrame.pack(side=TOP, anchor=W, padx=5, pady=(5,1))

    if os.path.exists(local_path('README.html')):
        def open_readme():
            open_file(local_path('README.html'))
        openReadmeButton = Button(outputDialogFrame, text='Open Documentation', command=open_readme)
        openReadmeButton.pack(side=LEFT, padx=5)

    outputDialogFrame.pack(side=TOP, anchor=W, pady=3)

    countDialogFrame = Frame(frames['rom_tab'])
    countLabel = Label(countDialogFrame, text='Generation Count')
    guivars['count'] = StringVar()
    countSpinbox = Spinbox(countDialogFrame, from_=1, to=100, textvariable=guivars['count'], width=3)

    countLabel.pack(side=LEFT)
    countSpinbox.pack(side=LEFT, padx=2)
    countDialogFrame.pack(side=TOP, anchor=W, padx=5, pady=(1,1))

    multiworldFrame = LabelFrame(frames['rom_tab'], text='Multi-World Generation')
    countLabel = Label(multiworldFrame, wraplength=300, justify=LEFT, text='This is used for co-op generations. Increasing World Count will drastically increase the generation time. For more information see https://github.com/TestRunnerSRL/bizhawk-co-op')
    countLabel.pack(side=TOP, anchor=W, padx=5, pady=(1,1))


    worldCountFrame = Frame(multiworldFrame)
    countLabel = Label(worldCountFrame, text='World Count')
    guivars['world_count'] = StringVar()
    countSpinbox = Spinbox(worldCountFrame, from_=1, to=100, textvariable=guivars['world_count'], width=3)

    countLabel.pack(side=LEFT)
    countSpinbox.pack(side=LEFT, padx=2)
    worldCountFrame.pack(side=LEFT, anchor=N, padx=5, pady=(1,1))

    playerNumFrame = Frame(multiworldFrame)
    countLabel = Label(playerNumFrame, text='Player Number')
    guivars['player_num'] = StringVar()
    countSpinbox = Spinbox(playerNumFrame, from_=1, to=100, textvariable=guivars['player_num'], width=3)

    countLabel.pack(side=LEFT)
    countSpinbox.pack(side=LEFT, padx=2)
    playerNumFrame.pack(side=LEFT, anchor=N, padx=5, pady=(1,1))
    multiworldFrame.pack(side=TOP, anchor=W, padx=5, pady=(1,1))




    # build gui
    ############

    widgets = {}

    for info in setting_infos:
        if info.gui_params:
            if info.gui_params['widget'] == 'Checkbutton':
                # determine the initial value of the checkbox
                default_value = 1 if info.gui_params['default'] == "checked" else 0
                # create a variable to access the box's state
                guivars[info.name] = IntVar(value=default_value)
                # create the checkbox
                widgets[info.name] = Checkbutton(frames[info.gui_params['group']], text=info.gui_params['text'], variable=guivars[info.name], justify=LEFT, wraplength=200, command=show_settings)
                widgets[info.name].pack(expand=False, anchor=W)
            elif info.gui_params['widget'] == 'Combobox':
                # create the variable to store the user's decision
                guivars[info.name] = StringVar(value=info.gui_params['default'])
                # create the option menu
                widgets[info.name] = Frame(frames[info.gui_params['group']])
                # dropdown = OptionMenu(widgets[info.name], guivars[info.name], *(info['options']))
                if isinstance(info.gui_params['options'], list):
                    info.gui_params['options'] = dict(zip(info.gui_params['options'], info.gui_params['options']))
                dropdown = ttk.Combobox(widgets[info.name], textvariable=guivars[info.name], values=list(info.gui_params['options'].keys()), state='readonly', width=30)
                dropdown.bind("<<ComboboxSelected>>", show_settings)
                dropdown.pack(side=BOTTOM, anchor=W)
                # label the option
                if 'text' in info.gui_params:
                    label = Label(widgets[info.name], text=info.gui_params['text'])
                    label.pack(side=LEFT, anchor=W, padx=5)
                # pack the frame
                widgets[info.name].pack(expand=False, side=TOP, anchor=W, padx=3, pady=3)
            elif info.gui_params['widget'] == 'Scale':
                # create the variable to store the user's decision
                guivars[info.name] = IntVar(value=info.gui_params['default'])
                # create the option menu
                widgets[info.name] = Frame(frames[info.gui_params['group']])
                # dropdown = OptionMenu(widgets[info.name], guivars[info.name], *(info['options']))
                minval = 'min' in info.gui_params and info.gui_params['min'] or 0
                maxval = 'max' in info.gui_params and info.gui_params['max'] or 100
                stepval = 'step' in info.gui_params and info.gui_params['step'] or 1


                scale = Scale(widgets[info.name], variable=guivars[info.name], from_=minval, to=maxval, tickinterval=stepval, resolution=stepval, showvalue=0, orient=HORIZONTAL, sliderlength=15, length=200, command=show_settings)
                scale.pack(side=BOTTOM, anchor=W)
                # label the option
                if 'text' in info.gui_params:
                    label = Label(widgets[info.name], text=info.gui_params['text'])
                    label.pack(side=LEFT, anchor=W, padx=5)
                # pack the frame
                widgets[info.name].pack(expand=False, side=TOP, anchor=W, padx=3, pady=3)
            elif info.gui_params['widget'] == 'Entry':
                # create the variable to store the user's decision
                guivars[info.name] = StringVar(value=info.gui_params['default'])
                # create the option menu
                widgets[info.name] = Frame(frames[info.gui_params['group']])

                entry = Entry(widgets[info.name], textvariable=guivars[info.name], width=30)
                entry.pack(side=BOTTOM, anchor=W)
                # label the option
                if 'text' in info.gui_params:
                    label = Label(widgets[info.name], text=info.gui_params['text'])
                    label.pack(side=LEFT, anchor=W, padx=5)
                # pack the frame
                widgets[info.name].pack(expand=False, side=TOP, anchor=W, padx=3, pady=3)


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



    # didn't refactor the rest, sorry


    # create the option menu

    settingsFrame.pack(fill=BOTH, anchor=W, padx=5, pady=(10,0))

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

    generateSeedFrame = Frame(mainWindow)
    generateButton = Button(generateSeedFrame, text='Generate Patched Rom', command=generateRom)

    seedLabel = Label(generateSeedFrame, text='Seed')
    guivars['seed'] = StringVar()
    seedEntry = Entry(generateSeedFrame, textvariable=guivars['seed'])
    seedLabel.pack(side=LEFT)
    seedEntry.pack(side=LEFT)
    generateButton.pack(side=LEFT, padx=(5, 0))

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

    show_settings()

    mainWindow.mainloop()

    # save settings on close
    with open('settings.sav', 'w') as outfile:
        settings = guivars_to_settings(guivars)
        json.dump(settings.__dict__, outfile)


if __name__ == '__main__':
    guiMain()
