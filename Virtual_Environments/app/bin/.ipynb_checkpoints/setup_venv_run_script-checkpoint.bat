SETLOCAL
set full_path=%~dpo
set app_path=%full_path:\bin\=%
set env_path=%app_path%\env
set activ=%env_path%\Scripts\activate.bat
set req=%env_path%\requirements.txt
set app=%app_path%\bin\app.py

py -m venv %env_path% && %activ% && python -m pip install --upgrade pip && pip install -r %req% && python %app%
ENDLOCAL