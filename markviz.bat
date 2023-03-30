@echo off
REM visualize RDF in web browser

setlocal
if "%1" == "" goto :usage
set HOMEDIR=%~dp0
set OUTFILE=%HOMEDIR%\markviz.htm
python %HOMEDIR%\markviz.py %1 > %OUTFILE% && start %OUTFILE%
goto :eof

:usage
echo.
echo   Visuzlize an RDF file in a web browser
echo.
echo   usage: %~n0 ^<RDF_Turtle_file^>
echo.

