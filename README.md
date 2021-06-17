# Datify
This Python3 module allows to extract parts of valid date from user input.
User input is processed through class `Datify`.
## Languages supported: 
- [x] English
- [x] Russian  -  [Readme на русском](README-ru.md) 
- [x] Ukrainian.

---

## Installing
Simply run `pip install datify` from your command line (pip must be installed).


## Class:
` Datify(user_input, year, month, date) ` : takes str when creating. Also, can take particular parameters like `year`, `month`, and `day` along with user input or without it. If no parameters are given, raises ValueError. **See the section *Formats* to discover default Datify's formats.**
### Class methods:
  #### Static:
  1. `findDate(string)` : Takes string. Returns substring with date in General Date format if it is contained in the given string.
  2. `isYear(year)` : Takes str or int. Returns True if given parameter suits year format.
  3. `isDigitMonth(month)` : Takes str or int. Returns True if given parameter suits digit month format.
  4. `isAlphaMonth(string)` : Takes str. Returns True if given string suits months dictionary. *For languages in which there are multiple forms of words it's basically enough to have only the main form of the word in dictionary - see `_isSameWord` function.*
  5. `getAlphaMonth(string)` :  Takes str. Returns number(int) of month name in given string according to months dictionary. If no month name is found in the string, returns None.
  6. `isDay(day)` : Takes str or int. Returns True if given parameter suits day format.
  7. `isDate(date)` : Takes str or int. Returns True if given parameter suits general date format (See the section *Default formats*).
  8. `isDatePart(string)` : Takes str. Returns True if given string contains at least one of date parts such as day, month, or year.
  9. `_getWordsList(string)` : from given string returns list of words splitted by a found separator in `config['SEPARATORS']` (See the section *Config*). If no separators are found, returns None.

  #### Instance:
  1. `date()` : returns datetime object from parameters of Datify object. If not all of the necessary parameters are known (`year`, `month`, and `day`), raises TypeError.
  2. `tuple()` : returns tuple from all parameters in format (day, month, year).
  3. `date_or_tuple()` : returns datetime object if all of the necessary parameters are known, otherwise returns tuple of all parameters.
  4. `setYear(year)` : Takes str or int. Extracts year from given parameter and sets `year` field of the called Datify object. If given parameter doesn't suit year format, raises ValueError. *If the year is given in shortened format, counts it as 20YY.*
  5. `setMonth(month)` : Takes str or int. Extracts month from given parameter and sets `month` field of the called Datify object. If given parameter doesn't suit month format and doesn't contain any month names, raises ValueError.
  6. `setDay(day)` : Takes str or int. Extracts day from given parameter and sets `day` field of the called Datify object. If given parameter doesn't suit day format, raises ValueError.

## Default formats:
> **Note that in this module the day is checked firstly, the month - after it. `06.07.2021` stands for `6th of July, 2021`!**
- General date format:
  `'[12][01]\d\d[01]\d[0123]\d$'` - `YYYYMMDD` - e.g. `20210706`
- Day formats:
  0 < day <= 31
  - For digit-only entries: `'[0123]?\d$'` - `D?D` - e.g. `13`, `05`, `6` etc.
  - For alpha-numeric entries: `'[0123]?\d\D+$'` - e.g. `1st`, `2nd`, `25th`, `3-е` etc.
- Month formats:
  0 < month <= 12
  - For digit-only entries: `'[01]?\d$'` - `M?M` - e.g. `06`, `7` etc.
  - For alphabethic strings: tries to find similar words in months dict.
- Year format:
  `'([012]\d\d\d$)|(\d\d$)'` - `YYYY` or `YY` - e.g. `2021` or `21`.
  > Note that if shortened year `YY` is given, it counts as `20YY`.

## Config:
You can customize splitters list, and change format of the all date parts, accessing them using `Datify.config['KEY']`.
n. Name : KEY -- description
1. Splitters : `'SPLITTERS'` -- set of the separators for `Datify._getWordsList`. Contains ` `, `.`, `-`, and `/` by default.
2. Formats (See section *Default formats*) :
  - Digit day : `'FORMAT_DAY_DIGIT'`
  - Alpha-numeric day : `'FORMAT_DAY_ALNUM'`
  - Digit month : `'FORMAT_MONTH_DIGIT'`
  - Digit year : `'FORMAT_YEAR_DIGIT'`
  - General date : `'FORMAT_DATE'`

For example:
```python
Datify('17_06_2021')  # ValueError  # Not works
Datify.config['SPLITTERS'].add('_')  # Adding new separator to the set
Datify('17_06_2021')  # <Datify object (17, 6, 2021)>  # Works!
```

---

## Examples:
I'll use different date formats in every example to show that Datify can handle them all. Let's begin!
```python
from datify import Datify  # Importing our main class
```
1. Extracting date from string with a Datify object
```python
user_input = '06.07.2021'  # Imitating user input. Note that day is first!
val = Datify(user_input)
print(val)  # Output: <Datify object (6, 7, 2021)>
```
Any string can be processed this way.

2. Getting exact date parameters from Datify
```python
user_input = '06/07'
val = Datify(user_input)

date_day = val.day  # 6
date_month = val.month  # 7
date_year = val.year  # None
```

3. Getting date in **datetime** object
```python
user_input = '06-07-21'
date = Datify(user_input).date()  # 2021-07-06 00:00:00
```
If there is a possibility to get an incomplite date, datetime will raise TypeError:
```python
user_input = '06/07'
date = Datify(user_input).date()  # TypeError: an integer is required (got type NoneType)
```
Use the other examples instead, if there is a chanse to get incomplete date.

4. Getting output in a **tuple**:
Order of values: day, month, year
```python
user_input = '6th of July 2021'
Datify(user_input).tuple()  # (6, 7, 2021)

user_input = '6th of July'
Datify(user_input).tuple()  # (6, 7, None)
```

5. Getting alphapetic month without creating Datify object
```python
Datify.getAlphaMonth('february')  # 2
```
7. Various checks for strings
```python
# Check for any date part
Datify.isDatePart('6')  # True (may be day or month)
Datify.isDatePart('31')  # True
Datify.isDatePart('june')  # True
Datify.isDatePart('jan')  # True
Datify.isDatePart('33')  # True (it might be year in `YY` spelling)
Datify.isDatePart('333')  # False
Datify.isDatePart('3131')  # False (it doesn't suit year format (from `10YY` to `21YY`))

# Check for date in General Date format
Datify.isDate('20210607')  # True

# Checks for particular date parts

# Year
Datify.isYear('2021')  # True
Datify.isYear('221')  # False

# Month
Datify.isDigitMonth('11')  # True (0 < str <= 12)
Datify.isAlphaMonth('June')  # True (compares string to dict and uses `_isSameWord` function

# Day
Datify.isDay('13')  # True (0 < str <= 31)
```

8. Getting date in General Date format from any string
```python
user_input = 'created "20200120"'
Datify.findDate(user_input)  # '20200120'
```

9. Parameters of an existing Daitfy object can be modified this way
```python
res = Datify('6th of July, 2021')  # <Datify object (6, 7, 2021)>
res.setYear(2018)
print(res.date())  # 2018-07-06 00:00:00
```
Also exact parameters can be set during creating object:
```python
Datify('6th of July, 2021', year=2018, month=3)  # <Datify object (6, 3, 2018)>
```

*Datify is much more powerful than you may think.*
