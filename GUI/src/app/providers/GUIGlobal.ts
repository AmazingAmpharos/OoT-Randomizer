import { Injectable, HostBinding, EventEmitter, Output } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { ProgressWindow } from '../pages/generator/progressWindow/progressWindow.component';

import * as post from 'post-robot';

@Injectable()
export class GUIGlobal {

  //Globals for GUI HTML
  public generator_tabsVisibilityMap: Object = {};
  public generator_settingsVisibilityMap: Object = {};

  public generator_settingsMap: Object = {};
  public generator_customColorMap: Object = {};

  public generator_presets: Object = {};

  globalVars: Map<string, any>;
  electronEvents: Array<any> = [];

  @HostBinding('class.indigo-pink') materialStyleIndigo: boolean = true;

  @Output() globalEmitter: EventEmitter<object> = new EventEmitter();
  
  constructor(private http: HttpClient) {
    this.globalVars = new Map<string, any>([
      ["appReady", false],
      ["appType", null],
      ["electronAvailable", false],
      ["webSourceVersion", ""],
      ["webIsMasterVersion", false],
      ["generatorSettingsArray", []],
      ["generatorSettingsObj", {}],
      ["generatorCosmeticsArray", []],
      ["generatorCosmeticsObj", {}]
    ]);
  }

  globalInit(appType: string) {

    if (!appType)
      appType = "generator"; //Generator is the default

    console.log("APP Type:", appType);
    this.setGlobalVar("appType", appType);

    if ((<any>window).electronAvailable) { //Electron/Offline mode

      if ((<any>window).apiPythonSourceFound) {
        this.setGlobalVar("electronAvailable", true);
        console.log("Electron API available");
        console.log("Running on OS:", (<any>window).apiPlatform);

        this.createElectronEvents();
        this.electronInit();
      }
      else {
        console.error("Improper setup, exit GUI");
      }
    }
    else { //Online/Web mode
      console.log("Electron API not available, assume web mode");

      if (!(<any>window).pythonSourceVersion) {
        console.error("No python version defined, exit");
        return;
      }

      this.setGlobalVar("webSourceVersion", (<any>window).pythonSourceVersion);

      if ((<any>window).pythonSourceIsMasterVersion)
        this.setGlobalVar("webIsMasterVersion", (<any>window).pythonSourceIsMasterVersion);

      console.log("Web version: " + (<any>window).pythonSourceVersion + " ; master version:", this.getGlobalVar("webIsMasterVersion"));

      this.webInit();
    }
  }

  ngOnDestroy() {
    if ((<any>window).electronAvailable) {
      this.destroyElectronEvents();
    }
  }

  createElectronEvents() { //Electron only

    var self = this;

    let maximizedEvent = post.on('window-maximized', function (event) {
      let res = event.data;

      if (res == true)
        self.globalEmitter.emit({ name: "window_maximized" });
      else
        self.globalEmitter.emit({ name: "window_unmaximized" });
    });

    this.electronEvents.push(maximizedEvent);
  }

  destroyElectronEvents() {
    this.electronEvents.forEach(postRobotEvent => {
      postRobotEvent.cancel();
    });
  }

  electronInit() {
    this.electronLoadGeneratorGUISettings().then(() => {
      this.setGlobalVar("appReady", true);
      this.globalEmitter.emit({ name: "init_finished" });
    }).catch(err => {
      console.error("exit due error:", err);
    });
  }

  webInit() {
    this.webLoadGeneratorGUISettings().then(() => {
      this.setGlobalVar("appReady", true);
      this.globalEmitter.emit({ name: "init_finished" });
    }).catch(err => {
      console.error("exit due error:", err);
    });
  }

  setGlobalVar(key: string, value: any) {
    if (this.globalVars.has(key)) {
      this.globalVars.set(key, value);
    }
  }

  getGlobalVar(key: string) {

    if (this.globalVars.has(key))
      return this.globalVars.get(key);

    return "error";
  }

