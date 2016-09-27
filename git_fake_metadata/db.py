# -*- coding: utf-8 -*-

import sqlite3
import re

from .defaults import DEFAULTS


def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None


class DB:
    _CURRENT_DB_VERSION = '0.1.0'
    _DB_DETECT_TYPES = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES

    def __init__(
        self,
        db_file=DEFAULTS['db_file'],
    ):

        self._db_file = db_file

        self._init_db()

    def _init_db(self):

        schema_filename = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'data',
            'db_schema.sql',
        )

        db_is_new = not os.path.exists(self._db_file)

        with sqlite3.connect(self._db_file) as con:
            if db_is_new:
                with open(schema_filename, 'rt') as fh:
                    con.executescript(fh.read())
                con.execute('INSERT INTO version (version) VALUES ("{}")'.format(
                    self._CURRENT_DB_VERSION,
                ))
                con.commit()
            else:
                cur = con.cursor()
                cur.execute('SELECT version FROM version')
                version = cur.fetchone()[0]
                if version != self._CURRENT_DB_VERSION:
                    raise Exception(
                        "DB schema mismatch."
                        " DB upgrade not yet implemented."
                        " Please delete your DB or implement upgrade."
                    )

    def _update_last_action_timestamp(self, timestamp):
        with sqlite3.connect(self._db_file, detect_types=self._DB_DETECT_TYPES) as con:
            cur = con.cursor()
            cur.execute(
                'SELECT COUNT(*) from last_action WHERE vcs_repo_path=?', (
                    self._repo_dir,
                )
            )
            if cur.fetchone()[0] == 0:
                cur.execute(
                    'INSERT INTO last_action (vcs_repo_path, timestamp) VALUES(?, ?)', (
                        self._repo_dir,
                        timestamp,
                    )
                )
            else:
                cur.execute(
                    'UPDATE last_action SET timestamp=? WHERE vcs_repo_path=?', (
                        self._repo_dir,
                        timestamp,
                    )
                )

    def _get_last_action_timestamp(self, start_date):

        plausible_metadata_compared_to_repo = self._config_get('plausible_metadata_compared_to_repo')

        if plausible_metadata_compared_to_repo == 'none':
            return start_date

        with sqlite3.connect(self._db_file, detect_types=self._DB_DETECT_TYPES) as con:
            con.create_function("REGEXP", 2, regexp)
            cur = con.cursor()
            if plausible_metadata_compared_to_repo == 'self':
                cur.execute(
                    'SELECT timestamp FROM last_action WHERE vcs_repo_path=?', (
                        self._repo_dir,
                    )
                )
            else:
                cur.execute(
                    '''
                    SELECT timestamp FROM last_action
                    WHERE timestamp = (SELECT MAX(timestamp)
                        FROM last_action
                        WHERE vcs_repo_path REGEXP ?)
                    ''', (
                        self._repo_dir,
                    )
                )
            row = cur.fetchone()

        if row:
            return row[0]
        else:
            return None
