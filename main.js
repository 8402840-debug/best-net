const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs');

function createWindow() {
  const win = new BrowserWindow({
    width: 1080,
    height: 860,
    minWidth: 580,
    minHeight: 520,
    icon: path.join(__dirname, 'icon.ico'),
    backgroundColor: '#0b0d12',
    show: false, // 先不显示，避免加载过程中的白屏闪烁
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });
  win.setMenuBarVisibility(false);
  win.once('ready-to-show', () => win.show());
  win.loadFile(path.join(__dirname, 'card-vault.html'));
}

app.whenReady().then(() => {
  createWindow();
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

// 通用保存文件对话框（JSON备份 / CSV导出都走这个）
ipcMain.handle('save-file', async (event, { content, defaultName, filters }) => {
  const { canceled, filePath } = await dialog.showSaveDialog({
    defaultPath: defaultName || 'export.txt',
    filters: filters && filters.length ? filters : [{ name: '所有文件', extensions: ['*'] }],
  });
  if (canceled || !filePath) return { ok: false, canceled: true };
  try {
    fs.writeFileSync(filePath, content, 'utf-8');
    return { ok: true, path: filePath };
  } catch (e) {
    return { ok: false, error: String(e) };
  }
});

// 通用打开文件对话框（导入备份用）
ipcMain.handle('open-file', async (event, { filters }) => {
  const { canceled, filePaths } = await dialog.showOpenDialog({
    filters: filters && filters.length ? filters : [{ name: '所有文件', extensions: ['*'] }],
    properties: ['openFile'],
  });
  if (canceled || filePaths.length === 0) return { ok: false, canceled: true };
  try {
    const content = fs.readFileSync(filePaths[0], 'utf-8');
    return { ok: true, content };
  } catch (e) {
    return { ok: false, error: String(e) };
  }
});
