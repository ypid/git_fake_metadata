# -*- coding: utf-8 -*-

import os
from configparser import ConfigParser
from glob import glob
import datetime

import pytimeparse

from .defaults import DEFAULTS


class Config:
    def __init__(
        self,
        config_dir=DEFAULTS['config_dir'],
        home_dir=os.getenv('HOME'),
    ):

        self._config_dir = config_dir
        self._home_dir = home_dir

        self._read_config()

    def _read_config(self):
        os.makedirs(self._config_dir, exist_ok=True)
        self._config = ConfigParser({
            'time_delta_min': '3m',
            'time_delta_max': '30m',
        })
        config_files = sorted(glob(os.path.join(self._config_dir, '*.ini')))
        self._config.read(config_files)

    def _config_get(self, option, raw=False, preprocess=True, possible_sections=[]):
        section = 'DEFAULT'
        possible_sections = [
            self._repo_dir,
        ]
        if self._repo_dir.startswith(self._home_dir):
            possible_sections.append(self._repo_dir[len(self._home_dir):].lstrip('/'))

        for possible_section in possible_sections:
            if self._config.has_section(possible_section):
                section = possible_section

        if option.startswith('time_delta'):
            time_delta = pytimeparse.parse(self._config.get(section, option))
            if preprocess:
                return datetime.timedelta(seconds=time_delta)
            else:
                return time_delta

        return self._config.get(section, option)
