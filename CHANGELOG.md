_The changelog started at ver. 1.1.0_

# 1.1.0

- Major RegExps fix.
- Marked the unnecessary methods as deprecated. The 1.1.0 update will rebuild the logic of the Datify without breaking the 
existing functionality, but the **2.0.0 version will be breaking the old code**.
- Started working on the major reconsidering the logic of Datify based on the [Dart implementation](https://github.com/mitryp/datifyDart).

The list of deprecated methods:
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