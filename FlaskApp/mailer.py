import smtplib
from cStringIO import StringIO
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email import Charset
from email.generator import Generator
class mailer(object):
    def __init__(self, user,passwd,smtp,puerto):
        self.user = user
        self.passwd = passwd
        self.smtp = smtp
        self.puerto= puerto
    def enviar(self,destino,asunto,mensaje):
        smtpserver = smtplib.SMTP(self.smtp,self.puerto)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(self.user, self.passwd)
        """header = 'To:' + destino + '\n' + 'From: ' + self.user + '\n' + 'Subject:'+asunto+' \n'
        msg = header + '\n'+mensaje+'\n\n'"""
        Charset.add_charset('utf-8', Charset.QP, Charset.QP, 'utf-8')
        msg = MIMEMultipart('alternative')
        msg['To'] = destino
        msg['From'] = self.user
        msg['Subject'] = asunto
        part2 = MIMEText(mensaje.encode('utf-8'), 'html')
        msg.attach(part2)
 

        smtpserver.sendmail(self.user, destino, msg.as_string())
        smtpserver.quit()
        """
        smtpserver.sendmail(self.user, destino, msg)
        smtpserver.close()
        """


