# README.TXT
# Crypto Exchange Websocket integration example
# Using a known websocket to receive real time data (we are using BITMEX Websocket and CCXT library (REST)
# the resulting output can be used on backend or front end solutions (100% portable to TKInter or other GUIs)
# Developed by Luciano Lima, 2017-2019
# This Project is an Open Source contribution for the software and traders communities.
# Released under GNU license (read GNU files included)
# luciano.lima1933@gmail.com
#
# REQUIREMENTS:
#   Python 3.6 or superior
#   Make sure you have the following Python libraries installed (use pip3 to install the missing ones):
#   sys
#   locale
#   time
#   websocket
#   curses
#   re
#   ccxt
#   dialog
# 
# EXECUTION
#   Once the libraries are installed, place the file into a directory and type:
#   python3.6 bitmex_websocket_v1.1.py
#
# TIPS
#   1 - You can create a shell script to call the above command line automatically;
#   2 - You can also turn .py scripts executable (search for Python help + your OS help)
#
# IMPROVEMENTS:
#   This project is made to allow a fast and reliable solution to receive Real time data from a crypto exchange
#   However, you can create a scrolling window for Times&Trades and/or Book Level II (Buy & Sell Offers)
#   Also you can adapt this code to Python Graphical Interfaces, scallable to Windows, Linux /Unix and other OS.
##################################################################################################################
