'''Backup incase sensors are not working'''
'''Order of the values in the FSRdata 
    1) Device not in (x2)
    2) Readjust
    3) Properly in (x2)
    4) Too loose (x2)
    5) Too tight (x2)
    6) Just right
    7) Checks time (x5)
'''

from gpiozero import LED
red_led = LED(20)
from sensor_library import*
import time
counter = 0
maxtime = 0

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.

disp.begin()


# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = 0
shape_width = 20
top = padding
med = 10
bottom = 20
# Move left to right keeping track of the current x position for drawing shapes.
x = padding

# Load default font.
font = ImageFont.load_default()


#Task 0
def filewrite(userinfo):
    
    f = open("Userinfo.txt", "a+") #create a new file... and add daily data
    f.write(str(userinfo[0]) + ' '+ str(userinfo[1])+ ' '+  str(userinfo[2])+  ' '+ str(userinfo[3])+ ' '+  str(userinfo[4])+ "\n")
    f.close

   
def userinfoo():   #(should this be like a log in thing, like they should do this first)
    userinfo =[]
    global maxtime
    print("Welcome to CULIP! Please enter your info below to personalize your CULIP experience:")
    name = input("Please enter your name: ")
    password = input("Please enter a password: ")
    flowtype = input("How would you describe your flowtype? \nHeavy, Medium or Light?: ")
    cuptype= input("what is you cup size? \n A) Below 18 \n B) Above 18 \n C) Had kids")
    userinfo.append(name)
    userinfo.append(password)
    userinfo.append(flowtype)
    userinfo.append(cuptype)
    if (flowtype.lower() == "heavy") and (cuptype.lower() == "a"):
        maxtime = 40
        print("dsf")
    elif (flowtype.lower() == "heavy") and (cuptype.lower() == "b"):
        maxtime = 60
    elif (flowtype.lower() == "heavy") and (cuptype.lower() == "c"):
        maxtime = 70
    elif (flowtype.lower() == "medium") and (cuptype.lower() == "a"):
        maxtime = 80
    elif (flowtype.lower() == "medium") and (cuptype.lower() == "b"):
        maxtime = 120
    elif (flowtype.lower() == "medium") and (cuptype.lower() == "c"):
        maxtime = 120
    elif (flowtype.lower() == "light") and (cuptype.lower() == "a"):
        maxtime = 110
    elif (flowtype.lower() == "light") and (cuptype.lower() == "b"):
        maxtime = 120
    elif (flowtype.lower() == "light") and (cuptype.lower() == "c"):
        maxtime = 120

    userinfo.append(maxtime)
    
    print(userinfo)
    filewrite(userinfo)
    main()
 
def text():
    disp.image(image)
    disp.display()
    time.sleep(5)
    disp.clear()
     
    draw.rectangle((0,0,width,height), outline=0, fill=0)

#Task 3
def timechecker(starttime,maxtime):
    import time
    global red_led
    
    maxtime =float(maxtime)
    
    red_led.off()
    

    while True:
        offtime= time.time()
        dur = offtime-starttime
        value = inside()
        if dur>=maxtime and value ==1:
            draw.text((x, top),    'Time to take it out!',  font=font, fill=255)
            text()
            
        if dur>maxtime+10 and value ==1:
            draw.text((x, top),    'It has been too long!',  font=font, fill=255)
            text()
            
            red_led.on()
            print("red led is on")
            time.sleep(5)
        if value==0:
            draw.text((x, top),    'Device is OFF',  font=font, fill=255)
            text()
            break
            onoff()
#Task 2
def orientation():
    from gpiozero import LED
    
    yellow_led = LED(16)
    blue_led = LED(21)
    
    while True:
        
        sensorvalues = avg_sensor_values()
        vfs1=sensorvalues[0]
        vfs2=sensorvalues[1]
        vfs3=sensorvalues[2]

        yellow_led.off()
        blue_led.off()
        
        diff12 = abs(vfs1-vfs2)
        diff23 = abs(vfs2-vfs3)
        diff31 = abs(vfs3-vfs1)
            
        if ((vfs1 > 3) or (vfs2 > 3) or (vfs3 > 3)):
            if ((diff12 < 5) and (diff23 < 5) and (diff31 < 5)):

                draw.text((x, top),    'Properly positioned!',  font=font, fill=255)
                text()
                
                blue_led.on()
                print("blue led is on")
                time.sleep(4)
                break
            else:
                draw.text((x, top),    'Readjust',  font=font, fill=255)
                text()
                yellow_led.on()
                print("yellow led is on")
                time.sleep(2)
                yellow_led.off()

        else:
            draw.text((x, top),    'Device is not in!',  font=font, fill=255)
            text()
            
                
def forcedata():
    forcedata=[]
    fs1 = Force_Sensing_Resistor(1)
    fs2 = Force_Sensing_Resistor(2)
    fs3 = Force_Sensing_Resistor(3)
    while True:
        for i in range(3):
            
            vfs1=fs3.force_scaled(80)
            time.sleep(0.1)
            print(vfs1)
            forcedata.append(vfs1)
        f = open("FSRdata.txt", "a+") #create a new file... and add daily data
        f.write(str(forcedata[0]) + ' '+ str(forcedata[1])+ ' '+  str(forcedata[2]) +"\n")
        f.close
        forcedata.clear()           
         
def big_sensor_values():
    
    vfs1=[]
    vfs2=[]
    vfs3=[]
