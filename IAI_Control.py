import serial
import time
import math
from valve import *


set_port = '/dev/ttyUSB0' 
set_baudrate = 38400
set_timeout = 3

ser = serial.Serial(set_port,set_baudrate,timeout=set_timeout)

# Preset waypoints for different shapes
waypoints = {
    'star': [[(130,40,0),(110,70,0),(130,100,0),(100,85,0),(90,100,0),(90,80,0),(70,70,0),(90,60,0),(90,40,0),(100,55,0),(130,40,0)]],
    'boat': [[(110,40,0),(130,50,0),(130,90,0),(110,100,0),(110,40,0)],
             [(110,70,0),(70,70,0),(70,65,0),(110,65,0)],
             [(90,70,0),(80,100,0),(70,70,0)]],
    'umbrella': [[(100,45,0),(100,70,0),(100,95,0)],
                 [(100,70,0),(120,70,0),(120, 75, 0), (115, 75, 0)]],
    'flake': [[(100,40,0),(100,100,0)],
              [(130,70,0),(70,70,0)],
              [(120,50,0),(80,90,0)],
              [(80,50,0),(120,90,0)],
              [(110,40,0),(100,50,0),(90,40,0)],
              [(70,60,0),(80,70,0),(70,80,0)],
              [(90,100,0),(100,90,0),(110,100,0),
               (130,80,0),(120,70,0),(130,60,10)]],
    'smile-face': [[(85,60,0), (95,60,0)],
                   [(85,80,0), (95,80,0)]]
}

def initialize():
    # Homing the robot by sending specific serial commands

    ser.write('!00232071b0\r\n'.encode())
    read = ser.readline().decode()
    print(read+'\n')

    time.sleep(3)

    ser.write('!0023307000000A0\r\n'.encode())
    read = ser.readline().decode()
    print(read+'\n')

    time.sleep(3)


def IAI_Robot_Move(message_id,axis,acceleration,speed,x_target,y_target,z_target) :
    # Send a command to move the robot to a specified position

    if message_id == 'absolute' :
        message_id = '234'
    elif  message_id == 'relative' :
        message_id = '235'

    axis_pattern = 0b0
    if 'x' in axis :
        axis_pattern = axis_pattern + 0b1
    if 'y' in axis :
        axis_pattern = axis_pattern + 0b10    
    if 'z' in axis :
        axis_pattern = axis_pattern + 0b100    
    byte_format = 2
    byte_adding = byte_format - len(hex(axis_pattern).lstrip('0x'))
    adding_text = ''
    for i in range(0,byte_adding):
        adding_text = adding_text + '0'
    axis_pattern = adding_text + hex(axis_pattern).lstrip('0x')

    byte_format = 4
    byte_adding = byte_format - len(hex(int(acceleration*100)).lstrip('0x'))
    adding_text = ''
    for i in range(0,byte_adding):
        adding_text = adding_text + '0'
    acceleration = adding_text + hex(int(acceleration*100)).lstrip('0x')

    byte_format = 4
    byte_adding = byte_format - len(hex(int(speed)).lstrip('0x'))
    adding_text = ''
    for i in range(0,byte_adding):
        adding_text = adding_text + '0'
    speed = adding_text + hex(int(speed)).lstrip('0x')

    position = '';
    byte_format = 8
    if 'x' in axis :
        if x_target >=0 :
            byte_adding = byte_format - len(hex(int(x_target*1000)).lstrip('0x'))
            adding_text = ''
            for i in range(0,byte_adding):
                adding_text = adding_text + '0'            
            position = position + adding_text + hex(int(x_target*1000)).lstrip('0x')
        else :
            x_target = -x_target
            position = position + hex(int(16**byte_format - x_target*1000)).lstrip('0x')
    if 'y' in axis :
        if y_target >=0 :
            byte_adding = byte_format - len(hex(int(y_target*1000)).lstrip('0x'))
            adding_text = ''
            for i in range(0,byte_adding):
                adding_text = adding_text + '0'            
            position = position + adding_text + hex(int(y_target*1000)).lstrip('0x')
        else :
            y_target = -y_target
            position = position + hex(int(16**byte_format - y_target*1000)).lstrip('0x')
    if 'z' in axis :
        if z_target >=0 :
            byte_adding = byte_format - len(hex(int(z_target*1000)).lstrip('0x'))
            adding_text = ''
            for i in range(0,byte_adding):
                adding_text = adding_text + '0'            
            position = position + adding_text + hex(int(z_target*1000)).lstrip('0x')
        else :
            z_target = -z_target
            position = position + hex(int(16**byte_format - z_target*1000)).lstrip('0x')

    string_command = '!00'+ message_id + axis_pattern + acceleration + acceleration + speed + position

    checksum = 0
    for i in range(0,len(string_command)) :
        checksum = checksum + ord(string_command[i])
    checksum = hex(int(checksum)).lstrip('0x')
    checksum = checksum[len(checksum)-2:len(checksum)]

    string_command = string_command + checksum
    print(string_command)
    
    ser.write((string_command +'\r\n').encode())
    read = ser.readline().decode()
    print(read+'\n')

