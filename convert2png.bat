@echo off
setlocal
PATH=C:\Program Files\ImageMagick-7.1.0-Q16;%PATH%
@echo on
@REM magick.exe convert -background none -size 512x512 %1 -define icon:auto-resize="256,128,96,64,48,32,16" %2
magick.exe convert -background none %*
