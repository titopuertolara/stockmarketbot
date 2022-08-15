from tabulate import tabulate
from utils import Tofu_reporter,whatsapp_sender,manage_db

account_sid = ''
auth_token = ''
sender=''
receiver=''
whatsapp=whatsapp_sender(account_sid,auth_token)


url1='https://www.morningstar.co.uk/uk/etf/snapshot/snapshot.aspx?id=0P0001GY9H'
url2='https://www.larepublica.co/indicadores-economicos/mercado-cambiario/dolar'
leeloo=Tofu_reporter(url1,url2,['PFE'])

db_path='history_stocks.db'
db_table='base'
txt_file='quant.txt'
db_obj=manage_db(db_path,db_table,txt_file)
db_obj.db_connect()

if __name__=="__main__":
    whatsapp.login()
    api_stock_dict={}
    api_stock_dict.update(leeloo.get_custom_stonks())
    api_stock_dict.update(leeloo.get_stonks_yf())
    api_stock_dict.update(leeloo.IB01_scraper_v2())
    
    
    trm=leeloo.get_usd_to_cop()
    
    db_obj.insert_data(api_stock_dict,trm)
    
    diff_df=db_obj.get_changes()
    whatsapp.send_message(sender,receiver,tabulate(diff_df, tablefmt="pipe", headers="keys"))