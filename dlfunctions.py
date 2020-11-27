import RTC_Driver
import os.path
import serial,time

ser = serial.Serial(port="/dev/ttyS1", baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,timeout=10)
rawDirPath = '/mnt/mmcblk0p1/STM32V1/RawDir'
bkpDirPath = '/mnt/mmcblk0p1/STM32V1/BkpDir'

# Global Variables
parameters = "PM,SO2,NOX,NO2"
units = "mg/Nm3,mg/Nm3,mg/Nm3"
analyzers = "analyzer_8,analyzer_742,analyzer_742"

site_id = "site_3017"
plant_name = "M/s.MGM Minerals Limited(Formerly MGM Steels Ltd.)"
plant_address1 = "Rourkela Rourkela"
plant_address2 = "754025 Odisha"
plant_country = "India"

station_name = "CEMS_1"
iso_latitude = "20.566567"
iso_longtitude = "85.896499"

#filename = site_id+'_'+station_name+'_'+year+month+date+hour+minte+"00"

a = ["NH3", "CO2", "CO", "HCL", "HF", "NO2", "NO", "NOX",
     "SO2", "F", "O3", "HG", "pH", "PM10", "PM2.5", "PM",
     "NOx", "SOx", "O3", "Flow", "TSS", "BOD", "COD", "PH", "DY"]                                                                                   
                                                                                                                                                    
code = ["21", "17", "04", "07", "06", "03", "02", "35",                                                                                             
        "01", "99", "08", "85", "50", "24", "39", "22",                                                                                             
        "35", "10", "08", "G5", "G1", "G3", "G2", "50", "DY"]                                                                                       
                                                                                                                                                    
ind_t = 0                                                                                                                                           
c_code = 0                                                                                                                                          
d_code = 0                                                                                                                                          
c_save = []                                                                                                                                         
# PAR[8][16], UNITS[8][10],ANALYZER[8][18]                                                                                                          
# Intialization of PAR                                                                                                                              
PAR = []                                                                                                                                            
UNITS = []                                                                                                                                          
ANALYZER = []                                                                                                                                       
zip_data =''                                                                                                                                        
                                                                                                                                                    
###################################                                                                                                                 
#ind_t = 3                                                                                                                                          
#year = 2020                                                                                                                                        
#month2 = 11                                                                                                                                        
#date = 26                                                                                                                                          
#hour = 12                                                                                                                                          
#min_t = 15                                                                                                                                         
d0 =124.0                                                                                                                                           
                                                                                                                                                    
class RTC_DATE_TIME:                                                                                                                                
    def __init__(self):                                                                                                                             
        ds3231 = RTC_Driver.SDL_DS3231(0, 0x68)                                                                                                     
        DS3231 = ds3231.read_datetime()                                                                                                             
        ds = str(DS3231)                                                                                                                            
        self.seconds = ds[17:]                                                                                                                      
        self.minutes = ds[14:16]                                                                                                                    
        self.hours = ds[11:13]                                                                                                                      
        self.year = ds[2:4]                                                                                                                         
        self.month = ds[5:7]                                                                                                                        
        self.day = ds[8:10]                                                                                                                         
        self.dir_format = ds[8:10] + ds[5:7] + ds[2:4]                                                                                              
        self.rtc_date = ds[8:10] + "/" + ds[5:7] + "/" + ds[2:4]                                                                                    
        self.rtc_time = ds[11:13] + ":" + ds[14:16] + ":" + ds[17:]                                                                                 
        self.rtc_dateTime = "Dt: " + self.rtc_date + " " + self.rtc_time        # for Oled display                                                  
        self.bkpdt = ds[8:10] + ds[5:7] + ds[2:4] + "_" + ds[11:13] + ds[14:16] + ds[17:]                                                           
        self.datfileName = site_id + "_" + station_name + "_" + ds[8:10] + ds[5:7] + ds[2:4] + ds[11:13] + ds[14:16] + "00"                         
                                                                                                                                                    
                                                                                                                                                    
def strcmp(string1,string2):                                                                                                                        
    if string1 == string2:                                                                                                                          
        return  True                                                                                                                                
    else:                                                                                                                                           
        return False                                                                                                                                
                                                                                                                                                    