##This function calculate the average value of the last ten values from the force sensor
    a = 0
    cred = []
    f = open("FSRdata.txt", "r")
    info=f.readlines()
    for line in info:
        i= line.split()
        cred.append(i)
   
    for j in range(len(cred)):
        vfs1.append(cred[j][0])
        vfs2.append(cred[j][1])
        vfs3.append(cred[j][2])
    print("done")
        
    
##    print(vfs1)
##    print(vfs2)
##    print(vfs3)
    return(vfs1,vfs2,vfs3)

def avg_sensor_values():
    
    biglist=big_sensor_values()
   # print(biglist)
    vfs1=[]
    vfs2=[]
    vfs3=[]
    vfs1=biglist[0]
    vfs2=biglist[1]
    vfs3=biglist[2]
    avg1 = 0
    avg2 = 0
    avg3 = 0
    svfs1=[]
    svfs2=[]
    svfs3=[]
    global counter

    c= counter*10
    for i in range(10):
        svfs1.append(float(vfs1[i+c]))
        print(vfs1[i+c])
        svfs2.append(float(vfs2[i+c]))
        print(vfs2[i+c])
        svfs3.append(float(vfs3[i+c]))
        print(vfs3[i+c])

    for b in range(10):
        avg1 += svfs1[b]
        avg2 += svfs2[b]
        avg3 += svfs3[b]

    avsf1 = avg1/10
    avsf2 = avg2/10
    avsf3 = avg3/10
    
    counter += 1
    return (avsf1,avsf2,avsf3)     
    
        
    
   
#Task4 (Creative)    
##This function Checks the fit of the dvice and determines if the cup is too tight or too lose for the user
def fit(): 
    
    sensorvalues = avg_sensor_values()
    vfs1=sensorvalues[0]
    vfs2=sensorvalues[1]
    vfs3=sensorvalues[2]

    if vfs3<10 and vfs2<10 and vfs1<10:
        print("too loose, get new size")
        draw.text((x, top),    'Device might be ',  font=font, fill=255)
        draw.text((x, med),    'too loose! ',  font=font, fill=255)
        draw.text((x, bottom),    'Maybe go up a size',  font=font, fill=255)
        text()

    elif vfs3>60 and vfs2>60 and vfs3>60:
        print("too tight, get new size")
        draw.text((x, top),    'Device might be ',  font=font, fill=255)
        draw.text((x, med),    'too tight! ',  font=font, fill=255)
        draw.text((x, bottom),    'Maybe go down a size',  font=font, fill=255)
        text()
    else:
        print("just right")
        draw.text((x, top),    'justright',  font=font, fill=255)
        text()
        

    

def inside():
    
    print("Checking if device is inside")
  
    sensorvalues = avg_sensor_values()
    vfs1=sensorvalues[0]
    vfs2=sensorvalues[1]
    vfs3=sensorvalues[2]

    if vfs3<5 and vfs2<5 and vfs1<5:
        output = 0 #outside
    else:
        output = 1 #still inside the person

    return(output)

##Task 1
def onoff(maxtime):
    global red_led
    red_led.off()
    maxtime = maxtime
    while True:
        user_input = input("Enter ON or OFF")
        
        if user_input.upper() == 'ON':
            start_time = time.time()
            print("Device is ON")
            draw.text((x, top),    'Device is ON',  font=font, fill=255)
            text()
            orientation() ##Need orientation to be right before user can check everything else
            while True:
                timern=time.time()
                durrr= timern-start_time
                if durrr>float(maxtime):
                    red_led.on()
                saction = input("What do you want to do?: \n A) Check orientation \n B) Check fit \n C) Check time \n D) Continue to use cup ")
                if saction.lower() == "a":
                    orientation()
                if saction.lower() == "b":
                    fit()
                if saction.lower() == "c":
                    timern=time.time()
                    elapsetime = timern-start_time
                    timeleft = float(maxtime) - elapsetime
                    print ("Time left until change: ", timeleft)
                if saction.lower() == "d":
                    break
                if not(saction.lower() == "d" or saction.lower() == "c" or saction.lower() == "b" or saction.lower() == "a"):
                    print("Invalid input. Try again")
                
            
            
            timechecker(start_time,maxtime)
        elif user_input.upper() == 'OFF':
            print("Device is OFF")
            draw.text((x, top),    'Device is OFF',  font=font, fill=255)
            text()
            break
        else:
            draw.text((x, top),    'Invalid input. Please try again',  font=font, fill=255)
            text()
            
        
def main():
    
    action = input("What do you want to do?: \n A) Log in and Turn on cup \n B) Make an account \n")
    if action.lower() == "b":
        userinfoo()
    elif action.lower() == "a":
        cred=[]
        name = input("Please enter your name:")
        name=name.lower()
        password = input("Please enter a password")
        password=password.lower()                    
        f = open("Userinfo.txt", "r")
        info=f.readlines()
        i=0
        usertime=0
        for line in info:
            
            i= line.split()
            cred.append(i)
        for j in range(len(cred)):
            if ((cred[j][0]).lower() == name) and ((cred[j][1]).lower() == password):
                usertime = cred[j][4]
                print(usertime + "\n\n\n")
                onoff(usertime)
        if usertime == 0:
            print("You do not have an account or have inputed the wrong username or password")
            main()
        
        


    else:
        print("Invalid input. Try again")
        main()
#orientation()
#main()
