#!/usr/bin/env python

#!/usr/bin/env python

import time
from DS3231 import DS3231_Driver

# Main Program
ds3231 = DS3231_Driver.SDL_DS3231(0, 0x68)

# comment out the next line after the clock has been initialized
# ds3231.write_now()                    #through Wifi
# ds3231.set_datetime()                 #through user input

# Main Loop - sleeps 10 seconds, then reads and prints values of all clocks


if __name__ == "__main__":
        key=raw_input("Enter the mode 1 or 2: ")
        if (key == '1'):
                ds3231.set_datetime()
        elif(key == '2'):
                pass

        while(1):

                DS3231=ds3231.read_datetime()
                ds=str(DS3231)

                dt1=ds[8:10]+ds[5:7]+ds[2:4]
                #print(dt1)
                _secs=ds[17:]
                _mnts=ds[14:16]
                secs=int(_secs)
                mnts=int(_mnts)
                if secs%5==0:
                        print(mnts, secs, dt1)
                        print(ds)
                        #print("DS3231=\t%s" % ds3231.read_datetime())
                        time.sleep(1)
                        print("")
