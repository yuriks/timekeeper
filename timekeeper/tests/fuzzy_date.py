import unittest
import datetime

from ..fuzzy_date import parse_fuzzy_datetime

class ParseFuzzyDatetimeTests(unittest.TestCase):
    def setUp(self):
        self.current_time = datetime.datetime(2013, 9, 10, 15, 0, 0) # 2013-09-10 15:00:00

    def test_timeOnly(self):
        inst = parse_fuzzy_datetime('12:00', self.current_time)
        self.assertEqual(inst, datetime.datetime(2013, 9, 10, 12, 0, 0))
        inst = parse_fuzzy_datetime('18:25', self.current_time)
        self.assertEqual(inst, datetime.datetime(2013, 9, 9, 18, 25, 0))
        inst = parse_fuzzy_datetime('08:55:25', self.current_time)
        self.assertEqual(inst, datetime.datetime(2013, 9, 10, 8, 55, 25))

    def test_datePositions(self):
        inst = parse_fuzzy_datetime('25/04/1991 15:00', self.current_time)
        self.assertEqual(inst, datetime.datetime(1991, 4, 25, 15, 0, 0))
        inst = parse_fuzzy_datetime('15:00 25/04/1991', self.current_time)
        self.assertEqual(inst, datetime.datetime(1991, 4, 25, 15, 0, 0))

    def test_incompleteYear(self):
        inst = parse_fuzzy_datetime('25/04/13 15:00', self.current_time)
        self.assertEqual(inst, datetime.datetime(2013, 4, 25, 15, 0, 0))
        inst = parse_fuzzy_datetime('25/04/80 15:00', self.current_time)
        self.assertEqual(inst, datetime.datetime(2080, 4, 25, 15, 0, 0))

    def test_incompleteDate(self):
        inst = parse_fuzzy_datetime('25/04 15:00', self.current_time)
        self.assertEqual(inst, datetime.datetime(2013, 4, 25, 15, 0, 0))
        inst = parse_fuzzy_datetime('25 15:00', self.current_time)
        self.assertEqual(inst, datetime.datetime(2013, 9, 25, 15, 0, 0))
