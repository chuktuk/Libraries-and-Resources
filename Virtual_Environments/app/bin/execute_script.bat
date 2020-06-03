py -m venv path\to\app\env &&
path\to\app\env\Scripts\activate.bat &&
py -m pip install --upgrade pip &&
pip install -r path\to\app\env\requirements.txt &&
python path\to\app\bin\app.py &&
deactivate