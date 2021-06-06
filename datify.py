# encoding: utf-8
# module datify

"""This module allows extracting valid date from user input.

User input is processed through class 'Datify'. Code  `Datify(string).date()`  will return datetime object if all 
parameters were given in the string. Otherwise it will raise TypeError. To get tuple of all available fields from 
string use  `Datify(string).tuple()` To get datetime object or tuple if datetime is unable to be created use  
`Datify(string).date_or_tuple()`
Languages supported: English, Russian, Ukrainian.

Datify can be used to identify separate parts of dates, e.g. '2021', 'july', '6th' through inner functions
isDay(day), isYear(year), isDigitMonth(month) for digit representation of month, and isAlphaMonth(month) for alpha
representation of month.
===
Datify can handle all of the cases of user input listed below and may work with some other cases. Try by yourself before
using:

'06.06.2021'                # Also, '-', '/', and ' ' can be used as separators instead '.', and new separators can be added
'6/6/2021'                  # to  `config['Separators']`
'July, 6th, 2021'
'6th of July, 2021'
'Декабрь, 6, 2021'
'6 декабря 2021 года'
'20 січня 2020'

and other.
===
Getting result:

Datify(str).date() -> datetime object or TypeError
Datify(str).tuple() -> tuple
Datify(str).date_or_tuple() -> datetime object or tuple

===
Extended version of documentation can be found on GitHub: https://github.com/MitryP/datify/
"""
import re

from datetime import datetime

config = {
    'Splitters': [' ', '/', '.', '-'],

    'FORMAT_DAY_DIGIT': r'[0123]?\d$',
    'FORMAT_DAY_ALNUM': r'[0123]?\d',
    'FORMAT_MONTH_DIGIT': r'[01]?\d$',
    'FORMAT_YEAR_DIGIT': r'[012]\d\d\d$|\d\d$',
    'FORMAT_DATE': r'[12][01]\d\d[01]\d[0123]\d$'
}

Months = {
    ('january', 'jan', 'январь', 'січень'): 1,
    ('february', 'feb', 'февраль', 'лютий'): 2,
    ('march', 'mar', 'март', 'березень'): 3,
    ('april', 'apr', 'апрель', 'квітень'): 4,
    ('may', 'май', 'травень'): 5,
    ('june', 'jun', 'июнь', 'червень'): 6,
    ('july', 'jul', 'июль', 'липень'): 7,
    ('august', 'aug', 'август', 'серпень'): 8,
    ('september', 'sep', 'сентябрь', 'вересень'): 9,
    ('october', 'oct', 'октябрь', 'жовтень'): 10,
    ('november', 'nov', 'ноябрь', 'листопад'): 11,
    ('december', 'dec', 'декабрь', 'грудень'): 12
}


def _isSameWord(str1: str, str2: str):
    """
    Tries to figure if given strings are the same words in different forms.
    Returns True or False.

    :param str1: str
    :param str2: str
    :return: Bool
    """

    return len(set(str1).difference(set(str2))) < len(str1) / 2 and (
        str1[0:2] == str2[0:2] if len(str1) < 4 else str1[0:3] == str2[0:3])