  copyToClipboard(content: string) {

    if (this.getGlobalVar('electronAvailable')) { //Electron
      post.send(window, 'copyToClipboard', { content: content }).then(event => {
        console.log('copied to clipboard');
      }).catch(err => {
        console.error(err);
      });
    }
    else { //Web
      let selBox = document.createElement('textarea');
      selBox.style.position = 'fixed';
      selBox.style.left = '0';
      selBox.style.top = '0';
      selBox.style.opacity = '0';
      selBox.value = content;

      document.body.appendChild(selBox);
      selBox.focus();
      selBox.select();
      document.execCommand('copy');

      document.body.removeChild(selBox);
    }
  }

  async browseForFile(fileTypes: any) { //Electron only

    if (!this.getGlobalVar('electronAvailable'))
      throw Error("electron_not_available");

    let event = await post.send(window, 'browseForFile', { fileTypes: fileTypes });
    let res = event.data;

    if (!res || res.length != 1 || !res[0] || res[0].length < 1)
      throw Error("dialog_cancelled");

    return res[0];
  }

  async browseForDirectory() { //Electron only

    if (!this.getGlobalVar('electronAvailable'))
      throw Error("electron_not_available");

    let event = await post.send(window, 'browseForDirectory');
    let res = event.data;

    if (!res || res.length != 1 || !res[0] || res[0].length < 1)
      throw Error("dialog_cancelled");

    return res[0];
  }

  async createAndOpenPath(path: string) { //Electron only

    if (!this.getGlobalVar('electronAvailable'))
      throw Error("electron_not_available");

    let event = await post.send(window, 'createAndOpenPath', path);
    let res = event.data;

    if (res == true)
      return true;
    else
      throw Error("path_not_opened");
  }

  minimizeWindow() { //Electron only

    if (!this.getGlobalVar('electronAvailable'))
      return;

    post.send(window, 'window-minimize').then(() => {
      console.log('window minimized');
    }).catch(err => {
      console.error(err);
    });
  }

  maximizeWindow() { //Electron only

    if (!this.getGlobalVar('electronAvailable'))
      return;

    post.send(window, 'window-maximize').then(() => {
      console.log('window maximize state updated');
    }).catch(err => {
      console.error(err);
    });
  }

  async isWindowMaximized() { //Electron only

    if (!this.getGlobalVar('electronAvailable'))
      throw Error("electron_not_available");

    try {
      let event = await post.send(window, 'window-is-maximized');
      let res = event.data;

      //console.log("window maximized state:", res);
      return res;
    }
    catch (err) {
      console.error(err);
      throw Error(err);
    }
  }

  closeWindow() { //Electron only

    if (!this.getGlobalVar('electronAvailable'))
      return;

    this.saveCurrentSettingsToFile();

    setTimeout(() => {

      post.send(window, 'window-close').then(() => {
        console.log('window closed');
      }).catch(err => {
        console.error(err);
      });
    });
  }

  async electronLoadGeneratorGUISettings() {

    var guiSettings = post.send(window, 'getGeneratorGUISettings');
    var lastUserSettings = post.send(window, 'getGeneratorGUILastUserSettings');

    try {
      var results = await Promise.all([guiSettings, lastUserSettings]);

      let res = JSON.parse(results[0].data);
      let userSettings = results[1].data;

      if (userSettings)
        userSettings = JSON.parse(userSettings);

      this.parseGeneratorGUISettings(res, userSettings);

    } catch (err) {
      console.error(err);
      throw Error(err);
    }
  }

