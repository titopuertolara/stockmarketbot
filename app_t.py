from tabulate import tabulate
from utils import Tofu_reporter,whatsapp_sender,manage_db
from email_handler import email_handler
from datetime import datetime
#account_sid = ''
#auth_token = ''
#sender=''
#receiver=''
#whatsapp=whatsapp_sender(account_sid,auth_token)
smtp_server=''
port=587
mail_obj=email_handler(smtp_server,port)
user=''
password=''


con_str=''
url1='https://www.morningstar.co.uk/uk/etf/snapshot/snapshot.aspx?id=0P0001GY9H'
url2='https://www.larepublica.co/indicadores-economicos/mercado-cambiario/dolar'
leeloo=Tofu_reporter(url1,url2,['PFE','NU'])

db_path='history_stocks.db'
db_table='base'
txt_file='quant.txt'
db_obj=manage_db(db_path,db_table,txt_file,con_str)
#db_obj.db_connect()
db_obj.postgres_connect()

if __name__=="__main__":
    
    #whatsapp.login()
    mail_obj.login(user,password)
    api_stock_dict={}
    api_stock_dict.update(leeloo.get_custom_stonks())
    api_stock_dict.update(leeloo.get_stonks_yf())
    api_stock_dict.update(leeloo.IB01_scraper_v2())
    
    
    
    
    
    
    
    trm=leeloo.get_usd_to_cop()
    
    
    
    db_obj.insert_data(api_stock_dict,trm)
    today=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    hour=str(today).split()[1].split(':')[0]
    print(today)
    print(hour)
    
    if hour=='17' or hour=='10' or hour=='14':
    	msg=db_obj.get_daily_report()
    	print('enviamos mensaje')
    	try:
    		mail_obj.send_message('andrespuertolara@gmail.com','Hola Jefe, así vas en trii',msg)
    	except Exception as e:
    		print(e)
    
    #diff_df=db_obj.get_changes()
    #msg=''
    #for i in diff_df.index:
    	#val=diff_df.loc[i,'diff']
    	#var=diff_df.loc[i,'var']
    	#msg+=f"{i} :{val} {var}\n"
    #print(msg)
    	
    	
    #print(diff_df)
    #whatsapp.send_message(sender,receiver,msg)