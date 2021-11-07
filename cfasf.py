import os,sys
import shutil
from config import *

pwd = os.getcwd()

bkpfld_path = os.path.join(pwd, bkpdir)
spcb_path = os.path.join(pwd, spcbdir)
cpcb_path = os.path.join(pwd, cpcbdir)

spcb_realtime_path = os.path.join(spcb_path, rtdir)
spcb_delayed_path = os.path.join(spcb_path, dlydir)

cpcb_realtime_path = os.path.join(cpcb_path, rtdir)
cpcb_delayed_path = os.path.join(cpcb_path, dlydir)


# Create BKPDIR,SPCB,CPCB folders in the present working directory(pwd) for functionality of the program.
def create_dirs_pwd():
    isdir1 = os.path.isdir(bkpdir)
    if isdir1 == 0:
        os.mkdir(bkpfld_path)
        print(bkpdir+" directory created")
    else:
        print(bkpdir+" directory is already exists.")

    isdir2 = os.path.isdir(spcbdir)
    if isdir2 == 0:
        os.mkdir(spcb_path)
        print(spcbdir+" directory created")
    else:
        print(spcbdir+" directory is already exists.")

    isdir3 = os.path.isdir(cpcbdir)
    if isdir3 == 0:
        os.mkdir(cpcb_path)
        print(cpcbdir+" directory created")
    else:
        print(cpcbdir+" directory is already exists.")


# Create directories Realtime and Delayed in CPCB.
def create_dirs_cpcb():
    sf1 = os.path.isdir(cpcb_realtime_path)
    if sf1 == 0:
        os.mkdir(cpcb_realtime_path)
        print(rtdir+" sub-directory created in "+cpcbdir)
    else:
        shutil.rmtree(cpcb_realtime_path)
        print(rtdir+" deleted in "+cpcbdir)
        os.mkdir(cpcb_realtime_path)
        print(rtdir+" sub-directory created in "+cpcbdir)

    sf2 = os.path.isdir(cpcb_delayed_path)
    if sf2 == 0:
        os.mkdir(cpcb_delayed_path)
        print(dlydir+" sub-directory created in "+cpcbdir)
    else:
        print(dlydir+" sub-directory already exists in "+cpcbdir)


# Create directories Realtime and Delayed in SPCB.
def create_dirs_spcb():
    sf1 = os.path.isdir(spcb_realtime_path)
    if sf1 == 0:
        os.mkdir(spcb_realtime_path)
        print(rtdir+" sub-directory created in "+spcbdir)
    else:
        shutil.rmtree(spcb_realtime_path)
        print(rtdir+" deleted in "+spcbdir)
        os.mkdir(spcb_realtime_path)
        print(rtdir+" sub-directory created in "+spcbdir)

    sf2 = os.path.isdir(spcb_delayed_path)
    if sf2 == 0:
        os.mkdir(spcb_delayed_path)
        print(dlydir+" sub-directory created in "+spcbdir)
    else:
        print(dlydir+" sub-directory already exists in "+spcbdir)


if __name__ == "__main__":
    create_dirs_pwd()
    create_dirs_cpcb()
    create_dirs_spcb()