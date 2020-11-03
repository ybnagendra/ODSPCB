import serial
import time

# Open port with baud rate
ser = serial.Serial(port="/dev/ttyS1", baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,timeout=100)
if __name__=="__main__":
        siteId = ''
        monitoringId = ''
        analyzerId = ''
        parameterId = ''
        while len(siteId) == 0:
            # Serial input
            ser.write('Enter site ID: ')
            siteId = ser.read()  # read serial port
            time.sleep(0.03)
            data_left = ser.inWaiting()  # check for remaining byte
            siteId += ser.read(data_left)
            ser.write(siteId + '\r\n')
        while len(monitoringId) == 0:
            ser.write('Enter monitoring ID: ')
            monitoringId = ser.read()  # read serial port
            time.sleep(0.03)
            data_left = ser.inWaiting()  # check for remaining byte
            monitoringId += ser.read(data_left)
            ser.write(monitoringId + '\r\n')
        while len(analyzerId) == 0:
            ser.write('Enter analyserID: ')
            analyzerId = ser.read()  # read serial port
            time.sleep(0.03)
            data_left = ser.inWaiting()  # check for remaining byte
            analyzerId += ser.read(data_left)
            ser.write(analyzerId + '\r\n')
        while len(parameterId) == 0:
            ser.write('Enter ParameterID: ')
            parameterId = ser.read()  # read serial port
            time.sleep(0.03)
            data_left = ser.inWaiting()  # check for remaining byte
            parameterId += ser.read(data_left)
            ser.write(parameterId + '\r\n')

        f = open('confdata.txt', 'w')
        f.write(siteId + '\n')
        f.write(monitoringId + '\n')
        f.write(analyzerId + '\n')
        f.write(parameterId + '\n')

        print("Program Ends")
