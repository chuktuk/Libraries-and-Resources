#!/usr/bin/env python3
'''This module will only print success if pyglet can be imported.
pyglet is not installed in my base environment but will be setup
in the virtual environment.

I realized that all of setup_venv.py can be executed in the
.bat or .sh script. Moving there simplifies this. setup_venv.py is
redundant at this point and not needed. Possibly. Actually having
issues running this in Windows now. May need to use this with 
execute_script2.bat (may also need to change between activate.ps1
and activate.bat depending on the system or where the execute_script
is run (terminal vs. powershell prompt)).

I have also noticed nuances with needing deactivate or not at the end of
the .bat script. If running from conda prompt, yes needed. 

To use this:

Windows: 
1. you need to edit the path\to\app in the appropriate .bat file
2. you need to edit the working_directory in env/setup_venv.py file (if using execute_script2.bat)
3. uses
    - execute_script.bat will work in conda/powershell type environments, though nuances with .bat vs .ps1
    - setup_venv_run_script.bat is the best option, and works from cmd prompt starting in any directory
        - just set the path\to\app in the .bat file first

Linux:
1. you need to edit the path/to/app in the bin/execute_script.sh file
2. can test using variables now
3. run the execute_script.bat file from the terminal.

old execute_script.py code
py -m venv path\to\app\env &&
path\to\app\env\Scripts\activate.bat &&
py -m pip install --upgrade pip &&
pip install -r path\to\app\env\requirements.txt &&
python path\to\app\bin\app.py &&
deactivate
'''

import pyglet

def main():
    print('Success!')
    
if __name__ == '__main__':
    main()