def init_ParUnitsAnalyzer():                                                                                                                        
    for i in range(8):  # Row entries of PAR                                                                                                        
        row = []                                                                                                                                    
        for j in range(16):  # Column entries of PAR                                                                                                
            row.append('\0')                                                                                                                        
        PAR.append(row)                                                                                                                             
                                                                                                                                                    
    for i in range(8):  # Row entries of UNITS                                                                                                      
        row = []                                                                                                                                    
        for j in range(10):  # Column entries of UNITS                                                                                              
            row.append('\0')                                                                                                                        
        UNITS.append(row)                                                                                                                           
                                                                                                                                                    
    for i in range(8):  # Row entries of ANALYZER                                                                                                   
        row = []                                                                                                                                    
        for j in range(18):  # Column entries of ANALYZER                                                                                           
            row.append('\0')                                                                                                                        
        ANALYZER.append(row)                                                                                                                        
                                                                                                                                                    
'''                                                                                                                                                 
# To print PAR[8][16], UNITS[8][10], ANALYZER[8][18]                                                                                                
def ParUnitsAnalyzer():                                                                                                                             
    # Prints PAR[8][16]                                                                                                                             
    for i in range(8):                                                                                                                              
        for j in range(16):                                                                                                                         
            print(PAR[i][j], end=" ")                                                                                                               
        print()                                                                                                                                     
                                                                                                                                                    
    # Prints UNITS[8][10]                                                                                                                           
    for i in range(8):                                                                                                                              
        for j in range(10):                                                                                                                         
            print(UNITS[i][j], end=" ")                                                                                                             
        print()                                                                                                                                     
                                                                                                                                                    
    # Prints ANALYZER[8][18]                                                                                                                        
    for i in range(8):                                                                                                                              
        for j in range(18):                                                                                                                         
            print(ANALYZER[i][j], end=" ")                                                                                                          
        print()                                                                                                                                     
'''                                                                                                                                                 
def set_parameters():                                                                                                                               
    init_ParUnitsAnalyzer()                                                                                                                         
    p_c = len(parameters)                                                                                                                           
    index1 = 0                                                                                                                                      
                                                                                                                                                    
    for par_count in range(0, p_c):                                                                                                                 
        if (parameters[par_count] == ','):                                                                                                          
            index1 = index1 + 1                                                                                                                     
                                                                                                                                                    
    global ind_t                                                                                                                                    
    ind_t = index1 + 1                                                                                                                              
    # print(ind_t)                                                                                                                                  
                                                                                                                                                    
    next = 0                                                                                                                                        
    Countq1 = 0                                                                                                                                     
    # Adding paramters to PAR[8][16] matrix                                                                                                         
    for Count in range(0, len(parameters)):                                                                                                         
        if (parameters[Count] == ','):                                                                                                              
            next = next + 1                                                                                                                         
            Countq1 = 0                                                                                                                             
        else:                                                                                                                                       
            PAR[next][Countq1] = parameters[Count]                                                                                                  
            Countq1 = Countq1 + 1                                                                                                                   
                                                                                                                                                    
    next = 0                                                                                                                                        
    Countq2 = 0                                                                                                                                     
                                                                                                                                                    
    for oo in range(0, 8):                                                                                                                          
        for oj in range(10):                                                                                                                        
            UNITS[oo][oj] = '\0'                                                                                                                    
                                                                                                                                                    
    # Adding units to UNITS[8][10] matrix                                                                                                           
    for Count in range(0, len(units)):                                                                                                              
        if (units[Count] == ','):                                                                                                                   
            next = next + 1                                                                                                                         
            Countq2 = 0                                                                                                                             
        else:                                                                                                                                       
            UNITS[next][Countq2] = units[Count]                                                                                                     
            Countq2 = Countq2 + 1                                                                                                                   
                                                                                                                                                    
    next = 0                                                                                                                                        
    Countq3 = 0                                                                                                                                     
                                                                                                                                                    
    # Adding units to ANALYZER[8][18] matrix                                                                                                        
    for Count in range(0, len(analyzers)):                                                                                                          
        if (analyzers[Count] == ','):                                                                                                               
            next = next + 1                                                                                                                         
            Countq3 = 0                                                                                                                             
        else:                                                                                                                                       
            ANALYZER[next][Countq3] = analyzers[Count]                                                                                              
            Countq3 = Countq3 + 1                                                                                                                   
    ##############################################################                                                                                  
    k = []                                                                                                                                          
    for i in range(8):                                                                                                                              
        par_str = ''                                                                                                                                
        for j in range(16):                                                                                                                         
            par_str = par_str + PAR[i][j].rstrip('\x00')                                                                                            
                                                                                                                                                    
        k.append(par_str)                                                                                                                           
                                                                                                                                                    
    for ind_r in range(ind_t):                                                                                                                      
        for zz in range(25):                                                                                                                        
            # c_code = strcmp(PAR[ind_r],a[zz])                                                                                                     
            c_code = strcmp(k[ind_r], a[zz])                                                                                                        
            if c_code == True:                                                                                                                      
                d_code = zz                                                                                                                         
                c_save.append(d_code)                                                                                                               
                                                                                                                                                    
    #print(list(c_save))                                                                                                                            
    ####################################################################################################################                            
    next = 0                                                                                                                                        
    Countq2 = 0                                                                                                                                     
                                                                                                                                                    
    for oo in range(0, 8):                                                                                                                          
        for oj in range(10):                                                                                                                        
            UNITS[oo][oj] = '\0'                                                                                                                    
                                                                                                                                                    
    # Adding units to UNITS[8][10] matrix                                                                                                           
    for Count in range(0, len(units)):                                                                                                              
        if (units[Count] == ','):                                                                                                                   
            next = next + 1                                                                                                                         
            Countq2 = 0                                                                                                                             
        else:                                                                                                                                       
            UNITS[next][Countq2] = units[Count]                                                                                                     
            Countq2 = Countq2 + 1                                                                                                                   
                                                                                                                                                    
    next = 0                                                                                                                                        
    Countq3 = 0                                                                                                                                     
                                                                                                                                                    
    # Adding units to ANALYZER[8][18] matrix                                                                                                        
    for Count in range(0, len(analyzers)):                                                                                                          
        if (analyzers[Count] == ','):                                                                                                               
            next = next + 1                                                                                                                         
            Countq3 = 0                                                                                                                             
        else:                                                                                                                                       
            ANALYZER[next][Countq3] = analyzers[Count]                                                                                              
            Countq3 = Countq3 + 1                                                                                                                   
    ####################################################################################################################                            
                                                                                                                                                    
    next = 0                                                                                                                                        
    Countq2 = 0                                                                                                                                     
                                                                                                                                                    
    for oo in range(0, 8):                                                                                                                          
        for oj in range(10):                                                                                                                        
            UNITS[oo][oj] = '\0'                                                                                                                    
                                                                                                                                                    
    # Adding units to UNITS[8][10] matrix                                                                                                           
    for Count in range(0, len(units)):                                                                                                              
        if (units[Count] == ','):                                                                                                                   
            next = next + 1                                                                                                                         
            Countq2 = 0                                                                                                                             
        else:                                                                                                                                       
            UNITS[next][Countq2] = units[Count]                                                                                                     
            Countq2 = Countq2 + 1                                                                                                                   
                                                                                                                                                    
    next = 0                                                                                                                                        
    Countq3 = 0                                                                                                                                     
                                                                                                                                                    
    # Adding units to ANALYZER[8][18] matrix                                                                                                        
    for Count in range(0, len(analyzers)):                                                                                                          
        if (analyzers[Count] == ','):                                                                                                               
            next = next + 1                                                                                                                         
            Countq3 = 0                                                                                                                             
        else:                                                                                                                                       
            ANALYZER[next][Countq3] = analyzers[Count]                                                                                              
            Countq3 = Countq3 + 1                                                                                                                   
                                                                                                                                                    
                                                                                                                                                    
