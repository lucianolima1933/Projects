# bitmex_websocket_v1.1.py
# an evolution of bitmex_data2py script
# it works with BitMEX Websocket to display data, ccxt, curses and dialog libraries
# developed by Luciano Lima 2018, 2019
#  --- Recent Updates log: ---
#  --- 27-02-2019: including Chart Data (using CCXT OHLC for 3mins and current trading Day), amplitude and frequency
#  --- 20-03-2019: allowing user to choose environment 1:Prod 2:Testnet
#  --- 16-04-2019: added error treatment on CCXT, fixing book LII data
#  --- 23-06-2019: adjustments to accomodate more digits in screen, as the price rose to >10k
#  ---
# Copyright © Luciano Lima (luciano.lima1933@gmail.com), 2017-2019
# Crypto Exchange Websocket integration example
# Using a known websocket to receive real time data (we are using BITMEX Websocket and CCXT library (REST)
# the resulting output can be used on backend or front end solutions (100% portable to TKInter or other GUIs)
# Developed by Luciano Lima, 2017-2019
# This Project is an Open Source contribution for the software and traders communities.
# Released under GNU license (read GNU files included)
# luciano.lima1933@gmail.com
#
# Standard Modules to be used
import sys
import locale
import time
import websocket
import curses
import re
import ccxt
from dialog import Dialog
try:
    import thread
except ImportError:
    import _thread as thread
from threading import Thread

locale.setlocale(locale.LC_ALL,'')     # following best practices to start the program !

# Dialog Box to ask user which environment to work (Prod or Testnet):
e = Dialog(dialog="dialog")
code1, mvalor2 = e.menu("Select the environment:",
                         choices=[("(1)", "Production Enviroment"),
                                  ("(2)", "TESTNET Environment")])

e.infobox("Environment is: %s" % mvalor2,None,None)


# Dialog Box to inform user about desired Asset to monitor:
d = Dialog(dialog="dialog")
code, mvalor1 = d.inputbox("Enter the asset name (default XBTUSD):",init="XBTUSD",title="BITMEX DATA - Inform the Asset")
d.infobox("Asset is: %s" % mvalor1,None,None)

# declaring global variables to use in websocket messages
msgtrade1time = ""
msgtrade1side = ""
msgtrade1size = ""
msgtrade1price = ""
msgtrade2time = ""
msgtrade2side = ""
msgtrade2size = ""
msgtrade2price = ""
msgtrade3time = ""
msgtrade3side = ""
msgtrade3size = ""
msgtrade3price = ""
msgtrade4time = ""
msgtrade4side = ""
msgtrade4size = ""
msgtrade4price = ""
msgtrade5time = ""
msgtrade5side = ""
msgtrade5size = ""
msgtrade5price = ""
msgtrade6time = ""
msgtrade6side = ""
msgtrade6size = ""
msgtrade6price = ""
msgtrade7time = ""
msgtrade7side = ""
msgtrade7size = ""
msgtrade7price = ""
msgtrade8time = ""
msgtrade8side = ""
msgtrade8size = ""
msgtrade8price = ""
msgtrade9time = ""
msgtrade9side = ""
msgtrade9size = ""
msgtrade9price = ""
msgtrade10time = ""
msgtrade10side = ""
msgtrade10size = ""
msgtrade10price = ""

msgbookbid1size = ""
msgbookbid1price= ""
msgbookask1size = ""
msgbookask1price = ""
msgbookbid2size = ""
msgbookbid2price= ""
msgbookask2size = ""
msgbookask2price = ""
msgbookbid3size = ""
msgbookbid3price= ""
msgbookask3size = ""
msgbookask3price = ""
msgbookbid4size = ""
msgbookbid4price= ""
msgbookask4size = ""
msgbookask4price = ""
msgbookbid5size = ""
msgbookbid5price= ""
msgbookask5size = ""
msgbookask5price = ""
msgbookbid6size = ""
msgbookbid6price= ""
msgbookask6size = ""
msgbookask6price = ""
msgbookbid7size = ""
msgbookbid7price= ""
msgbookask7size = ""
msgbookask7price = ""
msgbookbid8size = ""
msgbookbid8price= ""
msgbookask8size = ""
msgbookask8price = ""
msgbookbid9size = ""
msgbookbid9price= ""
msgbookask9size = ""
msgbookask9price = ""
msgbookbid10size = ""
msgbookbid10price= ""
msgbookask10size = ""
msgbookask10price = ""
# BitMEX candle data/chart data parameters:
if mvalor1 == "XBTUSD":
   symbol = "%s" % "BTC/USD"
