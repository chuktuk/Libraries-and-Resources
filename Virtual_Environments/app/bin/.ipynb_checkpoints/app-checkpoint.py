#!/usr/bin/env python3
'''This module will only print success if pyglet can be imported.
pyglet is not installed in my base environment but will be setup
in the virtual environment.

I realized that all of setup_venv.py can be executed in the
.bat or .sh script. Moving there simplifies this. setup_venv.py is
redundant at this point and not needed.

To use this:

Windows: 
1. you need to edit the path\to\app in the bin/execute_script.bat file
3. run the execute_script.bat file from the cmd prompt.

Linux:
1. you need to edit the path\to\app in the bin/execute_script.sh file
3. run the execute_script.bat file from the terminal.
'''

import pyglet

def main():
    print('Success!')
    
if __name__ == '__main__':
    main()