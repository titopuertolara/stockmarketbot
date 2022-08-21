import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class email_handler:
	def __init__(self,smtp_server,port):
		try:
			self.smtp=smtplib.SMTP(smtp_server,port)
			#self.smtp.quit()
		except Exception as e:
			print(f"Something wrong with smtp {e}")
	def login(self,email_sender,password):
		
		try:
			self.sender=email_sender
			
			self.smtp.ehlo()
			
			self.smtp.starttls()
			
			self.smtp.login(email_sender,password)
		except Exception as e:
			print(f"something wrong with login {e}")
	def send_message(self,email_destiny,subject,content):
		try:
			msg=MIMEMultipart('alternative')
			#subject=subject.encode('utf-8')
			#content=content.encode('utf-8')
			print(subject)
			msg['Subject']=str(subject)
			msg['From']="Sistema de gestión de saccs"
			msg['To']=email_destiny
			#message=f"Subject: {subject}\n\n{content}"
			message=MIMEText(content,'html')
			#message=MIMEMultipart('alternative')
			msg.attach(message)
			#print(message)
			self.smtp.sendmail(self.sender,email_destiny,msg.as_string())
			#print('Email sent :)')
			#self.smtp.quit()
		except Exception as e:
			print('Something wrong with send' ,e)
		
		
		
		
