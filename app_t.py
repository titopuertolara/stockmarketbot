from tabulate import tabulate
from utils import Tofu_reporter,whatsapp_sender,manage_db

account_sid = ''
auth_token = ''
sender=''
receiver=''
whatsapp=whatsapp_sender(account_sid,auth_token)

con_str=''
url1=''
url2=''
leeloo=Tofu_reporter(url1,url2,['PFE'])

db_path='history_stocks.db'
db_table='base'
txt_file='quant.txt'
db_obj=manage_db(db_path,db_table,txt_file,con_str)
#db_obj.db_connect()
db_obj.postgres_connect()

if __name__=="__main__":
    
    whatsapp.login()
    api_stock_dict={}
    api_stock_dict.update(leeloo.get_custom_stonks())
    api_stock_dict.update(leeloo.get_stonks_yf())
    api_stock_dict.update(leeloo.IB01_scraper_v2())
    
    
    
    
    
    
    
    trm=leeloo.get_usd_to_cop()
    
    db_obj.insert_data(api_stock_dict,trm)
    
    #diff_df=db_obj.get_changes()
    #msg=''
    #for i in diff_df.index:
    	#val=diff_df.loc[i,'diff']
    	#var=diff_df.loc[i,'var']
    	#msg+=f"{i} :{val} {var}\n"
    #print(msg)
    	
    	
    #print(diff_df)
    #whatsapp.send_message(sender,receiver,msg)