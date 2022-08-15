import sqlite3
import os 
from sqlalchemy import create_engine

conn=sqlite3.connect('history_stocks.db')
cur=conn.cursor()

query="""CREATE TABLE IF NOT EXISTS base (stock TEXT,value DOUBLE,cant INT,trm  DOUBLE,time DATETIME) """
cur.execute(query)
conn.commit()


con_str='postgres://hneontjeqglbyc:36b0140411d2b3c5eee5071eb40948cbe2375118b05237d2a1b6e8079b7bd3b4@ec2-34-234-240-121.compute-1.amazonaws.com:5432/d620ik01ncabkt'
query="""CREATE TABLE IF NOT EXISTS base (stock TEXT,value NUMERIC,cant NUMERIC,trm  NUMERIC,time NUMERIC) """
engine=create_engine(con_str)
conn=engine.raw_connection()
cur=conn.cursor()
cur.execute(query)
conn.commit()
