import unittest
import mainGUI
from datetime import *


class InitDate(unittest.TestCase):

    def tearDown(self):
        pass

    def setUp(self):
        self.new_date = mainGUI.Date(datetime.today())
        self.new_date.startH = 7
        self.new_date.endH = 15
        self.new_date.startHChange = 7
        self.new_date.load_date()

    def test_date_init(self):
        assert self.new_date.events == [], "Date not initializing correctly"

    def test_load_date(self):
        assert self.new_date.buttons[1]["text"] == "Nothing Scheduled", "Buttons not initializing correctly"


if __name__ == '__main__':
    unittest.main()
