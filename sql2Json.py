import pyodbc
import json
import datetime
import math
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
server = 'sqlserver' #your servers IP or DNS Hostname
database = 'databaseName'    #Your desired Database you want to create JSON from
username = 'UserName' #Username for migration, make sure the user has read access
password = 'Password' #Password, self explanatory
tablenames = ['tableName'] #Table Name,table to create JSON from
rowChunks = 25000

#Make sure you have installed and activate the required OBDC driver and change the next line
cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 10.0};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
#Sample select query

for tablename in tablenames:
    cursor.execute("SELECT * from " + tablename) 
    rows = cursor.fetchall()
    a_dict = dict()
    a_dict["tablename"] = tablename
    a_dict["columns"] =[column[0] for column in cursor.description]
    a_dict["nullable"] =[column[6] for column in cursor.description]
    rowCountSum = len(rows)
    timeToRun = math.ceil(rowCountSum / rowChunks)
    cname = []
    colSize = []
    i = 0;
    

    for row in cursor.columns(table=tablename):
         cname.append([x for x in row][5])
         colSize.append([x for x in row][7])
       
    a_dict["datatype"] = cname
    a_dict["columnSize"] = colSize

    for i in range(timeToRun):
        j = i
        j = i * rowChunks
        k = j + rowChunks
       
        data = []
        for row in rows[j:k]:
            data.append([x for x in row]) # or simply data.append(list(row))
        a_dict['rows']=data
        #with open(tablename+'.json', 'w',encoding='utf8') as f:
        with open('import_'+tablename+'_'+str(i).zfill(4)+'.json', 'w',encoding='utf8') as f:
            json.dump(a_dict, f,cls=DateEncoder,ensure_ascii=False)