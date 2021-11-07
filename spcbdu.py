# Creates delayed server zip file
import requests
import os, json
from zfgen import *
from auth import *
from config import *


# Filter zip files starts with site_id, station_name in SPCB
def filter_zipfiles_with_site_details():
    zipfiles_in_spcb = []
    for file in os.listdir(spcbdir):
        if file.startswith(fsw) & file.endswith(".zip"):
            zipfiles_in_spcb.append(file)
    return zipfiles_in_spcb


# Copies the delayed zip files from SPCB to Delayed.
# Deletes the copied zipfile in SPCB.
def move_zipfiles_to_delayed():
    zipfif = filter_zipfiles_with_site_details()

    for i in range(0, len(zipfif)):
        # Extracting zip file time
        filepath = os.path.join(spcbdir, zipfif[i])
        zfln = zipfif[i]

        # Extracting zip file time
        file_mnt = int(zfln[-8:-6])
        file_hrs = int(zfln[-10:-8])
        file_day = int(zfln[-12:-10])
        file_mon = int(zfln[-14:-12])
        file_yyyy = int(zfln[-18:-14])

        # Present time
        now_utc = datetime.datetime.utcnow()
        local_tz = pytz.timezone('Asia/Kolkata')  # Local timezone which we want to convert the UTC time
        now_utc = pytz.utc.localize(now_utc)  # Add timezone information to UTC time
        x = now_utc.astimezone(local_tz)  # Convert to local time
        mnt = int(x.strftime("%M"))
        hrs = int(x.strftime("%H"))
        day = int(x.strftime("%d"))
        mon = int(x.strftime("%m"))
        yyyy = int(x.strftime("%Y"))

        a = datetime.datetime(yyyy, mon, day, hrs, mnt, 0)
        b = datetime.datetime(file_yyyy, file_mon, file_day, file_hrs, file_mnt, 0)

        c = a - b
        minutes = divmod(c.total_seconds(), 60)  # returns (minutes, seconds)

        if minutes[0] > 18:
            newPath = shutil.copy(filepath, spcb_delayed_path)
            try:
                # remove zip file in SPCB
                rzfis = os.path.join(spcbdir, zfln)
                os.unlink(rzfis)
                # print("File deleted in "+spcbdir+" - ", zfln)
            except:
                pass
                # print("Error while deleting file in "+spcbdir+" - ", zfln)
        else:
            pass
            # print("File is in Realtime ", zfln)


# Returns delayed zipfile name to upload
def zipfile_for_delayed_upload():
    try:
        # zip files in folder
        zipfif = []
        # zip file received in minutes
        frim = []

        for x in os.listdir(spcb_delayed_path):
            zipfif.append(x)

        for i in range(0, len(zipfif)):
            # Extracting zip file time
            zfln = zipfif[i]

            fmin = int(zfln[-8:-6])
            fhrs = int(zfln[-10:-8])
            fday = int(zfln[-12:-10])
            fmon = int(zfln[-14:-12])
            fyear = int(zfln[-18:-14])

            # Present time
            now_utc = datetime.datetime.utcnow()
            local_tz = pytz.timezone('Asia/Kolkata')  # Local timezone which we want to convert the UTC time
            now_utc = pytz.utc.localize(now_utc)  # Add timezone information to UTC time
            x = now_utc.astimezone(local_tz)  # Convert to local time
            mnt = int(x.strftime("%M"))
            hrs = int(x.strftime("%H"))
            day = int(x.strftime("%d"))
            mon = int(x.strftime("%m"))
            yyyy = int(x.strftime("%Y"))

            a = datetime.datetime(yyyy, mon, day, hrs, mnt, 0)
            b = datetime.datetime(fyear, fmon, fday, fhrs, fmin, 0)
            # returns a timedelta object
            c = a - b

            # returns (minutes, seconds)
            minutes = divmod(c.total_seconds(), 60)
            frim.append(minutes[0])
        # print(zipfif)
        # print(frim)
        ofp = frim.index(min(frim))
        return zipfif[ofp]
    except ValueError:
        # print("No files in "+ spcbdir +"/"+dlydir+ " for delayed upload")
        return -1


