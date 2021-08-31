import pyodbc
import json
import datetime
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
class DateEncoder(json.JSONEncoder):  
    def default(self, obj):  
        if isinstance(obj, datetime.datetime):  
            return obj.strftime('%Y-%m-%d %H:%M:%S')  
        elif isinstance(obj, date):  
            return obj.strftime("%Y-%m-%d")  
        else:  
            return json.JSONEncoder.default(self, obj) 
server = 'kfibsql' #your servers IP or DNS Hostname
database = 'kf3'    #Your desired Database you want to create JSON from
username = 'kf3migrate' #Username for migration, make sure the user has read access
password = 'kf3migrate' #Password, self explanatory
tablename = 'kfvendor' #Table Name,table to create JSON from
querylimit = '' #If you want to add conditions to the qurery

#Make sure you have installed and activate the required OBDC driver and change the next line
cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 10.0};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
#Sample select query
cursor.execute("SELECT  * from " + tablename +' '+querylimit) 
rows = cursor.fetchall()
a_dict = dict()
a_dict["tablename"] = tablename
a_dict["columns"] =[column[0] for column in cursor.description]
cname = []
for row in cursor.columns(table=tablename):
     cname.append([x for x in row][5])
a_dict["datatype"] = cname
data = []
for row in rows:
    data.append([x for x in row]) # or simply data.append(list(row))
a_dict['rows']=data
#with open(tablename+'.json', 'w',encoding='utf8') as f:
with open('import.json', 'w',encoding='utf8') as f:
    json.dump(a_dict, f,cls=DateEncoder,ensure_ascii=False)