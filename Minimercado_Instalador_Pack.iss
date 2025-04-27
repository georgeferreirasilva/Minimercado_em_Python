[Setup]
AppName=Sistema de Minimercado
AppVersion=1.0
DefaultDirName=C:\Program Files\Minimercado\Sistema de Minimercado
DefaultGroupName=Minimercado
LicenseFile=licenca.txt
WizardImageFile=splash.bmp
WizardSmallImageFile=splash.bmp
SetupIconFile=icone.ico
WizardStyle=modern
UsePreviousAppDir=no
Compression=lzma
SolidCompression=yes
OutputBaseFilename=MinimercadoSetup
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
;WizardImageBackColor=$00C0C0FF
;Password=mercado2025  
; << Senha para instalação mercado2025

[Files]
Source: "dist\\minimercado_tkinter.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Sistema de Minimercado"; Filename: "{app}\minimercado_tkinter.exe"
Name: "{userdesktop}\Sistema de Minimercado"; Filename: "{app}\minimercado_tkinter.exe"; Flags: createonlyiffileexists
Name: "{group}\Desinstalar Sistema de Minimercado"; Filename: "{uninstallexe}"

[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar ícone na Área de Trabalho"; GroupDescription: "Opções adicionais:"

[Run]
;Filename: "https://seusite.com.br"; Description: "Visitar nosso site"; Flags: shellexec postinstall skipifsilent
Filename: "{app}\\minimercado_tkinter.exe"; Description: "Executar Sistema agora"; Flags: nowait postinstall skipifsilent
Filename: "{sys}\\cmd.exe"; Parameters: "/c echo ^G"; StatusMsg: "Finalizando instalação..."; Flags: runhidden

[Messages]
WelcomeLabel1=Bem-vindo ao Instalador do Sistema de Minimercado!
WelcomeLabel2=Este assistente irá instalar o Sistema de Minimercado no seu computador.
;WelcomeLabel3=Clique em Avançar para continuar.
FinishedLabel=Sistema de Minimercado instalado com sucesso! Obrigado!
