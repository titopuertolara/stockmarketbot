from utils import Tofu_reporter,whatsapp_sender,manage_db

account_sid = 'AC1739cc676ed44649ad40e2fee9ebc410'
auth_token = '3c5db0934d6c437e18da994681d99959'
sender='+14155238886'
receiver='+573202317773'
whatsapp=whatsapp_sender(account_sid,auth_token)
whatsapp.login()
whatsapp.send_message(sender,receiver,'hola')