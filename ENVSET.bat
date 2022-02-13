@echo off
@REM run ENV_readini.py and set all environment variables
SET ENVSET_CALL=-tw -ns %1
if "%~1"=="" ( SET ENVSET_CALL=-tw -ns CLANG)
if "%~1"=="-v" ( echo on & SET ENVSET_CALL=-tw -ns %~2)
FOR /F "usebackq TOKENS=1,* DELIMS==" %%G IN (`python %~dp0\ENV_readini.py %ENVSET_CALL%`) DO ( set %%G=%%~H)
