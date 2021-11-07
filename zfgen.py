import os.path
import datetime, time
import pytz
import zipfile
import serial
import serial.tools.list_ports
from aesencrypt import *
from cfasf import *

# Global Variables
zip_data = ''
datfln = ''
zipfln = ''

pollutants = ["NH3", "CO2", "CO", "HCL", "HF", "NO2", "NO", "NOX",
              "SO2", "F", "O3", "HG", "pH", "PM10", "PM2.5", "PM",
              "NOx", "SOx", "O3", "Flow", "TSS", "BOD", "COD", "PH", "DY"]

iso_codes = ["21", "17", "04", "07", "06", "03", "02", "35",
             "01", "99", "08", "85", "50", "24", "39", "22",
             "35", "10", "08", "G5", "G1", "G3", "G2", "50", "DY"]

sum_value = []

try:
    myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    comport = myports[0][0]
    print(comport)
except:
    print(comport)
    print("Default comport connected.")


class GetTime:
    def __init__(self):
        now_utc = datetime.datetime.utcnow()
        local_tz = pytz.timezone('Asia/Kolkata')  # Local timezone which we want to convert the UTC time
        now_utc = pytz.utc.localize(now_utc)  # Add timezone information to UTC time
        x = now_utc.astimezone(local_tz)  # Convert to local time

        self.timestamp = x.strftime('%Y-%m-%dT%H:%M:00Z')
        self.year = x.strftime('%Y')
        self.month = x.strftime('%m')
        self.date = x.strftime('%d')
        self.hour = x.strftime('%H')
        self.min_t = x.strftime('%M')
        self.seconds = x.strftime('%S')
        self.flnts = x.strftime('%Y%m%d%H%M00')


def create_text_file(filename):
    text_filepath = os.path.join(bkpfld_path, filename)
    is_textfile = os.path.isfile(text_filepath)
    if is_textfile:
        # print("File Exists")
        pass
    else:
        text_filepath = os.path.join(bkpfld_path, filename)
        f = open(text_filepath, "a")
        f.write(plant_name + "\n")
        f.write(plant_address1 + "\n")
        f.write(plant_address2 + "\n")
        f.write(plant_country + "\n\n")
        heading = "{:<12}{:<15}{:<15}{:<25}{:<15}{}\n".format("plantid", "analyzer", "station_id", "parameter", "value",
                                                              "TimeStamp")
        f.write(heading)
        f.close()
        print("New Text File Created")


def add_data_to_bkpfile(filename, data):
    text_filepath = os.path.join(bkpfld_path, filename)
    f = open(text_filepath, "a")
    f.write(data)
    f.close()


def collect_data():
    buf1 = ''
    buf2 = ''
    buf3 = ''
    buf4 = ''
    buf5 = ''
    buf6 = ''
    buf7 = ''
    buf8 = ''

    no_of_params = len(parameters)
    temp_store = []
    global sum_value
    sum_value = []

    try:
        # response = "+04.323+04.906+04.432+25.000+00.000+00.000+00.000+00.000"
        ser1 = serial.Serial(port=comport, baudrate=9600, timeout=2)
        if not ser1.is_open:
            ser1.open()
            # print('serial Port1 Open for sending #01')

        ser1.flush()
        ser1.flushInput()
        ser1.flushOutput()
        ser1.write(b'#01\r')
        time.sleep(0.03)
        response = ser1.readline().decode('ascii')
        ser1.flush()
        ser1.flushInput()
        ser1.flushOutput()
        ser1.close()

        received_buffer = response

        for i in range(0, 6):
            buf1 = buf1 + received_buffer[i + 1]

        for i in range(7, 13):
            buf2 = buf2 + received_buffer[i + 1]

        for i in range(14, 20):
            buf3 = buf3 + received_buffer[i + 1]

        for i in range(21, 27):
            buf4 = buf4 + received_buffer[i + 1]

        for i in range(28, 34):
            buf5 = buf5 + received_buffer[i + 1]

        for i in range(35, 41):
            buf6 = buf6 + received_buffer[i + 1]

        for i in range(42, 48):
            buf7 = buf7 + received_buffer[i + 1]

        for i in range(49, 55):
            buf8 = buf8 + received_buffer[i + 1]
    except:
        time.sleep(9)
        collect_data()

    # convert string to float
    try:
        temp1 = float(buf1)
        temp2 = float(buf2)
        temp3 = float(buf3)
        temp4 = float(buf4)
        temp5 = float(buf5)
        temp6 = float(buf6)
        temp7 = float(buf7)
        temp8 = float(buf8)

        temp_store.append(temp1)
        temp_store.append(temp2)
        temp_store.append(temp3)
        temp_store.append(temp4)
        temp_store.append(temp5)
        temp_store.append(temp6)
        temp_store.append(temp7)
        temp_store.append(temp8)

        # print(temp_store)
        for i in range(0, no_of_params):
            if temp_store[i] < MinMa[channels[i]] or temp_store[i] > MaxMa[channels[i]]:
                temp_store[i] = 0
            else:
                temp_store[i] = temp_store[i]

        sum_value = temp_store

        for sum_c in range(0, no_of_params):
            sum_value[sum_c] = ((sum_value[sum_c] - MinMa[channels[sum_c]]) * maxAbs[channels[sum_c]] * multiplyFactors[
                channels[sum_c]])
            sum_value[sum_c] = sum_value[sum_c] / (MaxMa[channels[sum_c]] - MinMa[channels[sum_c]])

        for i in range(0, no_of_params):
            if sum_value[i] < 0:
                sum_value[i] = 0
        # print(list(sum_value))

    except:
        time.sleep(9)
        collect_data()


