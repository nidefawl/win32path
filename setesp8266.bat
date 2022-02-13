@echo on
set ENABLE_GDB=0
set WIFI_PWD=asdfasdf
set WIFI_SSID=ddwrt
set DEBUG_VERBOSE_LEVEL=1
set COM_PORT=COM7
set COM_SPEED=115200
set COM_SPEED_SERIAL=115200
set SERIAL_BAUD_RATE=115200
SET ESP_HOME=C:\dev\esp8266
SET SMING_HOME=C:\dev\esp8266\Sming\Sming
@REM NOTE: path was set to 32bit python
SET PATH=C:\dev\esp8266\MinGW\bin;C:\dev\esp8266\MinGW\msys\1.0\bin;C:\Program Files\Git\cmd;C:\Python310\Scripts\;C:\Python310\;%~dp0;C:\Windows\System32;C:\Windows;C:\Windows\System32\OpenSSH
set COM_PORT_ESPTOOL=COM7
set COM_SPEED_ESPTOOL=460800
SET CC=gcc
SET CXX=g++