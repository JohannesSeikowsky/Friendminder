"""
Friendship Reminder App

This small app habitually sends out two reminders.
One containing a list of friends that I want to stay in touch with and
another containing to-dos that I've set with regard to certain people on the list.

This list of friends and to-dos plus the intervals within which each of the reminders
is to be sent are all set in a googlesheet.

Hence the code firstly connects to the sheeet, then constructs the email reminders 
based on content retrieved and moreover ensures that both reminders are sent
on the correct dates in the correct intervals.

That inveral setting is retrieved from cell A1 in the spreadsheet.
Then code is then set to be run once a day via a cronjob.
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from email_utils import send_email, email_myself
from datetime import datetime, timedelta
import configs


# connect to google sheet
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(configs.path_to_code + "client_secret.json", scope)
client = gspread.authorize(creds)
google_sheet = client.open(configs.spreadsheet_name).sheet1


# construct and send the relevant emails
def email_friend_list():
	""" send email with list of friends """
	friendlist_email = ""

	first_column = google_sheet.col_values(1)
	friends_list = first_column[3:] # because friend listing only starts at row 4
	friends = "\n".join(friends_list)

	friendlist_email += friends
	email_myself("Friends", friendlist_email)

def email_suggestions():
	""" send email with action suggestions related to friends """
	suggestions_email = ""
	friends_col = google_sheet.col_values(1)
	actions_col = google_sheet.col_values(2)

	for index, action in enumerate(actions_col):
		if action:
			friend = friends_col[index]
			suggestions_email += friend + " - " + action + "\n"

	email_myself("Friends - Suggestions", suggestions_email)


# get settings from spreadsheet
def get_settings_cell():
	settings_cell_coordinate = "A1"
	cell_value = google_sheet.acell(settings_cell_coordinate).value
	return cell_value

def parse_settings(settings):
	settings_dict = {}
	for setting in settings.split(","):
		setting_key, setting_val = setting.split(":")
		settings_dict[setting_key.strip()] = int(setting_val.strip())
	return settings_dict

def get_settings_from_spreadsheet():
	settings = get_settings_cell()
	settings = parse_settings(settings)
	return settings
spreadsheet_settings = get_settings_from_spreadsheet()


# Sending reminder emails when appropriate
reminders = { "general_reminder": configs.path_to_code + "settings/general_settings.txt",
"suggestions_reminder": configs.path_to_code + "settings/suggestions_settings.txt" }


def send_relevant_reminder(reminder):
	if reminder == "general_reminder":
		email_friend_list()
	else:
		email_suggestions()

def is_today(date):
	date = date.strftime("%d.%m")
	today = datetime.today().strftime("%d.%m")

	if date == today:
		return True
	else:
		return False

def get_reminder_settings(path):
	with open(path) as f:
		lines = f.readlines()
		vals = []
		for line in lines:
			val = line.split(",")[1].strip()
			vals.append(val)
		return vals

def get_interval_from_sheet(reminder):
	if reminder == "general_reminder":
		interval = spreadsheet_settings["General-Reminder"]
	else:
		interval = spreadsheet_settings["Suggestions-Reminder"]
	return interval

def get_all_lines(path):
	with open(path) as f:
		lines = f.readlines()
	return lines

def rewrite_date(set_interval, path):
	today = datetime.today()
	new_date = today + timedelta(days=int(set_interval))
	new_date = new_date.strftime("%d.%m")
	lines = get_all_lines(path)

	with open(path, "w") as f:
		lines[1] = "next date, " + new_date
		f.writelines(lines)

def rewrite_interval(interval, path):
	lines = get_all_lines(path)

	with open(path, "w") as f:
		lines[0] = "interval, " + str(interval) + "\n"
		f.writelines(lines)


def send_reminders():
	for reminder, reminder_path in reminders.items():
		# read settings from local file
		set_interval, next_date = get_reminder_settings(reminder_path)

		# send reminder if today is a send-date
		target_date = datetime.strptime(next_date, "%d.%m")
		if is_today(target_date):
			send_relevant_reminder(reminder)
			# record new next_date locally
			rewrite_date(set_interval, reminder_path)

		# send reminder if interval has changed
		interval = get_interval_from_sheet(reminder)
		if not int(set_interval) == interval:
			send_relevant_reminder(reminder)
			# record new interval and next_date locally
			rewrite_interval(interval, reminder_path )
			rewrite_date(interval, reminder_path)

try:
	send_reminders()
except Exception as e:
	subject = "Exception occured in Friendminder app"
	content = str(e)
	email_myself(subject, content)