def IAI_get_pos():
    #Request and return the current position of the robot

    s = "!0021207@@"
    ser.write((s + '\r\n').encode())
    read = ser.readline().decode()

    x = int(read[16:24], 16) / 1000
    y = int(read[31:40], 16) / 1000
    z = int(read[48:56], 16) / 1000

    return (x, y, z)

def IAI_Draw_Circle(radius,start_point, end_points, speed, x_center, y_center):
    #Draw a circle using parametric equation that creates each (x,y) position on the circle

    IAI_Robot_Move('absolute','xyz', 0.3, 100, x_center,y_center, 80)
    time.sleep(2)
    
    in_pos = False
    
    angle_increment = 2 * math.pi / 360

    for i in range(start_point, end_points):
        angle = i * angle_increment
        
        y_target = y_center + radius * math.cos(angle)
        x_target = x_center + radius * math.sin(angle)

        IAI_Robot_Move('absolute', 'xy', 0, speed, x_target, y_target,0)
        
        if not in_pos:
            time.sleep(2)
            IAI_Robot_Move('absolute', 'z', 0, speed, x_target, y_target,94)
            time.sleep(1)
            valveOn()
            in_pos = True
            
    valveOff()
    time.sleep(1)
    IAI_Robot_Move('absolute','xyz', 0.3, 100, x_center,y_center, 80)
    
    
def IAI_Draw_Waypoints(speed, x_center, y_center, shape_waypoints: list,sleep=0):
    # Move the robot along a series of waypoints

    IAI_Robot_Move('absolute', 'xy', 0.3, 100, x_center, y_center, 0)
    time.sleep(2)

    for waypoint in shape_waypoints:
        in_pos = False
        for coor in waypoint:
            IAI_Robot_Move('absolute', 'xy', 0.3, speed, *coor)
            time.sleep(sleep)
            if not in_pos:
                time.sleep(2)
                IAI_Robot_Move('absolute', 'z', 0.3, speed, coor[0],coor[1] , 94)
                time.sleep(1)
                in_pos = True
                valveOn()

        valveOff()
        time.sleep(1)
        IAI_Robot_Move('absolute', 'z', 0.3, 100, 0, 0, 80)

    time.sleep(1)
    valveOff()
    IAI_Robot_Move('absolute', 'xy', 0.3, 100, x_center, y_center, 80)

def IAI_Draw_Smile_Face(speed, x_center, y_center):
    # Draw a smiley face shape from preset waypoints

    smile_face_waypoints = waypoints['smile-face']
    IAI_Draw_Circle(30, 0, 360, speed, 100, 70)
    time.sleep(1)

    IAI_Draw_Circle(20, 0, 180, 30, 100, 70)
    time.sleep(1)

    IAI_Draw_Waypoints(speed, x_center, y_center, smile_face_waypoints)

def IAI_Draw_Star(speed, x_center, y_center):
    # Draw a star shape from preset waypoints

    star_waypoints = waypoints['star']
    IAI_Draw_Waypoints(speed, x_center, y_center, star_waypoints, 1.5)

def IAI_Draw_Boat(speed, x_center, y_center):
    # Draw a boat shape from preset waypoints

    boat_waypoints = waypoints['boat']
    IAI_Draw_Waypoints(speed, x_center, y_center, boat_waypoints, 1.5)

def IAI_Draw_Umbrella(speed, x_center, y_center):
    # Draw an umbrella shape from preset waypoints

    umbrella_waypoints = waypoints['umbrella']
    IAI_Draw_Waypoints(speed, x_center, y_center, umbrella_waypoints, 1)

    IAI_Draw_Circle(23, 180, 360, 50, 100, 70)

def IAI_Draw_Flake(speed, x_center, y_center):
    # Draw an flake shape from preset waypoints

    flake_waypoints = waypoints['flake']
    IAI_Draw_Waypoints(speed, x_center, y_center, flake_waypoints, 1)


def IAI_Free_Draw(x_center, y_center, strokes):
    # Allow custom drawing based on a series of strokes

    IAI_Robot_Move('absolute', 'xyz', 0.3, 100, x_center, y_center, 80)
    time.sleep(2)

    for stroke in strokes:
        in_pos = False
        for x, y in stroke:
            x += 40
            y += 70
            
            IAI_Robot_Move('absolute', 'xy', 0.3, 30, y, x, 0)
            
            if not in_pos:
                time.sleep(2)
                IAI_Robot_Move('absolute', 'z', 0.3, 30, y, x, 94)
                time.sleep(1)
                in_pos = True
                valveOn()
                
        valveOff()
        time.sleep(1)
        IAI_Robot_Move('absolute', 'z', 0.3, 30, y, x, 80)
        time.sleep(1)
    
    valveOff()
    IAI_Robot_Move('absolute', 'xyz', 0.3, 100, x_center, y_center, 80)
    





