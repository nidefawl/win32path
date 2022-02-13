@setlocal & echo off
call %~dp0\ENVSET PATH:GNU_UTILS
echo %PATH%|"%GNU_UTILS%\tr" ";" "\n"
