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

    clv_partner_entity_contact_information_pattern_fields = \
        ['id', 'name', 'street_name', 'street_number', 'street2', 'district',
         'notes', 'active',
         'count_contact_information_pattern_matches'
         ]

    common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
    user_id = common.authenticate(db_name, username, password, {})
    models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)

    if user_id:

        search_domain = []
        clv_partner_entity_contact_information_pattern_objects = models.execute_kw(
            db_name, user_id, password,
            'clv.partner_entity.contact_information_pattern', 'search_read',
            [search_domain, clv_partner_entity_contact_information_pattern_fields],
            {}
        )
        clv_partner_entity_contact_information_pattern = pd.DataFrame(clv_partner_entity_contact_information_pattern_objects)

        for i, row in clv_partner_entity_contact_information_pattern.iterrows():

            if row['street2'] is False:
                clv_partner_entity_contact_information_pattern['street2'].values[i] = None

        conn = sqlite3.connect(sqlite3_db_name)

        if initialize:

            clv_partner_entity_contact_information_pattern.to_sql(
                'clv_partner_entity_contact_information_pattern', conn, if_exists='replace', index=False)

        else:

            cur = conn.cursor()
            cur.execute('DELETE FROM clv_partner_entity_contact_information_pattern')
            conn.commit()

            clv_partner_entity_contact_information_pattern.to_sql(
                'clv_partner_entity_contact_information_pattern', conn, if_exists='append', index=False)

        sql = '''
            UPDATE clv_partner_entity_contact_information_pattern
            SET notes = NULL
            WHERE notes = '0';
            '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        conn.close()

    _logger.info(u'%s %s %s %s', '-->', 'Execution time:', secondsToStr(time() - start), '\n')

    return clv_partner_entity_contact_information_pattern
