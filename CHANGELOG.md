_The changelog started at ver. 1.1.0_

# 1.1.0

- Major RegExps fix.
- Marked a bunch of methods as deprecated. The 1.1.0 update rebuilds the logic of Datify without breaking the 
existing functionality, but the **2.0.0 version will break the old code**. From this version, the usage of the code 
marked as deprecated will raise DeprecationWarnings. Consider removing the deprecated functionality usage.
- Major reconsidering of the logic of Datify based on the [Dart implementation](https://github.com/mitryp/datifyDart).
  - Completely rewritten the parsing logic.
  - Now the class doesn't raise exceptions when the date is not found.
  - Now the methods are null-safe.
- Replaced the old configuration dictionary with the `DatifyConfig` class **(no backwards compatibility)**. 
See the documentation for more information.
- Added unit tests.
- Updated the README.
- Removed the russian README file.
- Added `example/example.py`.

The list of the deprecated methods:
- is_date_part
- is_date
- find_date
- is_day
- set_day
- is_digit_month
- is_alpha_month
- get_alpha_month
- set_month
- is_year
- set_year
- date_or_tuple
- setup_variables

**These methods will be removed in the 2.0.0 release.** Until then, the usage of these methods will produce 
DeprecationWarnings.