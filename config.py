# Global Variables
parameters = ["PM", "SO2"]
units = ["mg/m3", "ug/m3"]
analyzers = ["analyzer_215", "analyzer_831"]
MinMa = [4, 4, 4, 4]
MaxMa = [20, 20, 20, 20]
channels = [0, 1, 2, 3]
maxAbs = [1000, 1000, 2000, 1000]
multiplyFactors = [1, 2.62, 1, 1]


site_id = "site_2944"
station_name = "CEMS_1"
plant_name = "M/S Grewal Associates (P) Ltd."
plant_address1 = "Barbil Keonjhar"
plant_address2 = "758035 Odisha"
plant_country = "India"
iso_latitude = "22.117538"
iso_longtitude = "85.397970"
version = "ver1.0"
fsw = site_id+"_"+station_name+"_"

# Grewal AES key
AES256_KEY = "AES KEY"

# Site Sunjray Public Key
site_public_key = "SITE PUBLIC KEY"

# OSPCB Server Public Key
server_public_key = 'SERVER PUBLIC KEY'

# Site private key
site_private_key = "PRIVATE KEY"

# IP Addresses
sunjray_hostAddress = "113.19.81.38:9899"
ospcb_hostAddress = "ospcb-rtdas.com"

# Sunjray Realtime and Delayed urls
sunjray_realtime_url = "http://113.19.81.38:9899/sunjrayServer/realtimeUpload"
sunjray_delayed_url = "http://113.19.81.38:9899/sunjrayServer/delayedUpload"

# OSPCB Realtime and Delayed urls
ospcb_realtime_url = "http://ospcb-rtdas.com/OSPCBRTDASServer/realtimeUpload"
ospcb_delayed_url = "http://ospcb-rtdas.com/OSPCBRTDASServer/delayedUpload"

# Required directories for project functioning
bkpdir = "BKPFLD"
cpcbdir = "CPCB"
spcbdir = "SPCB"

# Required directories in CPCB and SPCB for zipfile storing
rtdir = "Realtime"
dlydir = "Delayed"
