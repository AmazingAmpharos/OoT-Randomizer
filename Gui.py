#!/usr/bin/env python3
from argparse import Namespace
from glob import glob
import json
import random
import os
import shutil
import logging
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

    createSpoilerVar = IntVar()
    createSpoilerCheckbutton = Checkbutton(checkBoxFrame, text="Create Spoiler Log (affects item layout)", variable=createSpoilerVar)
    suppressRomVar = IntVar()
    suppressRomCheckbutton = Checkbutton(checkBoxFrame, text="Do not create patched Rom", variable=suppressRomVar)
    compressRomVar = IntVar()
    compressRomCheckbutton = Checkbutton(checkBoxFrame, text="Compress patched Rom", variable=compressRomVar)
    openForestVar = IntVar()
    openForestCheckbutton = Checkbutton(checkBoxFrame, text="Open Forest", variable=openForestVar)
    openDoorVar = IntVar()
    openDoorCheckbutton = Checkbutton(checkBoxFrame, text="Open Door of Time", variable=openDoorVar)
    fastGanonVar = IntVar()
    fastGanonCheckbutton = Checkbutton(checkBoxFrame, text="Skip most of Ganon's Castle", variable=fastGanonVar)
    dungeonItemsVar = IntVar()
    dungeonItemsCheckbutton = Checkbutton(checkBoxFrame, text="Place Dungeon Items (Compasses/Maps)", onvalue=0, offvalue=1, variable=dungeonItemsVar)
    beatableOnlyVar = IntVar()
    beatableOnlyCheckbutton = Checkbutton(checkBoxFrame, text="Only ensure seed is beatable, not all items must be reachable", variable=beatableOnlyVar)
    hintsVar = IntVar()
    hintsCheckbutton = Checkbutton(checkBoxFrame, text="Gossip Stone Hints with Stone of Agony", variable=hintsVar)

    createSpoilerCheckbutton.pack(expand=True, anchor=W)
    suppressRomCheckbutton.pack(expand=True, anchor=W)
    compressRomCheckbutton.pack(expand=True, anchor=W)
    openForestCheckbutton.pack(expand=True, anchor=W)
    openDoorCheckbutton.pack(expand=True, anchor=W)
    fastGanonCheckbutton.pack(expand=True, anchor=W)
    dungeonItemsCheckbutton.pack(expand=True, anchor=W)
    beatableOnlyCheckbutton.pack(expand=True, anchor=W)
    hintsCheckbutton.pack(expand=True, anchor=W)

    bottomFrame = Frame(randomizerWindow)
    topOfBottomFrame = Frame(bottomFrame)
    bottomOfBottomFrame = Frame(bottomFrame)

    outputDirLabel = Label(topOfBottomFrame, text='Set Output Dir')
    dirVar = StringVar()
    dirEntry = Entry(topOfBottomFrame, textvariable=dirVar)

    def DirSelect():
        outputDirectory = None
        #check if a directory was selected already or not. If so, try to open it. 
        #could also add trying to create it if it fails to open, but then that might create a lot of unnecessary directories for an end user.
        if dirVar.get() is not None and dirVar.get() is not '':
            try:
                outputDirectory = filedialog.askdirectory(initialdir=dirVar.get(),title='Please select an output directory', mustexist=False)
            except:
                outputDirectory = filedialog.askdirectory(initialdir='.',title='Please select an output directory', mustexist=False)
        else:
            outputDirectory = filedialog.askdirectory(initialdir='.',title='Please select an output directory', mustexist=False)

        #as a minor note, you can define a non-created dir in linux through the filedialog.askdirectory, hence the mustexist flag, but you can't do that in windows. 
        #just tkinter things.
        dirVar.set(outputDirectory)
    dirSelectButton = Button(topOfBottomFrame, text='Select Dir', command=DirSelect)


    baseRomLabel = Label(topOfBottomFrame, text='Base Rom')
    romVar = StringVar()
    romEntry = Entry(topOfBottomFrame, textvariable=romVar)

    def RomSelect():
        rom = filedialog.askopenfilename(filetypes=[("Rom Files", (".z64", ".n64")), ("All Files", "*")])
        romVar.set(rom)
    romSelectButton = Button(topOfBottomFrame, text='Select Rom', command=RomSelect)

    #for now, only include this in unbundled gui version, until custom output directories are added for bundled
    if not is_bundled():
        outputDirLabel.pack(side=LEFT)
        dirEntry.pack(side=LEFT)
        dirSelectButton.pack(side=LEFT)

    romSelectButton.pack(side=RIGHT)
    romEntry.pack(side=RIGHT)
    baseRomLabel.pack(side=RIGHT)
    

    topOfBottomFrame.pack(side=TOP)

    checkBoxFrame.pack()

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
    kokiriOptionMenu = OptionMenu(kokiriFrame, colorVars[0], 'Kokiri Green', 'Goron Red', 'Zora Blue', 'Black', 'White', 'Purple', 'Yellow', 'Orange', 'Pink', 'Gray', 'Brown', 'Gold', 'Silver', 'Beige', 'Teal', 'Royal Blue', 'Sonic Blue', 'Blood Red', 'Blood Orange', 'NES Green', 'Dark Green', 'Random', 'True Random')
    kokiriOptionMenu.pack(side=RIGHT)
    kokiriLabel = Label(kokiriFrame, text='Kokiri Tunic Color')
    kokiriLabel.pack(side=LEFT)

    goronFrame = Frame(dropDownFrame)
    goronOptionMenu = OptionMenu(goronFrame, colorVars[1], 'Kokiri Green', 'Goron Red', 'Zora Blue', 'Black', 'White', 'Purple', 'Yellow', 'Orange', 'Pink', 'Gray', 'Brown', 'Gold', 'Silver', 'Beige', 'Teal', 'Royal Blue', 'Sonic Blue', 'Blood Red', 'Blood Orange', 'NES Green', 'Dark Green', 'Random', 'True Random')
    goronOptionMenu.pack(side=RIGHT)
    goronLabel = Label(goronFrame, text='Goron Tunic Color')
    goronLabel.pack(side=LEFT)

    zoraFrame = Frame(dropDownFrame)
    zoraOptionMenu = OptionMenu(zoraFrame, colorVars[2], 'Kokiri Green', 'Goron Red', 'Zora Blue', 'Black', 'White', 'Purple', 'Yellow', 'Orange', 'Pink', 'Gray', 'Brown', 'Gold', 'Silver', 'Beige', 'Teal', 'Royal Blue', 'Sonic Blue', 'Blood Red', 'Blood Orange', 'NES Green', 'Dark Green', 'Random', 'True Random')
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

    seedLabel = Label(bottomOfBottomFrame, text='Seed #')
    seedVar = StringVar()
    seedEntry = Entry(bottomOfBottomFrame, textvariable=seedVar)
    countLabel = Label(bottomOfBottomFrame, text='Count')
    countVar = StringVar()
    countSpinbox = Spinbox(bottomOfBottomFrame, from_=1, to=100, textvariable=countVar)

    def generateRom():
        nonlocal dirVar
        guiargs = Namespace
        guiargs.seed = int(seedVar.get()) if seedVar.get() else None
        guiargs.count = int(countVar.get()) if countVar.get() != '1' else None
        guiargs.bridge = bridgeVar.get()
        guiargs.kokiricolor = colorVars[0].get()
        guiargs.goroncolor = colorVars[1].get()
        guiargs.zoracolor = colorVars[2].get()
        guiargs.healthSFX = lowHealthSFXVar.get()
        guiargs.create_spoiler = bool(createSpoilerVar.get())
        guiargs.suppress_rom = bool(suppressRomVar.get())
        guiargs.compress_rom = bool(compressRomVar.get())
        guiargs.open_forest = bool(openForestVar.get())
        guiargs.open_door_of_time = bool(openDoorVar.get())
        guiargs.fast_ganon = bool(fastGanonVar.get())
        guiargs.nodungeonitems = bool(dungeonItemsVar.get())
        guiargs.beatableonly = bool(beatableOnlyVar.get())
        guiargs.hints = bool(hintsVar.get())
        guiargs.rom = romVar.get()
        if dirVar.get() is None:
            guiargs.output = None
        else:
            guiargs.output = dirVar.get()
            
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

    generateButton = Button(bottomOfBottomFrame, text='Generate Patched Rom', command=generateRom)

    bottomOfBottomFrame.pack(side=BOTTOM)

    seedLabel.pack(side=LEFT)
    seedEntry.pack(side=LEFT)
    countLabel.pack(side=LEFT, padx=(5, 0))
    countSpinbox.pack(side=LEFT)
    generateButton.pack(side=LEFT, padx=(5, 0))

    def open_output():
        logger = logging.getLogger('')
        nonlocal dirVar
        if dirVar is not None:
            try:
                open_file(output_path(dirVar.get()))
            except:
                logger.info('Unable to open file path, will attempt to create.')
                try:
                    os.mkdir(dirVar.get())
                    logger.info('Directory created.')
                    open_file(dirVar.get())
                except:
                    logger.info('Unable to create set output directory, resetting to default.')
                    dirVar.set('')
                    
                    open_file(output_path(''))

        else:
            open_file(output_path(''))

    openOutputButton = Button(farBottomFrame, text='Open Output Directory', command=open_output)

    openOutputButton.pack(side=RIGHT)

    dropDownFrame.pack(side=LEFT)
    rightHalfFrame.pack(side=RIGHT)
    topFrame.pack(side=TOP)
    bottomFrame.pack(side=BOTTOM)

    if args is not None:
        # load values from commandline args
        createSpoilerVar.set(int(args.create_spoiler))
        suppressRomVar.set(int(args.suppress_rom))
        compressRomVar.set(int(args.compress_rom))
        if args.nodungeonitems:
            dungeonItemsVar.set(int(not args.nodungeonitems))
        openForestVar.set(int(args.open_forest))
        openDoorVar.set(int(args.open_door_of_time))
        fastGanonVar.set(int(args.fast_ganon))
        beatableOnlyVar.set(int(args.beatableonly))
        hintsVar.set(int(args.hints))
        if args.count:
            countVar.set(str(args.count))
        if args.seed:
            seedVar.set(str(args.seed))
        bridgeVar.set(args.bridge)
        colorVars[0].set(args.kokiricolor)
        colorVars[1].set(args.goroncolor)
        colorVars[2].set(args.zoracolor)
        lowHealthSFXVar.set(args.healthSFX)
        romVar.set(args.rom)
        if args.output is not None:
            dirVar.set(args.output)

    mainWindow.mainloop()

if __name__ == '__main__':
    guiMain()
