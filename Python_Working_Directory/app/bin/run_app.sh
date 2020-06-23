#!/bin/bash

# the full_path line will always return the location of this .sh file
# app_path assumes the app main dir is one level above the .sh file
# all other paths are set from there
# this script will create a python virtual environment in app/env folder, activate it,
#   install requirements.txt located in the app/env folder,
#   execute the script app.py located in app/bin folder, then deactivate the venv

#full_path=$(pwd) # this pwd command will return the terminal's dir, not the app dir
full_path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
#full_path='/home/chucktucker/Documents/Libraries-and-Resources/Python_Working_Directory/app/bin'
app_path=${full_path//"/bin"/""}
env_path=$app_path"/env"
activ=$env_path"/bin/activate"
req=$env_path"/requirements.txt"
app=$app_path"/bin/app.py"

python3 -m venv $env_path &&
. $activ &&
python3 -m pip install --upgrade pip &&
pip install -r $req &&
python $app &&
deactivate