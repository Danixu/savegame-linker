@echo off

SET LANGS=(en es)
SET ROOT=%~dp0\..

for %%I IN %LANGS% DO (
	echo Generating lang %%I...
	
	"%ROOT%\tools\msgfmt.exe" "%ROOT%\lang\%%I\LC_MESSAGES\mainWindow.pot" -o "%ROOT%\lang\%%I\LC_MESSAGES\mainWindow.mo"
	"%ROOT%\tools\msgfmt.exe" "%ROOT%\lang\%%I\LC_MESSAGES\addGame.pot" -o "%ROOT%\lang\%%I\LC_MESSAGES\addGame.mo"
	"%ROOT%\tools\msgfmt.exe" "%ROOT%\lang\%%I\LC_MESSAGES\options.pot" -o "%ROOT%\lang\%%I\LC_MESSAGES\options.mo"
)

pause