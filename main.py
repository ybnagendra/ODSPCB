from time import sleep
from threading import *

from spcbdu import *
from spcbru import *


# Generate one zip file for every minute
class GMZIPFILE(Thread):
    def run(self):
        print("Program Started")
        create_dirs_pwd()
        create_dirs_spcb()
        while True:
            try:
                zfgen_main()
            except:
                pass


class SPCBUpload(Thread):
    def run(self):
        print("SPCB Upload Thread Starts")
        while True:
            try:
                spcbrumain()
            except:
                print("Exception in SPCB Realtime upload")
            try:
                spcbdumain()
            except:
                print("Exception in SPCB Delayed upload")


if __name__  == "__main__":
    t1 = GMZIPFILE()
    t1.start()
    sleep(5)

    t2 = SPCBUpload()
    t2.start()
    sleep(5)