else:
   symbol = "%s" % mvalor1

timeframe = '1m'
limit = 100
params = {'partial': False}   # <---------- no reversal
mbitmex = ccxt.bitmex ()

#f = open("times_and_trades_log.txt","a+")

def get_num_from_string(string):
    # This function retrieves numbers from a string and converts them to integers
    # Create empty string to store numbers as a string
    num =''
    # Loop through caracters in the string
    for i in string:
        # If one of the characters is a number, add it to the empty string
        if i in '1234567890':
            num+=i
    # Convert the string of numbers to an integer
    integer = int(num)
    return(integer)

# ============================== import from websocket script
# 26/02/2019 - important modification in 'on_message' function
# here, the message of websocket streamline will be broken and parsed
def on_message(ws, message):
    global msgtrade1time, msgtrade1side, msgtrade1size, msgtrade1price
    global msgtrade2time, msgtrade2side, msgtrade2size, msgtrade2price
    global msgtrade3time, msgtrade3side, msgtrade3size, msgtrade3price
    global msgtrade4time, msgtrade4side, msgtrade4size, msgtrade4price
    global msgtrade5time, msgtrade5side, msgtrade5size, msgtrade5price
    global msgtrade6time, msgtrade6side, msgtrade6size, msgtrade6price
    global msgtrade7time, msgtrade7side, msgtrade7size, msgtrade7price
    global msgtrade8time, msgtrade8side, msgtrade8size, msgtrade8price
    global msgtrade9time, msgtrade9side, msgtrade9size, msgtrade9price
    global msgtrade10time, msgtrade10side, msgtrade10size, msgtrade10price

    global msgbookbid1size, msgbookbid1price, msgbookask1size,msgbookask1price
    global msgbookbid2size, msgbookbid2price, msgbookask2size,msgbookask2price
    global msgbookbid3size, msgbookbid3price, msgbookask3size,msgbookask3price
    global msgbookbid4size, msgbookbid4price, msgbookask4size,msgbookask4price
    global msgbookbid5size, msgbookbid5price, msgbookask5size,msgbookask5price
    global msgbookbid6size, msgbookbid6price, msgbookask6size,msgbookask6price
    global msgbookbid7size, msgbookbid7price, msgbookask7size,msgbookask7price
    global msgbookbid8size, msgbookbid8price, msgbookask8size,msgbookask8price
    global msgbookbid9size, msgbookbid9price, msgbookask9size,msgbookask9price
    global msgbookbid10size, msgbookbid10price, msgbookask10size,msgbookask10price

    message1 = re.split(',',str(message))
    if "trade" in message1[0]:
       msgtradelen=len(message1)
       if "insert" in message1[1]:
           msgtrade1time=message1[2][-14:] 			#timestamp
           msgtrade1side=message1[4][-5:]			#side
           msgtrade1size=re.sub('[^0-9]', '', message1[5])  	#size
           msgtrade1price=re.sub('[^0-9.]', '', message1[6])    #price
           #f.write(str(msgtrade1time) +  " "  + str(msgtrade1side) + " " + str(msgtrade1size) + " " + str(msgtrade1price) + "\n")
           if msgtradelen > 13:
              msgtrade2time=message1[12][-14:]                  #timestamp
              msgtrade2side=message1[14][-5:]                   #side
              msgtrade2size=re.sub('[^0-9]', '', message1[15]) 	#size
              msgtrade2price=re.sub('[^0-9.]', '', message1[16])    #price
              #f.write(str(msgtrade2time) +  " "  + str(msgtrade2side) + " " + str(msgtrade2size) + " " + str(msgtrade2price) + "\n")
           if msgtradelen > 23:
              msgtrade3time=message1[22][-14:]                  #timestamp
              msgtrade3side=message1[24][-5:]                   #side
              msgtrade3size=re.sub('[^0-9]', '', message1[25]) 	#size
              msgtrade3price=re.sub('[^0-9.]', '', message1[26])    #price
              #f.write(str(msgtrade3time) +  " "  + str(msgtrade3side) + " " + str(msgtrade3size) + " " + str(msgtrade3price) + "\n")
           if msgtradelen > 33:
              msgtrade4time=message1[32][-14:]                  #timestamp
              msgtrade4side=message1[34][-5:]                   #side
              msgtrade4size=re.sub('[^0-9]', '', message1[35]) 	#size
              msgtrade4price=re.sub('[^0-9.]', '', message1[36])    #price
              #f.write(str(msgtrade4time) +  " "  + str(msgtrade4side) + " " + str(msgtrade4size) + " " + str(msgtrade4price) + "\n")
           if msgtradelen > 43:
              msgtrade5time=message1[42][-14:]                  #timestamp
              msgtrade5side=message1[44][-5:]                   #side
              msgtrade5size=re.sub('[^0-9]', '', message1[45]) 	#size
              msgtrade5price=re.sub('[^0-9.]', '', message1[46])    #price
              #f.write(str(msgtrade5time) +  " "  + str(msgtrade5side) + " " + str(msgtrade5size) + " " + str(msgtrade5price) + "\n")
           if msgtradelen > 53:
              msgtrade6time=message1[52][-14:]                  #timestamp
              msgtrade6side=message1[54][-5:]                   #side
              msgtrade6size=re.sub('[^0-9]', '', message1[55]) 	#size
              msgtrade6price=re.sub('[^0-9.]', '', message1[56])    #price
              #f.write(str(msgtrade6time) +  " "  + str(msgtrade6side) + " " + str(msgtrade6size) + " " + str(msgtrade6price) + "\n")
           if msgtradelen > 63:
              msgtrade7time=message1[62][-14:]                  #timestamp
              msgtrade7side=message1[64][-5:]                   #side
              msgtrade7size=re.sub('[^0-9]', '', message1[65]) 	#size
              msgtrade7price=re.sub('[^0-9.]', '', message1[66])    #price
              #f.write(str(msgtrade7time) +  " "  + str(msgtrade7side) + " " + str(msgtrade7size) + " " + str(msgtrade7price) + "\n")
           if msgtradelen > 73:
              msgtrade8time=message1[72][-14:]                  #timestamp
              msgtrade8side=message1[74][-5:]                   #side
              msgtrade8size=re.sub('[^0-9]', '', message1[75]) 	#size
              msgtrade8price=re.sub('[^0-9.]', '', message1[76])    #price
              #f.write(str(msgtrade8time) +  " "  + str(msgtrade8side) + " " + str(msgtrade8size) + " " + str(msgtrade8price) + "\n")
           if msgtradelen > 83:
              msgtrade9time=message1[82][-14:]                  #timestamp
              msgtrade9side=message1[84][-5:]                   #side
              msgtrade9size=re.sub('[^0-9]', '', message1[85]) 	#size
              msgtrade9price=re.sub('[^0-9.]', '', message1[86])    #price
              #f.write(str(msgtrade9time) +  " "  + str(msgtrade9side) + " " + str(msgtrade9size) + " " + str(msgtrade9price) + "\n")
           if msgtradelen > 93:
              msgtrade10time=message1[92][-14:]                  #timestamp
              msgtrade10side=message1[94][-5:]                   #side
              msgtrade10size=re.sub('[^0-9]', '', message1[95]) 	#size
              msgtrade10price=re.sub('[^0-9.]', '', message1[96])    #price
              #f.write(str(msgtrade10time) +  " "  + str(msgtrade10side) + " " + str(msgtrade10size) + " " + str(msgtrade10price) + "\n")


    elif "orderBook10" in message1[0]:
        if "update" in message1[1] and "bids" in message1[3]:
           #populate bids
           msgbookbid1size=re.sub('[^0-9]', '', message1[4])
           msgbookbid1price=re.sub('[^0-9.]', '', message1[3])
           msgbookbid2size=re.sub('[^0-9]', '', message1[6])
           msgbookbid2price=re.sub('[^0-9.]', '', message1[5])
           msgbookbid3size=re.sub('[^0-9]', '', message1[8])
           msgbookbid3price=re.sub('[^0-9.]', '', message1[7])
           msgbookbid4size=re.sub('[^0-9]', '', message1[10])
           msgbookbid4price=re.sub('[^0-9.]', '', message1[9])
           msgbookbid5size=re.sub('[^0-9]', '', message1[12])
           msgbookbid5price=re.sub('[^0-9.]', '', message1[11])
           msgbookbid6size=re.sub('[^0-9]', '', message1[14])
           msgbookbid6price=re.sub('[^0-9.]', '', message1[13])
           msgbookbid7size=re.sub('[^0-9]', '', message1[16])
           msgbookbid7price=re.sub('[^0-9.]', '', message1[15])
           msgbookbid8size=re.sub('[^0-9]', '', message1[18])
           msgbookbid8price=re.sub('[^0-9.]', '', message1[17])
           msgbookbid9size=re.sub('[^0-9]', '', message1[20])
           msgbookbid9price=re.sub('[^0-9.]', '', message1[19])
           msgbookbid10size=re.sub('[^0-9]', '', message1[22])
           msgbookbid10price=re.sub('[^0-9.]', '', message1[21])
           #populate asks
           if "asks" in message1[24]:
              msgbookask1size=re.sub('[^0-9]', '', message1[25])
              msgbookask1price=re.sub('[^0-9.]', '', message1[24])
              msgbookask2size=re.sub('[^0-9]', '', message1[27])
              msgbookask2price=re.sub('[^0-9.]', '', message1[26])
              msgbookask3size=re.sub('[^0-9]', '', message1[29])
              msgbookask3price=re.sub('[^0-9.]', '', message1[28])
              msgbookask4size=re.sub('[^0-9]', '', message1[31])
              msgbookask4price=re.sub('[^0-9.]', '', message1[30])
              msgbookask5size=re.sub('[^0-9]', '', message1[33])
              msgbookask5price=re.sub('[^0-9.]', '', message1[32])
              msgbookask6size=re.sub('[^0-9]', '', message1[35])
              msgbookask6price=re.sub('[^0-9.]', '', message1[34])
              msgbookask7size=re.sub('[^0-9]', '', message1[37])
              msgbookask7price=re.sub('[^0-9.]', '', message1[36])
              msgbookask8size=re.sub('[^0-9]', '', message1[39])
              msgbookask8price=re.sub('[^0-9.]', '', message1[38])
              msgbookask9size=re.sub('[^0-9]', '', message1[41])
              msgbookask9price=re.sub('[^0-9.]', '', message1[40])
              msgbookask10size=re.sub('[^0-9]', '', message1[43])
              msgbookask10price=re.sub('[^0-9.]', '', message1[42])

    return

