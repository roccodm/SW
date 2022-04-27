import psycopg2
import json
from collections import OrderedDict
from datetime import datetime,time


def generalInfo (data,recordid):
    record=OrderedDict()
    record["id"]=recordid
    record["Action"]=data["GeneralInfo"].get("ACTION")
    record["Gear"]=data["GeneralInfo"].get("GEAR")
    record["DataCollection"]=data["GeneralInfo"].get("DATA_COLLECTION")
    record["Partner"]=data["GeneralInfo"].get("PARTNER")
    record["N"]=data["GeneralInfo"].get("TRIAL_NUMBER")
    record["Area"]=data["GeneralInfo"].get("AREA_harbour")
    record["VesselName"]=data["GeneralInfo"].get("VESSEL_NAME")
    record["VesselNue"]=data["GeneralInfo"].get("VESSEL_NUE")
    return record

def interactionData (record, data):
    for key in data:
        record[key]=data.get(key)

def checkDate(day):
    if type(day)==str:
        return str(day)
    elif day != None:
        dt=datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(day) -2)
        return dt.strftime("%d/%m/%Y")
    else: return ""
      
def checkHour(hour):
    if type(hour)==str:
        return str(hour)
    elif hour != None:
        seconds = round(hour*86400)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return "%02d:%02d" % (hours, minutes)
    else: return ""

def checkHourFloat(hour):
    if type(hour)==str:
        return str(hour)
    elif hour != None:
        seconds = round(hour*86400)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return 0.0+hours+minutes/60
    else: return 0





connection = psycopg2.connect(user = "rocco",password = "XXXXXXX",host = "localhost",port = "5432",database = "delfi")
connection.set_client_encoding('utf8')

record=OrderedDict()
cursor = connection.cursor()


records=[]

# da qui ok

sql = "select data, id from reports where action='C1' and gear='SETNET' and data_collection='OBS'"
cursor.execute(sql)

while True:
    row = cursor.fetchone()
    if row == None:
        break
    data=row[0]
    errorIssue=False
    for section in ["OPERATIONAL DATA - PINGERED NET","OPERATIONAL DATA - CONTROL NET"]:
        if data["OperationalData"][section].get("LATITUDE (gg.ddddd)")!="":
            if section=="OPERATIONAL DATA - PINGERED NET": i=1;
            else: i=0;
            record=generalInfo(data,row[1])
            record["Date"]=checkDate(data["OperationalData"][section].get("SET_DATE_dd/mm/yyyy"))
            record["HaulN"]=i
            record["Lat"]=data["OperationalData"][section].get("LATITUDE (gg.ddddd)")
            record["Lon"]=data["OperationalData"][section].get("LONGITUDE (gg.ddddd)")
            record["StartAt"]=checkHour(data["OperationalData"][section].get("SET_TIME_h:min"))
            record["EndAt"]=checkHour(data["OperationalData"][section].get("HAUL_TIME_h:min"))
            duration=float(data["OperationalData"][section].get("SOAK_TIME_hours",0))
            if duration<1 and duration!=0:
                duration=checkHourFloat(duration)
            record["Duration"]=duration
            record["NetType"]=data["OperationalData"][section].get("NET_TYPE")
            record["NetLenght"]=data["OperationalData"][section].get("NET_LENGTH_m")
            record["Device"]="Pinger"
            record["DeviceN"]=data["OperationalData"][section].get("N_PINGER")
            record["DeviceSpacing"]=data["OperationalData"][section].get("PINGER_SPACING_m")
            if type(data["Catch"])==dict:
                try:
                    r=data["Catch"][str(i)]
                except KeyError:
                    print (row[1], i, type(data["Catch"]), "esco")
                    errorIssue=True
            else:
                try:
                    r=data["Catch"][i]
                except KeyError:
                    print (row[1], i, type(data["Catch"]), "esco")
                    errorIssue=True
            if not errorIssue:
                if r["Type"]=="PINGER CATCH": 
                    record["DeviceUsed"]="YES"
                else: record["DeviceUsed"]="NO"
                interactionData(record,r["InteractionData"])  
                tc=0.0
                sr=""
                for key in r["species"]:
                    val=r["species"][key].get("TOTAL_WEIGHT_kg")
                    if val==None: 
                        tc=0
                    else: 
                        tc+=float(val)
                        sr=sr+str(key)+":"+str(val)+","
                record["TC"]=tc
                record["SpeciesSummary"]=sr
                # parte comune
                records.append(record)
            else:
               print ("Attenzione, problema in record", row[1], "skippato su SETNET OBS: pare che manca una cala")


record1=record





# passiamo al prossimo: SET LOG

sql = "select data, id from reports where action='C1' and gear='SET' and data_collection='LOG'"
cursor.execute(sql)

