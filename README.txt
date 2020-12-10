AtemScheduler can be used as a scheduled switcher for BM Atem.
There are 3 parts
- mySQL database atemdb
- python script atemscheduler.py
- webapplication for add/editing schedule rules.

You need to run atemscheduler.py in python.
The python script use the mysql connector (pip install mysql-connector-python)
and the PyATEMMax lib from clvLabs  https://github.com/clvLabs/PyATEMMax

Edit atemscheduler.py for connection to mySQL
Edit 'host' table in atemdb for connect to the Atem box.
Hostname is the ip address of the Atem box.
Edit database_connection.php for connection to mySQL database.
Edit index.php for the number of input port of the switcher. (I used 8 input ports).

The field repeattime (Herhaal) is used in 2 ways.
- put day(s) in it for switching every that day at that time
	"ma,wo,za" or only 1 day. (Edit atemscheduler.py line 74 for your language).
- put minutes in it to repeat and how many times.
	180,3 (repeat this after 180 minutes and do it 3 times).
	180,0 or 180 (repeat every 180 minutes, forever).


