#!/bin/bash

# testing with pwd command to get directory

#app_path='/home/chucktucker/Documents/Libraries-and-Resources/Virtual_Environments/app'
full_path=$(PWD)
app_path=${full_path//'/bin'/''}
env_path=$app_path'/env'
activ=$env_path'/bin/activate'
req=$env_path'/requirements.txt'
app=$app_path'/bin/app.py'

python3 -m venv $env_path &&
. $activ &&
python3 -m pip install --upgrade pip &&
pip install -r $req &&
python $app &&
deactivate