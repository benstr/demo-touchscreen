const {app, BrowserWindow} = require('electron');
const ipc = require('electron').ipcMain;

app.on('window-all-closed', () => {
  app.quit()
})

app.on('ready', () => {

  var ui = new BrowserWindow({
		height: 444,
		width: 800,
		resizable: true,
    autoHideMenuBar: true,
    alwaysOnTop: true
	});
  ui.maximize();
	ui.loadURL('file://' + __dirname + '/ui.html');

	ui.on('closed', () => {
  		app.quit()
	})
});
