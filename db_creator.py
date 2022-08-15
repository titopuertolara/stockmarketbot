import sqlite3
import os 

conn=sqlite3.connect('history_stocks.db')
cur=conn.cursor()

query="""CREATE TABLE IF NOT EXISTS base (stock TEXT,value DOUBLE,cant INT,trm  DOUBLE,time DATETIME) """
cur.execute(query)
conn.commit()