import requests
import yfinance as yf
import requests
import bs4 as bs
import os
from twilio.rest import Client
import time
import sqlite3
import pandas as pd


# webscrapper and yahoo finance consult
class Tofu_reporter:
    
    def __init__(self,urlib01,urlcop,stocksyf):
        self.urlib01=urlib01
        self.urlcop=urlcop
        self.stocksyf=stocksyf
    def IB01_scraper(self):
        data=requests.get(self.urlib01)
        soup=bs.BeautifulSoup(data.text,'html.parser')
        boxes=soup.find_all('span',class_='header-nav-data')
        
        val=[float(v.text.replace('USD','').replace(',','.').strip()) for v in boxes if 'USD' in v.text]
        return {'IB01':val[0]}
        
    def IB01_scraper_v2(self):
        data=requests.get(self.urlib01)
        soup=bs.BeautifulSoup(data.text,'html.parser')
        #divs=soup.find_all('div',id='overviewQuickstatsDiv')
        td=soup.find_all('td',class_='line text')
        #table=divs.find_all('tr')
        
        return {'IB01':float(td[0].text.replace('USD\xa0',''))}
    
    
    def get_usd_to_cop(self):
        data=requests.get(self.urlcop)
        soup=bs.BeautifulSoup(data.text,'html.parser')
        #boxes=soup.find_all('span',class_='price')
        boxes=soup.find_all('div',class_='priceDetail')
        return {'USDTOCOP':float(boxes[0].text.replace('$','').replace('.','').replace(',','.'))}
    def get_stonks_yf(self):
        res_dict={}
        for s in self.stocksyf:
            comp=yf.Ticker(s)
            try:
                res_dict[s]=comp.info['currentPrice']
            except:
                pass
        return res_dict
    def get_custom_stonks(self):
        url1='https://www.larepublica.co/indicadores-economicos/movimiento-accionario/pfbcolom'
        url2='https://www.larepublica.co/indicadores-economicos/movimiento-accionario/geb'
        urls=[url1,url2]
        prefix=['PFBCOLOM','GEB']
        res_dict={}
        for url,name in zip(urls,prefix):
            data=requests.get(url)
            soup=bs.BeautifulSoup(data.text,'html.parser')
            self.boxes=soup.find_all('div',class_='priceDetail')
            res_dict[name]=float(self.boxes[0].text.replace('\n','').replace('$','').replace('.','').strip())
        return res_dict
   
   
# whastapp handler     
class whatsapp_sender:
    def __init__(self,account_sid,auth_token):
        
        self.account_sid=account_sid
        self.auth_token=auth_token
    
    def login(self):
        self.client=Client(self.account_sid,self.auth_token)
    def send_message(self,sender,receiver,message):
        
        try:
            message=self.client.messages.create(
                                        body=message,
                                        from_=f'whatsapp:{sender}',
                                        to=f'whatsapp:{receiver}'   
                                     )
        except Exception as e:
            
            print(e)
            
# database manager

class manage_db:
    def __init__(self,maindb,tablename,txtfile):
        self.maindb_path=maindb
        self.tablename=tablename
        self.txt_filename=txtfile
        
    def db_connect(self):
        self.conn=sqlite3.connect(self.maindb_path)
        self.cur=self.conn.cursor()
        
    def info_txt_file(self):
        with open(self.txt_filename,'r') as file:
            content=file.readlines()
        content=[i.replace('\n','') for i in content]
        stock_dict={}
        for s in content:
            name,cant,currency=s.split(',')
            stock_dict[name]={'quant':cant,'curr':currency}
        return stock_dict
    def insert_data(self,api_dict,trm):
        stock_db_dict=self.info_txt_file()
        
        trm_raw=trm['USDTOCOP']
        current_date=time.time()
        for s in stock_db_dict:
            
            cant=stock_db_dict[s]['quant']
            if stock_db_dict[s]['curr']=='USD':
                value=api_dict[s]*trm_raw
            else:
                value=api_dict[s]
            
            
            
            
            query=f"""INSERT INTO {self.tablename} (stock,value,cant,trm,time) 
                      VALUES ('{s}',{value},{cant},{trm_raw},{current_date})"""
            self.cur.execute(query)
            self.conn.commit()
    def get_info(self):
        
        query="""SELECT * FROM base"""
        df=pd.read_sql(query,self.conn)
        return df
    def get_changes(self):
        df=self.get_info()
        #print(df)
        df['fecha']=df['time'].apply(lambda x:time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(x))))
        df['total']=df['value']*df['cant']
        dates=df['fecha'].unique()
        show_df=pd.DataFrame()
        if len(dates)>1:
        	last_date=dates[-2]
        	actual_date=dates[-1]
        	print('last',last_date,'actual',actual_date)
        	#print(df)
        	for stock in df['stock'].unique():
        		actual_val=df[(df['stock']==stock)&(df['fecha']==actual_date)]['total'].values[0]
        		last_val=df[(df['stock']==stock)&(df['fecha']==last_date)]['total'].values[0]
        		show_df.loc[stock,'diff']=round(actual_val-last_val,1)
        		show_df.loc[stock,'var']=round(100*((actual_val-last_val)/last_val),1)
        	return show_df
        
        else:
        	show_df.loc[0,'warning']='waiting for more data'
        	return show_df
        	
            
