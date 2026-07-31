[Setup]
AppName=Tasktrack
AppVersion=1.1
DefaultDirName={userdocs}\tasktrack
OutputBaseFilename=tasktrackSetup
SolidCompression=yes
[Files]
Source: tasktrack.exe; DestDir: "{app}"
Source: saved.json; DestDir: "{app}"; DestName: "saved.json"; Flags: onlyifdoesntexist
Source: "main\*"; DestDir: "{app}\main"; Flags: recursesubdirs createallsubdirs
[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; Flags: unchecked
[Icons]
Name: "{group}\tasktrack"; Filename: "{app}\tasktrack.exe"
Name: "{commondesktop}\tasktrack"; Filename: "{app}\tasktrack.exe"
