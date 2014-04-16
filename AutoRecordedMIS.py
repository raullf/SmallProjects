'''
    title:auto submit seecmis on/off info.
          one Timer 9:00 am. trigger,another Timer 6:00 pm. trigger.
    author:lf(prez)
    time:2014/04/14
    version:v0.1
'''
import MySQLdb
import random
import time

d = {"host":"10.10.80.181",	\
	"db":"SEECMIS",	\
	"user":"root",	\
	"passwd":"seecdnz"
	}
	
def buildConStr(d):
	return ",".join(["%s=%s" %(k,v) in d.items()]);
	
def getConnection(s):
	return MySQLdb.connect(s)

def getUserMaxRecordDate(d):
	'''
		date format:
	'''
	sql = "SELECT USER_ID,DUTY_ON,DUTY_OFF,ATTDATE FROM TB_ATTENDANCE WHERE USER_ID = 36 AND ATTDATE = (SELECT MAX(ATTDATE) FROM TB_ATTENDANCE WHERE USER_ID = 36)"
	cursor = self.getConnection(self.buildConStr(d)).cursor()
	cursor.execute(sql)
	row = cursor.fetchone()
	return time.strptime(row[3],'%Y%m%d')


	
if __name__ == "__main__":
	

#get a connection from server.
con= MySQLdb.connect(host='10.10.80.181',user='root',passwd='seecdnz',db='SEECMIS')

cursor =con.cursor()

sql = "SELECT USER_ID,DUTY_ON,DUTY_OFF,ATTDATE FROM TB_ATTENDANCE WHERE USER_ID = 36 AND ATTDATE = (SELECT MAX(ATTDATE) FROM TB_ATTENDANCE WHERE USER_ID = 36)"
cursor.execute(sql)
row=cursor.fetchone()
print time.strptime(row[3],'%Y%m%d')

print (time.localtime() > time.strptime(row[3]+'235959','%Y%m%d%H%M%S'))
if ((time.localtime() > time.strptime(row[3]+'235959','%Y%m%d%H%M%S')) and (time.localtime().tm_yday != 25) and (time.localtime().tm_mon == 1) and (time.localtime().tm_yday != 31)):
    attdate = time.strftime('%Y%m%d',time.localtime(time.time()))
    print attdate
    startHr  = '09'
    startMin = random.randrange(0,35)
    startMill= random.randrange(0,60)

    startTime = startHr + (str(startMin)).rjust(2,'0') + (str(startMill)).rjust(2,'0')
    print startTime
    endHr  = 17
    endMin = random.randrange(startMin+1,60)
    endMill= random.randrange(0,60)

    endTime = str(endHr) + (str(endMin)).rjust(2,'0') + (str(endMill)).rjust(2,'0')
    print endTime
    print "insert"
    sql1 ="insert into TB_ATTENDANCE (USER_ID,DUTY_ON,DUTY_OFF,ATTDATE,ON_IP,OFF_IP) values (36,'%s','%s','%s','172.16.6.81','172.16.6.81')" % (startTime.rjust(2,'0'),endTime,attdate)
    print sql1
    cursor.execute(sql1)
    row=cursor.fetchone()
    print row
else:
    print "have data" 
cursor.close()
con.close()

