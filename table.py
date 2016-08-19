#!/usr/bin/python

import csv
import sqlite3 as lite
import sys

diskdb = None
memdb = None

# check is sqlite and nwd.db are availbe
try:
    diskdb = lite.connect('nwd.db')
    cur = diskdb.cursor()    
    cur.execute('SELECT SQLITE_VERSION()')
    data = cur.fetchone()
    print "SQLite version: %s" % data                
except lite.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(1)
finally:
    if diskdb:
        diskdb.close()

# Initialize tables on disk
try: 
   diskdb = lite.connect('nwd.db')
   cur = diskdb.cursor()
   cur.executescript("""
#	DROP TABLE IF EXISTS nic;
	CREATE TABLE IF NOT EXISTS nic 
	(Mac TEXT PRIMARY KEY, 
	 Type TEXT, 
	 Manufacturer TEXT, 
	 Device TEXT, 
	 Description TEXT
	);
#	DROP TABLE IF EXISTS device;
	CREATE TABLE IF NOT EXISTS device
	(DeviceID INTEGER PRIMARY KEY,
	 DeviceName TEXT,
	 DeviceDescription TEXT
	);
#	DROP TABLE IF EXISTS types_external;
	CREATE TABLE IF NOT EXISTS types_external
	(ExtTypeName TEXT PRIMARY KEY,
	 ExtTypeExtra TEST
	);
#	DROP TABLE IF EXISTS conf_external;
	CREATE TABLE IF NOT EXISTS conf_external
	(DeviceID INTEGER,
	 ExtTypeName TEXT,
	 Value TEXT,
	 PRIMARY KEY ( DeviceID, ExtTypeName)
	);
   """)
   diskdb.commit()
except lite.Error, e:
   if diskdb:
      diskdb.rollback()
   print "Error %s:" % e.args[0]
finally:
   if diskdb:
      diskdb.close()

# Initialize tables in memory
#memdb = lite.connect(':memory:')
#with memdb:
#   mem = memdb.cursor()
#   mem.execute("DROP TABLE IF EXISTS NicStatus")
#   mem.execute("CREATE TABLE NicStatus(Mac TEXT PRIMARY KEY, Status TEXT)")
      

# insert examples
def populate_db(cur, csv_fp):
    rdr = csv.reader(csv_fp)
    cur.executemany('''
        INSERT INTO nic (Mac, Type, Manufacturer, Device, Description)
        VALUES (?,?,?,?,?)''', rdr)


# add example NICs from csv file
try:
   csvdb = lite.connect('nwd.db')
   cur = csvdb.cursor()
   # init_db(cur)
   populate_db(cur, open('data/nic.csv'))
   csvdb.commit()
except lite.Error, e:
   if csvdb:
	csvdb.rollback()
finally:
   if csvdb:
	csvdb.close()

diskdb = lite.connect('nwd.db')
#memdb = lite.connect(':memory:')

with diskdb:
   diskdb.row_factory = lite.Row
   cur = diskdb.cursor()
   cur.execute("SELECT * FROM nic")
   nics = cur.fetchall()
   for nic in nics:
	print "%s %s" % (nic["mac"], nic["type"])   


