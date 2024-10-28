// main.js
const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');

let mainWindow; // 声明主窗口变量

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        frame: true,
        autoHideMenuBar: true, 
        resizable: false,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        },
    });

    mainWindow.loadFile(path.join(__dirname, 'index.html'));

    // 监听打开文件对话框的请求
    ipcMain.on('open-file-dialog', (event, index) => {
        dialog.showOpenDialog({ // 移除 parent 选项
            properties: ['openFile']
        }).then(result => {
            if (!result.canceled) {
                event.reply('selected-file', result.filePaths[0], index); // 发送所选文件路径和按钮编号
            }
        }).catch(err => {
            console.log(err);
        });
    });

    ipcMain.on('open-new-window', () => {
        const newWindow = new BrowserWindow({
            width: 800,
            height: 600,
            frame: false,
            resizable: false,
            webPreferences: {
                nodeIntegration: true,
                contextIsolation: false,
            },
        });
    
        newWindow.loadFile('frontend/process_gradio.html'); // 加载新的 HTML 文件
    });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
});