while True:
    errorIssue=False
    row = cursor.fetchone()
    if row == None:
        break
    data=row[0]
    for section in ["OPERATIONAL DATA - PINGERED NET","OPERATIONAL DATA - CONTROL NET"]:
        if data["OperationalData"][section].get("LATITUDE (gg.ddddd)")!="":
            if section=="OPERATIONAL DATA - PINGERED NET": i=1;
            else: i=0;
            record=generalInfo(data,row[1])
            record["Date"]=checkDate(data["OperationalData"][section].get("SET_DATE_dd/mm/yyyy"))
            record["HaulN"]=i
            record["Lat"]=data["OperationalData"][section].get("LATITUDE (gg.ddddd)")
            record["Lon"]=data["OperationalData"][section].get("LONGITUDE (gg.ddddd)")
            record["StartAt"]=checkHour(data["OperationalData"][section].get("SET_TIME_h:min"))
            record["EndAt"]=checkHour(data["OperationalData"][section].get("HAUL_TIME_h:min"))
            duration=float(data["OperationalData"][section].get("SOAK_TIME_hours",0))
            if duration<1 and duration!=0:
                duration=checkHourFloat(duration)
            record["Duration"]=duration
            record["NetType"]=data["OperationalData"][section].get("NET_TYPE")
            record["NetLenght"]=data["OperationalData"][section].get("NET_LENGTH_m")
            record["Device"]="Pinger"
            record["DeviceN"]=data["OperationalData"][section].get("N_PINGER")
            record["DeviceSpacing"]=data["OperationalData"][section].get("PINGER_SPACING_m")
            if type(data["Catch"])==dict:
                try:
                    r=data["Catch"][str(i)]
                except KeyError:
                    print (row[1], i, type(data["Catch"]), "esco")
                    errorIssue=True
            else:
                try:
                    r=data["Catch"][i]
                except:
                    print (row[1], i, type(data["Catch"]), "esco")
                    errorIssue=True
            if not errorIssue:
                if r["Type"]=="PINGER CATCH": record["DeviceUsed"]="YES"
                else: record["DeviceUsed"]="NO"
                interactionData(record,r["InteractionData"])  
                tc=0.0
                sr=""
                for key in r["species"]:
                    val=r["species"][key].get("TOTAL_WEIGHT_kg")
                    if val==None: 
                        tc=0
                    else: 
                        tc+=float(val)
                        sr=sr+str(key)+":"+str(val)+","
                record["TC"]=tc
                record["SpeciesSummary"]=sr
                # parte comune
                records.append(record)



# vediamo dopo... TRAWL LOG
sql = "select data, id from reports where action='C1' and gear='TRAWL' and data_collection='LOG'"
cursor.execute(sql)

while True:
    row = cursor.fetchone()
    if row == None:
        break
    data=row[0]
    for key in data["Catch"]:
        if type(key)==dict: r=key
        else: r=data["Catch"][key]
        if r["Type"]=="NO PINGER CATCH T": 
            used="NO"
            section="OPERATIONAL DATA - HAULS WITHOUT PINGER"
        else: 
            section="OPERATIONAL DATA - HAULS WITH PINGER"
            used="YES"
        record=generalInfo(data,row[1])
        record["Date"]=checkDate(data["OperationalData"][section].get("DATE_gg/mm/yyyy"))
        record["HaulN"]=data["OperationalData"][section].get("N_HAULS")
        record["Lat"]=None
        record["Lon"]=None
        record["StartAt"]=None
        record["EndAt"]=None
        record["Duration"]=checkHourFloat(data["OperationalData"][section].get("FISHING_TIME_hours"))
        record["NetType"]="TRAWL"
        record["NetLenght"]=None
        record["Device"]="Pinger"
        if used=="YES": record["DeviceN"]=1
        else: record["DeviceN"]=0
        record["DeviceSpacing"]=None
        record["DeviceUsed"]=used
        interactionData(record,r["InteractionData"])  
        tc=0.0
        sr=""
        for key in r["species"]:
            val=r["species"][key].get("TOTAL_WEIGHT_kg")
            if val==None: 
                tc=0
            else: 
                tc+=float(val)
                sr=sr+str(key)+":"+str(val)+","
        record["TC"]=tc
        record["SpeciesSummary"]=sr
        # parte comune
        records.append(record)


row=""
for key in record1:
    text="%s;" % key
    row=row+text
print (row)
for record in records:
   row=""
   for key in record:
       value=record.get(key,"")
       if value==None:
          value=""
       text="%s;" % value
       row=row+text
   print (row)
exit()
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################
#######################################################################################################################################################################################################



# PURSEIN obs
sql = "select data, id from reports where action='C1' and gear='PURSE' and data_collection='OBS'"
cursor.execute(sql)

