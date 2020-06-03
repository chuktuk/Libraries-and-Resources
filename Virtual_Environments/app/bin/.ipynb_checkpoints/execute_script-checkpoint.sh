#!/bin/bash

# may need to ensure the virtual environment is activated prior to installing requirements.txt

python3 -m venv /home/chucktucker/Documents/Libraries-and-Resources/Virtual_Environments/app/env &&
. /home/chucktucker/Documents/Libraries-and-Resources/Virtual_Environments/app/env/bin/activate &&
python3 -m pip install --upgrade pip &&
pip install -r /home/chucktucker/Documents/Libraries-and-Resources/Virtual_Environments/app/env/requirements.txt &&
python /home/chucktucker/Documents/Libraries-and-Resources/Virtual_Environments/app/bin/app.py &&
deactivate