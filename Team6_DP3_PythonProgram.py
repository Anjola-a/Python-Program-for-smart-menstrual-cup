'''
Team 6 DP3 Python code files
Anjola Adewale : 400255269
Saraf Raidah : 400266577


'''
#This try statement ensures handles errors due to imperoper wire connections
#We don't return 'None' as if they are no values read by the sensor, the device is not inside the user, which is a function on its own (inside function)
try:
    from gpiozero import LED
    red_led = LED(20)
    from sensor_library import*
    import time


    import Adafruit_GPIO.SPI as SPI
    import Adafruit_SSD1306

    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont
    maxtime=0

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

    '''
        Task 0
    '''    
    #The function writes user information  into a textfile
    def filewrite(userinfo):
        
        f = open("Userinfo.txt", "a+") 
        f.write(str(userinfo[0]) + ' '+ str(userinfo[1])+ ' '+  str(userinfo[2])+  ' '+ str(userinfo[3])+ ' '+  str(userinfo[4])+ "\n")
        f.close

    #The function collects userinfo into a textfile and generates the maxtime the user can have the device in for, based on flow type and cup size. 
    def userinfoo():  
        userinfo =[]
        global maxtime
        print("Welcome to CULIP! Please enter your info below to personalize your CULIP experience:")
        name = input("Please enter your name: ")
        password = input("Please enter a password: ")
        flowtype = input("How would you describe your flowtype? \nHeavy, Medium or Light?: ")
        while True:
            if flowtype.lower() == "heavy" or flowtype.lower()=="light" or flowtype.lower() == "medium":
                break
            else:
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
    #This function clears the OLED screen 
    def text():
        disp.image(image)
        disp.display()
        time.sleep(5)
        disp.clear()
         
        draw.rectangle((0,0,width,height), outline=0, fill=0)

    '''
        Task 2
    '''
    def orientation():#Checks orientation of the cup
        from gpiozero import LED
        global maxtime
        yellow_led = LED(16)
        blue_led = LED(21)
        
        while True:
            
            sensorvalues = avg_sensor_values()
            vfs1=sensorvalues[0]+34#Added value since sensor was consistently 34 below other sensor values
            vfs2=sensorvalues[1]
            vfs3=sensorvalues[2]

            yellow_led.off()
            blue_led.off()
            
            diff12 = abs(vfs1-vfs2)#Absolute difference is taken between the forces
            diff23 = abs(vfs2-vfs3)
            diff31 = abs(vfs3-vfs1)
                
            if ((vfs1 > 3) and (vfs2 > 3) or (vfs3 > 3)):#Once the sensor values are greater than 3,
                if ((diff12 < 10) and (diff23 < 10) and (diff31 < 10)):#If the difference between the sensors are less than 10, the cup is positioned well

                    draw.text((x, top),    'Properly positioned!',  font=font, fill=255)
                    text()
                    
                    blue_led.on()
                    print("blue led is on")
                    time.sleep(4)
                    break
                else:
                    draw.text((x, top),    'Readjust',  font=font, fill=255)#If the difference between the sensors are not less than 10, the cup must be readjusted
                    text()
                    yellow_led.on()
                    print("yellow led is on")
                    time.sleep(2)
                    yellow_led.off()

            else:#if the forces on the device are less than 3 then the device is not inside the user
                draw.text((x, top),    'Device is not in!',  font=font, fill=255)
                text()
                
        
                    
                
             
    def avg_sensor_values(): ##This function calculate the average value of the last ten values from the force sensor

        fs1 = Force_Sensing_Resistor(1)
        fs2 = Force_Sensing_Resistor(2)
        fs3 = Force_Sensing_Resistor(3)

        a = 0
        data1 = []
        for i in range(10):
            vfs1=fs1.force_scaled(100)
            time.sleep(0.1)
            data1.append(vfs1)
            print (data1[i])
            a+=data1[i]
        vfs1 = (a/10)
        print("The average value for force sensor 1 is: ",vfs1)
        
        b = 0
        data2 = []
        for i in range(10):
            vfs2=fs2.force_scaled(100)
            time.sleep(0.1)
            data2.append(vfs2)
            print (data2[i])
            b+=data2[i]
        vfs2 = b/10
        print("The average value for force sensor 2 is:",vfs2)
        
        c = 0
        data3 = []
        for i in range(10):
            vfs3=fs3.force_scaled(100)
            time.sleep(0.1)
            data3.append(vfs3)
            print (data3[i])
            c+=data3[i]
        vfs3 = c/10
        print("The average value for force sensor  3 is:",vfs3)

        return (round(vfs1,2),round(vfs2,2),round(vfs3,2))

    '''
        Task 3
    '''
    #This function compares the users maxtime with the duration of time the cup is in use to tell the user when to change
    def timechecker(starttime,maxtime):#r
        global red_led
        import time
        maxtime =float(maxtime)
        
        while True:
            offtime= time.time()
            dur = offtime-starttime
            value = inside() #Check if the device is still in use 1 for yes and 0 for no
            if dur>=maxtime and value ==1:#When the duation reaches assigned max time, the user receives notification to take out
                draw.text((x, top),    'Time to take it out!',  font=font, fill=255)
                text()
                
            if dur>maxtime+10 and value ==1:##After 10 secs past max is reached. user recieves another reminder
                draw.text((x, top),    'It has been too long!',  font=font, fill=255)
                text()
                
                red_led.on()
                print("red led is on")
                time.sleep(5)
            if value==0:
                draw.text((x, top),    'Device is OFF',  font=font, fill=255)
                text()
                red_led.off()
                break
        onoff(maxtime)
            
    '''
        Task 4
    '''   
    def fit():##This function Checks the fit of the device and determines if the cup is too tight or too lose for the user
        
        sensorvalues = avg_sensor_values()
        vfs1=sensorvalues[0]+28
        vfs2=sensorvalues[1]
        vfs3=sensorvalues[2]

        if vfs3<10 and vfs2<10 and vfs1<10:#If all forces are less than 10, cup is too small and they must go up a size
            print("too loose, get new size")
            draw.text((x, top),    'Device might be ',  font=font, fill=255)
            draw.text((x, med),    'too loose! ',  font=font, fill=255)
            draw.text((x, bottom),    'Maybe go up a size',  font=font, fill=255)
            text()

        elif vfs1>60 and vfs2>60 and vfs3>60:#If all forces are greater than 60, cup is too big and they must go down a size
            print("too tight, get new size")
            draw.text((x, top),    'Device might be ',  font=font, fill=255)
            draw.text((x, med),    'too tight! ',  font=font, fill=255)
            draw.text((x, bottom),    'Maybe go down a size',  font=font, fill=255)
            text()
        elif vfs1>30 and vfs2>30 and vfs3>30:#If all forces are greater than 30, the cup is a good size for the user
            print("just right")
            draw.text((x, top),    "just right",  font=font, fill=255)
            text()

    def inside():#Determines if the cup is inside the user
        
        print("Checking if device is inside")
      
        sensorvalues = avg_sensor_values()
        vfs1=sensorvalues[0]
        vfs2=sensorvalues[1]
        vfs3=sensorvalues[2]

        if vfs3<5 and vfs2<5 and vfs1<5: #If all forces are less than 5, the device is not in user
            output = 0 #outside(None)
        else:
            output = 1 #still inside the person

        return(output)

    '''
        Task 1
    '''
    def onoff(maxtime):# Function allows user to turn the device on or off. THe orientation function is automatic right after this
        
        global red_led
        while True:
            user_input = input("Enter ON or OFF")
            
            if user_input.upper() == 'ON':
                start_time = time.time()
                print("Device is ON")
                draw.text((x, top),    'Device is ON',  font=font, fill=255)
                text()
                orientation() ##Need orientation to be right before user can check everything else. Once it is considered to be in user, they can perform the other tasks
                while True:
                    timern=time.time()
                    durrr= timern-start_time
                    if durrr>float(maxtime):
                        red_led.on()
                        draw.text((x, top),    'Time to take it out!',  font=font, fill=255)
                        text()
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
                
            
    def main():#Function asks the user to make a new account or log back in, Once logged on, the On/Off is called
        
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

    main()
except OSError:
    print("Please check the wiring")
