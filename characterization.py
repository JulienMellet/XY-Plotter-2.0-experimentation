#!/usr/bin/python

import glob
import serial
import platform
import time
import processing
import kalman
import numpy as np
from io import StringIO


###############################################################################
# TODO: implement an interactive terminal with getch()?
# https://stackoverflow.com/questions/510357/python-read-a-single-character-from-the-user

def main():

    rx = processing.init_position()
    
    #port = serial_init()
    # Number of step on stepper motor
    d = 1314
    # Distance in centimeter
    x = 30
    
    buffer = StringIO()

    # For IMU
    I_Accelero = np.zeros(3)
    data_accel = np.zeros((3,3))
    s_acc = 0.0423639918

    # For Kalman Filter
    I_True = np.zeros(3)
    s_True = np.zeros(3)
    for i in range(3):
        s_True[i] = 0.00001
    
    start = time.time()
    print(start)
    
    duration = 0
    
    while duration < 15: # not sine_done(port):
        # Measurements
        print("1")
        I_LH, data_accel, s_acc = processing.get_position(rx)
        I_Accelero = data_accel[0]
        I_LH = [(I_LH[0][0] + I_LH[3][0]) / 2, (I_LH[0][1] + I_LH[3][1]) / 2, (I_LH[0][2] + I_LH[3][2]) / 2]
        print("2")
        # Kalman Filter of the position
        # Measurement of variances in static
        s_Accelero = s_acc[0]
        for i in range(3):
            s_Accelero[i] = s_Accelero[i]**2
        #print(s_Accelero)
        s_LH = [1.02121*10**(-6), 8.667*10**(-7), 9.6482*10**(-7)]

        # Update position calculated by Kalman filter
        #I_True, s_True = kalman.linear_kalman(data_accel, s_Accelero, I_LH, s_LH, I_True, s_True)

        # Madgwick fusion
        I_True = kalman.madgwick(data_accel, s_Accelero, I_LH, s_LH)
        
        duration = time.time() - start
        print(duration)
        # Print file
        # [duration, I_LH, I_Accelero, I_True]
        buffer.write("%s," % duration)
        for i in range(3):
            buffer.write("%s," % I_LH[i])
        for i in range(3):
            buffer.write("%s," % I_Accelero[i])
        for i in range(2):
            buffer.write("%s," % I_True[i])
        buffer.write("%s \n" % I_True[2])        

    
    BUF = buffer.getvalue()
    file = open("data_2_IMU05s_Sin2.txt","w")
    file.write(BUF)
    file.close()
    
    while True:
        pass


###############################################################################
def serial_init():
    PLATFORM = platform.system()
    if "Linux" in PLATFORM:
        SERIAL_PATH = "/dev/ttyUSB*"
    elif "Darwin" in PLATFORM:
        SERIAL_PATH = "/dev/tty.usb*"
    else: # Windows
        port = serial.Serial('COM6', 115200, timeout = 0)        # TODO ADAPT COM NUMBER !!
        SERIAL_PATH = 'WIN_WORKARAOUND'

    if SERIAL_PATH != 'WIN_WORKARAOUND':
        devices = glob.glob(SERIAL_PATH)
        port = serial.Serial(devices[0], 115200)

    success = port.isOpen()

    if success:
        print("Port open, waiting for calibration...\n")
        line = port.readline()
        while ("start".encode(encoding="utf-8") not in line):
            line = port.readline()
    else:
        print("\n!!! Error: serial device not found !!!")
        exit(-1)
    return port


###############################################################################
def sine_x(port):
    command = "M5" # L1 R" + str(int(d/3)) # 10cm
    port.write(command.encode(encoding="utf-8"))
    print(command)

def sine_done(port):
    line = port.readline()
    if ("ok".encode(encoding="utf-8") in line):
        return True
    else:
        return False

###############################################################################
def go_to(x, port):
    command = "X" + str(x)+ "\n"
    port.write(command.encode(encoding="utf-8"))
    print(command)

    # wait for acknowledgment
    line = port.readline()
    while ("ok".encode(encoding="utf-8") not in line):
        line = port.readline()


###############################################################################
if __name__ == "__main__":
    main()