class Datify:
    splitters = config['Splitters']
    day_format_digit = config['FORMAT_DAY_DIGIT']
    day_format_alnum = config['FORMAT_DAY_ALNUM']
    month_format_digit = config['FORMAT_MONTH_DIGIT']
    year_format = config['FORMAT_YEAR_DIGIT']
    date_format = config['FORMAT_DATE']

    def __init__(self, user_input: str = None, year: int = None, month: int = None, day: int = None):
        """
        Creates Datetime object. If no parameters are given, raises ValueError.

        :param user_input: Takes str, optional
        :param year: Takes int, optional
        :param month: Takes int, optional
        :param day: Takes int, optional
        """

        self.day, self.month, self.year, self.lost = None, None, None, list()
        if user_input:
            words = self.getWordsList(user_input)
            if words:
                for word in words:
                    if Datify.isDay(word) and not self.day:
                        self.setDay(word)

                    elif (Datify.isDigitMonth(word) or Datify.isAlphaMonth(word)) and not self.month:
                        self.setMonth(word)

                    elif Datify.isYear(word) and not self.year:
                        self.setYear(word)

                    else:
                        self.lost.append(word)

            elif user_input.isdigit() and len(user_input) > 4:
                search = re.search(Datify.date_format, user_input)
                if search:
                    search_str = search.group(0)
                    self.setYear(search_str[0:4])
                    self.setMonth(search_str[4:6])
                    self.setDay(search_str[6:8])

                else:
                    raise ValueError

            elif Datify.isDay(user_input):
                self.setDay(user_input)

            elif Datify.isAlphaMonth(user_input):
                self.setMonth(user_input)

            elif Datify.isYear(user_input):
                self.setYear(user_input)

            else:
                raise ValueError

        elif any((year, month, day)):
            self.year = year
            self.month = month
            self.day = day

        else:
            raise ValueError

    @staticmethod
    def isDay(string: str):
        """
        Find if the given string is suitable for the day format: e.g. '09' or '9,' or '9th'.
        Returns True or False

        :param string: Takes str
        :return: Bool
        """

        if string.isdigit():
            if re.match(Datify.day_format_digit, string) and 0 < int(string) <= 31:
                return True

            else:
                return False

        else:
            if re.match(Datify.day_format_alnum, string):
                return True

            else:
                return False

    def setDay(self, day: [str, int]):
        """
        Sets day of Datify's object manually.

        :param day: Takes str or int
        :return: no return
        """

        if Datify.isDay(day):
            if day.isdigit():
                self.day = int(day)

            elif re.match(Datify.day_format_alnum, day):
                day_re = re.search(Datify.day_format_alnum, day)

                if day_re:
                    day_str = day_re.group(0)

                    if day_str.find(','):
                        day_str = day_str.replace(',', '')

                    self.day = int(day_str)

                else:
                    raise ValueError

        else:
            raise ValueError

    @staticmethod
    def isDigitMonth(string: str):
        """
        Find if the given string is suitable for the month format: e.g. '09' or '9'.
        Returns True or False.

        :param string: Takes str
        :return: Bool
        """

        if re.match(Datify.month_format_digit, string) and 0 < int(string) <= 12:
            return True

        else:
            return False

    @staticmethod
    def isAlphaMonth(string: str):
        """
        Find if the given string is suitable for the month format: e.g. 'January' or 'jan' or 'январь' or 'января'.
        Returns True or False.

        :param string:
        :return:
        """

        word = string.lower()
        for month in Months.keys():
            if word in month or any(_isSameWord(month_name, word) for month_name in month):
                return True

            else:
                continue

        else:
            return False

    @staticmethod
    def getAlphaMonth(string: str):
        """
        Returns number of the given month name. If not found, returns None.

        :param string: Takes str
        :return: int or None
        """

        word = string.lower()
        for month in Months.keys():
            if word in month or any(_isSameWord(month_name, word) for month_name in month):
                return Months[month]

        else:
            return None

    def setMonth(self, month: [str, int]):
        """
        Sets month of Datify's object manually. Takes number of a month or its name.

        :param month: Takes str or int
        :return: no return
        """

        if Datify.isDigitMonth(str(month)):
            self.month = int(month)

        elif Datify.isAlphaMonth(str(month)):
            self.month = Datify.getAlphaMonth(month)

        else:
            raise ValueError

    @staticmethod
    def isYear(string: str):
        """
        Find if the given string is suitable for the year format: e.g. '14' or '2014'.
        Returns True or False.

        :param string: Takes str
        :return: Bool
        """

        if re.match(Datify.year_format, string):
            return True

        else:
            return False

    def setYear(self, year: [str, int]):
        """
        Sets year of Datify's object manually.

        :param year: Takes str or int
        :return: no return
        """

        if Datify.isYear(year):
            if len(str(year)) == 4:
                self.year = int(year)

            else:
                self.year = int(f'20{year}')

        else:
            raise ValueError

    @staticmethod
    def getWordsList(string: str):
        """
        Returns list of string's elements if given string contains one of the separators. Otherwise returns None.
        Example: Datify.getWordsList('04.06.2020')
        Return: ['04', '06', '2020']

        :param string: Takes str
        :return: list or None
        """

        for splitter in Datify.splitters:
            if string.find(splitter) > 0:
                return string.split(splitter)

            else:
                continue

        else:
            return None

    def date(self):
        """
        Returns datetime object if all needed parameters are known. Otherwise raises TypeError.

        :return: datetime object
        """

        try:
            return datetime(year=self.year, month=self.month, day=self.day)

        except TypeError:
            raise TypeError

    def tuple(self):
        """
        Returns tuple of known parameters.

        :return: datetime object or tuple
        """
        res = list()
        for val in (self.day, self.month, self.year):
            if val:
                res.append(val)

            else:
                continue

        else:
            return tuple(res)

    def date_or_tuple(self):
        """
        Returns datetime object if all needed parameters are known. Otherwise returns tuple of known parameters.

        :return: datetime object or tuple
        """

        try:
            return datetime(year=self.year, month=self.month, day=self.day)

        except TypeError:
            return self.tuple()
