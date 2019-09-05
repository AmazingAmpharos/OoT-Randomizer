import { Component, OnInit, ChangeDetectionStrategy, ChangeDetectorRef, ViewChild } from '@angular/core';

import { OverlayContainer } from '@angular/cdk/overlay';

import { GUIGlobal } from '../../providers/GUIGlobal';
import { MatGridList, MatGridTile } from '@angular/material';
import { NbTabsetComponent } from '@nebular/theme/components/tabset/tabset.component';
import { NbSelectComponent } from '@nebular/theme/components/select/select.component';
import { NbDialogService } from '@nebular/theme';
import { ColorPickerModule } from 'ngx-color-picker';
import { ngfModule, ngf } from "angular-file";

import { GUITooltip } from './guiTooltip/guiTooltip.component';
import { ProgressWindow } from './progressWindow/progressWindow.component';
import { DialogWindow } from './dialogWindow/dialogWindow.component';
import { ErrorDetailsWindow } from './errorDetailsWindow/errorDetailsWindow.component';
import { ConfirmationWindow } from './confirmationWindow/confirmationWindow.component';
import { TextInputWindow } from './textInputWindow/textInputWindow.component';

@Component({
  selector: 'app-generator',
  styleUrls: ['./generator.component.scss'],
  templateUrl: './generator.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class GeneratorComponent implements OnInit {

  tooltipComponent = GUITooltip;

  @ViewChild('refTabSet') tabSet: NbTabsetComponent;
  @ViewChild('refTabFooter') tabSetFooter: NbTabsetComponent;
  activeTab: string = "";
  activeFooterTab: string = "";
  settingsLocked: boolean = false;

  //Busy Spinners
  generatorBusy: boolean = true;
  settingsBusy: boolean = false;
  settingsBusySaveOnly: boolean = true;

  //For KeyValue pipe
  presetKeyOrder = (a, b) => { //SYSTEM PRESETS > BUILT-IN PRESETS > USER PRESETS

    if ("isNewPreset" in a.value) {
      return -1;
    }
    else if ("isNewPreset" in b.value) {
      return 1;
    }
    else if ("isDefaultPreset" in a.value) {
      return -1;
    }
    else if ("isDefaultPreset" in b.value) {
      return 1;
    }
    else if ("isProtectedPreset" in a.value) {
      return -1;
    }
    else if ("isProtectedPreset" in b.value) {
      return 1;
    }
    else
      return 1;
  };

  //Local (non persistent) Variables
  seedString: string = "";
  generateSeedButtonEnabled: boolean = true;

  constructor(private overlayContainer: OverlayContainer, private cd: ChangeDetectorRef, public global: GUIGlobal, private dialogService: NbDialogService) {
  }

  ngOnInit() {

    if ((<any>window).apiTestMode) {
      console.log("Test mode is active!");
    }

    //Refresh/render GUI on startup if ready or wait until ready event is fired
    if (this.global.getGlobalVar("appReady")) {
      this.generatorReady();
    }
    else {

      let eventSub = this.global.globalEmitter.subscribe(eventObj => {

        if (eventObj.name == "init_finished") {
          console.log("Init finished event");
          this.generatorReady();

          eventSub.unsubscribe();
        }
      });
    }  
  }

  generatorReady() {
    this.generatorBusy = false;

    //Set active tab on boot
    this.activeTab = this.global.getGlobalVar('generatorSettingsArray')[0].text;

    //Set active footer tab on boot
    if (this.global.getGlobalVar('appType') == 'generator') {
      this.activeFooterTab = "Generate From Seed";
    }
    else {
      this.activeFooterTab = "Generate From File";
    }

    this.recheckAllSettings();
    this.cd.markForCheck();
    this.cd.detectChanges();

    this.runEventListeners();

    //Electron only: Ensure settings string is up-to-date on app launch
    if (this.global.getGlobalVar('electronAvailable'))
      this.getSettingsString();

    //Remove pace and global spinner element if it exists (to prevent it from ever coming up again in the same session) 
    let pace = (<any>document).querySelector(".pace");

    if (pace) {
      pace.parentNode.removeChild(pace);
    }

    let globalSpinner = (<any>document).querySelector("#nb-global-spinner");

    if (globalSpinner) {
      globalSpinner.parentNode.removeChild(globalSpinner);
    }
  }

  runEventListeners() {

    //Subscribe to event listeners after initial rendering has concluded
    setTimeout(() => {

      this.tabSet.changeTab.subscribe(eventObj => {
        this.activeTab = eventObj.tabTitle;
      });

      this.tabSetFooter.changeTab.subscribe(eventObj => {
        this.activeFooterTab = eventObj.tabTitle;
      });

      this.global.globalEmitter.subscribe(eventObj => {

        if (eventObj.name == "refresh_gui") {
          this.cd.markForCheck();
          this.cd.detectChanges();
        }
        else if (eventObj.name == "dialog_error") {
          this.dialogService.open(DialogWindow, {
            autoFocus: true, closeOnBackdropClick: true, closeOnEsc: true, hasBackdrop: true, hasScroll: false, context: { dialogHeader: "Error", dialogMessage: eventObj.message }
          });
        }
      });

    }, 0);
  }

  generateSeed(fromPatchFile: boolean = false, webRaceSeed: boolean = false) {

    this.generateSeedButtonEnabled = false;

    //console.log("fromPatchFile:", fromPatchFile);
    //console.log(this.global.generator_settingsMap);
    //console.log(this.global.generator_customColorMap);

    if (this.global.getGlobalVar('electronAvailable')) { //Electron

      //Delay the generation if settings are currently locked to avoid race conditions
      if (this.settingsLocked) {
        setTimeout(() => {
          this.generateSeed(fromPatchFile, webRaceSeed);
        }, 50);

        return;
      }

      //Hack: Fix Generation Count being None occasionally
      if (!this.global.generator_settingsMap["count"] || this.global.generator_settingsMap["count"] < 1)
        this.global.generator_settingsMap["count"] = 1;

      let dialogRef = this.dialogService.open(ProgressWindow, {
        autoFocus: true, closeOnBackdropClick: false, closeOnEsc: false, hasBackdrop: true, hasScroll: false, context: { dashboardRef: this, totalGenerationCount: this.global.generator_settingsMap["count"] }
      });

      this.global.generateSeedElectron(dialogRef && dialogRef.componentRef && dialogRef.componentRef.instance ? dialogRef.componentRef.instance : null, fromPatchFile, fromPatchFile == false && this.seedString.trim().length > 0 ? this.seedString.trim() : "").then(res => {
        console.log('[Electron] Gen Success');

        this.generateSeedButtonEnabled = true;
        this.cd.markForCheck();
        this.cd.detectChanges();

        if (dialogRef && dialogRef.componentRef && dialogRef.componentRef.instance) {
          dialogRef.componentRef.instance.progressStatus = 1;
          dialogRef.componentRef.instance.progressPercentageCurrent = 100;
          dialogRef.componentRef.instance.progressPercentageTotal = 100;
          dialogRef.componentRef.instance.progressMessage = "Done. Enjoy.";
          dialogRef.componentRef.instance.progressErrorDetails = "";
          dialogRef.componentRef.instance.refreshLayout();
        }
      }).catch((err) => {
        console.log('[Electron] Gen Error');

        this.generateSeedButtonEnabled = true;
        this.cd.markForCheck();
        this.cd.detectChanges();

        if (dialogRef && dialogRef.componentRef && dialogRef.componentRef.instance) {
          dialogRef.componentRef.instance.progressStatus = -1;
          dialogRef.componentRef.instance.progressPercentageCurrent = 100;
          dialogRef.componentRef.instance.progressPercentageTotal = 100;
          dialogRef.componentRef.instance.progressMessage = err.short;
          dialogRef.componentRef.instance.progressErrorDetails = err.short === err.long ? "" : err.long;
          dialogRef.componentRef.instance.refreshLayout();
        }
      });
    }
    else { //Web

      this.global.generateSeedWeb(webRaceSeed, this.seedString.trim().length > 0 ? this.seedString.trim() : "").then(seedID => {

        //Save last seed id in browser cache
        localStorage.setItem("lastSeed", seedID);

        //Re-direct to seed (waiting) page
        let seedURL = (<any>window).location.protocol + "//" + (<any>window).location.host + "/seed/get?id=" + seedID;

        console.log('[Web] Success, will re-direct to:', seedURL);

        setTimeout(() => {
          (<any>window).location.href = seedURL;
        }, 250);

      }).catch((err) => {
        console.log('[Web] Gen Error');

        if (err.status == 403) { //Rate Limited
          this.dialogService.open(DialogWindow, {
            autoFocus: true, closeOnBackdropClick: true, closeOnEsc: true, hasBackdrop: true, hasScroll: false, context: { dialogHeader: "Error", dialogMessage: "You may only generate one seed per minute to prevent spam!" }
          });
        } 
        else if (err.hasOwnProperty('errorRomInPlando')) {
          console.log("Plando Error", err.errorRomInPlando);
          let plandoDisclaimer = "Your OoT ROM doesn't belong into the plandomizer setting. This entirely optional setting is used to plan out seeds before generation by manipulating spoiler log files. If you want to generate a normal seed, click YES.";
          this.dialogService.open(ConfirmationWindow, {
            autoFocus: true, closeOnBackdropClick: true, closeOnEsc: true, hasBackdrop: true, hasScroll: false, context: { dialogHeader: "Your rom doesn't belong here!", dialogMessage: plandoDisclaimer }
          }).onClose.subscribe(confirmed => {
            if (confirmed) {
              this.global.generator_settingsMap["distribution_file"] = null;
              this.generateSeed(fromPatchFile, webRaceSeed);
            } else {
              this.generateSeedButtonEnabled = true;
              this.cd.markForCheck();
              this.cd.detectChanges();
            }
          });
        }
        else {
          this.dialogService.open(DialogWindow, {
            autoFocus: true, closeOnBackdropClick: true, closeOnEsc: true, hasBackdrop: true, hasScroll: false, context: { dialogHeader: "Error", dialogMessage: err.error && typeof (err.error) == "string" ? err.error : err.message }
          });
        }

        this.generateSeedButtonEnabled = true;
        this.cd.markForCheck();
        this.cd.detectChanges();
      });
    }
  }

  async cancelGeneration() { //Electron only
    return await this.global.cancelGenerateSeedElectron();
  }

  patchROM() { //Web only

    this.generateSeedButtonEnabled = false;

    console.log("Patch ROM");

    this.global.patchROMWeb();

    //No callback, just deactivate button for 1 second
    setTimeout(() => {
      this.generateSeedButtonEnabled = true;
      this.cd.markForCheck();
      this.cd.detectChanges();
    }, 1000);
  }

  copySettingsString() {
    this.global.copyToClipboard(this.global.generator_settingsMap["settings_string"]);
  }

  getSettingsString() {

    this.settingsLocked = true;

    this.global.convertSettingsToString().then(res => {

      //console.log("String got:", res);
      this.global.generator_settingsMap["settings_string"] = res;
      this.global.saveCurrentSettingsToFile();

      this.settingsLocked = false;

      if (this.settingsBusy) { //Execute delayed task
        this.settingsBusy = false;
        this.afterSettingChange(this.settingsBusySaveOnly);
        this.settingsBusySaveOnly = true;
      }

      this.cd.markForCheck();
      this.cd.detectChanges();

    }).catch((err) => {

      this.settingsLocked = false;

      if (this.settingsBusy) { //Execute delayed task
        this.settingsBusy = false;
        this.afterSettingChange(this.settingsBusySaveOnly);
        this.settingsBusySaveOnly = true;
      }

      this.cd.markForCheck();
      this.cd.detectChanges();

      this.dialogService.open(ErrorDetailsWindow, {
        autoFocus: true, closeOnBackdropClick: true, closeOnEsc: true, hasBackdrop: true, hasScroll: false, context: { errorMessage: err }
      });
    });
  }

  importSettingsString() {

    this.generatorBusy = true;

    this.global.convertStringToSettings(this.global.generator_settingsMap["settings_string"]).then(res => {

      //console.log(res);

      this.global.applySettingsObject(res);
      this.global.saveCurrentSettingsToFile();

      this.recheckAllSettings("", false, true);

      this.generatorBusy = false;

      this.cd.markForCheck();
      this.cd.detectChanges();

    }).catch((err) => {

      this.generatorBusy = false;
      this.cd.markForCheck();
      this.cd.detectChanges();

      this.dialogService.open(DialogWindow, {
        autoFocus: true, closeOnBackdropClick: true, closeOnEsc: true, hasBackdrop: true, hasScroll: false, context: { dialogHeader: "Error", dialogMessage: "The entered settings string seems to be invalid!" }
      });
    });
  }

  loadPreset() {

    let targetPreset = this.global.generator_presets[this.global.generator_settingsMap["presets"]];

    if (targetPreset) {
      if (("isNewPreset" in targetPreset) && targetPreset.isNewPreset == true) {
        this.dialogService.open(DialogWindow, {
          autoFocus: true, closeOnBackdropClick: true, closeOnEsc: true, hasBackdrop: true, hasScroll: false, context: { dialogHeader: "Warning", dialogMessage: "You can not load this preset!" }
        });
      }
      else {

        if (("isDefaultPreset" in targetPreset) && targetPreset.isDefaultPreset == true) { //RESTORE DEFAULTS
          this.global.applyDefaultSettings();
        }
        else {
          this.global.applyDefaultSettings(); //Restore defaults first in case the user loads an old preset that misses settings
          this.global.applySettingsObject(this.global.generator_presets[this.global.generator_settingsMap["presets"]].settings);
        }

        this.recheckAllSettings("", false, true);
        this.afterSettingChange();

        //console.log("Preset loaded");
      }
    }
  }

  savePreset(refPresetSelect: NbSelectComponent<string>) {

    let targetPreset = this.global.generator_presets[this.global.generator_settingsMap["presets"]];

    if (targetPreset) {

      if ((("isNewPreset" in targetPreset) && targetPreset.isNewPreset == true)) { //NEW PRESET

        this.dialogService.open(TextInputWindow, {
          autoFocus: true, closeOnBackdropClick: true, closeOnEsc: true, hasBackdrop: true, hasScroll: false, context: { dialogHeader: "Create new preset", dialogMessage: "Enter preset name:" }
        }).onClose.subscribe(name => {

          if (name && typeof (name) == "string" && name.trim().length > 0) {

            let trimmedName = name.trim();

            if (trimmedName in this.global.generator_presets) {
              this.dialogService.open(DialogWindow, {
                autoFocus: true, closeOnBackdropClick: true, closeOnEsc: true, hasBackdrop: true, hasScroll: false, context: { dialogHeader: "Error", dialogMessage: "A preset with this name already exists! If you wish to overwrite an existing preset, please select it from the list and hit Save instead." }
              });
            }
            else {
              this.global.generator_presets[trimmedName] = { settings: this.global.createSettingsFileObject(false, true, !this.global.getGlobalVar('electronAvailable')) };
              this.global.generator_settingsMap["presets"] = trimmedName;
              this.global.saveCurrentPresetsToFile();

              this.cd.markForCheck();
              this.cd.detectChanges();

              refPresetSelect.setSelected = trimmedName;

              //console.log("Preset created");
            }
          }
        });
      }
      else if (("isDefaultPreset" in targetPreset) && targetPreset.isDefaultPreset == true) { //DEFAULT
        this.dialogService.open(DialogWindow, {
          autoFocus: true, closeOnBackdropClick: true, closeOnEsc: true, hasBackdrop: true, hasScroll: false, context: { dialogHeader: "Warning", dialogMessage: "System presets can not be overwritten!" }
        });
      }
      else if (("isProtectedPreset" in targetPreset) && targetPreset.isProtectedPreset == true) { //BUILT IN
        this.dialogService.open(DialogWindow, {
          autoFocus: true, closeOnBackdropClick: true, closeOnEsc: true, hasBackdrop: true, hasScroll: false, context: { dialogHeader: "Warning", dialogMessage: "Built in presets are protected and can not be overwritten!" }
        });
      }
      else { //USER PRESETS
        this.dialogService.open(ConfirmationWindow, {
          autoFocus: true, closeOnBackdropClick: true, closeOnEsc: true, hasBackdrop: true, hasScroll: false, context: { dialogHeader: "Confirm?", dialogMessage: "Do you want to overwrite the preset '" + this.global.generator_settingsMap["presets"] + "' ?" }
        }).onClose.subscribe(confirmed => {

          if (confirmed) {
            this.global.generator_presets[this.global.generator_settingsMap["presets"]] = { settings: this.global.createSettingsFileObject(false, true, !this.global.getGlobalVar('electronAvailable')) };
            this.global.saveCurrentPresetsToFile();

            console.log("Preset overwritten");
          }
        });
      }
    }
  }

  deletePreset() {

    let targetPreset = this.global.generator_presets[this.global.generator_settingsMap["presets"]];

    if (targetPreset) {
      if ((("isNewPreset" in targetPreset) && targetPreset.isNewPreset == true) || (("isDefaultPreset" in targetPreset) && targetPreset.isDefaultPreset == true)) {
        this.dialogService.open(DialogWindow, {
          autoFocus: true, closeOnBackdropClick: true, closeOnEsc: true, hasBackdrop: true, hasScroll: false, context: { dialogHeader: "Warning", dialogMessage: "System presets can not be deleted!" }
        });
      }
      else if (("isProtectedPreset" in targetPreset) && targetPreset.isProtectedPreset == true) {
        this.dialogService.open(DialogWindow, {
          autoFocus: true, closeOnBackdropClick: true, closeOnEsc: true, hasBackdrop: true, hasScroll: false, context: { dialogHeader: "Warning", dialogMessage: "Built in presets are protected and can not be deleted!" }
        });
      }
      else {
        this.dialogService.open(ConfirmationWindow, {
          autoFocus: true, closeOnBackdropClick: true, closeOnEsc: true, hasBackdrop: true, hasScroll: false, context: { dialogHeader: "Confirm?", dialogMessage: "Do you really want to delete the preset '" + this.global.generator_settingsMap["presets"] + "' ?" }
        }).onClose.subscribe(confirmed => {

          if (confirmed) {
            delete this.global.generator_presets[this.global.generator_settingsMap["presets"]];
            this.global.generator_settingsMap["presets"] = "[New Preset]";
            this.global.saveCurrentPresetsToFile();

            this.cd.markForCheck();
            this.cd.detectChanges();

            //console.log("Preset deleted");
          }
        });
      }
    }
  }

  openOutputDir() { //Electron only

    var path = "";

    if (!this.global.generator_settingsMap["output_dir"] || this.global.generator_settingsMap["output_dir"].length < 1)
      path = "Output";
    else
      path = this.global.generator_settingsMap["output_dir"];
 
    this.global.createAndOpenPath(path).then(() => {
      console.log("Output dir opened");
    }).catch(err => {
      console.error("Error:", err);

      if (err.message.includes("no such file or directory")) {
        this.dialogService.open(DialogWindow, {
          autoFocus: true, closeOnBackdropClick: true, closeOnEsc: true, hasBackdrop: true, hasScroll: false, context: { dialogHeader: "Error", dialogMessage: "The specified output directory does not exist!" }
        });
      }
      else {
        this.dialogService.open(DialogWindow, {
          autoFocus: true, closeOnBackdropClick: true, closeOnEsc: true, hasBackdrop: true, hasScroll: false, context: { dialogHeader: "Error", dialogMessage: err }
        });
      }
    });
  }

  browseForFile(setting: any) { //Electron only
    this.global.browseForFile(setting.file_types).then(res => {
      this.global.generator_settingsMap[setting.name] = res;
      this.cd.markForCheck();
      this.afterSettingChange();
    }).catch(err => {
      console.log(err);
    });
  }

  browseForDirectory(setting: any) { //Electron only
    this.global.browseForDirectory().then(res => {
      this.global.generator_settingsMap[setting.name] = res;
      this.cd.markForCheck();
      this.afterSettingChange();
    }).catch(err => {
      console.log(err);
    });
  }

  browseForPatchFile() { //Electron only
    this.global.browseForFile([{ name: 'Patch File Archive', 'extensions': ['zpfz', 'zpf'] }, { 'name': 'All Files', 'extensions': ['*'] }]).then(res => {
      this.global.generator_settingsMap['patch_file'] = res;
      this.cd.markForCheck();
      this.afterSettingChange(true);
    }).catch(err => {
      console.log(err);
    });
  }

  changeFooterTabSelection(event) {
    this.checkFooterTabVisibility(event);
  }

  checkFooterTabVisibility(event = null) {

    let title = "";

    if (event) {
      title = event.tabTitle;
      this.activeFooterTab = title;
    }
    else {
      title = this.activeFooterTab;
    }

    if (this.global.getGlobalVar('electronAvailable')) { //Electron

      if (title === "Generate From File") {

        let visibilityUpdates = [];
        visibilityUpdates.push({ target: { controls_visibility_tab: "main-tab,detailed-tab,other-tab" }, value: false });
        visibilityUpdates.push({ target: { controls_visibility_section: "preset-section" }, value: false });
        visibilityUpdates.push({ target: { controls_visibility_setting: "count,create_spoiler,world_count,distribution_file" }, value: false });

        visibilityUpdates.push({ target: { controls_visibility_tab: "cosmetics-tab,sfx-tab" }, value: this.global.generator_settingsMap['repatch_cosmetics'] });
        visibilityUpdates.push({ target: { controls_visibility_setting: "create_cosmetics_log" }, value: this.global.generator_settingsMap['repatch_cosmetics'] });

        this.toggleVisibility(visibilityUpdates, false);
      }
      else if (title === "Generate From Seed") {

        let visibilityUpdates = [];
        visibilityUpdates.push({ target: { controls_visibility_tab: "main-tab,detailed-tab,other-tab" }, value: true });
        visibilityUpdates.push({ target: { controls_visibility_section: "preset-section" }, value: true });
        visibilityUpdates.push({ target: { controls_visibility_setting: "count,create_spoiler,world_count,distribution_file" }, value: true });

        visibilityUpdates.push({ target: { controls_visibility_tab: "cosmetics-tab,sfx-tab" }, value: true });
        visibilityUpdates.push({ target: { controls_visibility_setting: "create_cosmetics_log" }, value: true });

        this.toggleVisibility(visibilityUpdates, false);
      }
    }
    else { //Web

      if (this.global.getGlobalVar("appType") == "generator") {

        if (title === "Generate From File") {

          let visibilityUpdates = [];
          visibilityUpdates.push({ target: { controls_visibility_tab: "main-tab,detailed-tab,other-tab" }, value: false });
          visibilityUpdates.push({ target: { controls_visibility_section: "preset-section" }, value: false });
          visibilityUpdates.push({ target: { controls_visibility_setting: "create_spoiler,world_count,distribution_file" }, value: false });

          visibilityUpdates.push({ target: { controls_visibility_setting: "rom,web_output_type,player_num" }, value: true });
          visibilityUpdates.push({ target: { controls_visibility_setting: "web_wad_file,web_common_key_file,web_common_key_string,web_wad_channel_id,web_wad_channel_title" }, value: this.global.generator_settingsMap['web_output_type'] == "wad" });

          visibilityUpdates.push({ target: { controls_visibility_tab: "cosmetics-tab,sfx-tab" }, value: this.global.generator_settingsMap['repatch_cosmetics'] });

          this.toggleVisibility(visibilityUpdates, false);
        }
        else if (title === "Generate From Seed") {

          let visibilityUpdates = [];
          visibilityUpdates.push({ target: { controls_visibility_tab: "main-tab,detailed-tab,other-tab" }, value: true });
          visibilityUpdates.push({ target: { controls_visibility_section: "preset-section" }, value: true });
          visibilityUpdates.push({ target: { controls_visibility_setting: "create_spoiler,world_count,distribution_file" }, value: true });

          visibilityUpdates.push({ target: { controls_visibility_setting: "rom,web_output_type,player_num" }, value: false });
          visibilityUpdates.push({ target: { controls_visibility_setting: "web_wad_file,web_common_key_file,web_common_key_string,web_wad_channel_id,web_wad_channel_title" }, value: false });

          visibilityUpdates.push({ target: { controls_visibility_tab: "cosmetics-tab,sfx-tab" }, value: true });

          this.toggleVisibility(visibilityUpdates, false);
        }
      }
      else if (this.global.getGlobalVar("appType") == "patcher") {

        if (title === "Generate From File") {

          let visibilityUpdates = [];
          visibilityUpdates.push({ target: { controls_visibility_tab: "cosmetics-tab,sfx-tab" }, value: this.global.generator_settingsMap['repatch_cosmetics'] });

          visibilityUpdates.push({ target: { controls_visibility_setting: "rom,web_output_type,player_num" }, value: true });
          visibilityUpdates.push({ target: { controls_visibility_setting: "web_wad_file,web_common_key_file,web_common_key_string,web_wad_channel_id,web_wad_channel_title" }, value: this.global.generator_settingsMap['web_output_type'] == "wad" });

          this.toggleVisibility(visibilityUpdates, false);
        }
      }
      else if (this.global.getGlobalVar("appType") == "patcher_only") {

        if (title === "Generate From File") {

          let visibilityUpdates = [];
          visibilityUpdates.push({ target: { controls_visibility_setting: "rom,web_output_type" }, value: true });
          visibilityUpdates.push({ target: { controls_visibility_setting: "web_wad_file,web_common_key_file,web_common_key_string,web_wad_channel_id,web_wad_channel_title" }, value: this.global.generator_settingsMap['web_output_type'] == "wad" });

          this.toggleVisibility(visibilityUpdates, false);
        }
      }
    }
  }

  updateCosmeticsCheckboxChange(value) {

    let visibilityUpdates = [];
    visibilityUpdates.push({ target: { controls_visibility_tab: "cosmetics-tab,sfx-tab" }, value: value });

    if (this.global.getGlobalVar('electronAvailable')) //Create Cosmetics Log is Electron only
      visibilityUpdates.push({ target: { controls_visibility_setting: "create_cosmetics_log" }, value: value });

    this.toggleVisibility(visibilityUpdates, false);
    this.afterSettingChange(true);
  }

  calculateRowHeight(listRef: MatGridList, tab: any) {
    let columnCount = this.verifyColumnCount(listRef.cols);
    let absoluteRowCount = 0;
    let absoluteRowIndex = 0;
    let gutterPercentage = 0;

    for (let i = 0; i < tab.sections.length; i++) {

      let section = tab.sections[i];

      absoluteRowIndex += this.getColumnWidth(null, tab.sections, i, tab.sections.length, section['col_span'] ? section['col_span'] : 0, columnCount);

      if (absoluteRowIndex >= columnCount) {
        absoluteRowIndex = 0;

        let columnRowCount = this.getColumnHeight(null, section, columnCount);
        absoluteRowCount += columnRowCount;
        gutterPercentage += (columnRowCount * 0.5);
      }
    }

    let heightPerRow = (100 - gutterPercentage) / absoluteRowCount;
    return heightPerRow + "%";
  }

  getColumnCount(tileRef: MatGridTile) {
    return this.verifyColumnCount(tileRef._gridList.cols);
  }

  verifyColumnCount(count: number) {

    if (count != 1 && count != 2 && count != 12) {
      return 1;
    }

    return count;
  }

  getColumnWidth(tileRef: MatGridTile, sections: any, index: number, length: number, colSpan: number = 0, columnCount: number = -1) {

    if (columnCount == -1) {
      columnCount = this.getColumnCount(tileRef);
    }

    //col_span override
    if (colSpan > 0)
      if (columnCount == 12) //Treat 12x1 column setup as 4x1 internally
        return 4 >= colSpan ? colSpan * 3 : 12;
      else
        return columnCount >= colSpan ? colSpan : columnCount;

    //Account for col_span override sections in a special way
    let searchIndex = 0;
    let sectionIndex = index;

    sections.forEach(section => {

      if (section.col_span > 0) {

        let sectionsToAdd;

        if (columnCount == 12) //Treat 12x1 column setup as 4x1 internally
          sectionsToAdd = (4 >= section.col_span ? section.col_span : 4) - 1;
        else
          sectionsToAdd = (columnCount >= section.col_span ? section.col_span : columnCount) - 1;

        length += sectionsToAdd;

        if (searchIndex < sectionIndex)
          index += sectionsToAdd;
      }

      searchIndex++;
    });

    if (columnCount == 2 && length % 2 != 0 && index == length - 1) { //If an odd number of cols exist with 2 cols length, make last col take the entire row size
      return 2;
    }
    else if (columnCount == 3 && length % 3 != 0 && index == length - 1) { //Make final column size 3 if it is on its row alone. If there are 2 columns, make the last column size 2
      if (index % 3 == 0)
        return 3;
      else
        return 2;
    }
    else if (columnCount == 4 && length % 4 != 0) { //Make final column size 4 if it is on its row alone. If there are 2 columns, make both size 2. Else just make the final one size 2

      if (index == length - 1) {
        if (index % 4 == 0)
          return 4;
        else if (index % 4 == 1)
          return 2;
        else
          return 2;
      }
      else if (index + 1 == length - 1) {
        if (index % 4 == 0)
          return 2;
      }
    }
    else if (columnCount == 12) { //We limit max sections per line at 4 in a 12x1 column setup

      if (index == length - 1) {
        if (index % 4 == 0)
          return 12;
        else if (index % 4 == 1)
          return 6;
        else if (index % 4 == 2)
          return 4;
      }
      else if (index + 1 == length - 1) {
        if (index % 4 == 0)
          return 6;
        else if (index % 4 == 1)
          return 4;
      }
      else if (index + 2 == length - 1) {
        if (index % 4 == 0)
          return 4;
      }

      return 3;
    }

    return 1;
  }

  getColumnHeight(tileRef: MatGridTile, section: any, columnCount: number = -1) {

    if (columnCount == -1) {
      columnCount = this.getColumnCount(tileRef);
    }

    let spanIndex = 0;

    switch (columnCount) {
      case 2:
        spanIndex = 1;
        break;
      case 12:
        spanIndex = 2;
        break;
    }

    return section.row_span[spanIndex];
  }

  findOption(options: any, optionName: string) {
    return options.find(option => { return option.name == optionName });
  }

  getVariableType(variable: any) {
    return typeof (variable);
  }

  getNextVisibleSetting(settings: any, startingIndex: number) {

    if (settings.length > startingIndex) {
      for (let i = startingIndex; i < settings.length; i++) {
        let setting = settings[i];

        if (this.global.generator_settingsVisibilityMap[setting.name] || !setting.hide_when_disabled)
          return setting;
      }
    }

    return null;
  }

  checkVisibility(newValue: any, setting: any, option: any = null, refColorPicker: HTMLInputElement = null, disableOnly: boolean = false, noValueChange: boolean = false) {

    if (!disableOnly && !noValueChange)
      this.afterSettingChange();

    //Array of settings that should have its visibility altered
    var targetSettings = [];

    if (setting["type"] === "Checkbutton" || setting["type"] === "Radiobutton" || setting["type"] === "Combobox") {
      let value = typeof (newValue) == "object" ? newValue.value : newValue;

      //Open color picker if custom color is selected
      if (refColorPicker && value == "Custom Color") {

        if (this.global.generator_customColorMap[setting.name].length < 1)
          this.global.generator_customColorMap[setting.name] = "#ffffff";

        refColorPicker.click();
      }

      //Build list of options
      setting.options.forEach(optionToAdd => {

        if (optionToAdd.name === option.name) //Add currently selected item last for priority
          return;

        targetSettings.push({ target: optionToAdd, value: optionToAdd.name != value });
      });

      targetSettings.push({ target: option, value: false });
    }

    //Handle activations/deactivations
    this.toggleVisibility(targetSettings, disableOnly, setting.name);
  }

  toggleVisibility(targetSettings: any, disableOnly: boolean, skipSetting: string = "") {

    var triggeredChange = false;

    targetSettings.forEach(setting => {

      let targetSetting = setting.target;
      let targetValue = setting.value;

      if (disableOnly && targetValue == true)
        return;

      if ("controls_visibility_tab" in targetSetting) {

        //console.log(targetSetting, setting);

        targetSetting["controls_visibility_tab"].split(",").forEach(tab => {
          this.global.generator_tabsVisibilityMap[tab.replace(/-/g, "_")] = targetValue;

          //Kick user out of active tab and go back to root if it gets disabled here
          if (!targetValue && this.global.getGlobalVar("generatorSettingsObj")) {

            if (this.activeTab == this.global.getGlobalVar("generatorSettingsObj")[tab.replace(/-/g, "_")].text) {
              //console.log("Kick user out of tab");
              this.tabSet.selectTab(this.tabSet.tabs.first);
            }
          }
        });
      }

      if ("controls_visibility_section" in targetSetting) {

        targetSetting["controls_visibility_section"].split(",").forEach(section => {

          let targetSection = null;

          //Find section
          for (let i = 0; i < this.global.getGlobalVar('generatorSettingsArray').length; i++) {
            let tab = this.global.getGlobalVar('generatorSettingsArray')[i];

            for (let n = 0; n < tab.sections.length; n++) {

              if (tab.sections[n].name === section.replace(/-/g, "_")) {
                targetSection = tab.sections[n];
                break;
              }
            }

            if (targetSection)
              break;
          }

          //Disable/Enable entire section
          if (targetSection) {

            targetSection.settings.forEach(setting => {

              if (targetValue == true && this.global.generator_settingsVisibilityMap[setting.name] == false) //Only trigger change if a setting gets re-enabled
                triggeredChange = true;

              this.global.generator_settingsVisibilityMap[setting.name] = targetValue;
            });
          }
        });
      }

      if ("controls_visibility_setting" in targetSetting) {

        targetSetting["controls_visibility_setting"].split(",").forEach(setting => {

          if (targetValue == true && this.global.generator_settingsVisibilityMap[setting] == false) //Only trigger change if a setting gets re-enabled
            triggeredChange = true;

          this.global.generator_settingsVisibilityMap[setting] = targetValue;
        });
      }
    });

    //Re-run function with every single setting to ensure integrity (nothing gets re-activated when it shouldn't)
    if (triggeredChange) {
      this.recheckAllSettings(skipSetting);
    }
  }

  recheckAllSettings(skipSetting: string = "", disableOnly: boolean = true, noValueChange: boolean = false) {

    this.global.getGlobalVar('generatorSettingsArray').forEach(tab => tab.sections.forEach(section => section.settings.forEach(checkSetting => {

      if (skipSetting && checkSetting.name === skipSetting)
        return;

      if (checkSetting["type"] === "Checkbutton" || checkSetting["type"] === "Radiobutton" || checkSetting["type"] === "Combobox") {

        let targetOption = checkSetting.options.find(option => {

          if (option.name === this.global.generator_settingsMap[checkSetting.name])
            return true;

          return false;
        });

        if (targetOption) {
          this.checkVisibility({ value: this.global.generator_settingsMap[checkSetting.name] }, checkSetting, targetOption, null, disableOnly, noValueChange);
        }
      }
    })));

    //Check bottom tabset last
    this.checkFooterTabVisibility();  
  }

  revertToPriorValue(settingName: string, forceChangeDetection: boolean) {

    let oldValue = this.global.generator_settingsMap[settingName];

    setTimeout(() => {
      this.global.generator_settingsMap[settingName] = oldValue;

      if (forceChangeDetection)
        this.cd.markForCheck();
    }, 0);
  }

  numberInputChange(newValue: any, setting: object) {

    //Existence check
    if (!newValue || newValue.length == 0) {
      this.revertToPriorValue(setting["name"], false);
      return;
    }     

    //Number check
    if (Number(parseInt(newValue)) != newValue) {
      this.revertToPriorValue(setting["name"], true);
      return;
    }

    //Min/Max check
    let settingMin: number = setting["min"];
    let settingMax: number = setting["max"];

    if (("min" in setting) && newValue < settingMin) {
      setTimeout(() => {
        this.global.generator_settingsMap[setting["name"]] = settingMin;
        this.cd.markForCheck();
        this.afterSettingChange();
      }, 0);
    }
    else if (("max" in setting) && newValue > settingMax) {
      setTimeout(() => {
        this.global.generator_settingsMap[setting["name"]] = settingMax;
        this.cd.markForCheck();
        this.afterSettingChange();
      }, 0);
    }
    else {
      setTimeout(() => {
        this.global.generator_settingsMap[setting["name"]] = parseInt(newValue);
        this.afterSettingChange();
      }, 0);
    }
  }

  afterSettingChange(saveOnly: boolean = false) {

    if (this.global.getGlobalVar('electronAvailable')) { //Electron

      //Show waiting spinner if another settings action is currently running and delay the task
      if (this.settingsLocked) {
        this.settingsBusy = true;

        if (!saveOnly)
          this.settingsBusySaveOnly = false;

        this.cd.markForCheck();
        this.cd.detectChanges();
        return;
      }

      this.settingsLocked = true;

      setTimeout(() => {
        //console.log(this.global.generator_settingsMap);
        //console.log(this.global.generator_customColorMap);

        if (saveOnly) {
          this.global.saveCurrentSettingsToFile();

          this.settingsLocked = false;

          if (this.settingsBusy) { //Execute delayed task
            this.settingsBusy = false;
            this.afterSettingChange(this.settingsBusySaveOnly);
            this.settingsBusySaveOnly = true;
          }

          this.cd.markForCheck();
          this.cd.detectChanges();
        }
        else {
          this.getSettingsString();
        }
      }, 0);
    }
    else { //Web

      setTimeout(() => {

        //console.log(this.global.generator_settingsMap);
        //console.log(this.global.generator_customColorMap);

        this.global.saveCurrentSettingsToFile();

        this.settingsLocked = false;
        this.cd.markForCheck();
        this.cd.detectChanges();
      }, 0);
    }
  }
}
