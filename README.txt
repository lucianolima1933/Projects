# README.TXT
# Copyright © Luciano Lima (luciano.lima1933@gmail.com), 2017-2019
# Crypto Exchange Websocket integration example
# Using a known websocket to receive real time data (we are using BITMEX Websocket and CCXT library (REST)
# the resulting output can be used on backend or front end solutions (100% portable to TKInter or other GUIs)
# Developed by Luciano Lima, 2017-2019
# This is only a piece of the whole solution, displayed here to contribute with Open Source community and Traders
# if you need a full working solution, able to send orders, set-up strategies, etc, fell free to send an e-mail.
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
#   Once the libraries are installed, place the file into a working directory and type:
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
DISCLAIMER:
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.


