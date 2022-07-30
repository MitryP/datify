from __future__ import annotations

import abc
import dataclasses

from datify import Datify

SearchRequest = dict[str, str]
"""A representation of a search request for the example.

In the example there should be a 'date' field in the dict to represent the searching by a date.
"""


@dataclasses.dataclass
class Date:
    """The class that represents a date in the example.

    Has nullable year, month, and day fields and a method that checks if the date satisfies the query.
    """

    year: int | None
    month: int | None
    day: int | None

    def __hash__(self):
        return hash((self.year, self.month, self.day))

    def satisfies(self, year: int | None = None, month: int | None = None, day: int | None = None) -> bool:
        """Returns True if the Date object satisfies the given year, month and day.
        If the Date object does not have the field, it considered equal to the given corresponding value.
        The same for the method arguments.
        """

        pairs = ((year, self.year), (month, self.month), (day, self.day))

        return all(
            any((None in pair, pair[0] == pair[1])) for pair in pairs
        )


class Events(abc.ABC):
    """Database emulation for the example.

    This class stores dates and the corresponding event descriptions and provides the method for
    record requesting from the storage.
    """
    _records = {
        Date(year=2021, month=12, day=31): 'New Year party 🎄',
        Date(year=2022, month=1, day=20): 'Birthday celebration 🎁',
        Date(year=2022, month=2, day=14): 'St. Valentines Day 💖',
        Date(year=2022, month=2, day=23): 'The cinema attendance 📽',
        Date(year=2022, month=5, day=23): 'A long-awaited Moment 🔥',
    }
    """Stores the dates and the corresponding event descriptions."""

    @classmethod
    def query(cls, year: int | None = None, month: int | None = None, day: int | None = None) -> str | None:
        """Returns an event descriptions based on the provided date parts.

        If no date parts provided or no corresponding event descriptions are found, the method returns None.
        """

        # handle empty requests
        if all((year is None, month is None, day is None)):
            return None

        # return the first string corresponding to the Date that satisfies the query, if any
        for record_date in cls._records:
            if record_date.satisfies(year, month, day):
                return cls._records[record_date]

        return None


def handle_request(search_request: SearchRequest) -> str:
    """Handles the SearchRequest requests.

    Returns a corresponding event description or the error message.
    """
    date_query = search_request['date']

    # Datify handles all the parsing inside freeing from even thinking about it!
    parsed = Datify.parse(date_query)

    response = Events.query(year=parsed.year, month=parsed.month, day=parsed.day)

    return response if response is not None else 'No events found for this query 👀'


if __name__ == '__main__':
    # define dates in the different formats
    dates = (
        '31.12.2021',  # common digit-only date format
        '2022-02-23',  # another commonly-used date format
        '23-02/2022',  # the supported separators can be combined in the string
        '20 of January',  # date is incomplete but still correctly parsed
        'May',  # just a month name
        '14 лютого 2022',  # Ukrainian date which stands for 14.02.2022
        'not a date',  # not a date at all
    )

    # 'request' all the dates and print the result
    for date in dates:
        print(f'{date}: {handle_request({"date": date})}')