  async webLoadGeneratorGUISettings() {

    var res = null;
    var userSettings = null;

    //Get generator settings
    if ((<any>window).webGeneratorSettingsMap) { //Master versions on the web pre-define a settings map to use before Angular will load
      res = (<any>window).webGeneratorSettingsMap;
      console.log("Settings map is available from the DOM");
    }
    else { //Dev versions on the web request a pre-built settings map from the server at runtime

      let url = (<any>window).location.protocol + "//" + (<any>window).location.host + "/angular/dev/" + this.getGlobalVar("webSourceVersion").replace(/ /g, "_") + "/utils/settings_list.json";
      console.log("Settings map is not available. Request it:", url);

      res = await this.http.get(url, { responseType: "json" }).toPromise();
    }

    //Get last user settings from browser cache for the appropriate app
    try {
      userSettings = localStorage.getItem(this.getGlobalVar("appType") == "generator" ? "generatorSettings_" + this.getGlobalVar("webSourceVersion") : "patcherSettings_" + this.getGlobalVar("webSourceVersion"));

    } catch (err) {
      console.error("Local storage not available");
    }

    if (userSettings && userSettings.length > 0)
      userSettings = JSON.parse(userSettings);

    //Get user presets if appType = generator
    if (this.getGlobalVar("appType") == "generator") {

      let userPresets = null;

      try {
        userPresets = localStorage.getItem("generatorPresets_" + this.getGlobalVar("webSourceVersion"));
      } catch { }

      if (userPresets && userPresets.length > 0) {

        userPresets = JSON.parse(userPresets);

        let adjustedUserPresets = {};

        //Tag user presets appropiately
        Object.keys(userPresets).forEach(presetName => {
          if (!(presetName in res.presets))
            adjustedUserPresets[presetName] = { settings: userPresets[presetName] };
        });

        Object.assign(res.presets, adjustedUserPresets);       
      }
    }

    this.parseGeneratorGUISettings(res, userSettings);
  }

  parseGeneratorGUISettings(guiSettings, userSettings) {

    const isRGBHex = /[0-9A-Fa-f]{6}/;

    //Intialize settings maps
    for (let tabIndex = 0; tabIndex < guiSettings.settingsArray.length; tabIndex++) {
      let tab = guiSettings.settingsArray[tabIndex];

      //Skip tabs that don't belong to this app and delete them from the guiSettings
      if ("app_type" in tab && tab.app_type && tab.app_type != this.getGlobalVar("appType")) {

        guiSettings.settingsArray.splice(tabIndex, 1);
        tabIndex--;

        let index = guiSettings.cosmeticsArray.findIndex(entry => entry.name == tab.name);
        if (index != -1)
          guiSettings.cosmeticsArray.splice(index, 1);

        delete guiSettings.settingsObj[tab.name];
        delete guiSettings.cosmeticsObj[tab.name];

        continue;
      }

      this.generator_tabsVisibilityMap[tab.name] = true;

      tab.sections.forEach(section => {
        section.settings.forEach(setting => {

          this.generator_settingsVisibilityMap[setting.name] = true;

          if (setting.type == "SearchBox" && userSettings && setting.name in userSettings) { //Special parsing for SearchBox data

            let valueArray = [];

            userSettings[setting.name].forEach(entry => {

              let optionEntry = setting.options.find(option => {
                if (option.name == entry)
                  return true;

                return false;
              });

              if (optionEntry)
                valueArray.push(optionEntry);
            });

            this.generator_settingsMap[setting.name] = valueArray;
          }
          else if (setting.type == "Combobox" && userSettings && setting.name in userSettings) { //Ensure combobox option exists before applying it (in case of outdated settings being loaded)

            if (section.is_colors && typeof (userSettings[setting.name]) == "string" && isRGBHex.test(userSettings[setting.name])) { //Custom Color is treated as an exception
              this.generator_settingsMap[setting.name] = userSettings[setting.name];
            }
            else {
              let optionEntry = setting.options.find(option => {
                if (option.name == userSettings[setting.name])
                  return true;

                return false;
              });

              this.generator_settingsMap[setting.name] = optionEntry ? userSettings[setting.name] : setting.default;
            }
          }
          else { //Everything else
            this.generator_settingsMap[setting.name] = userSettings && setting.name in userSettings ? userSettings[setting.name] : setting.default;
          }

          //Color section handling
          if (section.is_colors) {
            if (typeof (this.generator_settingsMap[setting.name]) == "string" && isRGBHex.test(this.generator_settingsMap[setting.name])) { //Resolve Custom Color
              this.generator_customColorMap[setting.name] = "#" + this.generator_settingsMap[setting.name];
              this.generator_settingsMap[setting.name] = "Custom Color";
            }
            else {
              this.generator_customColorMap[setting.name] = "";
            }
          }
        });
      });
    }

    //Add GUI only options
    this.generator_settingsMap["settings_string"] = userSettings && "settings_string" in userSettings ? userSettings["settings_string"] : "";
    this.generator_settingsVisibilityMap["settings_string"] = true;

    this.generator_settingsMap["patch_file"] = userSettings && "patch_file" in userSettings ? userSettings["patch_file"] : "";
    this.generator_settingsVisibilityMap["patch_file"] = true;

    this.generator_settingsMap["repatch_cosmetics"] = userSettings && "repatch_cosmetics" in userSettings ? userSettings["repatch_cosmetics"] : true;
    this.generator_settingsVisibilityMap["repatch_cosmetics"] = true;

    console.log("JSON Settings Data:", guiSettings);
    console.log("Last User Settings:", userSettings);
    console.log("Final Settings Map", this.generator_settingsMap);

    //Save settings after parsing them
    this.setGlobalVar('generatorSettingsArray', guiSettings.settingsArray);
    this.setGlobalVar('generatorSettingsObj', guiSettings.settingsObj);
    this.setGlobalVar('generatorCosmeticsArray', guiSettings.cosmeticsArray);
    this.setGlobalVar('generatorCosmeticsObj', guiSettings.cosmeticsObj);

    this.generator_presets = guiSettings.presets;
  }

