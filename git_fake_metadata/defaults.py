# -*- coding: utf-8 -*-

import os

from xdg.BaseDirectory import xdg_config_home

config_dir = os.path.join(xdg_config_home, 'git_fake_metadata')

DEFAULTS = {
    'config_dir': config_dir,
    'db_file': os.path.join(config_dir, 'db.sql'),
}

__all__ = ['DEFAULTS']
