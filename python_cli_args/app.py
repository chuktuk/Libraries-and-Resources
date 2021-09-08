#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import sys


# main function
def main():
    print(f'There were {len(sys.argv)} arguments supplied')
    for idx, arg in enumerate(sys.argv):
        print(f'Argument {idx:>6}: {arg}')


if __name__ == '__main__':
    main()
