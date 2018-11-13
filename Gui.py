#!/usr/bin/env python3
from argparse import Namespace
from glob import glob
import json
import random
import re
import os
import shutil
from tkinter import Scale, Checkbutton, OptionMenu, Toplevel, LabelFrame, Radiobutton, PhotoImage, Tk, BOTH, LEFT, RIGHT, BOTTOM, TOP, StringVar, IntVar, Frame, Label, W, E, X, N, S, NW, Entry, Spinbox, Button, filedialog, messagebox, ttk, HORIZONTAL, Toplevel
from tkinter.colorchooser import *
from urllib.parse import urlparse
from urllib.request import urlopen

from GuiUtils import ToolTips, set_icon, BackgroundTask, BackgroundTaskProgress, Dialog, ValidatingEntry
from Main import main, from_patch_file
from Utils import is_bundled, local_path, default_output_path, open_file, check_version
from Patches import get_tunic_color_options, get_navi_color_options
from Settings import Settings
from SettingsList import setting_infos
from version import __version__ as ESVersion
import webbrowser
import WorldFile

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
                    if 'Custom Color' in info.gui_params['options'] and re.match(r'^[A-Fa-f0-9]{6}$', value):
                        guivar.set('Custom (#' + value + ')')
                    else:
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
            # set guivar to hexcode if custom color
            if re.match(r'^Custom \(#[A-Fa-f0-9]{6}\)$', guivar.get()):
                result[name] = re.findall(r'[A-Fa-f0-9]{6}', guivar.get())[0]
            elif info.gui_params and 'options' in info.gui_params:
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
    mainWindow.resizable(False, False)

    set_icon(mainWindow)

    notebook = ttk.Notebook(mainWindow)
    frames['rom_tab'] = ttk.Frame(notebook)
    frames['rules_tab'] = ttk.Frame(notebook)
    frames['logic_tab'] = ttk.Frame(notebook)
    frames['other_tab'] = ttk.Frame(notebook)
    frames['aesthetic_tab'] = ttk.Frame(notebook)
    frames['aesthetic_tab_left'] = Frame(frames['aesthetic_tab'])
    frames['aesthetic_tab_right'] = Frame(frames['aesthetic_tab'])
    notebook.add(frames['rom_tab'], text='ROM Options')
    notebook.add(frames['rules_tab'], text='Main Rules')
    notebook.add(frames['logic_tab'], text='Detailed Logic')
    notebook.add(frames['other_tab'], text='Other')
    notebook.add(frames['aesthetic_tab'], text='Cosmetics')

    #######################
    # randomizer controls #
    #######################

    # hold the results of the user's decisions here
    guivars = {}
    widgets = {}

    # hierarchy
    ############

    #Rules Tab
    frames['open']   = LabelFrame(frames['rules_tab'], text='Open',   labelanchor=NW)
    frames['world']  = LabelFrame(frames['rules_tab'], text='World',   labelanchor=NW)
    frames['logic']  = LabelFrame(frames['rules_tab'], text='Shuffle',  labelanchor=NW)

    # Logic tab
    frames['rewards'] = LabelFrame(frames['logic_tab'], text='Remove Specific Locations', labelanchor=NW)
    frames['tricks']  = LabelFrame(frames['logic_tab'], text='Specific Expected Tricks', labelanchor=NW)

    #Other Tab
    frames['convenience'] = LabelFrame(frames['other_tab'], text='Speed Ups', labelanchor=NW)
    frames['other']       = LabelFrame(frames['other_tab'], text='Misc',      labelanchor=NW)

    #Aesthetics tab
    frames['cosmetics'] = LabelFrame(frames['aesthetic_tab'], text='General', labelanchor=NW)
    frames['tuniccolor'] = LabelFrame(frames['aesthetic_tab_left'], text='Tunic Color', labelanchor=NW)
    frames['navicolor']  = LabelFrame(frames['aesthetic_tab_right'], text='Navi Color',  labelanchor=NW)
    frames['lowhp']      = LabelFrame(frames['aesthetic_tab_left'], text='Low HP SFX',  labelanchor=NW)
    frames['navihint']   = LabelFrame(frames['aesthetic_tab_right'], text='Navi SFX', labelanchor=NW)


    # shared
    def toggle_widget(widget, enabled):
        widget_type = widget.winfo_class()
        if widget_type == 'Frame' or widget_type == 'TFrame' or widget_type == 'Labelframe':
            if widget_type == 'Labelframe':
                widget.configure(fg='Black'if enabled else 'Grey')
            for child in widget.winfo_children():
                toggle_widget(child, enabled)
        else:
            if widget_type == 'TCombobox':
                widget.configure(state= 'readonly' if enabled else 'disabled')
            else:
                widget.configure(state= 'normal' if enabled else 'disabled')

            if widget_type == 'Scale':
                widget.configure(fg='Black'if enabled else 'Grey')


    def show_settings(event=None):
        settings = guivars_to_settings(guivars)
        settings_string_var.set( settings.get_settings_string() )

        settings_valid = update_generation_type()

        # Update any dependencies
        for info in setting_infos:
            if info.gui_params and 'dependency' in info.gui_params:
                dep_met = settings_valid and info.gui_params['dependency'](guivars)
                toggle_widget(widgets[info.name], dep_met)

            if info.name in guivars and guivars[info.name].get() == 'Custom Color':
                color = askcolor()
                if color == (None, None):
                    color = ((0,0,0),'#000000')
                guivars[info.name].set('Custom (' + color[1] + ')')
        


    def update_logic_tricks(event=None):
        for info in setting_infos:
            if info.gui_params \
            and info.gui_params['widget'] == 'Checkbutton' \
            and info.gui_params['group'] == 'tricks':
                if guivars['all_logic_tricks'].get():
                    widgets[info.name].select()
                else:
                    widgets[info.name].deselect()

        settings = guivars_to_settings(guivars)
        settings_string_var.set( settings.get_settings_string() )


    fileDialogFrame = Frame(frames['rom_tab'])

    romDialogFrame = Frame(fileDialogFrame)
    baseRomLabel = Label(romDialogFrame, text='Base ROM')
    guivars['rom'] = StringVar(value='')
    romEntry = Entry(romDialogFrame, textvariable=guivars['rom'], width=40)

    def RomSelect():
        rom = filedialog.askopenfilename(filetypes=[("ROM Files", (".z64", ".n64")), ("All Files", "*")])
        if rom != '':
            guivars['rom'].set(rom)
    romSelectButton = Button(romDialogFrame, text='Select ROM', command=RomSelect, width=10)

    baseRomLabel.pack(side=LEFT, padx=(38,0))
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
    outputDialogFrame.pack(side=TOP, anchor=W, pady=3)

    countDialogFrame = Frame(frames['rom_tab'])
    countLabel = Label(countDialogFrame, text='Generation Count')
    guivars['count'] = StringVar()
    widgets['count'] = Spinbox(countDialogFrame, from_=1, to=100, textvariable=guivars['count'], width=3)

    if os.path.exists(local_path('README.html')):
        def open_readme():
            open_file(local_path('README.html'))
        openReadmeButton = Button(countDialogFrame, text='Open Documentation', command=open_readme)
        openReadmeButton.pack(side=RIGHT, padx=5)

    countLabel.pack(side=LEFT)
    widgets['count'].pack(side=LEFT, padx=2)
    countDialogFrame.pack(side=TOP, anchor=W, padx=5, pady=(1,1))


    # build gui
    ############

    # Add special checkbox to toggle all logic tricks
    guivars['all_logic_tricks'] = IntVar(value=0)
    widgets['all_logic_tricks'] = Checkbutton(frames['tricks'], text="Enable All Tricks", variable=guivars['all_logic_tricks'], justify=LEFT, wraplength=190, command=update_logic_tricks)
    widgets['all_logic_tricks'].pack(expand=False, anchor=W)

    for info in setting_infos:
        if info.gui_params and 'group' in info.gui_params:
            if info.gui_params['widget'] == 'Checkbutton':
                # determine the initial value of the checkbox
                default_value = 1 if info.gui_params['default'] == "checked" else 0
                # create a variable to access the box's state
                guivars[info.name] = IntVar(value=default_value)
                # create the checkbox
                widgets[info.name] = Checkbutton(frames[info.gui_params['group']], text=info.gui_params['text'], variable=guivars[info.name], justify=LEFT, wraplength=190, command=show_settings)
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
            elif info.gui_params['widget'] == 'Radiobutton':
                # create the variable to store the user's decision
                guivars[info.name] = StringVar(value=info.gui_params['default'])
                # create the option menu
                widgets[info.name] = LabelFrame(frames[info.gui_params['group']], text=info.gui_params['text'] if 'text' in info.gui_params else info["name"], labelanchor=NW)
                if isinstance(info.gui_params['options'], list):
                    info.gui_params['options'] = dict(zip(info.gui_params['options'], info.gui_params['options']))
                # setup orientation
                side = TOP
                anchor = W
                if "horizontal" in info.gui_params and info.gui_params["horizontal"]:
                    side = LEFT
                    anchor = N
                # add the radio buttons
                for option in info.gui_params["options"]:
                    radio_button = Radiobutton(widgets[info.name], text=option, value=option, variable=guivars[info.name], justify=LEFT, wraplength=190, indicatoron=False, command=show_settings)
                    radio_button.pack(expand=True, side=side, anchor=anchor)
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

                if 'validate' in info.gui_params:
                    entry = ValidatingEntry(widgets[info.name], command=show_settings, validate=info.gui_params['validate'], textvariable=guivars[info.name], width=30)
                else:
                    entry = Entry(widgets[info.name], textvariable=guivars[info.name], width=30)
                entry.pack(side=BOTTOM, anchor=W)
                # label the option
                if 'text' in info.gui_params:
                    label = Label(widgets[info.name], text=info.gui_params['text'])
                    label.pack(side=LEFT, anchor=W, padx=5)
                # pack the frame
                widgets[info.name].pack(expand=False, side=TOP, anchor=W, padx=3, pady=3)

            if 'tooltip' in info.gui_params:
                ToolTips.register(widgets[info.name], info.gui_params['tooltip'])


    # pack the hierarchy

    frames['logic'].pack( fill=BOTH, expand=True, anchor=N, side=RIGHT, pady=(5,1) )
    frames['open'].pack(  fill=BOTH, expand=True, anchor=W, side=TOP, pady=(5,1) )
    frames['world'].pack( fill=BOTH, expand=True, anchor=W, side=BOTTOM, pady=(5,1) )

    # Logic tab
    frames['rewards'].pack(fill=BOTH, expand=True, anchor=N, side=LEFT, pady=(5,1) )
    frames['tricks'].pack( fill=BOTH, expand=True, anchor=N, side=LEFT, pady=(5,1) )

    #Other Tab
    frames['convenience'].pack(fill=BOTH, expand=True, anchor=N, side=LEFT, pady=(5,1) )
    frames['other'].pack(      fill=BOTH, expand=True, anchor=N, side=LEFT, pady=(5,1) )

    #Aesthetics tab
    frames['cosmetics'].pack(fill=BOTH, expand=True, anchor=W, side=TOP)
    frames['aesthetic_tab_left'].pack( fill=BOTH, expand=True, anchor=W, side=LEFT)
    frames['aesthetic_tab_right'].pack(fill=BOTH, expand=True, anchor=W, side=RIGHT)

    #Aesthetics tab - Left Side
    frames['tuniccolor'].pack(fill=BOTH, expand=True, anchor=W, side=TOP, pady=(5,1) )
    frames['lowhp'].pack(     fill=BOTH, expand=True, anchor=W, side=TOP, pady=(5,1) )

    #Aesthetics tab - Right Side
    frames['navicolor'].pack( fill=BOTH, expand=True, anchor=W, side=TOP, pady=(5,1) )
    frames['navihint'].pack(  fill=BOTH, expand=True, anchor=W, side=TOP, pady=(5,1) )


    notebook.pack(fill=BOTH, expand=True, padx=5, pady=5)


    #Multi-World
    widgets['multiworld'] = LabelFrame(frames['rom_tab'], text='Multi-World Generation')
    countLabel = Label(widgets['multiworld'], wraplength=350, justify=LEFT, text='This is used for co-op generations. Increasing Player Count will drastically increase the generation time. For more information see:')
    hyperLabel = Label(widgets['multiworld'], wraplength=350, justify=LEFT, text='https://github.com/TestRunnerSRL/bizhawk-co-op', fg='blue', cursor='hand2')
    hyperLabel.bind("<Button-1>", lambda event: webbrowser.open_new(r"https://github.com/TestRunnerSRL/bizhawk-co-op"))
    countLabel.pack(side=TOP, anchor=W, padx=5, pady=0)
    hyperLabel.pack(side=TOP, anchor=W, padx=5, pady=0)

    worldCountFrame = Frame(widgets['multiworld'])
    countLabel = Label(worldCountFrame, text='Player Count')
    guivars['world_count'] = StringVar()
    widgets['world_count'] = Spinbox(worldCountFrame, from_=1, to=31, textvariable=guivars['world_count'], width=3)
    countLabel.pack(side=LEFT)
    widgets['world_count'].pack(side=LEFT, padx=2)
    worldCountFrame.pack(side=LEFT, anchor=N, padx=10, pady=(1,5))

    playerNumFrame = Frame(widgets['multiworld'])
    countLabel = Label(playerNumFrame, text='Player ID')
    guivars['player_num'] = StringVar()
    widgets['player_num'] = Spinbox(playerNumFrame, from_=1, to=31, textvariable=guivars['player_num'], width=3)
    countLabel.pack(side=LEFT)
    widgets['player_num'].pack(side=LEFT, padx=2)
    ToolTips.register(widgets['player_num'], 'Generate for specific Player.')
    playerNumFrame.pack(side=LEFT, anchor=N, padx=10, pady=(1,5))

    guivars['player_num_all'] = IntVar()
    widgets['player_num_all'] = Checkbutton(widgets['multiworld'], text='All Players', variable=guivars['player_num_all'], justify=LEFT, wraplength=190, command=show_settings)
    widgets['player_num_all'].pack(side=LEFT, anchor=N, padx=10, pady=(0,0))
    ToolTips.register(widgets['player_num_all'], '''\
                      Generate patches for all players.
                      Only available if Output Type is 
                      set to 'Patch File'.
                      ''')
    widgets['multiworld'].pack(side=TOP, anchor=W, padx=5, pady=(1,1))


    # create the generation menu
    def update_generation_type(event=None):
        if generation_notebook.tab(generation_notebook.select())['text'] == 'Generate From Seed':
            notebook.tab(1, state="normal")
            notebook.tab(2, state="normal")
            notebook.tab(3, state="normal")
            toggle_widget(widgets['multiworld'], True)
            toggle_widget(widgets['create_spoiler'], True)
            toggle_widget(widgets['count'], True)
            return True
        else:
            notebook.tab(1, state="disabled")
            notebook.tab(2, state="disabled")
            notebook.tab(3, state="disabled")
            toggle_widget(widgets['multiworld'], False)
            toggle_widget(widgets['create_spoiler'], False)
            toggle_widget(widgets['count'], False)
            return False



    generation_notebook = ttk.Notebook(mainWindow)
    frames['gen_from_seed'] = ttk.Frame(generation_notebook)
    frames['gen_from_file'] = ttk.Frame(generation_notebook)
    generation_notebook.add(frames['gen_from_seed'], text='Generate From Seed')
    generation_notebook.add(frames['gen_from_file'], text='Generate From File')
    generation_notebook.bind("<<NotebookTabChanged>>", show_settings)

    # From seed tab
    def import_settings(event=None):
        try:
            settings = guivars_to_settings(guivars)
            text = settings_string_var.get().upper()
            settings.seed = guivars['seed'].get()
            settings.update_with_settings_string(text)
            settings_to_guivars(settings, guivars)
            show_settings()
        except Exception as e:
            messagebox.showerror(title="Error", message="Invalid settings string")

    settingsFrame = Frame(frames['gen_from_seed'])
    settings_string_var = StringVar()
    widgets['setting_string'] = Entry(settingsFrame, textvariable=settings_string_var, width=30)

    label = Label(settingsFrame, text="Settings String")
    widgets['import_settings'] = Button(settingsFrame, text='Import Settings String', command=import_settings)
    label.pack(side=LEFT, anchor=W, padx=5)
    widgets['setting_string'].pack(side=LEFT, anchor=W)
    widgets['import_settings'].pack(side=LEFT, anchor=W, padx=5)

    settingsFrame.pack(fill=BOTH, anchor=W, padx=5, pady=(10,0))

    def multiple_run(settings, window):
        orig_seed = settings.seed
        for i in range(settings.count):
            settings.update_seed(orig_seed + '-' + str(i))
            window.update_title("Generating Seed %s...%d/%d" % (settings.seed, i+1, settings.count))
            main(settings, window)

    def generateRom():
        settings = guivars_to_settings(guivars)
        if settings.count:
            BackgroundTaskProgress(mainWindow, "Generating Seed %s..." % settings.seed, multiple_run, settings)
        else:
            BackgroundTaskProgress(mainWindow, "Generating Seed %s..." % settings.seed, main, settings)

    generateSeedFrame = Frame(frames['gen_from_seed'])
    generateButton = Button(generateSeedFrame, text='Generate Patched ROM', command=generateRom)

    seedLabel = Label(generateSeedFrame, text='Seed')
    guivars['seed'] = StringVar()
    widgets['seed'] = Entry(generateSeedFrame, textvariable=guivars['seed'], width=30)
    seedLabel.pack(side=LEFT, padx=(55, 5))
    widgets['seed'].pack(side=LEFT)
    generateButton.pack(side=LEFT, padx=(5, 0))

    generateSeedFrame.pack(side=BOTTOM, anchor=W, padx=5, pady=10)

    # From file tab
    patchDialogFrame = Frame(frames['gen_from_file'])

    patchFileLabel = Label(patchDialogFrame, text='Patch File')
    guivars['patch_file'] = StringVar(value='')
    patchEntry = Entry(patchDialogFrame, textvariable=guivars['patch_file'], width=45)

    def PatchSelect():
        patch_file = filedialog.askopenfilename(filetypes=[("Patch Files", ".zpf"), ("All Files", "*")])
        if patch_file != '':
            guivars['patch_file'].set(patch_file)
    patchSelectButton = Button(patchDialogFrame, text='Select File', command=PatchSelect, width=10)

    patchFileLabel.pack(side=LEFT, padx=(5,0))
    patchEntry.pack(side=LEFT, padx=3)
    patchSelectButton.pack(side=LEFT)

    patchDialogFrame.pack(side=TOP, anchor=W, padx=5, pady=(10,5))

    def generateFromFile():
        settings = guivars_to_settings(guivars)
        BackgroundTaskProgress(mainWindow, "Generating From File %s..." % os.path.basename(settings.patch_file), from_patch_file, settings)

    generateFileButton = Button(frames['gen_from_file'], text='Generate Patched ROM', command=generateFromFile)
    generateFileButton.pack(side=BOTTOM, anchor=E, pady=(0,10), padx=(0, 10))

    generation_notebook.pack(fill=BOTH, expand=True, padx=5, pady=5)


    guivars['checked_version'] = StringVar()

    if settings is not None:
        # load values from commandline args
        settings_to_guivars(settings, guivars)
    else:
        # try to load saved settings
        try:
            settingsFile = local_path('settings.sav')
            with open(settingsFile) as f:
                settings = Settings( json.load(f) )
                settings.update_seed("")
                settings_to_guivars(settings, guivars)
        except:
            pass

    show_settings()

    def gui_check_version():
        task = BackgroundTask(mainWindow, check_version, guivars['checked_version'].get())
        while task.running:
            mainWindow.update()

        if task.status:
            dialog = Dialog(mainWindow, title="Version Error", question=task.status, oktext='Don\'t show again', canceltext='OK')
            if dialog.result:
                guivars['checked_version'].set(ESVersion)

    mainWindow.after(1000, gui_check_version)
    mainWindow.mainloop()

    # save settings on close
    with open('settings.sav', 'w') as outfile:
        settings = guivars_to_settings(guivars)
        json.dump(settings.__dict__, outfile)


if __name__ == '__main__':
    guiMain()
