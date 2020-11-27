from dlfunctions import *                                                                                                                           
import RTC_Driver                                                                                                                                   
import time                                                                                                                                         
                                                                                                                                                    
class RTC_DATE_TIME:                                                                                                                                
    def __init__(self):                                                                                                                             
        ds3231 = RTC_Driver.SDL_DS3231(0, 0x68)                                                                                                     
        DS3231 = ds3231.read_datetime()                                                                                                             
        ds = str(DS3231)                                                                                                                            
        self.seconds = ds[17:]                                                                                                                      
        self.minutes = ds[14:16]                                                                                                                    
        self.hours = ds[11:13]                                                                                                                      
        self.dir_format = ds[8:10] + ds[5:7] + ds[2:4]                                                                                              
        self.rtc_date = ds[8:10] + "/" + ds[5:7] + "/" + ds[2:4]                                                                                    
        self.rtc_time = ds[11:13] + ":" + ds[14:16] + ":" + ds[17:]                                                                                 
        self.rtc_dateTime = "Dt: " + self.rtc_date + " " + self.rtc_time        # for Oled display                                                  
        self.bkpdt = ds[8:10] + ds[5:7] + ds[2:4] + "_" + ds[11:13] + ds[14:16] + ds[17:]                                                           
        self.datfileName = site_id + "_" + station_name + "_" + ds[8:10] + ds[5:7] + ds[2:4] + ds[11:13] + ds[14:16] + "00"                         
                                                                                                                                                    
if __name__ == "__main__":                                                                                                                          
                                                                                                                                                    
    init_ParUnitsAnalyzer()                                                                                                                         
    #ParUnitsAnalyzer()                                                                                                                             
    set_parameters()                                                                                                                                
    #ParUnitsAnalyzer()                                                                                                                             
    while True:                                                                                                                                     
        r=RTC_DATE_TIME()                                                                                                                           
        secs = int(r.seconds)                                                                                                                       
        mnts = int(r.minutes)                                                                                                                       
                                                                                                                                                    
        tRawDirpath = rawDirPath + '/Date_' + r.dir_format                                                                                          
        isexist_tRawDirPath = os.path.isdir(tRawDirpath)                                                                                            
        while (isexist_tRawDirPath == 0):                                                                                                           
            cdir1 = 'Date_' + r.dir_format                                                                                                          
            create_directory(rawDirPath,cdir1)                                                                                                      
            break                                                                                                                                   
                                                                                                                                                    
        tBkpDirpath = bkpDirPath + '/Date_' + r.dir_format                                                                                          
        isexist_tBkpDirPath = os.path.isdir(tBkpDirpath)                                                                                            
        while (isexist_tBkpDirPath == 0):                                                                                                           
            cdir2 = 'Date_' + r.dir_format                                                                                                          
            create_directory(bkpDirPath, cdir2)                                                                                                     
            break                                                                                                                                   
                                                                                                                                                    
        if secs%10 == 0:                                                                                                                            
            collect_data()                                                                                                                          
            if secs == 0:                                                                                                                           
                create_zipdata()                                                                                                                    
                #create_rawfile()                                                                                                                   
                                                                                                                                                    
                pth1 = rawDirPath + '/Date_' + r.dir_format                                                                                         
                rbkp_fln = r.datfileName                                                                                                            
                write_datainFile(pth1, rbkp_fln)                                                                                                    
                                                                                                                                                    
                # Bkp file of hourly data                                                                                                           
                # Append data to hourly file                                                                                                        
                pth2 = bkpDirPath + '/Date_' + r.dir_format                                                                                         
                hbkp_fln = 'File_hr' + r.hours                                                                                                      
                write_datainFile(pth2, hbkp_fln)                                                                                                    
                                                                                                                                                    
        time.sleep(1)                                                                                                                               
    print("Main End")                                                                                                                               
   
