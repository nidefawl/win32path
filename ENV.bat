@REM print all windows environment variables in a more readable way
@FOR /F "usebackq TOKENS=1,* DELIMS==" %%G IN (`set`) DO @( @echo %%G & @echo 			"%%H" )
