# Test code for "GG IWATCH 23" created by CARBONTEA LTD. in 2023.
# Use this code first to test your wireing/soldering.
# Before running this script you have to import and install
# in Thonny/Tools/Manage Packages the "ssd1306" display drivers &
# missing packages then scroll down to line 23/24 and fill in your
# wifi name/password within the double quotes!"
# Code works as described, no hidden features & no warranty, use at
# your own risk!!! Released under the MIT open source licence.
from machine import Pin,I2C,ADC,PWM
from ssd1306 import SSD1306_I2C
import random,math,time
import json,network,urequests
################### end of imports code #############################

######################### setup code for display ####################
i2c=I2C(0,sda=Pin(0),scl=Pin(1),freq=400000)
oled=SSD1306_I2C(128,64,i2c)
######################## end of setup code for display ##############

############### setup code for wifi connection ######################
wlan=network.WLAN(network.STA_IF)
wlan.active(True)
ssid="YOURWIFIACCESSPOINT" ################################ wifi name 
password="YOURWIFIPASSWORD"############################ wifi password 
wlan.connect(ssid,password)
########################## end of setup code for wifi connection ####

############### setup code for BTC fetching #########################
key="https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
data="fetching btc"
############### end of setup code for BTC fetching ##################

############### setup code for for time fetching ####################
key4="https://www.timeapi.io/api/Time/current/zone?timeZone=etc/utc"
data="fetching time"
############### end of setup code for for time fetching ##############

####### setup code for joystick up/down and left/right movement #####
LRAxis = ADC(Pin(26))############# left/right movement gpio pin "ADC"
UDAxis = ADC(Pin(27))################ up/down movement gpio pin "ADC"
LRValue=32000
UDValue=32000
joystickcounter=0
####### end of setup code for joystick up/down and left/right movement

####### setup code for piezzo buzzer for sound and music #############
buzzer=PWM(Pin(10))
buzzer.freq(500)
####### end of setup code for piezzo buzzer ##########################

############### setup code for motor rumble ##########################
motc=machine.PWM(machine.Pin(15))
############## end of setup code for motor rumble ####################

############## first bootup code #####################################
#oled.text("-=heck yeah=-",12,26)
oled.text("-=GGIWATCH23=-",10,28)
oled.show()############# rendering text onto display to see if it works

buzzer.duty_u16(30000)######## then beeping two times the piezzo buzzer
time.sleep(0.1)
buzzer.duty_u16(0)
time.sleep(0.5)
buzzer.duty_u16(20000)
time.sleep(0.1)
buzzer.duty_u16(0)

motc.duty_u16(32000)######## then rumbles two times the motor
time.sleep(0.2)
motc.duty_u16(0)
time.sleep(0.5)
motc.duty_u16(32000)
time.sleep(0.2)
motc.duty_u16(0)

oled.fill_rect(0,0,128,64,0)#x,y,w,h ######## then clearing the display
oled.show()
time.sleep(0.5)
############## end of first bootup code #####################################

global fetch
fetch=0 # fetching switch
global twosecdelay
twosecdelay=0 # showing fetched results for two seconds (main counter clock)
global data2 # just to have this defined as global empty string
data2=""
global data3 # temp storage to be displayed fro 2 seconds after fetched
data3=""

while True:
    global fetch
    global data2
    global data3
    global twosecdelay
    
    ########### spaghetti code for text positioning during various modes, BEWARE! #######
    if twosecdelay>0:
        if twosecdelay>=120:
            if len(data3)==8:
                xpos=33
            else:
                xpos=11
            ypos=28
        if len(data3)==8:
            if len(data2)==8:
                if len(data3)>8 or len(data3)==0:
                    xpos=11
                else:
                    xpos=33
            else:
                if len(data2)==13 and len(data3)==8:
                    xpos=33
                else:
                    xpos=11
        else:
            xpos=11
        ypos=28
    else:
        if len(data3)==8:
            xpos=33
        else:
            xpos=11
        ypos=28
    ########### end of spaghetti code for text positioning during various modes, BEWARE! 
        
        
    ######### joystick data ############################################################
    joystickcounter+=1
    if joystickcounter>=3:
        joystickcounter=0
        LRValue = LRAxis.read_u16()
        UDValue = UDAxis.read_u16()
    else:
        try:
            LRValue=LRValue
            UDValue=UDValue
        except Exception:
            LRValue=32000
            UDValue=32000
        
    ####################### LEFT/RIGHT function ###############################
    if int(LRValue)<15000:
        if fetch==0:# manual activate BTC fetching
            fetch=1
        else:
            pass
    if int(LRValue)>45000:
        fetch=0 # manual reset BTC fetching
        twosecdelay=0
        data3=""
        xpos=11
    ####################### end of LEFT/RIGHT function #########################
    
    ####################### UP/DOWN function ###################################
    if int(UDValue)<15000:
        if fetch==0:# manual activate time fetching
            fetch=2
        else:
            pass
    if int(UDValue)>45000:
        fetch=0 # manual reset time fetching
        twosecdelay=0
        data3=""
        xpos=11
    ####################### end of UP/DOWN function #############################   
        
    ####################### visual neatness under 10000, missing 0 in front of 08
    if int(UDValue)<10000:
        UDValue="0"+str(UDValue)
    if int(LRValue)<10000:
        LRValue="0"+str(LRValue)
    ####################### end of visual neatness under 10000, missing 0 etc. ##

    data2="U/D:"+str(UDValue)[:2]+" "+"L/R:"+str(LRValue)[:2]

    ######### end of joystick data ###############################################
    
    
    
    ########################### joystick data display ############################
    if fetch==0:
        oled.fill_rect(0,0,128,64,0)#x,y,w,h ######## then clearing the display
        if twosecdelay>0:
            try:
                oled.text(data3,xpos,ypos)
            except Exception:
                pass
        else:
            oled.text(data2,xpos,ypos)
        oled.show()
    ########################### end of joystick data display #####################
        
    
    ############################## BTC price fetch ###############################
    if fetch==1:
        try:
            datap="fetching BTC"
            oled.fill_rect(0,0,128,64,0)#x,y,w,h ######## then clearing the display

            try:
                if list(data3)[0]=="B" or list(data3)[0]=="f":
                    oled.text(data3,xpos,ypos)
                else:
                    oled.text(datap,xpos,ypos)
            except Exception:
                oled.text(datap,xpos,ypos)
                
            oled.show()

            dat=urequests.get(key)
            data9=dat.json()
            data2b="BTC: "+str(float(data9["price"]))
            data2=data2b
            data3="BTC: "+str(float(data9["price"]))
            twosecdelay=1
            fetch=0
        except Exception:
            data2="fetching FAIL"
            data3="fetching FAIL"
            fetch=0
            twosecdelay=1
    ############################# end of BTC price fetch ###########################

    ############################## time fetch ######################################
    if fetch==2:
        try:
            datap="fetching Time"
            oled.fill_rect(0,0,128,64,0)#x,y,w,h ######## then clearing the display

            try:
                if int(list(data3)[0])<10 or list(data3)[0]=="f":
                    oled.text(data3,xpos,ypos)
                else:
                    oled.text(datap,xpos,ypos)
            except Exception:
                oled.text(datap,xpos,ypos)
                
            oled.show()
            
            data4=urequests.get(key4)
            data4b=data4.json()
            hr=data4b["hour"]
            if hr<10:
                hr="0"+str(hr)
            mn=data4b["minute"]
            if mn<10:
                mn="0"+str(mn)
            sc=data4b["seconds"]
            if sc<10:
                sc="0"+str(sc)
            data4c=str(hr)+":"+str(mn)+":"+str(sc)
            data2=data4c
            data3=data4c

            twosecdelay=1
            fetch=0
        except Exception:
            data2="fetching FAIL"
            data3="fetching FAIL"
            fetch=0
            twosecdelay=1
    ############################# end of time fetch #################################
    
    fetch=0
            
    ############################# draw joystick input/BTC price/time on display ######
    
    if twosecdelay>0:
        twosecdelay+=1
        if twosecdelay>=120:
            twosecdelay=0
            oled.text(data3,xpos,ypos)
            data3=""
            data2=""
        oled.text(data3,xpos,ypos)        
    else:
        twosecdelay=0
        oled.text(data2,xpos,ypos)

    oled.show()
    ############################# end of draw joystick input/BTC price/time on display #
