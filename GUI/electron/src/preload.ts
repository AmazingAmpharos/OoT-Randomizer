import * as electron from 'electron';
import * as os from "os";
import * as fs from 'fs';
import * as path from 'path';

import * as post from 'post-robot';

const generator = electron.remote.require(path.join(__dirname, '../src/modules/generator.js'));
const commander = electron.remote.getGlobal("commandLineArgs");

var testMode = commander.release || electron.remote.app.isPackaged ? false : true;
console.log("Test Mode:", testMode);

var platform = os.platform();
console.log("Platform:", platform);

var pythonPath = commander.python ? commander.python : platform == "win32" ? "py" : "python3";
var pythonSourcePath = path.normalize(electron.remote.app.isPackaged ? electron.remote.app.getAppPath() + "/python/" : electron.remote.app.getAppPath() + "/../");
var pythonGeneratorPath = pythonSourcePath + "OoTRandomizer.py";

console.log("Python Executable Path:", pythonPath);
console.log("Python Source Path:", pythonGeneratorPath);

//Enable API in client window
electron.webFrame.executeJavaScript('window.electronAvailable = true;');
electron.webFrame.executeJavaScript('window.apiTestMode = ' + testMode + ';');
electron.webFrame.executeJavaScript('window.apiPlatform = "' + platform + '";');

//ELECTRON EVENTS
electron.remote.getCurrentWindow().on('maximize', () => {
  post.send(window, 'window-maximized', true);
});
electron.remote.getCurrentWindow().on('enter-full-screen', () => { //macOS exclusive
  post.send(window, 'window-maximized', true);
});
electron.remote.getCurrentWindow().on('enter-html-full-screen', () => {
  post.send(window, 'window-maximized', true);
});

electron.remote.getCurrentWindow().on('unmaximize', () => {
  post.send(window, 'window-maximized', false);
});
electron.remote.getCurrentWindow().on('leave-full-screen', () => {
  post.send(window, 'window-maximized', false);
});
electron.remote.getCurrentWindow().on('leave-html-full-screen', () => {
  post.send(window, 'window-maximized', false);
});


//FUNCTIONS
function dumpSettingsToFile(settingsObj) {
  settingsObj["check_version"] = true;    
  fs.writeFileSync(pythonSourcePath + "settings.sav", JSON.stringify(settingsObj, null, 4));
}

function dumpPresetsToFile(presetsString: string) {
  fs.writeFileSync(pythonSourcePath + "presets.sav", presetsString);
}

function displayPythonErrorAndExit(notPython3: boolean = false) {

  setTimeout(() => {

    if (notPython3)
      alert("The Python version used to run the GUI is not supported! Please ensure you have Python 3.6 or higher installed. You can specify the path to python using the 'python <path>' command line switch!");
    else
      alert("Please ensure you have Python 3.6 or higher installed before running the GUI. You can specify the path to python using the 'python <path>' command line switch!");

    electron.remote.app.quit();
  }, 500);
}

function readSettingsFromFile() {

  let path = pythonSourcePath + "settings.sav";

  if (fs.existsSync(path))
    return fs.readFileSync(path, 'utf8');
  else
    return false;
}

//POST ROBOT
post.on('getCurrentSourceVersion', function (event) {

  let versionFilePath = pythonSourcePath + "version.py"; //Read version.py from the python source

  if (fs.existsSync(versionFilePath)) {
    let versionString = fs.readFileSync(versionFilePath, 'utf8');
    versionString = versionString.substr(versionString.indexOf("'") + 1);
   
    return versionString.substr(0, versionString.indexOf("'"));
  }
  else {
    return false;
  }
});

post.on('getGeneratorGUISettings', function (event) {

  return electron.ipcRenderer.sendSync('getGeneratorGUISettings');
});

post.on('getGeneratorGUILastUserSettings', function (event) {

  return readSettingsFromFile();
});

post.on('copyToClipboard', function (event) {

  let data = event.data;

  if (!data || typeof (data) != "object" || Object.keys(data).length != 1 || !data["content"] || typeof (data["content"]) != "string" || data["content"].length < 1)
    return false;

  electron.remote.clipboard.writeText(data.content);

  return true;
});

post.on('browseForFile', function (event) {

  let data = event.data;

  if (!data || typeof (data) != "object" || Object.keys(data).length != 1 || !data["fileTypes"] || typeof (data["fileTypes"]) != "object")
    return false;

  return electron.remote.dialog.showOpenDialog({ filters: data.fileTypes, properties: ["openFile", "treatPackageAsDirectory"]});
});


post.on('browseForDirectory', function (event) {
  return electron.remote.dialog.showOpenDialog({ properties: ["openDirectory", "createDirectory", "treatPackageAsDirectory"] });
});

