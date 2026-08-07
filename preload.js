const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  exportBackup: (jsonStr) => ipcRenderer.invoke('export-backup', jsonStr),
  importBackup: () => ipcRenderer.invoke('import-backup'),
});
