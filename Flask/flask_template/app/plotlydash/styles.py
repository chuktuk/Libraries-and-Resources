#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The dash applications are not applying appropriate styles from static/styles.css using classes.

This module provides a python class to access the style information in a form that Dash recognizes."""


class Styles:
    def __init__(self):
        self.__repr__ = 'Custom css styles for dash app.'
        self.title_text = {
            'color':  '#191970'
        }
        self.sidebar_single_page = {
            'top': 0,
            'left': 0,
            'bottom': 0,
            'width': '20%',
            'padding': '20px 10px',
            'background-color': '#f8f9fa'
        }
        self.sidebar_multi_page = {
            'background-color':  '#f8f9fa'
        }
        self.dash_title_text = {
            'textAlign': 'center',
            'color':  '#191970',
            'margin-top': '30px',
            'margin-bottom': '20px'
        }
        self.dash_content = {
            'margin-left': '25%',
            'margin-right': '5%',
            'top': 0,
            'padding': '20px 10px'
        }
        self.dash_text = {
            'textAlign': 'center',
            'color':  '#191970'
        }
        self.dash_card_text = {
            'textAlign': 'center',
            'color':  '#0074D9'
        }