def create_rawdata():
    parameter_codes = []
    for i in range(0, len(parameters)):
        index_of_parameter = pollutants.index(parameters[i])
        iso_code = iso_codes[index_of_parameter]
        parameter_codes.append(iso_code)

    no_of_params = len(parameters)

    site_buff = site_id[5:]
    zip_data1 = ''
    zip_data2 = ''
    global zip_data
    zip_data = ''

    g = GetTime()
    yyyy = g.year
    yy = yyyy[2:]
    month = g.month
    date = g.date
    hour = g.hour
    min_t = g.min_t
    fts = g.flnts
    timestamp = g.timestamp

    global datfln
    datfln = site_id + "_" + station_name + "_" + fts + ".dat"
    global zipfln
    zipfln = site_id + "_" + station_name + "_" + fts + ".zip"

    textfln = fsw + date + month + yy + ".txt"
    create_text_file(textfln)

    data1 = plant_name + '\n' + plant_address1 + '\n' + plant_address2 + '\n' + plant_country + '\n'
    data2 = "{:5d}    1\n".format(no_of_params)

    for param in range(no_of_params):
        data3 = "  1{}{:<16} {:<10}{:<18}3         0     0     \n".format(parameter_codes[param], parameters[param],
                                                                              units[param], analyzers[param])
        data4 = " {}{:<24}{:<10}{:<21}\n".format(site_buff, station_name, iso_latitude, iso_longtitude)
        zip_data1 = zip_data1 + data3 + data4

    for param in range(no_of_params):
        d0 = str("{:.2f}".format(sum_value[param], 2))
        data5 = " {:<3}{:<5}   1{}{}{}{}{} 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1   1   0    1\nU {}\n".\
            format(parameter_codes[param],site_buff, yy, month, date, hour, min_t, d0)
        zip_data2 = zip_data2 + data5
    zip_data = data1 + data2 + zip_data1 + zip_data2
    print(zip_data)

    for i in range(0, no_of_params):
        d0 = str("{:.2f}".format(sum_value[i], 2))
        bkp_data = "{:<12}{:<15}{:<15}{:<25}{:<15}{}\n".format(site_id, analyzers[i], station_name, parameters[i], d0,
                                                             timestamp)
        add_data_to_bkpfile(textfln, bkp_data)
    # add_data_to_bkpfile(textfln, "\n")


# Create raw file with zip_data.
# This function is mainly written to check file format.
# This function is not needed to execute.
def create_rawfile():
    f = open('rawfile.txt', 'w')
    f.write(zip_data)
    f.close()


# Creates dat file with zip_data.
def create_datfile():
    enc_data = aes256cbc_encrypt(zip_data)
    f = open(datfln, 'wb')
    f.write(enc_data)
    f.close()


# Zips dat file.
def create_zipfile():
    with zipfile.ZipFile(zipfln, 'a', compression=zipfile.ZIP_DEFLATED) as my_zip:
        my_zip.write(datfln)
        my_zip.close()
    try:
        os.unlink(datfln)
    except:
        print("Error while deleting dat file: ", datfln)


# Copies the zip file in spcbdir & spcb_realtime dir.
def save_zipfile():
    shutil.copy(zipfln, spcbdir)
    shutil.copy(zipfln, spcb_realtime_path)
    os.unlink(zipfln)


# Main function of this file
# Combine all functions in this file for simplicity
def zfgen_main():
    g = GetTime()
    secs = int(g.seconds)
    if secs % 10 == 0:
        collect_data()
        if secs == 0:
            create_rawdata()
            create_datfile()
            create_zipfile()
            save_zipfile()
    time.sleep(1)


if __name__ == "__main__":
    while True:
        zfgen_main()
