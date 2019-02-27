@echo off
FOR /F "tokens=* USEBACKQ" %%F IN (`where python`) DO (
	SET pythonFolder=%%~dpF
)

SET LANGS=(en es)
SET ROOT=%~dp0\..


python "%pythonFolder%\Tools\i18n\pygettext.py" -d mainWindow -o "%ROOT%\lang\mainWindow.pot" "%ROOT%\mainWindow.pyw"
REM python "%pythonFolder%\Tools\i18n\pygettext.py" -d globals -o "%ROOT%\lang\globals.pot" "%ROOT%\globals.py"
REM python "%pythonFolder%\Tools\i18n\pygettext.py" -d CheckListCtrl -o "%ROOT%\lang\CheckListCtrl.pot" "%ROOT%\widgets\CheckListCtrl.py"
REM python "%pythonFolder%\Tools\i18n\pygettext.py" -d ShapedButton -o "%ROOT%\lang\ShapedButton.pot" "%ROOT%\widgets\ShapedButton.py"
python "%pythonFolder%\Tools\i18n\pygettext.py" -d addGame -o "%ROOT%\lang\addGame.pot" "%ROOT%\windows\addGame.py"
python "%pythonFolder%\Tools\i18n\pygettext.py" -d options -o "%ROOT%\lang\options.pot" "%ROOT%\windows\options.py"

for %%I IN %LANGS% DO (
	echo Generating lang %%I...
	
	if exist "%ROOT%\lang\%%I\LC_MESSAGES\mainWindow.pot" (
		ren "%ROOT%\lang\%%I\LC_MESSAGES\mainWindow.pot" "mainWindow.pot.old"
		"%ROOT%\tools\msgcat.exe" --use-first --no-location "%ROOT%\lang\%%I\LC_MESSAGES\mainWindow.pot.old" "%ROOT%\lang\mainWindow.pot" -o "%ROOT%\lang\%%I\LC_MESSAGES\mainWindow.pot"
		del "%ROOT%\lang\%%I\LC_MESSAGES\mainWindow.pot.old"
	) else (
		"%ROOT%\tools\msgcat.exe" --use-first --no-location "%ROOT%\lang\mainWindow.pot" -o "%ROOT%\lang\%%I\LC_MESSAGES\mainWindow.pot"
	)
	
	REM if exist "%ROOT%\lang\%%I\LC_MESSAGES\globals.pot" (
		REM ren "%ROOT%\lang\%%I\LC_MESSAGES\globals.pot" "globals.pot.old"
		REM "%ROOT%\tools\msgcat.exe" --use-first --no-location "%ROOT%\lang\%%I\LC_MESSAGES\globals.pot.old" "%ROOT%\lang\globals.pot" -o "%ROOT%\lang\%%I\LC_MESSAGES\globals.pot"
		REM del "%ROOT%\lang\%%I\LC_MESSAGES\globals.pot.old"
	REM ) else (
		REM "%ROOT%\tools\msgcat.exe" --use-first --no-location "%ROOT%\lang\globals.pot" -o "%ROOT%\lang\%%I\LC_MESSAGES\globals.pot"
	REM )
	
	REM if exist "%ROOT%\lang\%%I\LC_MESSAGES\CheckListCtrl.pot" (
		REM ren "%ROOT%\lang\%%I\LC_MESSAGES\CheckListCtrl.pot" "CheckListCtrl.pot.old"
		REM "%ROOT%\tools\msgcat.exe" --use-first --no-location "%ROOT%\lang\%%I\LC_MESSAGES\CheckListCtrl.pot.old" "%ROOT%\lang\CheckListCtrl.pot" -o "%ROOT%\lang\%%I\LC_MESSAGES\CheckListCtrl.pot"
		REM del "%ROOT%\lang\%%I\LC_MESSAGES\CheckListCtrl.pot.old"
	REM ) else (
		REM "%ROOT%\tools\msgcat.exe" --use-first --no-location "%ROOT%\lang\CheckListCtrl.pot" -o "%ROOT%\lang\%%I\LC_MESSAGES\CheckListCtrl.pot"
	REM )
	
	REM if exist "%ROOT%\lang\%%I\LC_MESSAGES\ShapedButton.pot" (
		REM ren "%ROOT%\lang\%%I\LC_MESSAGES\ShapedButton.pot" "ShapedButton.pot.old"
		REM "%ROOT%\tools\msgcat.exe" --use-first --no-location "%ROOT%\lang\%%I\LC_MESSAGES\ShapedButton.pot.old" "%ROOT%\lang\ShapedButton.pot" -o "%ROOT%\lang\%%I\LC_MESSAGES\ShapedButton.pot"
		REM del "%ROOT%\lang\%%I\LC_MESSAGES\ShapedButton.pot.old"
	REM ) else (
		REM "%ROOT%\tools\msgcat.exe" --use-first --no-location "%ROOT%\lang\ShapedButton.pot" -o "%ROOT%\lang\%%I\LC_MESSAGES\ShapedButton.pot"
	REM )
	
	if exist "%ROOT%\lang\%%I\LC_MESSAGES\addGame.pot" (
		ren "%ROOT%\lang\%%I\LC_MESSAGES\addGame.pot" "addGame.pot.old"
		"%ROOT%\tools\msgcat.exe" --use-first --no-location "%ROOT%\lang\%%I\LC_MESSAGES\addGame.pot.old" "%ROOT%\lang\addGame.pot" -o "%ROOT%\lang\%%I\LC_MESSAGES\addGame.pot"
		del "%ROOT%\lang\%%I\LC_MESSAGES\addGame.pot.old"
	) else (
		"%ROOT%\tools\msgcat.exe" --use-first --no-location "%ROOT%\lang\addGame.pot" -o "%ROOT%\lang\%%I\LC_MESSAGES\addGame.pot"
	)
	
	if exist "%ROOT%\lang\%%I\LC_MESSAGES\options.pot" (
		ren "%ROOT%\lang\%%I\LC_MESSAGES\options.pot" "options.pot.old"
		"%ROOT%\tools\msgcat.exe" --use-first --no-location "%ROOT%\lang\%%I\LC_MESSAGES\options.pot.old" "%ROOT%\lang\options.pot" -o "%ROOT%\lang\%%I\LC_MESSAGES\options.pot"
		del "%ROOT%\lang\%%I\LC_MESSAGES\options.pot.old"
	) else (
		"%ROOT%\tools\msgcat.exe" --use-first --no-location "%ROOT%\lang\options.pot" -o "%ROOT%\lang\%%I\LC_MESSAGES\options.pot"
	)
)

del "%ROOT%\lang\mainWindow.pot"
REM del "%ROOT%\lang\globals.pot"
REM del "%ROOT%\lang\CheckListCtrl.pot"
REM del "%ROOT%\lang\ShapedButton.pot"
del "%ROOT%\lang\addGame.pot"
del "%ROOT%\lang\options.pot"

pause