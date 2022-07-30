from __future__ import annotations

import unittest
from random import choice, randint

from datify import Datify, DatifyConfig
from datify.datify import _normalize_month_name


class DigitDatesTestCase(unittest.TestCase):
    strings = [
        '31.12.2021',
        '20/01/2022',
        '14 02 2022',
    ]

    def test_days(self):
        for s in self.strings:
            d = Datify.parse(s)
            self.assertEqual(int(s[:2]), d.day)

    def test_digit_months(self):
        for s in self.strings:
            d = Datify.parse(s)
            self.assertEqual(int(s[3:5]), d.month)

    def test_years(self):
        for s in self.strings:
            d = Datify.parse(s)
            self.assertEqual(int(s[6:]), d.year)

    def test_multiline_dates(self):
        date = '''31.
        12
        .2003'''

        d = Datify.parse(date)
        self.assertEqual((31, 12, 2003), d.tuple())


class AlphabeticMonthsTestCase(unittest.TestCase):
    dates = {
        '10 мая 2022': 5,
        '20th of January, 2021': 1,
        '14 лютого 2022': 2,
        '3 of may 2018': 5
    }

    def test_alphabetic_months(self):
        for date in self.dates:
            d = Datify.parse(date)
            self.assertEqual(self.dates[date], d.month)


class GeneralDatesTestCase(unittest.TestCase):
    dates = {
        '20190301': (1, 3, 2019),
        '20220831': (31, 8, 2022),
        '20201201': (1, 12, 2020),
        '2020-01-20': (20, 1, 2020),  # the separators are not supported now
        '2001.12.21': (21, 12, 2001)  # the separators are not supported now
    }

    def test_general_dates(self):
        for date in self.dates:
            d = Datify.parse(date)
            self.assertEqual(self.dates[date], d.tuple())


class MonthFormsTestCase(unittest.TestCase):
    ukrainian = [
        'січня',
        'лютого',
        'березня',
        'квітня',
        'травня',
        'червня',
        'липня',
        'серпня',
        'вересня',
        'жовтня',
        'листопада',
        'грудня',
    ]

    russian = [
        'января',
        'февраля',
        'марта',
        'апреля',
        'мая',
        'июня',
        'июля',
        'августа',
        'сентября',
        'октября',
        'ноября',
        'декабря'
    ]

    def test_month_forms(self):
        def test_month_list(lst: list[int]) -> None:
            for n in range(len(lst)):
                sep = _choose_from_set(Datify.config.splitters)
                date_str = sep.join(map(str,
                                        (randint(1, 31),
                                         lst[n],
                                         randint(2000, 2022))
                                        ))
                self.assertEqual(n + 1, Datify.parse(date_str).month)

        test_month_list(self.ukrainian)
        test_month_list(self.russian)


class IncompleteDatesTestCase(unittest.TestCase):
    dates = {
        '10 of Jan': (10, 1, None),
        'липень 2022': (None, 7, 2022),
        'июнь 2021': (None, 6, 2021),
        '10 2004': (10, None, 2004)
    }

    def test_incomplete_dates(self):
        for date in self.dates:
            d = Datify.parse(date)

            # test the incomplete dates defined correctly
            self.assertEqual(self.dates[date], d.tuple())

            # test the incomplete dates return None on .date() call
            self.assertIsNone(d.date())


class PredefiningDatesTestCase(unittest.TestCase):
    dates = {
        '20200101': (3, 12, 2021),
        '20040120': (31, 12, 2003),
        '11th of June 2004': (11, 7, 2004)
    }

    def test_predefining_dates(self):
        for date in self.dates:
            d = Datify.parse(date, day=self.dates[date][0], month=self.dates[date][1], year=self.dates[date][2])
            self.assertEqual(self.dates[date], d.tuple())


class SettingsTestCase(unittest.TestCase):
    def test_splitters_adding(self):
        sep = '%'
        Datify.config.splitters.add(sep)
        date = 10, 7, 2006

        date_str = sep.join(map(str, date))
        self.assertEqual(date, Datify.parse(date_str).tuple())

        Datify.config.splitters.remove(sep)

    def test_day_first(self):
        dates = [_random_date() for _ in range(100)]
        DatifyConfig.day_first = False

        for date in dates:
            d = Datify.parse(date[0])
            expected = date[1]
            day_month = (expected.day, expected.month)
            expected_tuple = (*(day_month if expected.day > 12 else reversed(day_month)), expected.year)
            self.assertEqual(expected_tuple, d.tuple(),
                             msg=f'{date[0]} should be equal to {expected_tuple}')

        DatifyConfig.day_first = True


class RandomTests(unittest.TestCase):
    tests_count = 10_000

    def test_random(self):
        for i in range(self.tests_count):
            date_str, expected = _random_date(i > self.tests_count / 2)
            d = Datify.parse(date_str)
            self.assertEqual(expected.tuple(), d.tuple(), msg=f'date_str={date_str} was {d.tuple()}')
            self.assertEqual(Datify.parse(date_str).tuple(), d.tuple(), msg='Datify.parse({0}) should be equal to '
                                                                            'Datify({0})'.format(date_str))


class LocalizationTests(unittest.TestCase):
    french_months = (
        'Janvier',
        'Février',
        'Mars',
        'Avril',
        'Peut',
        'Juin',
        'Juillet',
        'Août',
        'Septembre',
        'Octobre',
        'Novembre',
        'Décembre',
    )

    def _cleanup(self):
        for i in range(len(self.french_months)):
            DatifyConfig.months[i].remove(_normalize_month_name(self.french_months[i]))

    def test_locale_addition(self):
        # test that the locale of the wrong length is not added to the config
        self.assertRaises(ValueError, lambda: DatifyConfig.add_months_locale(self.french_months[::2]))

        # test that the correct locale is added correctly
        try:
            DatifyConfig.add_months_locale(self.french_months)
        except ValueError as e:
            self.fail('Unexpected exception raised: {}'.format(e))

        # cleanup
        self._cleanup()

    def test_added_locale_is_processed(self):
        DatifyConfig.add_months_locale(self.french_months)

        dates = {
            '20 septembre 2022': (20, 9, 2022),
            '17 Peut 2020': (17, 5, 2020),
            '2 Avril 2008': (2, 4, 2008),
        }

        for date in dates:
            d = Datify.parse(date)
            self.assertEqual(dates[date], d.tuple())

        # cleanup
        self._cleanup()


def _random_date(is_alphanumeric: bool = False) -> tuple[str, Datify]:
    sep: str = _choose_from_set(DatifyConfig.splitters)
    day = randint(1, 31)
    month_num = randint(1, 12)
    year = randint(1917, 2022)

    return (sep.join(
        map(str, (day, _choose_from_set(DatifyConfig.months[month_num - 1]) if is_alphanumeric else month_num,
                  year))), Datify(year=year, day=day, month=month_num))


def _choose_from_set(st: set[...]) -> ...:
    return choice(tuple(st))


if __name__ == '__main__':
    unittest.main()
