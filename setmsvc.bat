SET ENVSET_CALL=%~1
if "%ENVSET_CALL%"=="" ( SET ENVSET_CALL=MSVC2019)
call %~dp0\ENVSET %ENVSET_CALL%
call "%VCVARS_BAT%" amd64