import copy
import omega_gpio
# import datetime
import time


# import urllib2

class KEYPAD:
    def getPressKey(self):
        a = [0, 1, 2, 3, 11, 18, 8, 9]
        r = [0, 1, 2, 3]
        c = [18, 11, 8, 9]

        key = [
            ["1", "2", "3", "A"],
            ["4", "5", "6", "B"],
            ["7", "8", "9", "C"],
            ["*", "0", "#", "D"],
        ]

        values = [
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
        ]

        lastvalues = copy.deepcopy(values)

        # close before open if used
        for pin in a:
            try:
                omega_gpio.closepin(pin)
            except:
                e = 1  # dummy command :-)

        # pin init
        for pin in r:
            omega_gpio.initpin(pin, 'out')

        for pin in c:
            omega_gpio.initpin(pin, 'in')

        while True:
            rpos = 0
            for rpin in r:
                omega_gpio.setoutput(r[0], 0)
                omega_gpio.setoutput(r[1], 0)
                omega_gpio.setoutput(r[2], 0)
                omega_gpio.setoutput(r[3], 0)
                omega_gpio.setoutput(rpin, 1)
                time.sleep(0.05)
                cpos = 0
                for cpin in c:
                    input = omega_gpio.readinput(cpin)
                    values[rpos][cpos] = input
                    cpos = cpos + 1
                rpos = rpos + 1

            for x in range(0, 4):
                for y in range(0, 4):
                    if values[x][y] != lastvalues[x][y]:
                        self.keycode = key[x][y]
                        if values[x][y] == 1:
                            return self.keycode

            lastvalues = copy.deepcopy(values)

    def checkKey(self):
        a = [0, 1, 2, 3, 11, 18, 8, 9]
        r = [0, 1, 2, 3]
        c = [18, 11, 8, 9]

        key = [
            ["1", "2", "3", "A"],
            ["4", "5", "6", "B"],
            ["7", "8", "9", "C"],
            ["*", "0", "#", "D"],
        ]

        values = [
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
        ]

        lastvalues = copy.deepcopy(values)

        # close before open if used
        for pin in a:
            try:
                omega_gpio.closepin(pin)
            except:
                e = 1  # dummy command :-)

        # pin init
        for pin in r:
            omega_gpio.initpin(pin, 'out')

        for pin in c:
            omega_gpio.initpin(pin, 'in')

        if True:
            rpos = 0
            for rpin in r:
                omega_gpio.setoutput(r[0], 0)
                omega_gpio.setoutput(r[1], 0)
                omega_gpio.setoutput(r[2], 0)
                omega_gpio.setoutput(r[3], 0)
                omega_gpio.setoutput(rpin, 1)
                time.sleep(0.05)
                cpos = 0
                for cpin in c:
                    input = omega_gpio.readinput(cpin)
                    values[rpos][cpos] = input
                    cpos = cpos + 1
                rpos = rpos + 1

            for x in range(0, 4):
                for y in range(0, 4):
                    if values[x][y] != lastvalues[x][y]:
                        keycode = key[x][y]
                        if values[x][y] == 1:
                            if keycode == '1':
                                print(keycode)
                            elif keycode == '2':
                                print(keycode)
                            elif keycode == '3':
                                print(keycode)
                            elif keycode == '4':
                                print(keycode)
                            elif keycode == '5':
                                print(keycode)
                            elif keycode == '6':
                                print(keycode)
                            elif keycode == '7':
                                print(keycode)
                            elif keycode == '8':
                                print(keycode)
                            elif keycode == '9':
                                print(keycode)
                            elif keycode == '0':
                                print(keycode)
                            elif keycode == 'A':
                                print(keycode)
                            elif keycode == 'B':
                                print(keycode)
                            elif keycode == 'C':
                                print(keycode)
                            elif keycode == 'D':
                                print(keycode)
                            elif keycode == '*':
                                print(keycode)
                            elif keycode == '#':
                                print(keycode)

            lastvalues = copy.deepcopy(values)


if __name__ == "__main__":
    print("Press any Key ")
    k = KEYPAD()

    while True:
        k.checkKey()
        # time.sleep(2)
        # key=k.getPressKey()
        # print("Pressed Key: ", key)
        # print("")
        # time.sleep(2)
