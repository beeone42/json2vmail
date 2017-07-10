#!/usr/bin/env python

import os, json, sys, urllib, urllib2, time, pymysql

CONFIG_FILE = 'config.json'

"""
Open and load a file at the json format
"""

def open_and_load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as config_file:
            return json.loads(config_file.read())
    else:
        print "File [%s] doesn't exist, aborting." % (CONFIG_FILE)
        sys.exit(1)

                        
"""
Main
"""

if __name__ == "__main__":
    config = open_and_load_config()
    url = config['url']
    print url
    try:
        print "downloading datas..."
        res = json.loads(urllib2.urlopen(config['url']).read())
        print "connecting mysql..."
        con = pymysql.connect(host = config['db_host'],
                              user = config['db_user'],
                              passwd = config['db_pass'],
                              db = config['db_data'])
        cursor = con.cursor()
        
        print "inserting domains..." 
        cursor.execute("TRUNCATE domain")
        for d in res['domains']:
            cursor.execute("INSERT INTO domain (domain, backupmx) VALUES (%s,0)", (d))
        con.commit()
        
        print "inserting aliases..." 
        cursor.execute("TRUNCATE alias")
        for u in res['users']:
            cursor.execute("INSERT INTO alias (address, goto, active) VALUES (%s,%s,1)", (u['alias'], u['email']))
        con.commit()
        
        print "done"
        con.close()
    except Exception as e:
        print e
