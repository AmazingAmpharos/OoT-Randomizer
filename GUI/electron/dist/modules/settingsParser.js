const fs = require('fs');
const path = require('path');

var settingsData = {};

function parseSettings() {

    var responseSettings = JSON.parse(fs.readFileSync(path.join(__dirname, "../utils/settings_list.json")));
    var responseMapping = JSON.parse(fs.readFileSync(path.join(__dirname, "../utils/settings_mapping.json")));

    var resultObject = {};
    var resultArray = [];

    var resultCosmeticsObject = {};
    var resultCosmeticsArray = [];

    responseMapping.Tabs.forEach(tab => {

        var tabName = tab.name.replace(/-/g, "_");
        var tabIsCosmetics = "is-cosmetics" in tab && tab["is-cosmetics"] == true ? true : false;

        resultObject[tabName] = { text: tab["text"], sections: {} };

        if (tabIsCosmetics)
            resultCosmeticsObject[tabName] = { text: tab["text"], sections: {} };

        var tabEntry = { name: tabName, text: tab["text"], sections: [] };

        tab.sections.forEach(section => {

            var sectionName = section.name.replace(/-/g, "_");
            resultObject[tabName].sections[sectionName] = { text: section["text"], is_colors: section["is-colors"], is_sfx: section["is-sfx"], col_span: section["col-span"], row_span: section["row-span"], subheader: section["subheader"], settings: {} };

            if (tabIsCosmetics)
              resultCosmeticsObject[tabName].sections[sectionName] = { text: section["text"], is_colors: section["is-colors"], is_sfx: section["is-sfx"], col_span: section["col-span"], row_span: section["row-span"], subheader: section["subheader"], settings: {} };

          var sectionEntry = { name: sectionName, text: section["text"], is_colors: section["is-colors"], is_sfx: section["is-sfx"], col_span: section["col-span"], row_span: section["row-span"], subheader: section["subheader"], settings: [] };

            section.settings.forEach(setting => {

                var settingName = setting.name;
                var settingEntry = { controls_visibility_tab: setting["controls-visibility-tab"], controls_visibility_section: setting["controls-visibility-section"], controls_visibility_setting: setting["controls-visibility-setting"], min: setting["min"], max: setting["max"], file_types: setting["file-types"], no_line_break: setting["no-line-break"], current_value: undefined };

                //Find setting in responseSettings, then add that data into the obj
                let settingData = responseSettings.find(setting => {
                    return setting.name == settingName;
                });

                var optionsObj = {};
                var optionsArray = [];

                if (settingData) {

                    settingEntry.default = settingData.default;
                    settingEntry.text = settingData.text;
                    settingEntry.type = settingData.type;

                    if (settingData.options) {
                        settingData.options.forEach(option => {
                          optionsObj[option["name"]] = { text: option["text"], tooltip: option["tooltip"], controls_visibility_tab: option["controls-visibility-tab"], controls_visibility_section: option["controls-visibility-section"], controls_visibility_setting: option["controls-visibility-setting"] };
                          optionsArray.push({ name: option["name"], text: option["text"], tooltip: option["tooltip"], controls_visibility_tab: option["controls-visibility-tab"], controls_visibility_section: option["controls-visibility-section"], controls_visibility_setting: option["controls-visibility-setting"] });
                        });
                    }

                    settingEntry.tooltip = settingData.tooltip; 
                    settingEntry.current_value = settingEntry.default;
                }

                settingEntry.options = optionsObj;

                resultObject[tabName].sections[sectionName].settings[settingName] = settingEntry;

                if (tabIsCosmetics)
                    resultCosmeticsObject[tabName].sections[sectionName].settings[settingName] = settingEntry;

                let settingEntryArray = JSON.parse(JSON.stringify(settingEntry));

                settingEntryArray.name = settingName;
                settingEntryArray.options = optionsArray;
                delete settingEntryArray.current_value;

                sectionEntry.settings.push(settingEntryArray);
            });

            tabEntry.sections.push(sectionEntry);
        });

        resultArray.push(tabEntry);

        if (tabIsCosmetics)
            resultCosmeticsArray.push(tabEntry);
    });

    //Save globally
    settingsData = { settingsArray: resultArray, settingsObject: resultObject, cosmeticsArray: resultCosmeticsArray, cosmeticsObject: resultCosmeticsObject };  
}

module.exports = {
    generate: function () {
        parseSettings();
    },
    getSettingsData: function () {
        return { settingsArray: settingsData.settingsArray, settingsObj: settingsData.settingsObject, cosmeticsArray: settingsData.cosmeticsArray, cosmeticsObject: settingsData.cosmeticsObject };
    }
};