def collect_data():                                                                                                                                 
                                                                                                                                                    
    buf1 = ''                                                                                                                                       
    buf2 = ''                                                                                                                                       
    buf3 = ''                                                                                                                                       
    buf4 = ''                                                                                                                                       
    buf5 = ''                                                                                                                                       
    buf6 = ''                                                                                                                                       
    buf7 = ''                                                                                                                                       
    buf8 = ''                                                                                                                                       
    global ind_t                                                                                                                                    
    count_temp = 0                                                                                                                                  
    temp_store = []                                                                                                                                 
    sum_value = []                                                                                                                                  
    minMa = [4, 4, 4,4]                                                                                                                             
    channels = [0, 1, 2, 3]                                                                                                                         
    maxAbs = [1000, 2000, 2000, 1000]                                                                                                               
    multiplyFactors = [1, 1, 1, 1]                                                                                                                  
                                                                                                                                                    
    #response = "+04.023+07.906+05.432+25.000+00.000+00.000+00.000+00.000"                                                                          
    if ser.is_open == False:                                                                                                                        
        ser.open()                                                                                                                                  
        print('Serial Port Open')                                                                                                                   
    ser.flush()                                                                                                                                     
    ser.flushInput()                                                                                                                                
    ser.flushOutput()                                                                                                                               
    print('Flush serial port before use')                                                                                                           
    ser.write('#01\r')                                                                                                                              
    response = ser.read()  # read serial port                                                                                                       
    time.sleep(0.03)                                                                                                                                
    data_left = ser.inWaiting()  # check for remaining byte                                                                                         
    response += ser.read(data_left)                                                                                                                 
    ser.close()                                                                                                                                     
                                                                                                                                                    
    aRxBuffer = response                                                                                                                            
                                                                                                                                                    
    for i in range(0, 6):                                                                                                                           
        buf1 = buf1 + aRxBuffer[i + 1]                                                                                                              
                                                                                                                                                    
    for i in range(7, 13):                                                                                                                          
        buf2 = buf2 + aRxBuffer[i + 1]                                                                                                              
                                                                                                                                                    
    for i in range(14, 20):                                                                                                                         
        buf3 = buf3 + aRxBuffer[i + 1]                                                                                                              
                                                                                                                                                    
    for i in range(21, 27):                                                                                                                         
        buf4 = buf4 + aRxBuffer[i + 1]                                                                                                              
                                                                                                                                                    
    for i in range(28, 34):                                                                                                                         
        buf5 = buf5 + aRxBuffer[i + 1]                                                                                                              
                                                                                                                                                    
    for i in range(35, 41):                                                                                                                         
        buf6 = buf6 + aRxBuffer[i + 1]                                                                                                              
                                                                                                                                                    
    for i in range(42, 48):                                                                                                                         
        buf7 = buf7 + aRxBuffer[i + 1]                                                                                                              
                                                                                                                                                    
    for i in range(49, 55):                                                                                                                         
        buf8 = buf8 + aRxBuffer[i + 1]                                                                                                              
                                                                                                                                                    
    # convert string to float                                                                                                                       
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
                                                                                                                                                    
    sum_value = temp_store                                                                                                                          
                                                                                                                                                    
    ######################################################################                                                                          
    for k in range(0, ind_t):                                                                                                                       
        if temp_store[k] < 4 or temp_store[k] > 20:                                                                                                 
            if count_temp > 4:                                                                                                                      
                temp_store[k] = 0                                                                                                                   
            else:                                                                                                                                   
                count_temp = count_temp + 1                                                                                                         
                aRxBuffer = ''                                                                                                                      
                                                                                                                                                    
    # prints values in aRxBuffer as list                                                                                                            
    #print('*' * 50)                                                                                                                                
    #print(list(temp_store))                                                                                                                        
    #print(list(sum_value))                                                                                                                         
                                                                                                                                                    
    ##########################################################################                                                                      
    for k in range(0, 8):                                                                                                                           
        if temp_store[k] < 4:                                                                                                                       
            temp_store[k] = 0                                                                                                                       
            sum_value[k] = 0                                                                                                                        
        elif temp_store[k] > 20:                                                                                                                    
            temp_store[k] = 0                                                                                                                       
            sum_value[k] = 0                                                                                                                        
        else:                                                                                                                                       
            pass                                                                                                                                    
    # Elimates the values<4 and values>20 in aRxBuffer                                                                                              
    # print('*' * 50)                                                                                                                               
    # print(list(temp_store))                                                                                                                       
    # print(list(sum_value))                                                                                                                        
                                                                                                                                                    
    for sum_c in range(0, ind_t):                                                                                                                   
        sum_value[sum_c] = ((sum_value[sum_c] - minMa[channels[sum_c]]) * maxAbs[channels[sum_c]] * multiplyFactors[                                
            channels[sum_c]])                                                                                                                       
        sum_value[sum_c] = sum_value[sum_c] / 16                                                                                                    
                                                                                                                                                    
    # prints values after calibration                                                                                                               
    #print(list(sum_value))                                                                                                                         
                                                                                                                                                    
    for i in range(0, ind_t):                                                                                                                       
        if sum_value[i] < 0:                                                                                                                        
            sum_value[i] = 0                                                                                                                        
    #prints values after calibration and elimantes the values less than Zero                                                                        
    #print(list(sum_value))                                                                                                                         
                                                                                                                                                    
                                                                                                                                                    
