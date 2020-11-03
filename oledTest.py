# To Capture image OLED Display

from OmegaExpansion import oledExp
import time

def welcomeMessage():
    oledExp.setVerbosity(0)
    oledExp.driverInit()
    oledExp.setCursor(3, 0)
    oledExp.write("Welcome to OnionOmega")
    oledExp.setCursor(4, 0)
    oledExp.write("Data Logger Project")
    time.sleep(2)

def displayModes():
    oledExp.clear()
    oledExp.setCursor(0, 0)
    oledExp.write("Select mode(1,2,3):")
    oledExp.setCursor(1, 0)
    oledExp.write("1. CONF MODE")
    oledExp.setCursor(2, 0)
    oledExp.write("2. RUN MODE")
    oledExp.setCursor(3, 0)
    oledExp.write("3. BACKUP MODE")
    oledExp.setCursor(5, 0)
    oledExp.write("Mode of Operation:")

def conf_oledDisplay1():
    oledExp.clear()
    oledExp.setCursor(0, 0)
    oledExp.write("Conf. Processing")
    oledExp.setCursor(6, 0)
    oledExp.write("*********************")
    oledExp.setCursor(7, 3)
    oledExp.write("CONFIGURE MODE")

def conf_oledDisplay2(self):
    oledExp.setCursor(2, 0)
    oledExp.write("Configuartion done")
    oledExp.setCursor(4, 9)
    oledExp.write("WAIT")
    time.sleep(2)
    oledExp.clear()

def run_oledDisplay1():
    d = GET_DATE_TIME()
    print("Remove Pendrive to enter run mode")
    oledExp.setCursor(0, 0)
    oledExp.write(d.oledDate)
    oledExp.setCursor(1, 0)
    oledExp.write("*********************")
    oledExp.setCursor(2, 3)
    oledExp.write("Remove USB to ")
    oledExp.setCursor(3, 3)
    oledExp.write("enter run mode ")
    oledExp.setCursor(6, 0)
    oledExp.write("*********************")
    oledExp.setCursor(7, 3)
    oledExp.write("WAITING MODE")
    time.sleep(2)

def run_oledDisplay2():
    oledExp.setCursor(3, 0)
    oledExp.write("USB Connected")
    time.sleep(1)
    oledExp.clear()

def bkp_oledDisplay1():
    oledExp.clear()
    oledExp.setCursor(0, 0)
    oledExp.write("Enter FROM and TO")
    oledExp.setCursor(1, 0)
    oledExp.write("dates in the format:")
    oledExp.setCursor(2, 0)
    oledExp.write("dd*mm*yy ")
    oledExp.setCursor(3, 0)
    oledExp.write("Ex: 23/01/20")
    time.sleep(2)

def bkp_oledDisplay2():
    oledExp.clear()
    oledExp.setCursor(1, 0)
    oledExp.write("FROM DATE: ")
    oledExp.setCursor(2, 0)
    oledExp.write(fromDate)

def bkp_oledDisplay3():
    oledExp.clear()
    oledExp.setCursor(1, 0)
    oledExp.write("TO DATE: ")
    oledExp.setCursor(2, 0)
    oledExp.write(toDate)

if __name__ == "__main__":
    welcomeMessage()

    raw_input("Press any Key: ")
    oledExp.clear()
    time.sleep(1)
    displayModes()

    raw_input("Press any Key: ")
    oledExp.clear()
    time.sleep(1)
    conf_oledDisplay1()

    raw_input("Press any Key: ")
    oledExp.clear()
    time.sleep(1)
    conf_oledDisplay2()

    raw_input("Press any Key: ")
    oledExp.clear()
    time.sleep(1)
    run_oledDisplay1()

    raw_input("Press any Key: ")
    oledExp.clear()
    time.sleep(1)
    run_oledDisplay2()

    raw_input("Press any Key: ")
    oledExp.clear()
    time.sleep(1)
    bkp_oledDisplay1()

    raw_input("Press any Key: ")
    oledExp.clear()
    time.sleep(1)
    bkp_oledDisplay2()

    raw_input("Press any Key: ")
    oledExp.clear()
    time.sleep(1)
    bkp_oledDisplay3()



