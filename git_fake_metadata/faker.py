# -*- coding: utf-8 -*-

"""
test
"""

import os
import logging
import datetime
from random import randint
import subprocess

import git

from ._meta import __version__
from .defaults import DEFAULTS
from .config import Config


class MetaDataFaker:
    def __init__(
        self,
        conf=None,
        repo_dir=None,
    ):

        self._entities = {}
        self._conf = conf
        self._repo_dir = self._get_repo_dir(repo_dir)

    def _config_get(self, )

    def _get_repo_dir(self, repo_dir):
        if not repo_dir:
            try:
                repo_dir = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'])
                repo_dir = repo_dir.decode('utf-8').strip()
            except subprocess.CalledProcessError:
                raise IOError('Given working directory is not a git repository.')

        return repo_dir

    def _get_random_delay(self):
        random_delay = datetime.timedelta(
            seconds=randint(
                self._conf._config_get('time_delta_min').seconds,
                self._conf._config_get('time_delta_max').seconds,
            )
        )
        return random_delay

    def _get_most_recent_commit_datetime(self):
        """
        Using _get_last_vcs_datetime for now.
        """
        latest_epoch_time = 0
        repo = git.Git()
        repo.update_environment(TZ='UTC')
        for line in repo.log('--all', '--format=%at %ct').split('\n'):
            author_date, committer_date = line.split(' ')
            latest_epoch_time = max(
                latest_epoch_time,
                int(author_date),
                int(committer_date),
            )
        return datetime.datetime.utcfromtimestamp(latest_epoch_time)

    def _get_last_vcs_datetime(self):
        repo = git.Repo()
        commit = repo.head.commit
        start_date = min(
            commit.authored_date - commit.author_tz_offset,
            commit.committed_date - commit.committer_tz_offset,
        )
        return datetime.datetime.utcfromtimestamp(start_date)

    def _set_time(self, time_string, start_date):
        hour_minute = time_string.split(':')
        return start_date.replace(hour=int(hour_minute[0]), minute=int(hour_minute[1]))

    def _date_time_in_range(self, date_time_range, start_date):
        end_date = datetime.datetime.strptime(
            '2323-05-23 23:23:23',
            '%Y-%m-%d %H:%M:%S'
        )
        earliest_start_date = end_date
        for time_range in date_time_range.split(','):
            times = time_range.split('-')
            from_time = self._set_time(times[0], start_date)
            to_time = self._set_time(times[1], start_date)
            if start_date < from_time:
                earliest_start_date = min(from_time, earliest_start_date)
            elif start_date < to_time:
                earliest_start_date = min(start_date, earliest_start_date)

        if earliest_start_date != end_date:
            return earliest_start_date

        return self._date_time_in_range(
            date_time_range,
            start_date.replace(hour=0, minute=0) + datetime.timedelta(days=1)
        )

    def _get_faked_time(self):
        start_date = self._get_last_vcs_datetime()

        date_time_range = self._conf._config_get('date_time_range')
        start_date = self._date_time_in_range(date_time_range, start_date)

        #  print(self._get_last_action_timestamp(start_date))
        #  self._update_last_action_timestamp(start_date)
        print(start_date)
        #  if self._date_time_in_range()

        #  print(time.gmtime(555.0))
        #  print(datetime.time(0, 0, 555))

        #  start_date.replace(hour=18)

        #  print(start_date + self._get_random_delay())

    def git_commit_wrapper(self):
        env = {
            'GIT_AUTHOR_DATE': "/usr/bin",
            'GIT_COMMITTER_DATE ': "/usr/bin",

        }
        subprocess.call(['git', 'commit'], env=env)

if __name__ == '__main__':
    from argparse import ArgumentParser

    args_parser = ArgumentParser(
        description=__doc__,
    )
    args_parser.add_argument(
        '-V', '--version',
        action='version',
        version=__version__,
    )
    args_parser.add_argument(
        '-d', '--debug',
        help="Print lots of debugging statements.",
        action='store_const',
        dest='loglevel',
        const=logging.DEBUG,
        default=logging.WARNING,
    )
    args_parser.add_argument(
        '-v', '--verbose',
        help="Be verbose.",
        action='store_const',
        dest='loglevel',
        const=logging.INFO,
    )
    args = args_parser.parse_args()

    logger = logging.getLogger(__file__)
    logging.basicConfig(
        format='%(levelname)s: %(message)s',
        level=args.loglevel,
    )

    conf = Config()
    meta_data_faker = MetaDataFaker(conf=conf)
    #  meta_data_faker.git_commit_wrapper()
    print(meta_data_faker._get_faked_time())
