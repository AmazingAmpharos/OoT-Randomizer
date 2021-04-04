const fs = require('fs-extra');
const path = require('path');

const del = require('del');
const express = require('express');
const makeDir = require('make-dir');
const open = require('open');

const protocol = 'http';
const host = 'localhost';
const baseURL = 'localhost';

var port = 80;
var app;
var server;

async function startApp() {
    await setupAngular();
    startServer();
}

async function setupAngular() {
    console.log("[App] Setup Angular");

    let appPath = path.resolve("./public/angular/dev/Test/app");
    let utilsPath = path.resolve("./public/angular/dev/Test/utils");

    //Create Angular folders or clean them up
    if (!fs.existsSync(appPath)) {
        await makeDir(appPath, { mode: 0o777 });
    }
    else {
        await del(appPath + '/*', { dot: true });
    }

    if (!fs.existsSync(utilsPath)) {
        await makeDir(utilsPath, { mode: 0o777 });
    }
    else {
        await del(utilsPath + '/*', { dot: true });
    }

    //Copy Angular app
    fs.copySync("../dist/ootr-electron-gui", appPath);

    //Copy util files
    fs.copyFileSync("./settingsParser/settings_list.json", utilsPath + "/settings_list.json");
    fs.copyFileSync("./index_web.html", appPath + "/index.html");

    console.log("[App] Angular Setup completed");
}

function startServer() {

    console.log('[App] Starting server');

    //(Re)create Express app, HTTP(S) servers
    app = express();
    server = require('http').createServer(app);

    app.use(express.static('public', { dotfiles: 'allow' }));

    //ROUTES
    app.get('/', function (req, res) {
        res.redirect("/angular/dev/Test/app");
    });

    console.log(`[App] Attempting to listen on server`);
    server.on('error', err => {
        switch (err.code) {
            case 'EADDRINUSE':
                console.error(`[App] Listen for server in use, is the webserver already running?`);
                break;
            default:
                console.error('[App] Server unhandled error: ', err);
                break;
        }
    });

    //We intentionally wait until everything is loaded before starting the server
    server.listen({
        host: host,
        port: port
    }, () => {
        console.log('[App] Server running on %s://%s:%d', protocol, baseURL, port);
        open(protocol + "://" + host + ":" + port);
    });
}

startApp();
