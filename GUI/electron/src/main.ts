import { app, BrowserWindow, shell, session, ipcMain, globalShortcut, Menu, MenuItem } from "electron";
import * as os from "os";
import * as fs from "fs";
import * as path from "path";
import * as url from "url";

import * as windowStateKeeper from "electron-window-state";
import * as commander from 'commander';

var win: BrowserWindow;
var isRelease: boolean = false;

function createApp() {

  //Fix up empty node command line in bundled mode (crashes commander otherwise)
  if (app.isPackaged) {
    process.argv[0] = 'main.js';
    process.argv.unshift('node');

    //Fix PATH on macOS when bundled
    if (os.platform() == "darwin") {
      process.env.PATH = ['/usr/local/bin', process.env.PATH].join(':');
    }
  }

  //Parse command line
  commander
    .option('p, python <path>', 'Path to your python executable')
    .option('r, release', 'Runs electron in release mode')
    .parse(process.argv);

  global["commandLineArgs"] = commander;
  isRelease = commander.release || app.isPackaged;

  //Load the previous window state with fallback to defaults
  let mainWindowState = windowStateKeeper({
    defaultWidth: 961,
    defaultHeight: 888
  });

  //Browser Window common options
  let browserOptions = { icon: path.join(__dirname, '../src/assets/icon/png/64x64.png'), title: 'OoT Randomizer GUI', opacity: 1.00, backgroundColor: '#000000', minWidth: 880, minHeight: 680, width: mainWindowState.width, height: mainWindowState.height, x: mainWindowState.x, y: mainWindowState.y, show: false, webPreferences: { nodeIntegration: false, contextIsolation: true, webviewTag: false, preload: path.join(__dirname, 'preload.js') } };

  //Override menu (only need dev tools shortcut)
  let appMenu = new Menu();
  let subMenu = new Menu();

  subMenu.append(new MenuItem({
    label: 'Toggle Developer Tools',
    accelerator: os.platform() === 'darwin' ? 'Alt+Cmd+I' : 'Ctrl+Shift+I',
    click: () => { win.webContents.openDevTools(); }
  }));

  subMenu.append(new MenuItem({
    label: 'Refresh GUI',
    accelerator: 'F5',
    click: () => { win.webContents.reload(); }
  }));

  appMenu.append(new MenuItem({
    label: 'Electron',
    type: 'submenu',
    role: null,
    accelerator: null,
    submenu: subMenu
  }));

  //macOS specific overrides
  if (os.platform() == "darwin") {
    browserOptions["titleBarStyle"] = 'hiddenInset'; //macOS uses titleBarStyle to maintain a native feel with the finder menu and shortcuts users expect

    //Alter the dock icon on macOS and make it bounce to indicate activity until the browser window is created
    app.dock.setIcon(path.join(__dirname, '../src/assets/icon/png/64x64.png'));
    app.dock.bounce("critical");
  }
  else {
    browserOptions["frame"] = false; //Hide menu and frame entirely on every other platform since we use our custom title bar
    browserOptions["fullscreen"] = false; //Fullscreen mode is confusing with our custom title bar on Windows/Linux
    browserOptions["fullscreenable"] = false;
  }

  win = new BrowserWindow(browserOptions);
  win.setMenu(appMenu);

  //WindowStateKeeper will automatically persist window state changes to file
  mainWindowState.manage(win);

  //Run Content Security Policy
  manageCSP();

  if (!isRelease) {
    win.loadURL("http://localhost:4200/"); //Dev server
  }
  else { //Load release dist

    //Check if it exists first
    let indexPath = path.join(__dirname, '../../dist/ootr-electron-gui/index.html');

    if (!fs.existsSync(indexPath)) {

      console.error("No release found");

      setTimeout(() => {
        app.quit();
      }, 0);

      throw Error("No Electron GUI found! Did you compile it properly?");
    }

    win.loadURL(
      url.format({
        pathname: indexPath,
        protocol: "file:",
        slashes: true
      })
    );
  }

  win.once('ready-to-show', () => {
    win.show();

    if (!isRelease && !win.isMaximized()) //Open dev tools automatically if dev mode and not maximized
      win.webContents.openDevTools();
  });

  //macOS exclusive, goes to idle state
  win.on("closed", () => {
    win = null;
  });
}

//LISTENERS
app.on("ready", createApp);

//macOS exclusive, handles soft re-launches
app.on("activate", () => {
  if (win === null) {
    createApp();
  }
});

