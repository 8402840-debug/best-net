const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  saveFile: (content, defaultName, filters) =>
    ipcRenderer.invoke('save-file', { content, defaultName, filters }),
  openFile: (filters) => ipcRenderer.invoke('open-file', { filters }),
});