# Reads zipfile in byte form and returns data
def read_zipfile(zfln):
    filepath = os.path.join(spcb_delayed_path, zfln)
    f = open(filepath, "rb")
    while True:
        data = f.read()
        if not data:
            break
        return data


# Add boundaries to zipfile data
# After adding boundaries to zipfile data.  Creates spcbduf.txt with added data.
def add_boundaries_to_zipfile_data(upload_zipfile_name):
    try:
        os.unlink("spcbduf.txt")
        # print("File Deleted: spcbduf.txt")
    except:
        print("Error while deleting file: spcbduf.txt")

    dzipfln = upload_zipfile_name
    #print(dzipfln)
    zipbuffer = read_zipfile(dzipfln)
    #print(zipbuffer)

    # Create zip file
    # Append-adds at last
    data = '--WebKitFormBoundary7MA4YWxkTrZu0gW\r\n\
Content-Disposition:form-data;name="file";filename="{}"\r\n\
Content-Type:application/zip\r\n\r\n'.format(dzipfln)

    endb = "\r\n--WebKitFormBoundary7MA4YWxkTrZu0gW--\r\n"

    try:
        file1 = open("spcbduf.txt", "wb")  # append mode
        file1.write(data.encode())
        file1.write(zipbuffer)
        file1.write(endb.encode())
        file1.close()
    except:
        dzf = os.path.join(spcb_delayed_path, dzipfln)
        os.unlink(dzf)


# Reads data from spcbduf.txt and returns data
def read_data_to_upload():
    fileName = "spcbduf.txt"
    f = open(fileName, "rb")
    while True:
        data = f.read()
        if not data:
            break
        return data


# Returns length of uploaded data.
def len_of_upload_data():
    upload_data = read_data_to_upload()
    k = len(upload_data)
    return str(k)


# sunjray delayed upload with file name dszfile.zip
def spcb_delayed_upload(x):
    auth, sign, ts = spcb_authorization()
    header = {
        'Host': ospcb_hostAddress,
        'User-Agent': 'DTU',
        'Authorization': 'Bearer ' + auth,
        'Signature': sign,
        'siteId': site_id,
        'timestamp': ts,
        'Content-Type': 'multipart/form-data;boundary=WebKitFormBoundary7MA4YWxkTrZu0gW'
    }
    header['Content-Length'] = len_of_upload_data()
    # print(header)

    # Upload data
    mydata = read_data_to_upload()

    try:
        print("\n**************SPCB Delayed Upload****************")
        print("Uploaded delayed File Name: ", x)
        resp = requests.post(ospcb_delayed_url, headers=header,data=mydata, timeout=180)
        servermsg = json.loads(resp.text)
        if servermsg["status"] == "Success":
            print("\n************SPCB Delayed Upload Response**************")
            print("Successfully uploaded delayed File Name: ", x)
            print(servermsg)
            try:
                dzf = os.path.join(spcb_delayed_path, x)
                os.unlink(dzf)
                print("Deleted uploaded delayed file : ", dzf)
            except:
                pass
                print("Error while deleting uploaded delayed file  ", dzf)
        else:
            print(servermsg)
            time.sleep(30)

    except requests.ConnectionError as e:
        print("Exception raised in delayed upload. \nFile Name: ", x)
        print("OOPS!! Connection Error. Make sure you are connected to Internet.\nTechnical Details given below.")
        print(str(e))
    except requests.Timeout as e:
        print("Exception raised in delayed upload. \nFile Name: ", x)
        print("OOPS!! Timeout Error")
        print(str(e))
    except requests.RequestException as e:
        print("Exception raised in delayed upload. \nFile Name: ", x)
        print("OOPS!! General Error")
        print(str(e))
    except KeyboardInterrupt:
        print("Exception raised in delayed upload. \nFile Name: ", x)
        print("Someone closed the program")


def spcbdumain():
    move_zipfiles_to_delayed()
    dzf = zipfile_for_delayed_upload()
    if dzf != -1:
        add_boundaries_to_zipfile_data(dzf)
        spcb_delayed_upload(dzf)
    else:
        pass


if __name__ == "__main__":
    spcbdumain()