app.on("window-all-closed", () => {

  //Ensures the electron process always shuts down properly if all windows have been closed
  //Don't do this on macOS as users expect to be able to re-launch the app quickly from the dock after all windows get closed
  if (os.platform() != "darwin") {

    setTimeout(() => {
      app.quit();
    }, 1000);
  }
});

//Limit navigation to safe URLs and defer unsafe popups to system browser as well as handle page loading errors
app.on('web-contents-created', (event, contents) => {
  contents.on('will-navigate', (event, navigationUrl) => {
    const parsedUrl = new URL(navigationUrl);

    //console.log("Navigation attempt to:", parsedUrl.origin);

    //Whitelist for dev server in dev mode
    if (!isRelease) {
      if (parsedUrl.origin === 'http://localhost:4200') {
        return;
      }
    }

    event.preventDefault();
  });

  contents.on('new-window', (event, navigationUrl) => {

    const parsedUrl = new URL(navigationUrl);

    //console.log("New window creation attempt:", parsedUrl.origin);

    //Whitelist for dev server in dev mode
    if (!isRelease) {
      if (parsedUrl.origin === 'http://localhost:4200') {
        return;
      }
    }
        
    event.preventDefault();
    shell.openExternal(navigationUrl);
  });

  contents.on("did-fail-load", () => {
    console.error("GUI load failed");

    setTimeout(() => {
      app.quit();
    }, 0);

    if (!isRelease)
      throw Error("Couldn't connect to localhost:4200. Please start the Angular development server first before attempting to boot the Electron GUI!");
    else
      throw Error("The Electron GUI failed to load. Please delete the dist folder and re-compile!");
  });

});

//CSP
function manageCSP() {

  session.defaultSession.webRequest.onHeadersReceived((details, callback) => {
    callback({
      responseHeaders: {
        ...details.responseHeaders,
        'Content-Security-Policy': ['default-src \'self\' *.gstatic.com; img-src \'self\' data: *; style-src \'self\' \'unsafe-inline\' *.googleapis.com; script-src \'self\' \'unsafe-eval\' \'unsafe-inline\' *.googleapis.com; connect-src \'self\' *.githubusercontent.com ws: localhost:4200*']
      }
    })
  });

}

//IPC
ipcMain.on('getGeneratorGUISettings', (event, arg) => {

  let pythonRootPath = app.isPackaged ? app.getAppPath() + "/python/" : app.getAppPath() + "/../";

  //Load compiled settings_list.json
  let compiledSettingsMapPath = path.normalize(pythonRootPath + "data/generated/settings_list.json");
  let guiSettings;

  if (fs.existsSync(compiledSettingsMapPath)) {
    guiSettings = JSON.parse(fs.readFileSync(compiledSettingsMapPath, 'utf8'));
  }
  else {
    console.error("No settings_list.json found!");

    setTimeout(() => {
      app.quit();
    }, 0);

    throw Error("No settings_list.json found! Please restart the GUI using the Gui.py");
  }

  //Add static presets
  guiSettings.presets = {
    "[New Preset]": { isNewPreset: true },
    "Default / Beginner": { isDefaultPreset: true }
  };

  //Load built in presets
  let builtInPresetsPath = path.normalize(pythonRootPath + "data/presets_default.json");

  if (fs.existsSync(builtInPresetsPath)) {
    let builtInPresets = JSON.parse(fs.readFileSync(builtInPresetsPath, 'utf8'));
    let adjustedBuiltInPresets = {};

    //Tag built in presets appropiately
    Object.keys(builtInPresets).forEach(presetName => {
      if (!(presetName in guiSettings.presets))
        adjustedBuiltInPresets[presetName] = { isProtectedPreset: true, settings: builtInPresets[presetName] };
    });

    Object.assign(guiSettings.presets, adjustedBuiltInPresets);
  }

  //Load user presets
  let userPresetPath = path.normalize(pythonRootPath + "presets.sav");

  if (fs.existsSync(userPresetPath)) {
    let userPresets = JSON.parse(fs.readFileSync(userPresetPath, 'utf8'));
    let adjustedUserPresets = {};

    //Tag user presets appropiately
    Object.keys(userPresets).forEach(presetName => {
      if (!(presetName in guiSettings.presets))
        adjustedUserPresets[presetName] = { settings: userPresets[presetName] };
    });

    Object.assign(guiSettings.presets, adjustedUserPresets);
  }

  event.returnValue = JSON.stringify(guiSettings);
})