def on_error(ws, error):
    print(error)
    return

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
        #time.sleep(1)
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())
# ================================== end of import

def call_websocket():
    global mvalor2
    if mvalor2 == "(1)":		# Prod environment
       #websocket.enableTrace(True)
       ws = websocket.WebSocketApp("wss://www.bitmex.com/realtime?subscribe=instrument,orderBook10:" + mvalor1 + ",trade:" + mvalor1,
                                    on_message = on_message,
                                    on_error = on_error,
                                    on_close = on_close)
    elif mvalor2 == "(2)":		# TESTNET Environment
         ws = websocket.WebSocketApp("wss://testnet.bitmex.com/realtime?subscribe=instrument,orderBook10:" + mvalor1 + ",trade:" + mvalor1,
                                      on_message = on_message,
                                      on_error = on_error,
                                      on_close = on_close)


    ws.run_forever()

    return

# main screen
def main(screen):
    global msgtrade1time, msgtrade1side, msgtrade1size, msgtrade1price
    global msgtrade2time, msgtrade2side, msgtrade2size, msgtrade2price
    global msgtrade3time, msgtrade3side, msgtrade3size, msgtrade3price
    global msgtrade4time, msgtrade4side, msgtrade4size, msgtrade4price
    global msgtrade5time, msgtrade5side, msgtrade5size, msgtrade5price
    global msgtrade6time, msgtrade6side, msgtrade6size, msgtrade6price
    global msgtrade7time, msgtrade7side, msgtrade7size, msgtrade7price
    global msgtrade8time, msgtrade8side, msgtrade8size, msgtrade8price
    global msgtrade9time, msgtrade9side, msgtrade9size, msgtrade9price
    global msgtrade10time, msgtrade10side, msgtrade10size, msgtrade10price

    global msgbookbid1size, msgbookbid1price, msgbookask1size,msgbookask1price
    global msgbookbid2size, msgbookbid2price, msgbookask2size,msgbookask2price
    global msgbookbid3size, msgbookbid3price, msgbookask3size,msgbookask3price
    global msgbookbid4size, msgbookbid4price, msgbookask4size,msgbookask4price
    global msgbookbid5size, msgbookbid5price, msgbookask5size,msgbookask5price
    global msgbookbid6size, msgbookbid6price, msgbookask6size,msgbookask6price
    global msgbookbid7size, msgbookbid7price, msgbookask7size,msgbookask7price
    global msgbookbid8size, msgbookbid8price, msgbookask8size,msgbookask8price
    global msgbookbid9size, msgbookbid9price, msgbookask9size,msgbookask9price
    global msgbookbid10size, msgbookbid10price, msgbookask10size,msgbookask10price

    global mvalor2, mbitmex, symbol,timeframe,limit,params
    mwin3count = 0

    curses.start_color()			# activate color usage
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)  # Sell color on Times & Trades
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN) # Buy color on Times&Trades

    # Screen definitions
    height,width = screen.getmaxyx()
    #previous value screen.addstr(0, int(width/2.7),"xxx......
    if mvalor2 == "(1)":
       screen.addstr(0, 0, "              --- BITMEX PROD DATA Developed by Luciano Lima ---                ")
    elif mvalor2 == "(2)":
       screen.addstr(0, 0, "              --- BITMEX TEST DATA Developed by Luciano Lima ---                ")

    win1 = curses.newwin(18, 39, 2, 0)
    win2 = curses.newwin(18, 39, 2, 41)
    win3 = curses.newwin(5, 80, 20, 0)
    win1.box()
    win2.box()
    win3.box()
    height1,width1 = win1.getmaxyx()
    height2,width2 = win2.getmaxyx()
    win1.addstr(1, int(width1/3.2), "Book LII " + "%s" % mvalor1)
    win1.addstr(2, 1, "SIZE     BID ")
    win1.addstr(2, 20,"ASK       SIZE")
    win2.addstr(1, int(width2/3.3), "Times & Trades " + "%s" % mvalor1)
    win2.addstr(2, 1, "Timestamp")
    win2.addstr(2, 14, "Side")
    win2.addstr(2, 20, "Size")
    win2.addstr(2, 28, "Price")
    win3.addstr(1, 1, "Chart Data                                            |Amp|Frequency")

    #call_websocket()
    t = Thread(target=call_websocket)
    t.start()

    try:
        while True:
            # book
            win1.addstr(3,1,msgbookbid1size + "   ")
            win1.addstr(3,10,msgbookbid1price + "   ")
            win1.addstr(4,1,msgbookbid2size + "   ")
            win1.addstr(4,10,msgbookbid2price + "   ")
            win1.addstr(5,1,msgbookbid3size + "   ")
            win1.addstr(5,10,msgbookbid3price + "   ")
            win1.addstr(6,1,msgbookbid4size + "   ")
            win1.addstr(6,10,msgbookbid4price + "   ")
            win1.addstr(7,1,msgbookbid5size + "   ")
            win1.addstr(7,10,msgbookbid5price + "   ")
            win1.addstr(8,1,msgbookbid6size + "   ")
            win1.addstr(8,10,msgbookbid6price + "   ")
            win1.addstr(9,1,msgbookbid7size + "   ")
            win1.addstr(9,10,msgbookbid7price + "   ")
            win1.addstr(10,1,msgbookbid8size + "   ")
            win1.addstr(10,10,msgbookbid8price + "   ")
            win1.addstr(11,1,msgbookbid9size + "   ")
            win1.addstr(11,10,msgbookbid9price + "   ")
            win1.addstr(12,1,msgbookbid10size + "   ")
            win1.addstr(12,10,msgbookbid10price + "   ")

            win1.addstr(3,30,msgbookask1size + " ")
            win1.addstr(3,20,msgbookask1price + "   ")
            win1.addstr(4,30,msgbookask2size + " ")
            win1.addstr(4,20,msgbookask2price + "   ")
            win1.addstr(5,30,msgbookask3size + " ")
            win1.addstr(5,20,msgbookask3price + "   ")
            win1.addstr(6,30,msgbookask4size + " ")
            win1.addstr(6,20,msgbookask4price + "   ")
            win1.addstr(7,30,msgbookask5size + " ")
            win1.addstr(7,20,msgbookask5price + "   ")
            win1.addstr(8,30,msgbookask6size + " ")
            win1.addstr(8,20,msgbookask6price + "   ")
            win1.addstr(9,30,msgbookask7size + " ")
            win1.addstr(9,20,msgbookask7price + "   ")
            win1.addstr(10,30,msgbookask8size + " ")
            win1.addstr(10,20,msgbookask8price + "   ")
            win1.addstr(11,30,msgbookask9size + " ")
            win1.addstr(11,20,msgbookask9price + "   ")
            win1.addstr(12,30,msgbookask10size + " ")
            win1.addstr(12,20,msgbookask10price + "   ")

            # times and trades

            # 1st trade
            win2.addstr(3,1,msgtrade1time)    	            # timestamp
            if "Sell" in msgtrade1side:
               win2.addstr(3,14,msgtrade1side,curses.color_pair(1))          # Sell side
            else:
               win2.addstr(3,14,msgtrade1side,curses.color_pair(2))          # Buy side
            win2.addstr(3,20,msgtrade1size + "    ")         # size
            win2.addstr(3,28,msgtrade1price + "   ")            # price
            #2nd trade
            win2.addstr(4,1,msgtrade2time)    	            # timestamp
            if "Sell" in msgtrade2side:
               win2.addstr(4,14,msgtrade2side,curses.color_pair(1))          # Sell side
            else:
               win2.addstr(4,14,msgtrade2side,curses.color_pair(2))          # Buy side
               win2.addstr(4,20,msgtrade2size + "    ")         # size
               win2.addstr(4,28,msgtrade2price + "   ")            # price
            #3rd trade
            win2.addstr(5,1,msgtrade3time)    	            # timestamp
            if "Sell" in msgtrade3side:
               win2.addstr(5,14,msgtrade3side,curses.color_pair(1))          # Sell side
            else:
               win2.addstr(5,14,msgtrade3side,curses.color_pair(2))          # Buy side
               win2.addstr(5,20,msgtrade3size + "    ")         # size
               win2.addstr(5,28,msgtrade3price + "   ")            # price
            #4th trade
            win2.addstr(6,1,msgtrade4time)    	            # timestamp
            if "Sell" in msgtrade4side:
               win2.addstr(6,14,msgtrade4side,curses.color_pair(1))          # Sell side
            else:
               win2.addstr(6,14,msgtrade4side,curses.color_pair(2))          # Buy side
               win2.addstr(6,20,msgtrade4size + "    ")         # size
               win2.addstr(6,28,msgtrade4price + "   ")            # price
            #5th trade
            win2.addstr(7,1,msgtrade5time)    	            # timestamp
            if "Sell" in msgtrade5side:
               win2.addstr(7,14,msgtrade5side,curses.color_pair(1))          # Sell side
            else:
               win2.addstr(7,14,msgtrade5side,curses.color_pair(2))          # Buy side
               win2.addstr(7,20,msgtrade5size + "    ")         # size
               win2.addstr(7,28,msgtrade4price + "   ")            # price
            #6th trade
            win2.addstr(8,1,msgtrade6time)    	            # timestamp
            if "Sell" in msgtrade6side:
               win2.addstr(8,14,msgtrade6side,curses.color_pair(1))          # Sell side
            else:
               win2.addstr(8,14,msgtrade6side,curses.color_pair(2))          # Buy side
               win2.addstr(8,20,msgtrade6size + "    ")         # size
               win2.addstr(8,28,msgtrade6price + "   ")            # price
            #7th trade
            win2.addstr(9,1,msgtrade7time)    	            # timestamp
            if "Sell" in msgtrade7side:
               win2.addstr(8,14,msgtrade7side,curses.color_pair(1))          # Sell side
            else:
               win2.addstr(9,14,msgtrade7side,curses.color_pair(2))          # Buy side
               win2.addstr(9,20,msgtrade7size + "    ")         # size
               win2.addstr(9,28,msgtrade7price + "   ")            # price
            #8th trade
            win2.addstr(10,1,msgtrade8time)    	            # timestamp
            if "Sell" in msgtrade8side:
               win2.addstr(10,14,msgtrade8side,curses.color_pair(1))          # Sell side
            else:
               win2.addstr(10,14,msgtrade8side,curses.color_pair(2))          # Buy side
               win2.addstr(10,20,msgtrade8size + "    ")         # size
               win2.addstr(10,28,msgtrade8price + "   ")            # price
            #9th trade
            win2.addstr(11,1,msgtrade9time)    	            # timestamp
            if "Sell" in msgtrade9side:
               win2.addstr(11,14,msgtrade9side,curses.color_pair(1))          # Sell side
            else:
               win2.addstr(11,14,msgtrade9side,curses.color_pair(2))          # Buy side
               win2.addstr(11,20,msgtrade9size + "    ")         # size
               win2.addstr(11,28,msgtrade9price + "   ")            # price
            #10th trade
            win2.addstr(12,1,msgtrade10time)    	            # timestamp
            if "Sell" in msgtrade10side:
               win2.addstr(12,14,msgtrade10side,curses.color_pair(1))          # Sell side
            else:
               win2.addstr(12,14,msgtrade10side,curses.color_pair(2))          # Buy side
               win2.addstr(12,20,msgtrade10size + "    ")         # size
               win2.addstr(12,28,msgtrade10price + "   ")            # price

            if mwin3count == 360:
               # Isolating Win3 to avoid braking rate limit
               # Win3 Data	 --> Candle 3min/Chart Data
               # 3 min chart data
               since3min = mbitmex.milliseconds() - limit * 60 * 1000
               # 1 day chart data
               since1day = mbitmex.milliseconds() - 1 * 86400 * 1000
               # drawning 3 min data
               candles3min = mbitmex.fetch_ohlcv(symbol, timeframe, since3min, limit, params)
               num_candles3min = len(candles3min)
               ampl_candle3min = candles3min[num_candles3min - 1][2] - candles3min[num_candles3min - 1][3]
               freq_candle3min = '{0:.3g}'.format(ampl_candle3min * 0.10)
               win3.addstr(2, 1, "3m " + '{}: O:{} H:{} L:{} C:{}'.format(
                           mbitmex.iso8601(candles3min[num_candles3min - 1][0]),
                           candles3min[num_candles3min - 1][1],
                           candles3min[num_candles3min - 1][2],
                           candles3min[num_candles3min - 1][3],
                           candles3min[num_candles3min - 1][4]) + "|" + str(ampl_candle3min) + "|" + str(freq_candle3min) + " ")
               # drawning 1 day data
               #candles1day = mbitmex.fetch_ohlcv(symbol, timeframe, since1day, limit, params)
               candles1day = mbitmex.fetch_ohlcv(symbol, '1d', since1day)
               num_candles1day = len(candles1day)
               ampl_candle1day = candles1day[num_candles1day - 1][2] - candles1day[num_candles1day - 1][3]
               freq_candle1day = '{0:.3g}'.format(ampl_candle1day * 0.10)
               win3.addstr(3, 1, "1d " + '{}: O: {} H: {} L:{} C:{}'.format(
                           mbitmex.iso8601(candles1day[num_candles1day - 1][0]),
                           candles1day[num_candles1day - 1][1],
                           candles1day[num_candles1day - 1][2],
                           candles1day[num_candles1day - 1][3],
                           candles1day[num_candles1day - 1][4]) + "|" + str(ampl_candle1day) + "|" + str(freq_candle1day) + " ")
               # Sleep to avoid extra load and/or reaching rate limit
               mwin3count = 0
               win3.refresh()
            time.sleep(0.5)
            screen.refresh()
            win1.refresh()
            win2.refresh()
            mwin3count = mwin3count+1
    except ccxt.NetworkError:
           time.sleep(2)
           curses.wrapper(main)
           pass
    except KeyboardInterrupt:
         #ws.close()
         curses.endwin()
         print("\n \n --- End of Program! Thank You !!! ---")
         time.sleep(1)
         sys.exit()   			#  break first streaming
         sys.exit()			#  break ccxt requests
         sys.exit()
         pass

    # BitMEX Book LII parameters:
    #mbooklimit = 10 				# sets 10 lines the DOM (Depth of Market - Price Book)

    # BitMEX candle data/chart data parameters:
    # symbol = 'BTC/USD'
    #symbol = "%s" % mvalor1
    #timeframe = '1m'
    #limit = 100
    #params = {'partial': False}   # <---------- no reversal

    # BitMEX times & trades parameters:


    # Basic example to work with windows using Python and curses
    # left here only to clarify the initial developments:
    #for count in ['3', '2', '1', 'Go!']:
    #    win1.addstr(1, 1, 'Win1: ' + count)
    #    win2.addstr(1, 1, 'Win2: ' + count)


# calling the main Module:
curses.wrapper(main)

# Finishing the code/program according to best practices:
sys.exit()
