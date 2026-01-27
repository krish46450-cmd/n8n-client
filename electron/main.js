const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let flaskProcess;
const FLASK_PORT = 5000;
const isDev = process.argv.includes('--dev');

function getFlaskPath() {
  if (isDev) {
    return path.join(__dirname, '..');
  }
  return path.join(process.resourcesPath, 'app');
}

function startFlaskServer() {
  return new Promise((resolve, reject) => {
    const flaskPath = getFlaskPath();

    // Use virtual environment Python if available
    let pythonExecutable;
    const venvPath = path.join(flaskPath, 'venv', 'bin', 'python3');
    const fs = require('fs');

    if (fs.existsSync(venvPath)) {
      pythonExecutable = venvPath;
    } else {
      pythonExecutable = process.platform === 'win32' ? 'python' : 'python3';
    }

    console.log('Starting Flask server from:', flaskPath);
    console.log('Using Python:', pythonExecutable);

    flaskProcess = spawn(pythonExecutable, ['app.py'], {
      cwd: flaskPath,
      env: {
        ...process.env,
        FLASK_ENV: isDev ? 'development' : 'production',
        PYTHONUNBUFFERED: '1'
      }
    });

    flaskProcess.stdout.on('data', (data) => {
      console.log(`Flask: ${data}`);
      const output = data.toString();
      if (output.includes('Running on') || output.includes('WARNING')) {
        setTimeout(() => resolve(), 2000);
      }
    });

    flaskProcess.stderr.on('data', (data) => {
      console.error(`Flask Error: ${data}`);
    });

    flaskProcess.on('close', (code) => {
      console.log(`Flask process exited with code ${code}`);
    });

    flaskProcess.on('error', (err) => {
      console.error('Failed to start Flask server:', err);
      reject(err);
    });

    setTimeout(() => resolve(), 5000);
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1000,
    minHeight: 700,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false
    },
    icon: path.join(__dirname, '..', 'static', 'icon.png'),
    title: 'Dump Analyzer',
    backgroundColor: '#ffffff'
  });

  mainWindow.loadURL(`http://localhost:${FLASK_PORT}`);

  if (isDev) {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  mainWindow.webContents.on('did-fail-load', () => {
    setTimeout(() => {
      if (mainWindow) {
        mainWindow.loadURL(`http://localhost:${FLASK_PORT}`);
      }
    }, 1000);
  });
}

app.whenReady().then(async () => {
  try {
    const fixPath = await import('fix-path');
    fixPath.default();

    await startFlaskServer();
    createWindow();

    app.on('activate', () => {
      if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
      }
    });
  } catch (error) {
    console.error('Failed to start application:', error);
    dialog.showErrorBox('Startup Error', 'Failed to start the Flask server. Please check the logs.');
    app.quit();
  }
});

app.on('window-all-closed', () => {
  if (flaskProcess) {
    flaskProcess.kill();
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  if (flaskProcess) {
    flaskProcess.kill();
  }
});

ipcMain.handle('select-file', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openFile'],
    filters: [
      { name: 'Dump Files', extensions: ['dmp', 'dump'] },
      { name: 'All Files', extensions: ['*'] }
    ]
  });
  return result.filePaths;
});

ipcMain.handle('select-directory', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openDirectory']
  });
  return result.filePaths;
});

ipcMain.handle('select-image', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openFile'],
    filters: [
      { name: 'Images', extensions: ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'] },
      { name: 'All Files', extensions: ['*'] }
    ]
  });
  return result.filePaths;
});
