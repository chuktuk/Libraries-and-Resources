SET LOCAL
SETLOCAL
set full_path=%~dp0
set app_path=%full_path:\bin\=%
set env_path=%app_path%\env
set activ=%env_path%\Scripts\activate.bat
set req=%env_path%\requirements.txt
set app=%app_path%\bin\app.py

echo %full_path% && echo %app_path% && echo %env_path% && echo %activ% && echo %req% && echo %app%
ENDLOCAL