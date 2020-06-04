SETLOCAL
set app_path=C:/Users/CRTUCKER/Documents/Virtual_Environments
set env_path=%app_path%/env
set activ=%env_path%/Scripts/activate.bat
set req=%env_path%/requirements.txt
set app=%app_path%/bin/app.py

py -m venv %env_path% && %activ% && python -m pip install --upgrade pip && pip install -r %req% && python %app%
ENDLOCAL