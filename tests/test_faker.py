import datetime

from nose.tools import assert_equals

from git_fake_metadata import MetaDataFaker


def get_datetime_from_string(date_string):
    return datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')


def test_date_time_in_range():
    meta_data_faker = MetaDataFaker()
    tests_data = [
        {
            'start_date': '2007-03-04 16:08:12',
            'date_time_range': '17:00-20:00',
            'expected': '2007-03-04 17:00:12',
        },
        {
            'start_date': '2007-03-04 17:08:12',
            'date_time_range': '17:00-20:00',
            'expected': '2007-03-04 17:08:12',
        },
        {
            'start_date': '2007-03-04 20:08:12',
            'date_time_range': '17:00-20:00',
            'expected': '2007-03-05 17:00:12',
        },
        {
            'start_date': '2007-03-04 20:08:12',
            'date_time_range': '17:00-20:00,08:00-09:00',
            'expected': '2007-03-05 08:00:12',
        },
        {
            'start_date': '2007-03-04 20:08:12',
            'date_time_range': '08:00-09:00,17:00-20:00',
            'expected': '2007-03-05 08:00:12',
        },
    ]
    for test_data in tests_data:
        start_date = datetime.datetime.strptime(
            test_data['start_date'],
            '%Y-%m-%d %H:%M:%S'
        )
        date_time_range = test_data['date_time_range']
        assert_equals(
            meta_data_faker._date_time_in_range(date_time_range, start_date),
            get_datetime_from_string(test_data['expected'])
        )
