const fs = require("fs");
const path = require("path");

let compiledSettingsMapPath = path.normalize(path.join(__dirname, '../../../data/generated/settings_list.json'));
let guiSettings;

if (fs.existsSync(compiledSettingsMapPath)) {
  guiSettings = JSON.parse(fs.readFileSync(compiledSettingsMapPath, 'utf8'));
}
else {
  console.error("No settings_list.json found!");
  return;
}

//Add static presets
guiSettings.presets = {
  "[New Preset]": { isNewPreset: true },
  "Default / Beginner": { isDefaultPreset: true }
};

//Load built in presets
let builtInPresetsPath = path.normalize(path.join(__dirname, '../../../data/presets_default.json'));

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

let file = JSON.stringify(guiSettings);
let targetPath = path.join(__dirname, 'settings_list.json');

console.log("Settings map:", guiSettings);

fs.writeFileSync(targetPath, file);

console.log("DONE!");
