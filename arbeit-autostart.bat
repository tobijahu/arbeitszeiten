@echo off

if not "%1" == "max" start cmd /c %0 max & exit/b



:: Befehle ab hier werden im geöffneter cmd.exe ausgeführt

arbeitcli.py



pause
