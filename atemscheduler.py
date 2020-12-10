#!/usr/bin/env python

import sys
import time
import logging
from datetime import datetime
from datetime import timedelta 
import PyATEMMax #https://github.com/clvLabs/PyATEMMax
import mysql.connector #pip install mysql-connector-python
from mysql.connector import Error
try:
    import thread
except ImportError:
    import _thread as thread


#MariaDB settings. Port = 3306 or 3307
mysqlconfig = {
  'user': 'user',
  'password': 'pass',
  'host': '192.168.0.1',
  'port': '3307',
  'database': 'Atemdb',
  'raise_on_warnings': True
}

writelog = 0

args = sys.argv[1:]
if len(args):
	CW = args[0]
	if CW == '-l':
		writelog = 1
		print ("Logfile will be made.")

if writelog:
	logging.basicConfig(filename=time.strftime("%Y%m%d%H%M%S") + '.log', level=logging.INFO)
	logging.info('Started')
    
try:
	connection = mysql.connector.connect(**mysqlconfig)
	if connection.is_connected():
		db_Info = connection.get_server_info()
		print("Connected to MySQL Server version ", db_Info)
		if writelog:
			logging.info(time.strftime("%Y%m%d%H%M%S") + ": Connected to MySQL Server version " + db_Info)
		mycursor = connection.cursor(dictionary=True)
		mycursor.execute("SELECT * FROM host")
		records = mycursor.fetchall()
		for row in records:
			host = row["hostname"]
except Error as e:
	print("Error while connecting to MySQL", e)
	if writelog:
		logging.warning(time.strftime("%Y%m%d%H%M%S") + ": Error while connecting to MySQL" + e)
	
try:
	connectionthread = mysql.connector.connect(**mysqlconfig)
	if connectionthread.is_connected():
		db_Info = connectionthread.get_server_info()
		print("Thread connected to MySQL Server version ", db_Info)
		if writelog:
			logging.info(time.strftime("%Y%m%d%H%M%S") + ": Thread connected to MySQL Server version " + db_Info)
except Error as e:
	print("Error while connecting to MySQL", e)
	if writelog:
		logging.warning(time.strftime("%Y%m%d%H%M%S") + ": Error while connecting thread to MySQL" + e)

switcher = PyATEMMax.ATEMMax()
switcher.connect(host)
while True:
	try:
		while switcher.waitForConnection(infinite=False):
			weekdays = ("ma","di","wo","do","vr","za","zo") #Dutch
			dayrun = False
			otherday = False
			currentdtime = time.strftime("%Y%m%d%H%M%S",time.localtime())
			timenow = time.strftime("%H:%M:%S",time.localtime())
			if not connectionthread.is_connected():
				connectionthread.reconnect(attempts=5, delay=0)
			mycursor = connectionthread.cursor(dictionary=True)
			getqry = "SELECT * FROM schedules WHERE processed = 0"
			mycursor.execute(getqry)
			records = mycursor.fetchall()
			print(time.strftime("%H:%M:%S",time.localtime()), end="\r")
			for row in records:
				logrow = str(row)
				id = row["id"]
				swtime = row["swtime"]
				swdate = row["swdate"]
				time_object = datetime.strptime(str(swtime), '%H:%M:%S').time()
				date_object = datetime.strptime(str(swdate), '%Y-%m-%d').date()
				datetime_str = datetime.combine(date_object , time_object)
				dtime = datetime_str.strftime("%Y%m%d%H%M%S")
				input = row["scene"]
				trans_type = row["transition"]
				repeattime = row["repeattime"]
				if timenow == datetime_str.strftime("%H:%M:%S"):
					if len(repeattime) > 0:
						if weekdays[datetime.today().weekday()] in repeattime:
							dayrun = True
							otherday = False
						elif repeattime.replace(',','').isalpha():
							otherday = True
				if (currentdtime == dtime or dayrun) and not otherday:
					switcher.setPreviewInputVideoSource(0,input)
					if 'Cut' in trans_type:
						switcher.execCutME(0)
					else:
						transitions = {'Mix': 0, 'Dip': 1, 'Wipe': 2, 'DVE': 3}
						result = transitions.get(trans_type, 'default')
						switcher.setTransitionStyle(0,result)
						switcher.execAutoME(0)
					print("Transition " + trans_type + " to input: " + str(input) + " at " + time.strftime("%H:%M:%S",time.localtime()))
					if writelog:
						logging.info(time.strftime("%Y%m%d%H%M%S") + ": Transition " + trans_type + "  to input: " + str(input) + " at " + time.strftime("%H:%M:%S",time.localtime()))
					if not connectionthread.is_connected():
						connectionthread.reconnect(attempts=5, delay=0)
						mycursor = connectionthread.cursor()
					if len(repeattime) > 0 and not dayrun:
						if repeattime[0:2] in weekdays: #days in repeattime, not minutes
							dayrun = True
						elif "," in repeattime and repeattime.replace(',','').isdigit(): #minutes,repeatnumber 
							repeattimenew = repeattime.split(',')[0]
							repeattimenumber = repeattime.split(',')[1]
							if repeattimenumber == "0": #continuous
								newdtime = datetime_str + timedelta(minutes=int(repeattimenew))
								new_time_object = datetime.time(newdtime)
								new_date_object = datetime.date(newdtime)
								qry = "UPDATE schedules SET swtime = '" + new_time_object.strftime("%H:%M:%S") + "', swdate ='" + new_date_object.strftime("%Y-%m-%d") + "' WHERE id = " + str(id) + ";"
							elif repeattimenumber == "1": #last run was done
								qry = "UPDATE schedules SET processed = 1 WHERE id = " + str(id) + ";"
							else:
								newdtime = datetime_str + timedelta(minutes=int(repeattimenew))
								repeattime = repeattimenew + "," + str(int(repeattimenumber) - 1)
								new_time_object = datetime.time(newdtime)
								new_date_object = datetime.date(newdtime)
								qry = "UPDATE schedules SET swtime = '" + new_time_object.strftime("%H:%M:%S") + "', swdate = '" + new_date_object.strftime("%Y-%m-%d") + "', repeattime = '" + repeattime + "' WHERE id = " + str(id) + ";"
						else:	# repeat after x minutes. Same as x,0 Continuous
							newdtime = datetime_str + timedelta(minutes=int(repeattime))
							new_time_object = datetime.time(newdtime)
							new_date_object = datetime.date(newdtime)
							qry = "UPDATE schedules SET swtime = '" + new_time_object.strftime("%H:%M:%S") + "', swdate ='" + new_date_object.strftime("%Y-%m-%d") + "' WHERE id = " + str(id) + ";"
					else:
						qry = "UPDATE schedules SET processed = 1 WHERE id = " + str(id) + ";"
					if not dayrun:
						mycursor.execute(qry)
						connectionthread.commit()
					time.sleep(1) #wait for next second.
				dayrun = False
			connectionthread.close() #will clear sql query in buffer
			time.sleep(0.25) #no need 100's loops a second
	except Exception:
		print("connectionthread error")
		connectionthread.close()
		if writelog:
			logging.warning(time.strftime("%Y%m%d%H%M%S") + ": connectionthread error")
		time.sleep(10)







