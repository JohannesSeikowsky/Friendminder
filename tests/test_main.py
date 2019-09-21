# from friendminder import main
import sys
sys.path.append('/home/johannes/code/friendminder')

import unittest, datetime, random
from main import is_today, get_reminder_settings


class FriendminderTests(unittest.TestCase):
	""" some basic tests """

	def test_is_today(self):
		# check is_today for today
		today = datetime.datetime.today()
		self.assertTrue(is_today(today))

		interval = random.randint(1, 10)
		# check is_today or future dates
		future_date = today + datetime.timedelta(days=interval)
		self.assertFalse(is_today(future_date))

		# check is_today for past dates
		past_date = today - datetime.timedelta(days=interval)
		self.assertFalse(is_today(past_date))


	def test_get_reminder_settings(self):
		paths = ["/home/johannes/code/friendminder/settings/general_settings.txt",
					"/home/johannes/code/friendminder/settings/suggestions_settings.txt"]

		for path in paths:				
			vals = get_reminder_settings(path)
			self.assertTrue(len(vals) == 2) # check length
			self.assertTrue(vals[0].isdigit()) # check if interval is numeric


if __name__ == "__main__":
	unittest.main()