while True:
    row = cursor.fetchone()
    if row == None:
        break
    data=row[0]
    for key in data["Catch"]:
        if type(key)==dict: r=key
        else: r=data["Catch"][key]

        record=generalInfo(data,row[1])
        record["Date"]=checkDate(data["OperationalData"]["OPERATIONAL DATA"].get("DATE_gg/mm/yyyy"))
        record["HaulN"]=int(data["OperationalData"]["OPERATIONAL DATA"].get("N_TOTAL_HAULS_PINGER"))+int(data["OperationalData"]["OPERATIONAL DATA"].get("N_TOTAL_HAULS_NO_PINGER"))
        record["Lat"]=r["OperationalData"].get("LATITUDE_gg.ddddd")
        record["Lon"]=r["OperationalData"].get("LONGITUDE_gg.ddddd")
        record["StartAt"]=checkHour(r["OperationalData"].get("START_h:min"))
        record["Duration"]=None
        record["NetType"]="PURSE"
        record["NetLenght"]=None
        record["Device"]="Pinger"
        record["DeviceUsed"]=r["OperationalData"]["PINGER"]
        interactionData(record,r["InteractionData"])  
        tc=0.0
        sr=""
        for key in r["species"]:
            val=r["species"][key].get("TOTAL_WEIGHT_kg")
            if val==None: 
                tc=0
            else: 
                tc+=float(val)
                sr=sr+str(key)+":"+str(val)+","
        record["TC"]=tc
        record["SpeciesSummary"]=sr
        # parte comune
        records.append(record)


# TRAWL OBS
sql = "select data, id from reports where action='C1' and gear='TRAWL' and data_collection='OBS'"
cursor.execute(sql)

while True:
    row = cursor.fetchone()
    if row == None:
        break
    data=row[0]
    for key in data["Catch"]:
        if type(key)==dict: r=key
        else: r=data["Catch"][key]

        record=generalInfo(data,row[1])
        record["Date"]=checkDate(data["OperationalData"]["OPERATIONAL DATA"].get("DATE_gg/mm/yyyy"))
        record["HaulN"]=int(data["OperationalData"]["OPERATIONAL DATA"].get("N_HAULS_PINGER"))+int(data["OperationalData"]["OPERATIONAL DATA"].get("N_HAULS_NO_PINGER"))
        record["Lat"]=r["OperationalData"].get("LATITUDE_START_gg.ddddd")
        record["Lon"]=r["OperationalData"].get("LONGITUDE_START_gg.ddddd")
        record["StartAt"]=checkHour(r["OperationalData"].get("START_h:min"))
        record["Duration"]=None
        record["NetType"]="TRAWL"
        record["NetLenght"]=None
        record["Device"]="Pinger"
        record["DeviceUsed"]=r["OperationalData"]["PINGER"]
        interactionData(record,r["InteractionData"])  
        tc=0.0
        sr=""
        for key in r["species"]:
            val=r["species"][key].get("TOTAL_WEIGHT_kg")
            if val==None: 
                tc=0
            else: 
                tc+=float(val)
                sr=sr+str(key)+":"+str(val)+","
        record["TC"]=tc
        record["SpeciesSummary"]=sr
        # parte comune
        records.append(record)



# C2 ############################################################################################################################################

# setnet obs
sql = "select data, id from reports where action='C2' and gear='SETNET' and data_collection='OBS'"
cursor.execute(sql)

while True:
    row = cursor.fetchone()
    if row == None:
        break
    data=row[0]
    for section in ["OPERATIONAL DATA - NET WITH LEDS","OPERATIONAL DATA - NET WITHOUT LEDS"]:
        if data["OperationalData"][section].get("LATITUDE (gg.ddddd)")!="":
            if section=="OPERATIONAL DATA - NET WITH LEDS": i=1;
            else: i=0;
            record=generalInfo(data,row[1])
            record["Date"]=checkDate(data["OperationalData"][section].get("SET_DATE_dd/mm/yyyy"))
            record["HaulN"]=i
            record["Lat"]=data["OperationalData"][section].get("LATITUDE (gg.ddddd)")
            record["Lon"]=data["OperationalData"][section].get("LONGITUDE (gg.ddddd)")
            record["StartAt"]=checkHour(data["OperationalData"][section].get("SET_TIME_h:min"))
            record["Duration"]=checkHour(data["OperationalData"][section].get("HAUL_TIME_h:min"))
            record["NetType"]=data["OperationalData"][section].get("NET_TYPE")
            record["NetLenght"]=data["OperationalData"][section].get("NET_LENGTH_m")
            record["Device"]="LED"
            if type(data["Catch"])==dict:
                r=data["Catch"][str(i)]
            else:
                try:
                    r=data["Catch"][i]
                except KeyError:
                    print (row[1], i, type(data["Catch"]), "esco")
                    break
            if r["Type"]=="LEDS CATCH": record["DeviceUsed"]="YES"
            else: record["DeviceUsed"]="NO"
            interactionData(record,r["InteractionData"])  
            tc=0.0
            sr=""
            for key in r["species"]:
                val=r["species"][key].get("TOTAL_WEIGHT_kg")
                if val==None: 
                    tc=0
                else: 
                    tc+=float(val)
                    sr=sr+str(key)+":"+str(val)+","
            record["TC"]=tc
            record["SpeciesSummary"]=sr
            # parte comune
            records.append(record)


