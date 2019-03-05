@echo off

SET LANGS=(en es)
SET ROOT=%~dp0\..

for %%I IN %LANGS% DO (
	echo Generating lang %%I...
	
	for /f "delims=" %%J in ('dir /b /s "%ROOT%\lang\%%I\*.pot"') DO (
		IF EXIST "%ROOT%\lang\%%I\LC_MESSAGES\globals.pot" (
			"%ROOT%\tools\msgcat.exe" --no-location --use-first "%ROOT%\lang\%%I\LC_MESSAGES\globals.pot" "%%J" -o "%ROOT%\lang\%%I\LC_MESSAGES\globals.pot"
		) else (
			"%ROOT%\tools\msgcat.exe" --no-location "%%J" -o "%ROOT%\lang\%%I\LC_MESSAGES\globals.pot"
		)
	)
	"%ROOT%\tools\msgfmt.exe" "%ROOT%\lang\%%I\LC_MESSAGES\globals.pot" -o "%ROOT%\lang\%%I\LC_MESSAGES\globals.mo"
	del "%ROOT%\lang\%%I\LC_MESSAGES\globals.pot"
)

pause