#!/usr/bin/env python3
"""stackfiles.py is a python script that allows the user to combine multiple flat data files
with the same headers into one csv file."""

def stackfiles():
    p=True
    while p:
        try:
            path=str(input('Enter the full path to the files using forward slashes (Ex. D:/Griff/Project_Name/Raw/20200101): '))
            p=False
        except ValueError:
            print('Invalid data entry. Please enter the pathway as a text string.')
    
    pat=True
    while pat:
        try:
            pattern=str(input('Enter the file pattern then press enter: '))
            pat=False
        except ValueError:
            print('Invalid data entry. Please enter the file pattern as a text string.')
    
    filenames = glob(path + '*' + pattern + '*')
    
    mdf=True
    while mdf:
        try:
            dataframes = [pd.read_csv(f, low_memory=False) for f in filenames]
            mdf=False
        except FileNotFoundError:
            print('File ' + f + ' not found.')
        except Exception as e:
            print(type(e), e)
        
    df_complete = pd.concat(dataframes)
    
    return df_complete
    
    

def make_csv(df_complete):
    f=True
    while f:
        try:
            filename=str(input('Enter the full path and name for the new file using forward slashes: '))
            f=False
        except ValueError:
            print('Please enter the filename as a string.')
    
    d=True
    while d:
        try:
            delim=str(input('Enter a delimiter for your new file.'))
            d=False
        except ValueError:
            print('Please use , or | or \t as your delimiter.')
    
    df_complete.to_csv(filename, index=False, sep=delim)
    
def main():
    if 'pd' not in globals():
        import pandas as pd
        
    if 'glob' not in globals():
        from glob import glob
    
    df_complete = stackfiles()
    
    make_csv(df_complete)
        
if __name__ == '__main__':
    main()