# email utilities
import smtplib, configs

def send_email(target, subject, content):
	mail = smtplib.SMTP("smtp.gmail.com", 587)
	mail.ehlo()
	mail.starttls()

	gmail_acc = configs.gmail_account
	gmail_pw = configs.gmail_pw
	mail.login(gmail_acc, gmail_pw)

	msg_content = "Subject:{}\n\n{}".format(subject, content)
	mail.sendmail(gmail_acc, target, msg_content)
	mail.close()

def email_myself(subject, content):
	recipient = configs.gmail_account
	send_email(recipient, subject, content)