def create_zipdata():                                                                                                                               
    PARW = []                                                                                                                                       
    for i in range(8):                                                                                                                              
        par_str = ''                                                                                                                                
        for j in range(16):                                                                                                                         
            par_str = par_str + PAR[i][j].rstrip('\x00')                                                                                            
        PARW.append(par_str)                                                                                                                        
                                                                                                                                                    
    UNITSW = []                                                                                                                                     
    for i in range(8):                                                                                                                              
        units_str = ''                                                                                                                              
        for j in range(10):                                                                                                                         
            units_str = units_str + UNITS[i][j].rstrip('\x00')                                                                                      
        UNITSW.append(units_str)                                                                                                                    
                                                                                                                                                    
    ANALYZERW = []                                                                                                                                  
    for i in range(8):                                                                                                                              
        anz_str = ''                                                                                                                                
        for j in range(18):                                                                                                                         
            anz_str = anz_str + ANALYZER[i][j].rstrip('\x00')                                                                                       
        ANALYZERW.append(anz_str)                                                                                                                   
                                                                                                                                                    
                                                                                                                                                    
    S_buf = site_id[5:]                                                                                                                             
    ZIP_DATA1 = ''                                                                                                                                  
    ZIP_DATA2 = ''                                                                                                                                  
    global zip_data                                                                                                                                 
    zip_data = ''                                                                                                                                   
    #print(S_buf)                                                                                                                                   
    # get time                                                                                                                                      
    r=RTC_DATE_TIME()                                                                                                                               
    year = r.year                                                                                                                                   
    month2 = r.month                                                                                                                                
    date = r.day                                                                                                                                    
    hour = r.hours                                                                                                                                  
    min_t = r.minutes                                                                                                                               
                                                                                                                                                    
    #print("*************************************************\n")                                                                                   
    #print(year, month2, date, hour, min_t)                                                                                                         
                                                                                                                                                    
    zip_data1 = plant_name + '\n' + plant_address1 +'\n' + plant_address2 +'\n'+ plant_country+'\n'                                                 
    #print(zip_data1)                                                                                                                               
    zip_data2 = "    {}    1\n".format(ind_t)                                                                                                       
    #print(zip_data2)                                                                                                                               
    for yy in range(ind_t):                                                                                                                         
        #zip_data3 = "   1{}-{}-{}-{}3         0     0     \n".format(code[c_save[yy]],PAR[yy],UNITS[yy],ANALYZER[yy])                              
        zip_data3 = "   1{} {} {} {}   3         0     0     \n".format(code[c_save[yy]], PARW[yy], UNITSW[yy], ANALYZERW[yy])                      
        zip_data4 = "{} {} {} {}\n".format(S_buf, station_name,iso_latitude,iso_longtitude)                                                         
        ZIP_DATA1 = ZIP_DATA1 + zip_data3 + zip_data4                                                                                               
                                                                                                                                                    
    for yy in range(ind_t):                                                                                                                         
        #d0 is to be added                                                                                                                          
        #zip_data5 = "%3s%5s    1%02d%02d%02d%02d%02d 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1   1   0    1\nU%5s\n".format('22',S_buf,year-2000,month2,date,ho
ur,min_t,d0)                                                                                                                                        
        zip_data5 = "{}   {}    1{}{}{}{}{} 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1   1   0    1\nU{}\n".format(code[c_save[yy]],S_buf,year,month2,date,hour,m
in_t,d0)                                                                                                                                            
        ZIP_DATA2 = ZIP_DATA2 + zip_data5                                                                                                           
    zip_data = zip_data1 + zip_data2 + ZIP_DATA1 + ZIP_DATA2                                                                                        
    print(zip_data)                                                                                                                                 
                                                                                                                                                    
def create_directory(pth,dir1):                                                                                                                     
    dst_dir_path = os.path.join(pth, dir1)                                                                                                          
    os.mkdir(dst_dir_path)                                                                                                                          
                                                                                                                                                    
def write_datainFile(pth,filename):                                                                                                                 
    completeName = os.path.join(pth, filename + ".txt")                                                                                             
    f = open(completeName, "a")                                                                                                                     
    f.write(zip_data)                                                                                                                               
    f.close()                                                                                                                                       
                                                                                                                                                    
                                                                                                                                                    
def create_rawfile():                                                                                                                               
    print(zip_data)                                                                                                                                 
    #create raw file      
