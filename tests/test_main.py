# from friendminder import main
import sys
sys.path.append('/home/johannes/code/friendminder')

import unittest, datetime, random
import main


class FriendminderTests(unittest.TestCase):
	""" some basic tests """

	def test_is_today(self):
		# checking is_today for today
		today = datetime.datetime.today()
		self.assertTrue(main.is_today(today))

		# checking fis_today or future dates
		interval = random.randint(0, 10)
		future_date = today + datetime.timedelta(days=interval)
		self.assertFalse(main.is_today(future_date))

		# checking is_today for past dates
		interval = random.randint(0, 10)
		past_date = today - datetime.timedelta(days=interval)
		self.assertFalse(main.is_today(past_date))


	def test_get_reminder_settings(self):
		path = "/home/johannes/code/friendminder/" + "settings/general_settings.txt"
		vals = main.get_reminder_settings(path)
		self.assertTrue(len(vals) == 2)

if __name__ == "__main__":
	unittest.main()
