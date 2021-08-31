import pymssql
import json
conn = pymssql.connect(
    server='192.168.0.15', 
    user='mysql', 
    password='mysql', 
    database='kf3',
    charset='UTF-8'
    #charset='BIG5HKSCS'
)
cursor = conn.cursor(as_dict=True)  
#cursor.execute('SELECT * from kfpolicy where PID>350001 AND PID<400000')


cursor.execute('SELECT namechi,remarks from kfaccount where AID>309000 AND AID<500000')

# while row:  
    # print (str(row[0])+str(row[1])+str(row[2]))
    # row = cursor.fetchone()
colNames = ""
colNameList = []
for i in range(len(cursor.description)):
        desc = cursor.description[i]
        colNameList.append(desc[0])

        # colNames = ','.join(colNameList)
#print (colNameList)



    
  
from datetime import date, datetime
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
def robust_decode(bs):
    '''Takes a byte string as param and convert it into a unicode one.
First tries UTF8, and fallback to Latin1 if it fails'''
    cr = None
    try:
        cr = bs.decode('ascii')
    except UnicodeDecodeError:
        try: 
            cr = bs.decode('BIG5HKSCS')
        except UnicodeDecodeError:
            cr = bs.decode('UTF-8')
    return cr
    
    
rows = cursor.fetchall() 

for x in rows:
    for y in x:
       if isinstance(x[y],str):
            print (str(x[y]).encode('UTF-8'))
            #print (str(robust_decode(x[y].encode('UTF-8'))))
       else:
            print (x[y])


# with open('data.json', 'w') as outfile:
     # (json.dump(rows,outfile,cls=ComplexEncoder))
    
cursor.close()
conn.close()