# passiamo al prossimo: SET LOG

sql = "select data, id from reports where action='C2' and gear='SET' and data_collection='LOG'"
cursor.execute(sql)

while True:
    row = cursor.fetchone()
    if row == None:
        break
    data=row[0]
    for section in ["OPERATIONAL DATA - NET WITH LEDS","OPERATIONAL DATA - NET WITHOUT LEDS"]:
        if data["OperationalData"][section].get("LATITUDE (gg.ddddd)")!="":
            if section=="OPERATIONAL DATA - NET WITH LEDS": i=1;
            else: i=0;
            record=generalInfo(data,row[1])
            record["Date"]=checkDate(data["OperationalData"][section].get("SET_DATE_dd/mm/yyyy"))
            record["HaulN"]=i
            record["Lat"]=data["OperationalData"][section].get("LATITUDE (gg.ddddd)")
            record["Lon"]=data["OperationalData"][section].get("LONGITUDE (gg.ddddd)")
            record["StartAt"]=checkHour(data["OperationalData"][section].get("SET_TIME_h:min"))
            record["Duration"]=checkHour(data["OperationalData"][section].get("HAUL_TIME_h:min"))
            record["NetType"]=data["OperationalData"][section].get("NET_TYPE")
            record["NetLenght"]=data["OperationalData"][section].get("NET_LENGTH_m")
            record["Device"]="LED"
            if type(data["Catch"])==dict:
                r=data["Catch"][str(i)]
            else:
                try:
                    r=data["Catch"][i]
                except KeyError:
                    print (row[1], i, type(data["Catch"]), "esco")
                    break
            if r["Type"]=="LEDS CATCH": record["DeviceUsed"]="YES"
            else: record["DeviceUsed"]="NO"
            interactionData(record,r["InteractionData"])  
            tc=0.0
            sr=""
            for key in r["species"]:
                val=r["species"][key].get("TOTAL_WEIGHT_kg")
                if val==None: 
                    tc=0
                else: 
                    tc+=float(val)
                    sr=sr+str(key)+":"+str(val)+","
            record["TC"]=tc
            record["SpeciesSummary"]=sr
            # parte comune
            records.append(record)

# TRAWL OBS
sql = "select data, id from reports where action='C2' and gear='TRAWL' and data_collection='OBS'"
cursor.execute(sql)

while True:
    row = cursor.fetchone()
    if row == None:
        break
    data=row[0]
    for key in data["Catch"]:
        if type(key)==dict: r=key
        else: r=data["Catch"][key]

        record=generalInfo(data,row[1])
        record["Date"]=checkDate(data["OperationalData"]["OPERATIONAL DATA"].get("DATE_gg/mm/yyyy"))
        record["HaulN"]=int(data["OperationalData"]["OPERATIONAL DATA"].get("N_HAULS_LED"))+int(data["OperationalData"]["OPERATIONAL DATA"].get("N_HAULS_NO_LED"))
        record["Lat"]=r["OperationalData"].get("LATITUDE_START_gg.ddddd")
        record["Lon"]=r["OperationalData"].get("LONGITUDE_START_gg.ddddd")
        record["StartAt"]=checkHour(r["OperationalData"].get("START_h:min"))
        record["Duration"]=None
        record["NetType"]="TRAWL"
        record["NetLenght"]=None
        record["Device"]="LED"
        record["DeviceUsed"]=r["OperationalData"]["LED"]
        interactionData(record,r["InteractionData"])  
        tc=0.0
        sr=""
        for key in r["species"]:
            val=r["species"][key].get("TOTAL_WEIGHT_kg")
            if val==None: 
                tc=0
            else: 
                tc+=float(val)
                sr=sr+str(key)+":"+str(val)+","
        record["TC"]=tc
        record["SpeciesSummary"]=sr
        # parte comune
        records.append(record)





# questo lascialo in fondo

row=""
for key in record:
    text="%s;" % key
    row=row+text
print (row)
for record in records:
   row=""
   for key in record:
       text="%s;" % record.get(key)
       row=row+text
   print (row)

