[Setup]
AppName=TurboWin
AppVersion=1.0
DefaultDirName={pf}\TurboWin
DefaultGroupName=TurboWin
UninstallDisplayIcon={app}\main.exe
OutputDir=dist
OutputBaseFilename=instalador_TurboWin
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\TurboWin"; Filename: "{app}\main.exe"
Name: "{commondesktop}\TurboWin"; Filename: "{app}\main.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na Área de Trabalho"; GroupDescription: "Ícones:"
