# Control an LED and read a Button using a web browser
import time
import network
import socket
from machine import Pin,PWM,ADC
from picobricks import SSD1306_I2C
from utime import sleep
import utime
from math import fabs

#from time import sleep
WIDTH = 128
HEIGHT = 64
"""
sda=machine.Pin(4)
scl=machine.Pin(5)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=1000000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
"""
led = Pin(7, Pin.OUT)
ledState = 'LED State Unknown'

current_time=utime.time()
utime.sleep(1)


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = (RED, GREEN, BLUE)


current_time=utime.time()

ssid = "My SSID"
password = "MY Password"

#DC
motor_1 = Pin(21, Pin.OUT)
motor_2 = Pin(22, Pin.OUT)
#servo
"""
servo1=PWM(Pin(21))
servo2=PWM(Pin(22))
servo1.freq(50)
servo2.freq(50)
"""
angleupdown=4770
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

html = """<!DOCTYPE html><html>
<head><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}
body{background-color:white;}
button{background-color:white; border:0px; color:#e62b2b;}

.body_div{background-color:white; display:flex; width:800px; height:400px;  justify-content: center; align-items: center;}
.center_div{display:flex; background-color:white; width:750px; height:350px; flex-direction: row; border-radius: 25px;}
.leftdiv{background-color:#f9b333;width:375px; box-shadow: 0px 15px 10px 0px #e62b2b; height:350px; border-top-left-radius:150px; border-bottom-left-radius:150px; border-bottom-right-radius:150px; border-top-left-radius:150px; flex-direction: column; justify-content: center; align-items: center;}
.first{display:flex; margin:30px 30px 0px 30px; margin-top:60px; }
.buttonup{ display:flex; width:60px; height:60px; border-radius:100px; flex-direction: column; justif-content:center; align-items:center; margin-left:100px; font-size:50px;}

.seccond{ display:flex; flex-direction:row; justify-content:space-between;  margin:20px 30px 20px 30px;}
.buttonleft{ transform: rotate(-90deg); display:flex; width:60px; height:60px; border-radius:100px; flex-direction: column; justify-content: center;  align-items:center; font-size:50px;}
.buttonright{transform: rotate(-90deg); display:flex; width:60px; height:60px; border-radius:100px; flex-direction: column; justify-content: center; align-items:center; font-size:50px;}
.buttonstop{display:flex; width:50px; height:50px; border-radius:100px; flex-direction: column; justify-content:center; align-items:center;  margin-top:10px; font-size:50px;}
.sec1{display:flex; width:50px; height:50px; border-radius:100px; flex-direction: column; justif-content:center; align-items:center; margin-left:0px;  margin-top:10px;}
.sec2{display:flex; width:50px; height:50px; border-radius:100px; flex-direction: column; justif-content:center; align-items:center; margin-right:0px;  margin-top:10px;}
.third{ margin:0px 30px 30px 30px; display:flex;}
.rightdiv{background-color:#ee7131;  box-shadow: 0px 15px 10px 0px #f9b333; width:375px; height:350px;   border-top-right-radius:150px; border-bottom-left-radius:150px; border-bottom-right-radius:150px;}

.buttondown{display:flex; width:60px; height:60px; border-radius:100px; flex-direction: column; justif-content:center; align-items:center; margin-left:100px; font-size:50px;}
.servodown{color:#f9b333; display:flex; width:60px; height:60px; border-radius:100px; flex-direction: column; justif-content:center; align-items:center; margin-left:120px; font-size:50px;}
.servoup{ color:#f9b333; display:flex; width:60px; height:60px; border-radius:100px; flex-direction: column; justif-content:center; align-items:center; margin-left:120px; font-size:50px;}
.servoleft{ color:#f9b333; transform: rotate(-90deg); display:flex; width:60px; height:60px; border-radius:100px; flex-direction: column; justify-content: center;  align-items:center; font-size:50px;}
.servoright{ color:#f9b333; transform: rotate(-90deg); display:flex; width:60px; height:60px; border-radius:100px; flex-direction: column; justify-content: center; align-items:center; font-size:50px;}
.servostop{ color:#f9b333; display:flex; width:50px; height:50px; border-radius:100px; flex-direction: column; justify-content:center; align-items:center;  margin-top:10px; font-size:50px;}
</style></head>
<form> 
<center><div class="body_div">
    <div class="center_div">
        <div class="leftdiv" >
            <div class="first">
                <button class="buttonup" name="motordriver" value="up" type="submit">&#9650;</button>
            </div>
            <div class="seccond">
                <button class="buttonleft" name="motordriver" value="left" type="submit">&#9650;</button>
                <button class="buttonstop" name="motordriver" value="stop" type="submit"></button>
                <button class="buttonright" name="motordriver" value="right" type="submit">&#9660;</button>
                <button class="sec1"></button>
            </div>
            <div class="third">
				<button class="buttondown" name="motordriver" value="down" type="submit">&#9660;</button>
            </div>
        </div>
        <div class="rightdiv" >
            <div class="first">
                <button class="servoup" name="servo" value="sup" type="submit">&#9651;</button>
            </div>
            <div class="seccond">
				<button class="sec2"></button>
                <button class="servoleft" name="servo" value="sleft" type="submit">&#8865;</button>
                <button class="servostop" name="servo" value="sstop" type="submit"></button>
                <button class="servoright" name="servo" value="sright" type="submit">&#8857;</button>
                
            </div>
            <div class="third">
				<button class="servodown" name="servo" value="sdown" type="submit">&#120247;</button>
            </div>
        </div>
    </div>
</div></center>
</form>
</body></html>
"""
"""
oled.text("Power On",30,0)
oled.text("Waiting for ",20, 30)
oled.text("Connection",23, 40)
oled.show()
time.sleep(2)
oled.fill(0)
"""
# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)
    
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )
    
# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)
"""
oled.text("IP",50, 0)
oled.text(str(status[0]),20, 10)
oled.text("Connected",25, 20)
oled.show()
"""
def CalculateAngle(angle):
   angle = fabs((angle * (6000 / 180)) + 2000)
   angle = round(angle)
   return angle
"""
servo1_limited=180
servo1_angle=0
servo2_limited=180
servo2_angle=0
"""
while True:
    sleep(0.1)  
    try:       
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print("request:")
        print(request)
        request = str(request)
        motordriver_up = request.find('motordriver=up')
        motordriver_down = request.find('motordriver=down')
        motordriver_stop = request.find('motordriver=stop')
        motordriver_right = request.find('motordriver=right')
        motordriver_left = request.find('motordriver=left')
        
        servo_up = request.find('servo=sup')
        servo_down = request.find('servo=sdown')
        servo_stop = request.find('servo=sstop')
        servo_right = request.find('servo=sright')
        servo_left = request.find('servo=sleft')
        
        print( 'motordriver up = ' + str(motordriver_up))
        print( 'motordriver down = ' + str(motordriver_down))
        print( 'motordriver stop = ' + str(motordriver_stop))
        print( 'motordriver right = ' + str(motordriver_right))
        print( 'motordriver left = ' + str(motordriver_left))
        
        print( 'servo up = ' + str(servo_up))
        print( 'servo down = ' + str(servo_down))
        print( 'servo stop = ' + str(servo_stop))
        print( 'servo right = ' + str(servo_right))
        print( 'servo left = ' + str(servo_left))
        
        
        
        if motordriver_up == 8:
            print("Motor Driver on")
            motor_1.high()
            motor_2.high()
            
        if motordriver_down == 8:
            print("Motor Driver off")
            motor_1.low()
            motor_2.low()
            
        if motordriver_stop == 8:
            print("Motor Driver off")
            motor_1.low()
            motor_2.low()
            
        if motordriver_right == 8:
            print("Motor Driver off")
            motor_1.low()
            motor_2.high()
            
        if motordriver_left == 8:
            print("Motor Driver off")
            motor_1.high()
            motor_2.low()
            
        """
        if servo_up == 8:
            servo1_angle=servo1_angle-10
            servo1.duty_u16(CalculateAngle(servo1_angle)) 
            sleep(0.3)
             
            
        if servo_down == 8:
            servo1_angle=servo1_angle+10
            servo1.duty_u16(CalculateAngle(servo1_angle))
            
        if servo_stop == 8:
            servo1.duty_u16(0) #180 degree
            sleep(0.3)
            servo2.duty_u16(0) #180 degree
            sleep(0.3)
            
        if servo_right == 8:
            servo2_angle=servo2_angle+20
            servo2.duty_u16(CalculateAngle(servo2_angle))
            sleep(0.3)
            
            
        if servo_left == 8:
            servo2_angle=servo2_angle-20
            servo2.duty_u16(CalculateAngle(servo2_angle))
            sleep(0.3)
        """
        # Create and send response
      
        response = html 
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('connection closed')
