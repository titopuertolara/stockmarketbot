import sqlite3
import os 
from sqlalchemy import create_engine

conn=sqlite3.connect('history_stocks.db')
cur=conn.cursor()

query="""CREATE TABLE IF NOT EXISTS base (stock TEXT,value DOUBLE,cant INT,trm  DOUBLE,time DATETIME) """
cur.execute(query)
conn.commit()


con_str=''
query="""CREATE TABLE IF NOT EXISTS base (stock TEXT,value NUMERIC,cant NUMERIC,trm  NUMERIC,time NUMERIC) """
engine=create_engine(con_str)
conn=engine.raw_connection()
cur=conn.cursor()
cur.execute(query)
conn.commit()
