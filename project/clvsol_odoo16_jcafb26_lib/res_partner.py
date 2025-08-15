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

    res_partner_fields = ['id', 'name', 'type',
                          'street_name', 'street', 'street_number', 'street_number2', 'street2', 'district',
                          'zip', 'city_id', 'state_id', 'country_id',
                          'active'
                          ]

    common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
    user_id = common.authenticate(db_name, username, password, {})
    models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)

    if user_id:

        search_domain = []
        res_partner_objects = models.execute_kw(
            db_name, user_id, password,
            'res.partner', 'search_read',
            [search_domain, res_partner_fields],
            {}
        )
        res_partner = pd.DataFrame(res_partner_objects)

        res_partner.insert(res_partner.columns.get_loc("city_id") + 1, 'city', None)
        res_partner.insert(res_partner.columns.get_loc("state_id") + 1, 'country_state', None)
        res_partner.insert(res_partner.columns.get_loc("country_id") + 1, 'country', None)

        for i, row in res_partner.iterrows():

            if row['street_name'] is False:
                res_partner['street_name'].values[i] = None

            if row['street'] is False:
                res_partner['street'].values[i] = None

            if row['street_number'] is False:
                res_partner['street_number'].values[i] = None

            if row['street_number2'] is False:
                res_partner['street_number2'].values[i] = None

            if row['street2'] is False:
                res_partner['street2'].values[i] = None

            if row['zip'] is False:
                res_partner['zip'].values[i] = None

            if row['city_id']:
                res_partner['city_id'].values[i] = row['city_id'][0]
                res_partner['city'].values[i] = row['city_id'][1]
            else:
                res_partner['city_id'].values[i] = None

            if row['state_id']:
                res_partner['state_id'].values[i] = row['state_id'][0]
                res_partner['country_state'].values[i] = row['state_id'][1]
            else:
                res_partner['state_id'].values[i] = None

            if row['country_id']:
                res_partner['country_id'].values[i] = row['country_id'][0]
                res_partner['country'].values[i] = row['country_id'][1]
            else:
                res_partner['country_id'].values[i] = None

        conn = sqlite3.connect(sqlite3_db_name)

        if initialize:

            res_partner.to_sql('res_partner', conn, if_exists='replace', index=False)

        else:

            cur = conn.cursor()
            cur.execute('DELETE FROM res_partner')
            conn.commit()

            res_partner.to_sql('res_partner', conn, if_exists='append', index=False)

        sql = '''
            UPDATE res_partner
            SET district = NULL
            WHERE district = '0';
            '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        conn.close()

    _logger.info(u'%s %s %s %s', '-->', 'Execution time:', secondsToStr(time() - start), '\n')

    return res_partner
