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
      ["apiAvailable", false],
      ["generatorSettingsArray", []],
      ["generatorSettingsObj", {}],
      ["generatorCosmeticsArray", []],
      ["generatorCosmeticsObj", {}]
    ]);

    this.globalInit();
  }

  globalInit() {

    if ((<any>window).apiAvailable) {

      if ((<any>window).apiPythonSourceFound) {
        this.setGlobalVar("apiAvailable", true);
        console.log("Electron API available!");
        console.log("Running on OS:", (<any>window).apiPlatform);

        this.createElectronEvents();
        this.electronInit();
      }
      else {
        console.log("The GUI is not used in the offline context!");
      }
    }
    else {
      console.error("Could not load electron API!");
      alert("Electron could not be intialized or the app was launched outside the electron context, the app won't work correctly!");
    }
  }

  ngOnDestroy() {
    this.destroyElectronEvents();
  }

  createElectronEvents() {

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
    this.loadGeneratorGUISettings().then(() => {
      this.setGlobalVar("appReady", true);
      this.globalEmitter.emit({ name: "init_finished" });
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
    post.send(window, 'copyToClipboard', { content: content }).then(event => {
      console.log('copied');
    }).catch(err => {
      console.error(err);
    });
  }

  async browseForFile(fileTypes: any) {

    let event = await post.send(window, 'browseForFile', { fileTypes: fileTypes });
    let res = event.data;

    if (!res || res.length != 1 || !res[0] || res[0].length < 1)
      throw Error("dialog_cancelled");

    return res[0];
  }

  async browseForDirectory() {

    let event = await post.send(window, 'browseForDirectory');
    let res = event.data;

    if (!res || res.length != 1 || !res[0] || res[0].length < 1)
      throw Error("dialog_cancelled");

    return res[0];
  }

  async createAndOpenPath(path: string) {

    let event = await post.send(window, 'createAndOpenPath', path);
    let res = event.data;

    if (res == true)
      return true;
    else
      throw Error("path_not_opened");
  }

  minimizeWindow() {

    if (!this.getGlobalVar('apiAvailable'))
      return;

    post.send(window, 'window-minimize').then(() => {
      console.log('minimized');
    }).catch(err => {
      console.error(err);
    });
  }

  maximizeWindow() {

    if (!this.getGlobalVar('apiAvailable'))
      return;

    post.send(window, 'window-maximize').then(() => {
      console.log('maximize state updated');
    }).catch(err => {
      console.error(err);
    });
  }

  async isWindowMaximized() {

    if (!this.getGlobalVar('apiAvailable')) {
        throw Error("api_not_available");
    }

    try {
      let event = await post.send(window, 'window-is-maximized');
      let res = event.data;

      console.log("window maximized state:", res);
      return res;
    }
    catch (err) {
      console.error(err);
      throw Error(err);
    }
  }

  closeWindow() {

    if (!this.getGlobalVar('apiAvailable'))
      return;

    this.saveCurrentSettingsToFile();

    setTimeout(() => {

      post.send(window, 'window-close').then(() => {
        console.log('closed');
      }).catch(err => {
        console.error(err);
      });
    });
  }

  async loadGeneratorGUISettings() {

    var guiSettings = post.send(window, 'getGeneratorGUISettings');
    var lastUserSettings = post.send(window, 'getGeneratorGUILastUserSettings');

    try {
      var results = await Promise.all([guiSettings, lastUserSettings]);

      let res = JSON.parse(results[0].data);
      let userSettings = results[1].data;

      if (userSettings)
        userSettings = JSON.parse(userSettings);

      //console.log(res);
      console.log("userSettings", userSettings);

      this.setGlobalVar('generatorSettingsArray', res.settingsArray);
      this.setGlobalVar('generatorSettingsObj', res.settingsObj);
      this.setGlobalVar('generatorCosmeticsArray', res.cosmeticsArray);
      this.setGlobalVar('generatorCosmeticsObj', res.cosmeticsObj);

      this.generator_presets = res.presets;

      var isRGBHex = /[0-9A-Fa-f]{6}/g;

      //Intialize settings maps
      res.settingsArray.forEach(tab => {

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

              console.log(setting.name, valueArray);

              this.generator_settingsMap[setting.name] = valueArray;
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
      });

      //Add GUI only options
      this.generator_settingsMap["settings_string"] = userSettings && "settings_string" in userSettings ? userSettings["settings_string"] : "";
      this.generator_settingsVisibilityMap["settings_string"] = true;

      this.generator_settingsMap["patch_file"] = userSettings && "patch_file" in userSettings ? userSettings["patch_file"] : "";
      this.generator_settingsVisibilityMap["patch_file"] = true;

      this.generator_settingsMap["repatch_cosmetics"] = userSettings && "repatch_cosmetics" in userSettings ? userSettings["repatch_cosmetics"] : false;
      this.generator_settingsVisibilityMap["repatch_cosmetics"] = true;

      console.log(this.generator_settingsMap);

    } catch (err) {
      console.error(err);
      throw Error(err);
    }
  }

  async versionCheck() {

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

    var isRGBHex = /[0-9A-Fa-f]{6}/g;

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
            else { //Everything else            
              this.generator_settingsMap[setting.name] = settingsObj[setting.name];
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
          }
        });
      });
    });
  }

  applyDefaultSettings() {

    let cleanSettings = this.createSettingsFileObject(false, true);

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

  createSettingsFileObject(includeFromPatchFileSettings: boolean = true, sanitizeForPreset: boolean = false) {

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

    //Keys not saved in presets
    if (sanitizeForPreset) {
      delete settingsFile["cosmetics_only"];
      delete settingsFile["distribution_file"];
      delete settingsFile["checked_version"];
      delete settingsFile["rom"];
      delete settingsFile["output_dir"];
      delete settingsFile["output_file"];
      delete settingsFile["count"];
      delete settingsFile["world_count"];
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
    }

    return settingsFile;
  }

  saveCurrentSettingsToFile() {
    post.send(window, 'saveCurrentSettingsToFile', this.createSettingsFileObject()).then(event => {
      console.log("success");
    }).catch(err => {
      console.error(err);
    });
  }

  convertSettingsToString() {
    var self = this;

    return new Promise<string>(function (resolve, reject) {

      post.send(window, 'convertSettingsToString', self.createSettingsFileObject()).then(event => {

        console.log("returned, wait for success");

        var listenerSuccess = post.once('convertSettingsToStringSuccess', function (event) {

          listenerError.cancel();

          let data = event.data;

          console.log("success");

          resolve(data);
        });

        var listenerError = post.once('convertSettingsToStringError', function (event) {

          listenerSuccess.cancel();

          let data = event.data;

          console.log("error", data);

          reject(data);
        });

      }).catch(err => {
        console.error(err);
        reject(err);
      });
    });
  }

  convertStringToSettings(settingsString: string) {
    var self = this;

    return new Promise(function (resolve, reject) {

      post.send(window, 'convertStringToSettings', settingsString).then(event => {

        console.log("returned, wait for success");

        var listenerSuccess = post.once('convertStringToSettingsSuccess', function (event) {

          listenerError.cancel();

          let data = event.data;

          console.log("success getting settings");

          resolve(data);
        });

        var listenerError = post.once('convertStringToSettingsError', function (event) {

          listenerSuccess.cancel();

          let data = event.data;

          console.log("error", data);

          reject(data);
        });

      }).catch(err => {
        console.error(err);
        reject(err);
      });
    });
  }

  createPresetFileObject() {

    let presetsFile: any = {};

    //Create presets object
    Object.keys(this.generator_presets).forEach(presetKey => {
      let preset = this.generator_presets[presetKey];

      if (!("isNewPreset" in preset) && !("isDefaultPreset" in preset) && !("isProtectedPreset" in preset) && ("settings" in preset) && typeof (preset.settings) == "object" && Object.keys(preset.settings).length > 0) {
        console.log("store " + presetKey, preset.settings);
        presetsFile[presetKey] = preset.settings;
      }
    });

    return presetsFile;
  }

  saveCurrentPresetsToFile() {
    post.send(window, 'saveCurrentPresetsToFile', JSON.stringify(this.createPresetFileObject(), null, 4)).then(event => {
      console.log("success");
    }).catch(err => {
      console.error(err);
    });
  }

  generateSeed(progressWindowRef: ProgressWindow, fromPatchFile: boolean = false, useStaticSeed: string = "") {
    var self = this;

    return new Promise(function (resolve, reject) {

      post.send(window, 'generateSeed', { settingsFile: self.createSettingsFileObject(fromPatchFile), staticSeed: useStaticSeed }).then(event => {

        console.log("returned, start progress window");

        var listenerProgress = post.on('generateSeedProgress', function (event) {

          let data = event.data;

          console.log("progress report", data);

          if (progressWindowRef) {
            progressWindowRef.progressPercentage = data.progress;
            progressWindowRef.progressMessage = data.message;
            progressWindowRef.refreshLayout();
          }
        });

        var listenerSuccess = post.once('generateSeedSuccess', function (event) {

          listenerProgress.cancel();
          listenerCancel.cancel();
          listenerError.cancel();

          let data = event.data;

          console.log("success", data);

          resolve();
        });

        var listenerError = post.once('generateSeedError', function (event) {

          listenerProgress.cancel();
          listenerCancel.cancel();
          listenerSuccess.cancel();

          let data = event.data;

          console.log("error", data);

          reject(data);
        });

        var listenerCancel = post.once('generateSeedCancelled', function (event) {

          listenerProgress.cancel();
          listenerSuccess.cancel();
          listenerError.cancel();

          console.log("user cancelled");

          reject("Generation cancelled.");
        });
      }).catch(err => {
        console.error(err);
        reject(err);
      });
    });
  }

  async cancelGenerateSeed() {

    try {

      let event = await post.send(window, 'cancelGenerateSeed');
      let data = event.data;

      if (data == true)
        return;
      else
        throw Error("cancel_failed");
    }
    catch (err) {
      console.error("couldn't cancel due post error", err);
      throw Error(err);
    }
  }
}
