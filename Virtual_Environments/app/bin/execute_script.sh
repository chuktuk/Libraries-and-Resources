#!/bin/bash

# works very well on my laptop

# run command
# source execute_script.sh

# update app_path to reuse
# or see Python_Working_Directory for way to always get working dir

app_path='/home/chucktucker/Documents/Libraries-and-Resources/Virtual_Environments/app'
#full_path=$(PWD)
#app_path=${full_path//'/bin'/''}
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


# original code, replaced to use variables
# python3 -m venv /home/chucktucker/Documents/Libraries-and-Resources/Virtual_Environments/app/env &&
# . /home/chucktucker/Documents/Libraries-and-Resources/Virtual_Environments/app/env/bin/activate &&
# python3 -m pip install --upgrade pip &&
# pip install -r /home/chucktucker/Documents/Libraries-and-Resources/Virtual_Environments/app/env/requirements.txt &&
# python /home/chucktucker/Documents/Libraries-and-Resources/Virtual_Environments/app/bin/app.py &&
# deactivate