  async versionCheck() { //Electron only

    if (!this.getGlobalVar('electronAvailable'))
      throw Error("electron_not_available");

    try {

      var event = await post.send(window, 'getCurrentSourceVersion');

      var res = event.data;
      var result = { hasUpdate: false, currentVersion: "", latestVersion: "" };

      if (res && res.length > 0) {

        console.log("Local:", res);
        result.currentVersion = res;

        this.globalEmitter.emit({ name: "local_version_checked", version: res });

        var remoteFile = await this.http.get("https://raw.githubusercontent.com/TestRunnerSRL/OoT-Randomizer/Dev/version.py", { responseType: "text" }).toPromise();

        let remoteVersion = remoteFile.substr(remoteFile.indexOf("'") + 1);
        remoteVersion = remoteVersion.substr(0, remoteVersion.indexOf("'"));

        console.log("Remote:", remoteVersion);
        result.latestVersion = remoteVersion;

        let currentSplit = res.replace('v', '').replace(' ', '.').split('.');
        let remoteSplit = remoteVersion.replace('v', '').replace(' ', '.').split('.');

        //Compare versions
        if (Number(remoteSplit[0]) > Number(currentSplit[0])) {
          result.hasUpdate = true;
        }
        else if (Number(remoteSplit[0]) == Number(currentSplit[0])) {
          if (Number(remoteSplit[1]) > Number(currentSplit[1])) {
            result.hasUpdate = true;
          }
          else if (Number(remoteSplit[1]) == Number(currentSplit[1])) {
            if (Number(remoteSplit[2]) > Number(currentSplit[2])) {
              result.hasUpdate = true;
            }
          }
        }

        return result;  
      }
      else {
        return result;
      }
    }
    catch (err) {
      console.error(err);
      throw Error(err);
    }
  }

  applySettingsObject(settingsObj) {

    if (!settingsObj)
      return;

    const isRGBHex = /[0-9A-Fa-f]{6}/;

    this.getGlobalVar('generatorSettingsArray').forEach(tab => {
      tab.sections.forEach(section => {
        section.settings.forEach(setting => {

          if (setting.name in settingsObj) {

            if (setting.type == "SearchBox") { //Special parsing for SearchBox data

              let valueArray = [];

              settingsObj[setting.name].forEach(entry => {

                let optionEntry = setting.options.find(option => {
                  if (option.name == entry)
                    return true;

                  return false;
                });

                if (optionEntry)
                  valueArray.push(optionEntry);
              });

              this.generator_settingsMap[setting.name] = valueArray;
            }
            else if (setting.type == "Combobox") { //Ensure combobox option exists before applying it (in case of outdated settings being loaded)

              let optionEntry = setting.options.find(option => {
                if (option.name == settingsObj[setting.name])
                  return true;

                return false;
              });

              if (optionEntry)
                this.generator_settingsMap[setting.name] = settingsObj[setting.name];
            }
            else { //Everything else            
              this.generator_settingsMap[setting.name] = settingsObj[setting.name];
            }

            //Color section handling
            if (section.is_colors) {

              if (typeof (settingsObj[setting.name]) == "string" && isRGBHex.test(settingsObj[setting.name])) { //Resolve Custom Color
                this.generator_customColorMap[setting.name] = "#" + settingsObj[setting.name];
                this.generator_settingsMap[setting.name] = "Custom Color";
              }
              else {
                this.generator_customColorMap[setting.name] = "";
              }
            }
          }
        });
      });
    });
  }

  applyDefaultSettings() {

    let cleanSettings = this.createSettingsFileObject(false, true, !this.getGlobalVar('electronAvailable'));

    this.getGlobalVar('generatorSettingsArray').forEach(tab => {
      tab.sections.forEach(section => {
        section.settings.forEach(setting => {

          if (setting.name in cleanSettings) {
            this.generator_settingsMap[setting.name] = setting.default; 
          }
        });
      });
    });
  }

  createSettingsFileObject(includeFromPatchFileSettings: boolean = true, includeSeedSettingsOnly: boolean = false, sanitizeForBrowserCache: boolean = false) {

    let settingsFile: any = {};

    Object.assign(settingsFile, this.generator_settingsMap);

    //Add in custom colors
    Object.keys(this.generator_customColorMap).forEach(colorSettingName => {
      if (this.generator_customColorMap[colorSettingName].length > 0 && settingsFile[colorSettingName] === "Custom Color") {
        settingsFile[colorSettingName] = this.generator_customColorMap[colorSettingName].substr(1);
      }
    });

    //Resolve search box entries (name only)
    this.getGlobalVar("generatorSettingsArray").forEach(tab => {

      tab.sections.forEach(section => {
        section.settings.forEach(setting => {

          if (setting.type == "SearchBox") {

            let valueArray = [];

            settingsFile[setting.name].forEach(entry => {
              valueArray.push(entry.name);
            });

            settingsFile[setting.name] = valueArray;
          }      
        });
      });
    });

    //Delete keys the python source doesn't need
    delete settingsFile["presets"];
    delete settingsFile["open_output_dir"];

    //Delete fromPatchFile keys if mode is fromSeed
    if (!includeFromPatchFileSettings) {
      delete settingsFile["patch_file"];
      delete settingsFile["repatch_cosmetics"];
    }

    //Delete keys not included in the seed
    if (includeSeedSettingsOnly) {
      delete settingsFile["patch_file"];
      delete settingsFile["repatch_cosmetics"];
      delete settingsFile["cosmetics_only"];
      delete settingsFile["distribution_file"];
      delete settingsFile["checked_version"];
      delete settingsFile["rom"];
      delete settingsFile["output_dir"];
      delete settingsFile["output_file"];
      delete settingsFile["count"];
      delete settingsFile["player_num"];
      delete settingsFile["create_cosmetics_log"];
      delete settingsFile["compress_rom"];
      delete settingsFile["settings_string"];

      //Delete Cosmetics keys
      this.getGlobalVar("generatorCosmeticsArray").forEach(tab => {
        tab.sections.forEach(section => {
          section.settings.forEach(setting => {
            delete settingsFile[setting.name];
          });
        });      
      });

      //Web only keys
      if (!this.getGlobalVar('electronAvailable')) {
        delete settingsFile["web_wad_file"];
        delete settingsFile["web_common_key_file"];
        delete settingsFile["web_common_key_string"];
        delete settingsFile["web_wad_channel_id"];
        delete settingsFile["web_wad_channel_title"];
        delete settingsFile["web_output_type"];
      }
    }

    //Delete keys the browser can't save (web only)
    if (sanitizeForBrowserCache) {

      if (settingsFile["rom"] && typeof (settingsFile["rom"]) == "object") //File objects can not be saved due browser sandbox
        delete settingsFile["rom"];

      if (settingsFile["patch_file"] && typeof (settingsFile["patch_file"]) == "object")
        delete settingsFile["patch_file"];

      if (settingsFile["distribution_file"] && typeof (settingsFile["distribution_file"]) == "object")
        delete settingsFile["distribution_file"];

      if (settingsFile["web_wad_file"] && typeof (settingsFile["web_wad_file"]) == "object")
        delete settingsFile["web_wad_file"];

      if (settingsFile["web_common_key_file"] && typeof (settingsFile["web_common_key_file"]) == "object")
        delete settingsFile["web_common_key_file"];
    }

    return settingsFile;
  }

  saveCurrentSettingsToFile() {

    if (this.getGlobalVar('electronAvailable')) { //Electron
      post.send(window, 'saveCurrentSettingsToFile', this.createSettingsFileObject()).then(event => {
        console.log("settings saved to file");
      }).catch(err => {
        console.error(err);
      });
    }
    else { //Web
      localStorage.setItem(this.getGlobalVar("appType") == "generator" ? "generatorSettings_" + this.getGlobalVar("webSourceVersion") : "patcherSettings_" + this.getGlobalVar("webSourceVersion"), JSON.stringify(this.createSettingsFileObject(true, false, true)));
    }
  }

  convertSettingsToString() {
    var self = this;

    return new Promise<string>(function (resolve, reject) {

      if (self.getGlobalVar('electronAvailable')) { //Electron

        post.send(window, 'convertSettingsToString', self.createSettingsFileObject(false, true)).then(event => {

          var listenerSuccess = post.once('convertSettingsToStringSuccess', function (event) {

            listenerError.cancel();

            let data = event.data;
            resolve(data);
          });

          var listenerError = post.once('convertSettingsToStringError', function (event) {

            listenerSuccess.cancel();

            let data = event.data;

            console.error("[convertSettingsToString] Python Error:", data);
            reject(data);
          });

        }).catch(err => {
          console.error("[convertSettingsToString] Post-Robot Error:", err);
          reject(err);
        });
      }
      else { //Web
        let url = (<any>window).location.protocol + "//" + (<any>window).location.host + "/settings/parse?version=" + (self.getGlobalVar("webIsMasterVersion") ? "" : "dev_") + self.getGlobalVar("webSourceVersion").replace(/ /g, "_");
        console.log("Request string from:", url);

        self.http.post(url, JSON.stringify(self.createSettingsFileObject(false, true, true)), { responseType: "text", headers: { "Content-Type": "application/json" } }).toPromise().then(res => {
          resolve(res);
        }).catch(err => {
          console.error("[convertSettingsToString] Web Error:", err);
          reject(err);
        });
      }
    });
  }

  convertStringToSettings(settingsString: string) {
    var self = this;

    return new Promise(function (resolve, reject) {

      if (self.getGlobalVar('electronAvailable')) { //Electron

        post.send(window, 'convertStringToSettings', settingsString).then(event => {

          var listenerSuccess = post.once('convertStringToSettingsSuccess', function (event) {

            listenerError.cancel();

            let data = event.data;
            resolve(data);
          });

          var listenerError = post.once('convertStringToSettingsError', function (event) {

            listenerSuccess.cancel();

            let data = event.data;

            console.error("[convertStringToSettings] Python Error:", data);
            reject(data);
          });

        }).catch(err => {
          console.error("[convertStringToSettings] Post-Robot Error:", err);
          reject(err);
        });
      }
      else { //Web
        let url = (<any>window).location.protocol + "//" + (<any>window).location.host + "/settings/get?version=" + (self.getGlobalVar("webIsMasterVersion") ? "" : "dev_") + self.getGlobalVar("webSourceVersion").replace(/ /g, "_") + "&settingsString=" + settingsString;
        console.log("Request settings from:", url);

        self.http.get(url, { responseType: "text" }).toPromise().then(res => {

          let settingsObj = self.convertRawSettingsToObj(res);
          resolve(settingsObj);

        }).catch(err => {
          console.error("[convertStringToSettings] Web Error:", err);
          reject(err);
        });
      }
    });
  }

  convertRawSettingsToObj(rawSettings: string) { //Web only

    var settingsResult = {};

    var lines = rawSettings.split("\n");
    var lineSettingElement = "";

    lines.forEach(line => {

      if (line.trim().length == 0 || line.includes("Online Patcher")) //Remove title line
        return;

      let lineValue: any = "";

      if (line.includes(":")) { //setting with value
        lineSettingElement = line.trim().substr(0, line.trim().indexOf(":"));
        lineValue = line.trim().substr(line.trim().indexOf(":") + 1);
        lineValue = lineValue.trim();
      }
      else {
        lineValue = line.trim(); //just option without setting
      }

      if (lineValue.length < 1)
        return;

      if (lineSettingElement in settingsResult) { //Exception for listboxes/arrays

        if (typeof (settingsResult[lineSettingElement]) != "object" || !Array.isArray(settingsResult[lineSettingElement])) {
          //Transform value into array
          let originalValue = settingsResult[lineSettingElement];

          settingsResult[lineSettingElement] = [];
          settingsResult[lineSettingElement].push(originalValue);
        }

        settingsResult[lineSettingElement].push(Number(parseInt(lineValue)) != lineValue ? lineValue : parseInt(lineValue));
      }
      else {

        if (lineValue == "True") //Checkbox True/False handling
          settingsResult[lineSettingElement] = true;
        else if (lineValue == "False")
          settingsResult[lineSettingElement] = false;
        else //String/Numbers/Array first value
          settingsResult[lineSettingElement] = Number(parseInt(lineValue)) != lineValue ? lineValue : parseInt(lineValue);

        if (lineSettingElement == "disabled_locations" || lineSettingElement == "allowed_tricks") {
          //DIRTY: Transform value into array for both listboxes or the rando doesn't understand single disabled locations/tricks
          let originalValue = settingsResult[lineSettingElement];

          settingsResult[lineSettingElement] = [];
          settingsResult[lineSettingElement].push(originalValue);
        }
      }
    });

    return settingsResult;
  }

  createPresetFileObject() {

    let presetsFile: any = {};

    //Create presets object
    Object.keys(this.generator_presets).forEach(presetKey => {
      let preset = this.generator_presets[presetKey];

      if (!("isNewPreset" in preset) && !("isDefaultPreset" in preset) && !("isProtectedPreset" in preset) && ("settings" in preset) && typeof (preset.settings) == "object" && Object.keys(preset.settings).length > 0) {
        //console.log("store " + presetKey, preset.settings);
        presetsFile[presetKey] = preset.settings;
      }
    });

    return presetsFile;
  }

  saveCurrentPresetsToFile() {

    if (this.getGlobalVar('electronAvailable')) { //Electron
      post.send(window, 'saveCurrentPresetsToFile', JSON.stringify(this.createPresetFileObject(), null, 4)).then(event => {
        console.log("presets saved to file");
      }).catch(err => {
        console.error(err);
      });
    }
    else { //Web
      if (this.getGlobalVar("appType") == "generator") //Generator only
        localStorage.setItem("generatorPresets_" + this.getGlobalVar("webSourceVersion"), JSON.stringify(this.createPresetFileObject(), null, 4));
    }
  }

  generateSeedElectron(progressWindowRef: ProgressWindow, fromPatchFile: boolean = false, useStaticSeed: string = "") { //Electron only
    var self = this;

    return new Promise(function (resolve, reject) {

      post.send(window, 'generateSeed', { settingsFile: self.createSettingsFileObject(fromPatchFile), staticSeed: useStaticSeed }).then(event => {

        var listenerProgress = post.on('generateSeedProgress', function (event) {

          let data = event.data;

          //console.log("progress report", data);

          if (progressWindowRef) {
            progressWindowRef.currentGenerationIndex = data.generationIndex;
            progressWindowRef.progressPercentageCurrent = data.progressCurrent;
            progressWindowRef.progressPercentageTotal = data.progressTotal;
            progressWindowRef.progressMessage = data.message;
            progressWindowRef.refreshLayout();
          }
        });

        var listenerSuccess = post.once('generateSeedSuccess', function (event) {

          listenerProgress.cancel();
          listenerCancel.cancel();
          listenerError.cancel();

          let data = event.data;
          resolve();
        });

        var listenerError = post.once('generateSeedError', function (event) {

          listenerProgress.cancel();
          listenerCancel.cancel();
          listenerSuccess.cancel();

          let data = event.data;

          console.error("[generateSeedElectron] Python Error:", data);
          reject(data);
        });

        var listenerCancel = post.once('generateSeedCancelled', function (event) {

          listenerProgress.cancel();
          listenerSuccess.cancel();
          listenerError.cancel();

          reject({ short: "Generation cancelled.", long: "Generation cancelled." });
        });
      }).catch(err => {
        console.error("[generateSeedElectron] Post-Robot Error:", err);
        reject({ short: err, long: err });
      });
    });
  }

  async cancelGenerateSeedElectron() { //Electron only

    if (!this.getGlobalVar('electronAvailable'))
      throw Error("electron_not_available");

    try {

      let event = await post.send(window, 'cancelGenerateSeed');
      let data = event.data;

      if (data == true)
        return;
      else
        throw Error("cancel_failed");
    }
    catch (err) {
      console.error("[cancelGenerateSeedElectron] Couldn't cancel due Post-Robot Error:", err);
      throw Error(err);
    }
  }

  generateSeedWeb(raceSeed: boolean = false, useStaticSeed: string = "") { //Web only
    var self = this;

    return new Promise<any>(function (resolve, reject) {

      let settingsFile = self.createSettingsFileObject(false, false, true);

      if (raceSeed) {
        useStaticSeed = ""; //Static seeds aren't allowed in race mode
        settingsFile["create_spoiler"] = true; //Force spoiler mode to on
        settingsFile["encrypt"] = true;
      }
      else {
        delete settingsFile["encrypt"];
      }

      if (useStaticSeed) {
        console.log("Use Static Seed:", useStaticSeed);
        settingsFile["seed"] = useStaticSeed;
      }
      else {
        delete settingsFile["seed"];
      }

      console.log(settingsFile);
      console.log("Race Seed:", raceSeed);

      //Request Seed Generation
      let url = (<any>window).location.protocol + "//" + (<any>window).location.host + "/seed/create?version=" + (self.getGlobalVar("webIsMasterVersion") ? "" : "dev_") + self.getGlobalVar("webSourceVersion").replace(/ /g, "_");
      console.log("Request seed id from:", url);

      self.http.post(url, JSON.stringify(settingsFile), { responseType: "text", headers: { "Content-Type": "application/json" } }).toPromise().then(res => {
        resolve(res);
      }).catch(err => {
        console.error("[generateSeedWeb] Web Error:", err);
        reject(err);
      });
    });
  }

  patchROMWeb() { //Web only
 
    let settingsFile = this.createSettingsFileObject();

    if (typeof (<any>window).patchROM === "function") //Try to call patchROM function on the DOM
      (<any>window).patchROM(5, settingsFile); //Patch Version 5
    else
      console.error("[patchROMWeb] Patcher not available!");
  }
}
