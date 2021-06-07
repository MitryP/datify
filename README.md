# Datify
This Python3 module allows to extract parts of valid date from user input.
User input is processed through class `Datify`.
## Languages supported: 
- [x] English
- [x] Russian 
- [x] Ukrainian.

---
## Installing
`---`
---

## Class:
` Datify(user_input, year, month, date) ` : takes str when creating. Also, can take particular parameters like `year`, `month`, and `day` along with user input or without it. If no parameters are given, raises ValueError.
**See the section *Formats* to discover default Ditify's formats**
### Class methods:
  #### Static:
  1. `isYear(year)` : Takes str or int. Returns True if given parameter suits year format.
  2. `isDigitMonth(month)` : Takes str or int. Returns True if given parameter suits digit month format.
  3. `isAlphaMonth(string)` : Takes str. Returns True if given string suits months dictionary. *For languages in which there are multiple forms of words it's basically enough to have only the main form of the word in dictionary - see `_isSameWord` function.*
  4. `getAlphaMonth(string)` :  Takes str. Returns number(int) of month name in given string according to months dictionary. If no month name is found in the string, returns None.
  5. `isDay(day)` : Takes str or int. Returns True if given parameter suits day format.
  6. `isDate(date)` : Takes str or int. Returns True if given parameter suits general date format (See the section *Formats*).
  7. `isDatePart(string)` : Takes str. Returns True if given string contains at least one of date parts such as day, month, or year.
  8. `_getWordsList(string)` : from given string returns list of words splitted by a found separator in `config['Separators']` (See the section *Config*). If no separators are found, returns None.

  #### Instance methods:
  1. `date()` : returns datetime object from parameters of Datify object. If not all of the necessary parameters are known (`year`, `month`, and `day`), raises TypeError.
  2. `tuple()` : returns tuple from all known parameters. *Be careful using it because of there is no accurate way to know if number is a day or a month!*
  3. `date_or_tuple()` : returns datetime object if all of the necessary parameters are known, otherwise returns tuple from all known parameters.
  4. `setYear(year)` : Takes str or int. Extracts year from given parameter and sets `year` field of the called Datify object. If given parameter doesn't suit year format, raises ValueError. *If the year is given in shortened format, counts it as 20YY.*
  5. `setMonth(month)` : Takes str or int. Extracts month from given parameter and sets `month` field of the called Datify object. If given parameter doesn't suit month format and doesn't contain any month names, raises ValueError.
  6. `setDay(day)` : Takes str or int. Extracts day from given parameter and sets `day` field of the called Datify object. If given parameter doesn't suit day format, raises ValueError.

## Global functions:
1. `_isSameWords(str1, str2)` : Takes two str. Tries to figure out if the given strings are different forms of the same word. It's necessary for languages such as Russian, and Ukrainian. For words with less than 4 symbols, compares the first two symbols of the strings and checks if difference between chars is not very big. For longer words does the same but compares the first three symbols. Try not to use it anywhere, because its effect may be upredictable outside of the context of month names.


## Examples:
