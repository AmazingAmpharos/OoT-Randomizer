import { app, BrowserWindow, shell, session, ipcMain, globalShortcut } from "electron";
import * as os from "os";
import * as fs from "fs";
import * as path from "path";
import * as url from "url";

import * as windowStateKeeper from "electron-window-state";
import * as commander from 'commander';

const settingsParser = require(path.join(__dirname, 'modules/settingsParser'));
settingsParser.generate();

var win: BrowserWindow;
var isRelease: boolean = false;

function createApp() {

  //Parse command line
  commander
    .option('p, python <path>', 'Path to your python executable')
    .option('r, release', 'Runs electron in release mode')
    .parse(process.argv);

  global["commandLineArgs"] = commander;
  isRelease = commander.release;

  //Load the previous window state with fallback to defaults
  let mainWindowState = windowStateKeeper({
    defaultWidth: 960,
    defaultHeight: 930
  });

  let browserOptions = { icon: path.join(__dirname, 'assets/icon/png/64x64.png'), title: 'OoT Randomizer GUI', opacity: 1.00, backgroundColor: '#000000', minWidth: 880, minHeight: 680, width: mainWindowState.width, height: mainWindowState.height, x: mainWindowState.x, y: mainWindowState.y, fullscreen: false, fullscreenable: false, show: false, webPreferences: { nodeIntegration: false, contextIsolation: true, webviewTag: false, preload: path.join(__dirname, 'preload.js') } };

  //macOS uses titleBarStyle
  if (os.platform() == "darwin")
    browserOptions["titleBarStyle"] = 'hiddenInset';
  else
    browserOptions["frame"] = false;

  win = new BrowserWindow(browserOptions);

  //WindowStateKeeper will automatically persist window state changes to file
  mainWindowState.manage(win);

  //Run Content Security Policy
  manageCSP();

  if (!isRelease) {
    win.loadURL("http://localhost:4200/"); //Dev server
  }
  else { //Load release dist
    win.loadURL(
      url.format({
        pathname: path.join(__dirname, `/../../dist/ootr-electron-gui/index.html`),
        protocol: "file:",
        slashes: true
      })
    );
  }

  win.once('ready-to-show', () => {
    win.show();

    if (!isRelease) //Open dev tools automatically if dev mode
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

//Limit navigation to safe URLs and defer unsafe popups to system browser
app.on('web-contents-created', (event, contents) => {
  contents.on('will-navigate', (event, navigationUrl) => {
    const parsedUrl = new URL(navigationUrl);

    console.log("Navigation attempt to:", parsedUrl.origin);

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

    console.log("New window creation attempt:", parsedUrl.origin);

    //Whitelist for dev server in dev mode
    if (!isRelease) {
      if (parsedUrl.origin === 'http://localhost:4200') {
        return;
      }
    }
        
    event.preventDefault();

    console.log("Deferred to system browser");

    shell.openExternal(navigationUrl);
  });
});

//CSP
function manageCSP() {

  session.defaultSession.webRequest.onHeadersReceived((details, callback) => {
    callback({
      responseHeaders: {
        ...details.responseHeaders,
        'Content-Security-Policy': ['default-src \'self\' *.gstatic.com; img-src \'self\' data: *; style-src \'self\' \'unsafe-inline\' *.googleapis.com; script-src \'self\' \'unsafe-eval\' *.googleapis.com; connect-src \'self\' *.githubusercontent.com ws: localhost:4200*']
      }
    })
  });

}

//IPC
ipcMain.on('getGeneratorGUISettings', (event, arg) => {

  let guiSettings = settingsParser.getSettingsData();

  //Add static presets
  guiSettings.presets = {
    "[New Preset]": { isNewPreset: true },
    "Default": { isDefaultPreset: true }
  };

  //Load built in presets
  let builtInPresetsPath = path.join(__dirname, 'utils/presets.json');

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
  let userPresetPath = path.normalize(app.getAppPath() + "/../presets.sav");

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
