SETLOCAL
set app_path=D:/ChuckTucker/Documents/CompSci/Libraries-and-Resources/Virtual_Environments/app
set env_path=%app_path%/env
set activ=%env_path%/Scripts/activate.bat
set req=%env_path%/requirements.txt
set app=%app_path%/bin/app.py


py -m venv %env_path% && %activ% && py -m pip install --upgrade pip && pip install -r %req% && python %app% && deactivate
ENDLOCAL