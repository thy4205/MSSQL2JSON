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
server = '' #your servers IP or DNS Hostname
database = ''    #Your desired Database you want to create JSON from
username = '' #Username for migration, make sure the user has read access
password = '' #Password, self explanatory

#table name 
tablenames = ['table1','table2'] 


#if your table have an update date, table that in this list will be ignore the update date. (Select all)
#please refer to line 43 for the statement 
#designed to be used with JSON2MYSQLpy
constantTable = []

#tables that needs to be truncated before the import, use with caution
#designed to be used with JSON2MYSQLpy
tableToClear = []

#Line of data to be included in each JSON file.
rowChunks = 25000

#Make sure you have installed and activate the required OBDC driver and change the next line
#To connect to SQL Server 2005, you need to use SQL Server Native Clinet 10.0 ODBC driver.
cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 10.0};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()


for tablename in tablenames:
    print (tablename)
    needUpd = tablename in constantTable
    needUpdStr ="" if tablename in constantTable else  " WHERE UpdDate>='2023-01-01'"
    cursor.execute("SELECT * from " + tablename + needUpdStr) 
    rows = cursor.fetchall()
    a_dict = dict()
    a_dict["tablename"] = tablename
    a_dict["columns"] =[column[0] for column in cursor.description]
    a_dict["nullable"] =[column[6] for column in cursor.description]
    a_dict["clearTable"] = tablename in tableToClear
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