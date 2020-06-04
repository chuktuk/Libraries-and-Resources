SETLOCAL
set app_path=C:\Users\CRTUCKER\Documents\Libraries-and-Resources\Virtual_Environments\app
set env_path=%app_path%\env
set activ=%env_path%\Scripts\activate.bat
set req=%env_path%\requirements.txt
set app=%app_path%\bin\app.py


py -m venv %env_path% &&
%activ% &&
py -m pip install --upgrade pip &&
pip install -r %req% &&
python %app% &&
deactivate

::py -m venv path\to\app\env &&
::path\to\app\env\Scripts\activate.bat &&
::py -m pip install --upgrade pip &&
::pip install -r path\to\app\env\requirements.txt &&
::python path\to\app\bin\app.py &&
::deactivate