post.on('createAndOpenPath', function (event) {

  let data = event.data;

  //Use python dir if not specified otherwise
  if (!data || typeof (data) != "string" || data.length < 1) {
    data = pythonSourcePath;
  }
  else {
    if (!path.isAbsolute(data))
      data = pythonSourcePath + data;
  }

  if (fs.existsSync(data)) {
    return electron.remote.shell.openItem(data);
  }
  else {
    fs.mkdirSync(data);
    return electron.remote.shell.openItem(data);
  }
});

post.on('window-minimize', function (event) {
  electron.remote.getCurrentWindow().minimize();
});

post.on('window-maximize', function (event) {

  let currentWindow = electron.remote.getCurrentWindow();

  if (currentWindow.isMaximized()) {
    currentWindow.unmaximize();
  }
  else {
    currentWindow.maximize();
  }
});

post.on('window-is-maximized', function (event) {
  return electron.remote.getCurrentWindow().isMaximized();
});

post.on('window-close', function (event) {

  //Only close the window on macOS, on every other OS exit immediately
  if (os.platform() == "darwin") {
    electron.remote.getCurrentWindow().close();
  }
  else {
    electron.remote.app.quit();
  }
});

post.on('saveCurrentSettingsToFile', function (event) {

  let data = event.data;

  if (!data || typeof (data) != "object" || Object.keys(data).length < 1)
    return false;

  //Write settings obj to settings.sav
  dumpSettingsToFile(data);
});

post.on('convertSettingsToString', function (event) {

  let data = event.data;

  if (!data || typeof (data) != "object" || Object.keys(data).length < 1)
    return false;

  //Write settings obj to settings.sav
  dumpSettingsToFile(data);

  //console.log("generate string with settings obj", data);

  generator.parseSettings(pythonPath, pythonGeneratorPath).then(res => {
    //console.log('[Preload] Success');

    post.send(window, 'convertSettingsToStringSuccess', res);
  }).catch((err) => {

    if (err.includes("ImportError: No module named tkinter")) {
      displayPythonErrorAndExit(true);
    }

    post.send(window, 'convertSettingsToStringError', err);
  });

  return true;
});

post.on('convertStringToSettings', function (event) {

  let data = event.data;

  if (!data || typeof (data) != "string" || data.length < 1)
    return false;

  //console.log("get settings from string", data);

  generator.getSettings(pythonPath, pythonGeneratorPath, data).then(res => {
    //console.log('[Preload] Success');

    post.send(window, 'convertStringToSettingsSuccess', res);
  }).catch((err) => {

    if (err.includes("ImportError: No module named tkinter")) {
      displayPythonErrorAndExit(true);
    }

    post.send(window, 'convertStringToSettingsError', err);
  });

  return true;
});

post.on('saveCurrentPresetsToFile', function (event) {

  let data = event.data;

  if (!data || typeof (data) != "string" || data.length < 1)
    return false;

  //Write file contents to presets.sav
  dumpPresetsToFile(data);

  //console.log("presets saved to .sav");
});

post.on('generateSeed', function (event) {

  let data = event.data;

  if (!data || typeof (data) != "object" || Object.keys(data).length != 2 || !("settingsFile" in data) || !("staticSeed" in data))
    return false;

  let settingsFile = data.settingsFile;

  if (!settingsFile || typeof (settingsFile) != "object" || Object.keys(settingsFile).length < 1)
    return false;

  //Write settings obj to settings.sav
  dumpSettingsToFile(settingsFile);

  //console.log("generate seed with settings:", data);

  generator.romBuilding(pythonPath, pythonGeneratorPath, data).then(res => {
    //console.log('[Preload] Success');
    post.send(window, 'generateSeedSuccess', res);
  }).catch((err) => {

    if (err.long.includes("ImportError: No module named tkinter")) {
      displayPythonErrorAndExit(true);
    }

    if (err.short == "user_cancelled")
      post.send(window, 'generateSeedCancelled'); 
    else
      post.send(window, 'generateSeedError', err);
  });

  return true;
});

post.on('cancelGenerateSeed', function (event) {

  if (generator.cancelRomBuilding())
    return true;

  return false;
});

//GENERATOR EVENTS
generator.on("patchJobProgress", status => {
  //console.log("Patch job reports in at " + status.progress + "%! Message: " + status.message);
  post.send(window, 'generateSeedProgress', status);
});


//STARTUP
//Test if we are in the proper path, else exit
if (fs.existsSync(pythonGeneratorPath)) {
  electron.webFrame.executeJavaScript('window.apiPythonSourceFound = true;');
}
else {
  alert("The GUI is not placed in the correct location...");
  electron.remote.app.quit();
}

//Test if python executable exists and can be called
generator.testPythonPath(pythonPath).then(() => {
  console.log("Python executable confirmed working");
}).catch(err => {
  console.error(err);
  displayPythonErrorAndExit();
});
