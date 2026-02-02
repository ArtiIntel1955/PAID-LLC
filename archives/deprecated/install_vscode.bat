@echo off
echo Installing Visual Studio Code...

REM Download the VS Code installer
powershell -Command "Invoke-WebRequest -Uri 'https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user' -OutFile 'vscode_installer.exe' -Headers @{'Referer'='https://code.visualstudio.com/'}"

REM Run the installer silently
if exist "vscode_installer.exe" (
    echo Running VS Code installer...
    start /wait vscode_installer.exe /VERYSILENT /NORESTART
    del vscode_installer.exe
    echo VS Code installation completed.
) else (
    echo Failed to download VS Code installer.
)

pause