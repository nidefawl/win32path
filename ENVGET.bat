@echo off
@REM run ENV_readini.py and print results
setlocal
SET ENVSET_CALL=-tw -ns %1
if "%~1"=="" ( SET ENVSET_CALL=-tw -ns CLANG)
if "%~1"=="-v" ( echo on & SET ENVSET_CALL=-tw -ns PATH)
FOR /F "usebackq TOKENS=1,* DELIMS==" %%G IN (`%~dp0ENV_readini.py %ENVSET_CALL%`) DO ( echo %%G & echo 			%%H)