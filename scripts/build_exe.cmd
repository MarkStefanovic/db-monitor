SET "project=DbMonitor"
@ECHO OFF & SETLOCAL
for %%i in ("%~dp0..") DO SET "folder=%%~fi"
@ECHO ON
del /S /Q "%folder%\dist\"
mkdir "%folder%\dist\assets\"
mkdir "%folder%\dist\log\"
poetry run pyinstaller "%folder%\%project%.spec" --distpath %folder%\dist\ --specpath %folder% --workpath %folder%\build
ECHO F | xcopy /Y "%folder%\config.json" "%folder%\dist\config.json"
xcopy /Y /E "%folder%\assets" "%folder%\dist\assets"
xcopy /Y /E "%folder%\.venv\Lib\site-packages\PyQt5\Qt\plugins\platforms" "%folder%\dist\platforms"