# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from xmlrpc import client
import pandas as pd
import sqlite3
from time import time
from datetime import timedelta

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


def secondsToStr(t):
    return str(timedelta(seconds=t))


def get_sqlite(server_url, db_name, username, password, sqlite3_db_name, initialize=False):

    start = time()

    _logger.info(u'%s %s %s %s', '-->', 'get_sqlite', server_url, db_name)

    res_users_fields = ['id', 'name', 'partner_id', 'company_id', 'parent_id', 'tz', 'lang', 'country_id',
                        'login', 'password', 'active', 'image_1920']

    common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
    user_id = common.authenticate(db_name, username, password, {})
    models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)

    if user_id:

        search_domain = []
        res_users_objects = models.execute_kw(
            db_name, user_id, password,
            'res.users', 'search_read',
            [search_domain, res_users_fields],
            {}
        )
        res_users = pd.DataFrame(res_users_objects)
        res_users.insert(res_users.columns.get_loc("partner_id") + 1, 'partner', None)
        res_users.insert(res_users.columns.get_loc("company_id") + 1, 'company', None)
        res_users.insert(res_users.columns.get_loc("parent_id") + 1, 'parent', None)
        res_users.insert(res_users.columns.get_loc("country_id") + 1, 'country', None)

        for i, row in res_users.iterrows():

            if row['partner_id']:
                res_users['partner_id'].values[i] = row['partner_id'][0]
                res_users['partner'].values[i] = row['partner_id'][1]
            else:
                res_users['partner_id'].values[i] = None

            if row['company_id']:
                res_users['company_id'].values[i] = row['company_id'][0]
                res_users['company'].values[i] = row['company_id'][1]
            else:
                res_users['company_id'].values[i] = None

            if row['parent_id']:
                res_users['parent_id'].values[i] = row['parent_id'][0]
                res_users['parent'].values[i] = row['parent_id'][1]
            else:
                res_users['parent_id'].values[i] = None

            if row['country_id']:
                res_users['country_id'].values[i] = row['country_id'][0]
                res_users['country'].values[i] = row['country_id'][1]
            else:
                res_users['country_id'].values[i] = None

        conn = sqlite3.connect(sqlite3_db_name)

        if initialize:

            res_users.to_sql('res_users', conn, if_exists='replace', index=False)

        else:

            cur = conn.cursor()
            cur.execute('DELETE FROM res_users')
            conn.commit()

            res_users.to_sql('res_users', conn, if_exists='append', index=False)

        conn.close()

    _logger.info(u'%s %s %s %s', '-->', 'Execution time:', secondsToStr(time() - start), '\n')

    return res_users
