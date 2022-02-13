setlocal
set GIT_ASK_YESNO=C:/Program Files/Git/mingw64/libexec/git-core/git-gui--askyesno
set GIT_ASKPASS=C:/Program Files/Git/mingw64/libexec/git-core/git-gui--askpass
set SSH_ASKPASS=C:/Program Files/Git/mingw64/libexec/git-core/git-gui--askpass
set PLINK_PROTOCOL=ssh
@REM set GIT_DIR=C:/dev/vscode-extension-development/vscode/.git
@REM set GIT_WORK_TREE=C:/dev/vscode-extension-development/vscode
set HOME=C:\Users\Michael
set PATH=C:\Program Files\Git\bin;C:\Program Files\Git\usr\bin;%PATH%
@REM "C:\Program Files\Git\mingw64\bin\wish.exe" "C:\Program Files\Git\mingw64\libexec\git-core\git-gui" -- "--working-dir" "C:\dev\vscode-extension-development\vscode\build."
start "" "C:\Program Files\Git\mingw64\bin\wish.exe" "C:/Program Files/Git/mingw64/bin/gitk" %1
endlocal