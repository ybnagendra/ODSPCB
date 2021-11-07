import requests
import json
import datetime, time
from auth import *
from config import *

pwd = os.getcwd()


# Delete real time timeout zip files in SPCB Realtime directory after 10 minutes.
# List all files in SPCB Realtime directory(spcb_realtime_path).
# Filter zip files with site_id and station_name in SPCB Realtime directory.
# Extract created time from file name
# Calculate the difference of time from Realtime to file created time.
# If the difference is more than 10 minutes, then the file is not eligible for realtime upload. So deletes that -
#  zipfile from Realtime directory.
def del_realtime_timeout_zipfiles():
    list_of_zipfiles = []
    allfiles = os.listdir(spcb_realtime_path)

    for file in allfiles:
        if file.startswith(fsw) & file.endswith(".zip"):
            list_of_zipfiles.append(file)

    for i in range(0, len(list_of_zipfiles)):
        name_of_zipfile = list_of_zipfiles[i]

        # Extracting zip file time
        file_mnt = int(name_of_zipfile[-8:-6])
        file_hrs = int(name_of_zipfile[-10:-8])
        file_day = int(name_of_zipfile[-12:-10])
        file_mon = int(name_of_zipfile[-14:-12])
        file_yyyy = int(name_of_zipfile[-18:-14])

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

        c = a - b  # returns a timedelta object
        minutes = divmod(c.total_seconds(), 60)  # returns (minutes, seconds)
        if minutes[0] > 10:
            try:
                zipfile_path = os.path.join(spcb_realtime_path, name_of_zipfile)
                print(zipfile_path)
                os.unlink(zipfile_path)
                print("File deleted in " + spcbdir + "/Realtime- ", name_of_zipfile)
            except:
                print("Error while deleting file in " + spcbdir + "/Realtime- ", name_of_zipfile)


# Returns Realtime zipfile name to upload.
def zipfile_for_realtime_upload():
    try:
        zipfiles = []         # zip files in folder
        # zip file received in minutes
        frim = []

        for x in os.listdir(spcb_realtime_path):
            zipfiles.append(x)

        for i in range(0, len(zipfiles)):
            # Extracting zip file time
            name_of_zipfile = zipfiles[i]

            # Extracting zip file time
            file_mnt = int(name_of_zipfile[-8:-6])
            file_hrs = int(name_of_zipfile[-10:-8])
            file_day = int(name_of_zipfile[-12:-10])
            file_mon = int(name_of_zipfile[-14:-12])
            file_yyyy = int(name_of_zipfile[-18:-14])

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
            c = a - b       # returns a timedelta object
            minutes = divmod(c.total_seconds(), 60)     # returns (minutes, seconds)

            if 2 < minutes[0] < 10:
                frim.append(minutes[0])
        ofp = frim.index(max(frim))
        return zipfiles[ofp]
    except ValueError:
        # print("No files in "+spcbdir+"/"+rtdir+ " for realtime upload")
        return -2


# Read upload zipfile
def read_zipfile(zfln):
    filepath = os.path.join(spcb_realtime_path, zfln)
    f = open(filepath, "rb")
    while True:
        data = f.read()
        if not data:
            break
        return data


# Adds boundaries to the zipfile data
def add_boundaries_to_zipfile_data(upload_zipfile_name):
    try:
        os.unlink("spcbruf.txt")
        # print("File Deleted: spcbruf.txt")
    except:
        pass
        # print("Error while deleting file: spcbruf.txt")

    zipbuffer = read_zipfile(upload_zipfile_name)
    # print(zipbuffer)

    # Create zip file
    # Append-adds at last
    data = '--WebKitFormBoundary7MA4YWxkTrZu0gW\r\n\
Content-Disposition:form-data;name="file";filename="{}"\r\n\
Content-Type:application/zip\r\n\r\n'.format(upload_zipfile_name)
    # print(data)

    endb = "\r\n--WebKitFormBoundary7MA4YWxkTrZu0gW--\r\n"

    file1 = open("spcbruf.txt", "wb")  # append mode
    file1.write(data.encode())
    file1.write(zipbuffer)
    file1.write(endb.encode())
    file1.close()


# Reads data from spcbruf.txt
def read_data_to_upload():
    fileName = "spcbruf.txt"
    f = open(fileName, "rb")
    while True:
        data = f.read()
        if not data:
            break
        return data


# Returns length of uploaded data
def len_of_upload_data():
    upload_data = read_data_to_upload()
    k = len(upload_data)
    return str(k)


# Uploads the Realtime zip file
# Deletes the zip file from SPCB/Realtime folder after getting Success message from the server.
def spcb_realtime_upload(upload_zipfile_name):
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

    upload_data = read_data_to_upload()

    try:
        print("\n**************SPCB Realtime upload****************")
        print("Uploaded Realtime File Name: ", upload_zipfile_name)
        resp = requests.post(ospcb_realtime_url, headers=header, data=upload_data, timeout=180)
        servermsg = json.loads(resp.text)
        print("status code " + str(resp.status_code))

        if servermsg["status"] == "Success":
            print("\n*********SPCB Realtime Upload Response**********")
            print("Successfully uploaded Realtime file Name: ", upload_zipfile_name)
            print(servermsg)

            try:
                rmzfit = os.path.join(spcb_realtime_path, upload_zipfile_name)
                os.unlink(rmzfit)
                print("Deleted Real time uploaded file in " + spcbdir + "/Realtime: ", upload_zipfile_name)
            except:
                print("Error while deleting Real time uploaded file in " + spcbdir + "/Realtime: ", upload_zipfile_name)
        else:
            print(servermsg)
            time.sleep(30)

    except requests.ConnectionError as e:

        print("Exception raised in Real time upload. \nFile Name: ", upload_zipfile_name)

        print("OOPS!! Connection Error. Make sure you are connected to Internet.\nTechnical Details given below.")

        print(str(e))

    except requests.Timeout as e:

        print("Exception raised in Real time upload. \nFile Name: ", upload_zipfile_name)

        print("OOPS!! Timeout Error")

        print(str(e))

    except requests.RequestException as e:

        print("Exception raised in Real time upload. \nFile Name: ", upload_zipfile_name)

        print("OOPS!! General Error")

        print(str(e))

    except KeyboardInterrupt:

        print("Exception raised in Real time upload. \nFile Name: ", upload_zipfile_name)

        print("Someone closed the program")


def spcbrumain():
    del_realtime_timeout_zipfiles()
    upload_zipfile_name = zipfile_for_realtime_upload()
    if upload_zipfile_name != -2:
        add_boundaries_to_zipfile_data(upload_zipfile_name)
        spcb_realtime_upload(upload_zipfile_name)
        return 1
    else:
        return 0


if __name__ == "__main__":
    spcbrumain()