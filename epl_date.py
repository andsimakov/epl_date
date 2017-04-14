import unittest


def leap_year(year):
    """Checks if given year is the leap year
    :param year: int
    :return: boolean
    """
    if year <= 99:
        year += 2000
    return year % 4 == 0 and year % 100 != 0 or year % 400 == 0


def day_check(month, day):
    """Checks if a month/day couple meet some requirement
    :param month: int
    :param day: int
    :return: boolean
    """
    short_months = [4, 6, 9, 11]
    return month in short_months and day > 30 or month is 2 and day > 29


def epl_date(input_str):
    """Converts A/B/C string to a date formatted as 'yyyy-mm-dd'.
    Tries to return the earliest possible legal date
    between Jan 1, 2000 and Dec 31, 2999 inclusively

    :param input_str: string with a name of input string file
    :return: 'yyyy-mm-dd' string or 'A/B/C is illegal'
    """
    lst = sorted(list(map(int, input_str.split('/'))))
    illegal_msg = '{} is illegal'.format(input_str)

    # BASE CASE: More than one 0 or all numbers > 12
    if lst.count(0) > 1 or all(num > 12 for num in lst) or sum(num > 31 for num in lst) == 2:
        return illegal_msg

    # BASE CASE: Year 2000 or > 2031
    if 0 in lst or sum(num > 31 for num in lst) == 1 or sum(num >= 2000 for num in lst) == 1:
        year_idx = next(i for i, v in enumerate(lst) if v > 31 or v == 0)
        year = lst[year_idx]
        del lst[year_idx]
        month = lst[0]
        day = lst[1]

    else:
        year = lst[0]
        month = lst[1]
        day = lst[2]
        if month > 12:
            month, year = year, month
            if day_check(month, day):
                day, year = year, day
            elif month is 2 and day is 29:
                if not leap_year(year):
                    day, year = year, day

    if year <= 99:
        year += 2000
    result = '{}-{:02d}-{:02d}'.format(year, month, day)

    # Final check
    if day_check(month, day):
        return illegal_msg
    elif month is 2 and day is 29:
        if leap_year(year):
            return result
        else:
            return illegal_msg
    else:
        return result


# Test cases
class Test(unittest.TestCase):
    def test_leap_year(self):
        self.assertEqual(leap_year(0), True)
        self.assertEqual(leap_year(16), True)
        self.assertEqual(leap_year(28), True)
        self.assertEqual(leap_year(2000), True)
        self.assertEqual(leap_year(2016), True)
        self.assertEqual(leap_year(2028), True)
        self.assertEqual(leap_year(1900), False)
        self.assertEqual(leap_year(2100), False)
        self.assertEqual(leap_year(2200), False)

    def test_day_check(self):
        self.assertEqual(day_check(1, 30), False)
        self.assertEqual(day_check(9, 31), True)
        self.assertEqual(day_check(4, 30), False)
        self.assertEqual(day_check(2, 29), False)

    def test_epl_date(self):
        self.assertEqual(epl_date('2001/1/1'), '2001-01-01')
        self.assertEqual(epl_date('2999/12/31'), '2999-12-31')
        self.assertEqual(epl_date('1/2/3'), '2001-02-03')
        self.assertEqual(epl_date('3/20/1'), '2001-03-20')

        self.assertEqual(epl_date('3/00/0'), '3/00/0 is illegal')
        self.assertEqual(epl_date('0/0/0'), '0/0/0 is illegal')
        self.assertEqual(epl_date('13/15/14'), '13/15/14 is illegal')
        self.assertEqual(epl_date('07/32/33'), '07/32/33 is illegal')

        self.assertEqual(epl_date('3/00/1'), '2000-01-03')
        self.assertEqual(epl_date('99/19/9'), '2099-09-19')
        self.assertEqual(epl_date('18/2000/04'), '2000-04-18')
        self.assertEqual(epl_date('12/42/2'), '2042-02-12')
        self.assertEqual(epl_date('2012/42/2'), '2012/42/2 is illegal')
        self.assertEqual(epl_date('31/2008/9'), '31/2008/9 is illegal')

        self.assertEqual(epl_date('11/20/1'), '2001-11-20')
        self.assertEqual(epl_date('7/7/7'), '2007-07-07')
        self.assertEqual(epl_date('6/8/7'), '2006-07-08')
        self.assertEqual(epl_date('1/11/04'), '2001-04-11')

        self.assertEqual(epl_date('31/9/20'), '2031-09-20')
        self.assertEqual(epl_date('30/10/20'), '2020-10-30')
        self.assertEqual(epl_date('30/10/2'), '2002-10-30')
        self.assertEqual(epl_date('31/31/10'), '2031-10-31')

        self.assertEqual(epl_date('9/31/30'), '2031-09-30')
        self.assertEqual(epl_date('28/2/29'), '2028-02-29')
        self.assertEqual(epl_date('27/2/29'), '2029-02-27')
        self.assertEqual(epl_date('27/2/30'), '2030-02-27')
        self.assertEqual(epl_date('9/31/00'), '9/31/00 is illegal')
        self.assertEqual(epl_date('4/2025/31'), '4/2025/31 is illegal')

        self.assertEqual(epl_date('2/2100/29'), '2/2100/29 is illegal')
        self.assertEqual(epl_date('2020/29/2'), '2020-02-29')
        self.assertEqual(epl_date('56/30/2'), '56/30/2 is illegal')


if __name__ == '__main__':
    unittest.main()
