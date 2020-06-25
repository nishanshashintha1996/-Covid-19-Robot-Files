import urllib.request, json
import RPi.GPIO as GPIO

import picamera
from time import sleep

import pyqrcode

#set_room = int(102)

#start gpio pin

GPIO.setmode(GPIO.BOARD)

#assign gpio pins to line traking sensor

left_sensor_02 = 16
left_sensor_01 = 18

right_sensor_01 = 22
right_sensor_02 = 24

#set gpio pin as input

GPIO.setup(left_sensor_02,GPIO.IN)
GPIO.setup(left_sensor_01,GPIO.IN)
GPIO.setup(right_sensor_01,GPIO.IN)
GPIO.setup(right_sensor_02,GPIO.IN)

#set gpio pin as output

GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)


GPIO.setup(37, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)

#set moter control output to LOW states

GPIO.output(37, GPIO.LOW)
GPIO.output(35, GPIO.LOW)
GPIO.output(33, GPIO.LOW)
GPIO.output(31, GPIO.LOW)


#start program with connect IOT Platform

while True:
    #read robot control from IOT Platform
    with urllib.request.urlopen("https://robot.findx.lk/robot_control_api.php") as url:
        data = json.loads(url.read().decode())
        
        # get control values
        mode = data['mode'];
        room_number = data['room_number'];
        m_left = data['m_left'];
        m_right = data['m_right'];
        m_front = data['m_front'];
        m_back = data['m_back'];
        m_stop = data['m_stop'];
        m_tray = data['m_tray'];
        f_tray = data['f_tray'];
        
        #print("m tray", m_tray, "\n");
        #print("f tray", f_tray, "\n");
        
        
        if m_tray == 1:
            # Open Medicine Tray of Robot
            print("m tray is 1 \n");
            
            GPIO.output(13, GPIO.HIGH)
            sleep(1)
            
            GPIO.output(13, GPIO.LOW)
            sleep(1)
        
        if f_tray == 1:
            # Open Food Tray of Robot
            print("f tray is 1 \n");
            GPIO.output(11, GPIO.HIGH)
            
            sleep(1)
            GPIO.output(11, GPIO.LOW)
            
            sleep(1)

        
        
        
        
        
        if mode=="manual":
            #Start Manual mode
            print("manual")
            if m_stop==1:
                #stop Robot
                print("stop")
                #Stop Left Moter
                GPIO.output(37, GPIO.LOW)
                GPIO.output(35, GPIO.LOW)
                # 
                # stop right motor
                GPIO.output(33, GPIO.LOW)
                GPIO.output(31, GPIO.LOW)
            
            if m_left==1:
                print("left")
                # #Left Moter Backward
                GPIO.output(37, GPIO.LOW)
                GPIO.output(35, GPIO.HIGH)
                # 
                # #Right Moter Forward
                GPIO.output(33, GPIO.LOW)
                GPIO.output(31, GPIO.HIGH)
            
            if m_right==1:
                print("right")
                # #Left Moter Forward
                GPIO.output(37, GPIO.HIGH)
                GPIO.output(35, GPIO.LOW)
                # 
                # #Right Moter Backword
                GPIO.output(33, GPIO.HIGH)
                GPIO.output(31, GPIO.LOW)
                
            if m_front==1:
                print("front")
                # #Left Moter Forward
                GPIO.output(37, GPIO.HIGH)
                GPIO.output(35, GPIO.LOW)
                # 
                # #Right Moter Forward
                GPIO.output(33, GPIO.LOW)
                GPIO.output(31, GPIO.HIGH)
            
            if m_back==1:
                print("back")
                # #Left Moter Backward
                GPIO.output(37, GPIO.LOW)
                GPIO.output(35, GPIO.HIGH)
                # 
                # #Right Moter Backword
                GPIO.output(33, GPIO.HIGH)
                GPIO.output(31, GPIO.LOW)
        
        elif mode=="auto":
            #start Auto mode with line following
            if room_number == "":
                print("Please Enter Room Number")
            else:
                #in auto mode
                while True:
                    
                    if mode == "manual":
                            break
                        
                    #read line traking sensor input
                    left_sensor_02_data = GPIO.input(left_sensor_02)
                    left_sensor_01_data = GPIO.input(left_sensor_01)

                    right_sensor_01_data = GPIO.input(right_sensor_01)
                    right_sensor_02_data = GPIO.input(right_sensor_02)
                    
                    
                    print("L2 ",left_sensor_02_data,"L1 ",left_sensor_01_data,"R1 ",right_sensor_01_data,"R2 ",right_sensor_02_data)
                    
                    
                    
                    
                    if right_sensor_01_data == 0 and left_sensor_01_data == 0 and right_sensor_02_data == 0 and left_sensor_02_data == 0:
                        
                        #when all sensor in black line stop robot for read qr code of room
                        
                        #Left Moter Forward
                        GPIO.output(37, GPIO.LOW)
                        GPIO.output(35, GPIO.LOW)

                        #Right Moter Forward
                        GPIO.output(31, GPIO.LOW)
                        GPIO.output(33, GPIO.LOW)
                        
                        
                        with urllib.request.urlopen("https://robot.findx.lk/robot_control_api.php") as url:
                            data = json.loads(url.read().decode())
                            
                            mode = data['mode'];
                            
                            
                            
                            if mode =="manual":
                                break
                        
                        
                        #take picture of qr code in line
                        
                        print("About to take a picture ")
                        with picamera.PiCamera() as camera:
                            camera.resolution = (1280,720)
                            sleep(3)
                            camera.capture("qr.jpg")
                        print("picture taken")
                        

                        try:
                            
                            #decode qr and read value
                            from pyzbar.pyzbar import decode
                            from PIL import Image
                            d = decode(Image.open('qr.jpg'))
                            qrcode = d[0].data.decode('ascii')
                            #print (qrcode)
                            if qrcode == "":
                                print("No QR")
                            else:
                                room_no = qrcode[:3]
                                turn = qrcode[3]
                                print("room", room_no, "\n", "Turn", turn)
                                
                                if int(room_number[:3]) == int(room_no):
                                    while True:
                                        
                                        #when reach given room robot goto that room
                                        
                                        with urllib.request.urlopen("https://robot.findx.lk/robot_control_api.php") as url:
                                            data = json.loads(url.read().decode())
                                            
                                            mode = data['mode'];
                                            
                                            
                                            if mode =="manual":
                                                break
                                            
                                            
                                            if turn == "L":
                                                
                                                #if room in left side robot turn to left
                                                
                                                #turn_left
                                                
                                                # #Left Moter Backward
                                                GPIO.output(37, GPIO.LOW)
                                                GPIO.output(35, GPIO.HIGH)
                                                # 
                                                # #Right Moter Forward
                                                GPIO.output(33, GPIO.LOW)
                                                GPIO.output(31, GPIO.HIGH)
                                                
                                                sleep(1)
                                                break
                                                
                                            
                                            if turn == "R":
                                                #if room in right side robot turn to right
                                                #turn_left
                                                
                                                # #Left Moter Forward
                                                GPIO.output(37, GPIO.HIGH)
                                                GPIO.output(35, GPIO.LOW)
                                                # 
                                                # #Right Moter Backword
                                                GPIO.output(33, GPIO.HIGH)
                                                GPIO.output(31, GPIO.LOW)
                                                
                                                sleep(1)
                                                break
                                    
                                        
                                        
                                else:
                                
                                    while True:
                                        
                                        left_sensor_02_data = GPIO.input(left_sensor_02)
                                        left_sensor_01_data = GPIO.input(left_sensor_01)

                                        right_sensor_01_data = GPIO.input(right_sensor_01)
                                        right_sensor_02_data = GPIO.input(right_sensor_02)
                                        
                                        
                                        
                                        
                                        if right_sensor_01_data == 0 and left_sensor_01_data == 0 and right_sensor_02_data == 0 and left_sensor_02_data == 0:
                                            # #Left Moter Forward
                                            GPIO.output(37, GPIO.HIGH)
                                            GPIO.output(35, GPIO.LOW)
                                            # 
                                            # #Right Moter Forward
                                            GPIO.output(33, GPIO.LOW)
                                            GPIO.output(31, GPIO.HIGH)
                                        else:
                                            break
                                    
                                
                                
                                
                            
                        except IndexError as error:
                            print("No QR")
                        
                        
                        
                        
                        
                        
                        
                        
                    else:
                     
                        if right_sensor_01_data == 0 and right_sensor_02_data == 0:
                            
                            #Left Moter Forward
                            GPIO.output(37, GPIO.HIGH)
                            GPIO.output(35, GPIO.LOW)

                            #Right Moter Forward
                            GPIO.output(31, GPIO.HIGH)
                            GPIO.output(33, GPIO.LOW)
                            
                        else:
                            if left_sensor_01_data == 0 and left_sensor_02_data == 0:
                                #Left Moter Forward
                                GPIO.output(37, GPIO.HIGH)
                                GPIO.output(35, GPIO.LOW)

                                #Right Moter Forward
                                GPIO.output(31, GPIO.HIGH)
                                GPIO.output(33, GPIO.LOW)
                            else:
                                
                                if right_sensor_01_data == 1 and left_sensor_01_data == 1:
                                    #Left Moter Forward
                                    GPIO.output(37, GPIO.HIGH)
                                    GPIO.output(35, GPIO.LOW)

                                    #Right Moter Forward
                                    GPIO.output(31, GPIO.HIGH)
                                    GPIO.output(33, GPIO.LOW)
                                else:
                                
                                    if right_sensor_01_data == 0:
                                        #Left Moter Forward
                                        GPIO.output(37, GPIO.HIGH)
                                        GPIO.output(35, GPIO.LOW)

                                        #Right Moter Forward
                                        GPIO.output(33, GPIO.LOW)
                                        GPIO.output(31, GPIO.LOW)
                              
                                    if left_sensor_01_data == 0:
                                        #Left Moter Forward
                                        GPIO.output(37, GPIO.LOW)
                                        GPIO.output(35, GPIO.LOW)

                                        #Right Moter Forward
                                        GPIO.output(31, GPIO.HIGH)
                                        GPIO.output(33, GPIO.LOW)
                
                
                
                
                
                
            