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


def get_sqlite(server_url, db_name, username, password, sqlite3_db_name,
               clv_patient_category,
               clv_patient_marker,
               clv_patient_tag,
               initialize=False
               ):

    start = time()

    _logger.info(u'%s %s %s %s', '-->', 'get_sqlite', server_url, db_name)

    clv_patient_fields = ['id', 'name', 'code', 'gender', 'birthday', 'phase_id',
                          'address_name', 'street', 'street_name', 'street_number', 'street2', 'street_number2', 'district',
                          'zip', 'city_id', 'state_id', 'country_id',
                          'mobile', 'email', 'category_ids', 'marker_ids', 'tag_ids',
                          'active'
                          ]

    common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
    user_id = common.authenticate(db_name, username, password, {})
    models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)

    if user_id:

        search_domain = []
        clv_patient_objects = models.execute_kw(
            db_name, user_id, password,
            'clv.patient', 'search_read',
            [search_domain, clv_patient_fields],
            {}
        )
        clv_patient = pd.DataFrame(clv_patient_objects)
        clv_patient.insert(clv_patient.columns.get_loc("phase_id") + 1, 'phase', None)
        clv_patient.insert(clv_patient.columns.get_loc("city_id") + 1, 'city', None)
        clv_patient.insert(clv_patient.columns.get_loc("state_id") + 1, 'country_state', None)
        clv_patient.insert(clv_patient.columns.get_loc("country_id") + 1, 'country', None)
        clv_patient.insert(clv_patient.columns.get_loc("category_ids") + 1, 'categories', None)
        clv_patient.insert(clv_patient.columns.get_loc("marker_ids") + 1, 'markers', None)
        clv_patient.insert(clv_patient.columns.get_loc("tag_ids") + 1, 'tags', None)

        for i, row in clv_patient.iterrows():

            if row['phase_id']:
                clv_patient['phase_id'].values[i] = row['phase_id'][0]
                clv_patient['phase'].values[i] = row['phase_id'][1]
            else:
                clv_patient['phase_id'].values[i] = None

            if not row['street_name']:
                clv_patient['street_name'].values[i] = None

            if not row['street_number']:
                clv_patient['street_number'].values[i] = None

            if not row['street_number2']:
                clv_patient['street_number2'].values[i] = None

            if not row['street2']:
                clv_patient['street2'].values[i] = None

            if row['zip'] is False:
                clv_patient['zip'].values[i] = None

            if row['city_id']:
                clv_patient['city_id'].values[i] = row['city_id'][0]
                clv_patient['city'].values[i] = row['city_id'][1]
            else:
                clv_patient['city_id'].values[i] = None

            if row['state_id']:
                clv_patient['state_id'].values[i] = row['state_id'][0]
                clv_patient['country_state'].values[i] = row['state_id'][1]
            else:
                clv_patient['state_id'].values[i] = None

            if row['country_id']:
                clv_patient['country_id'].values[i] = row['country_id'][0]
                clv_patient['country'].values[i] = row['country_id'][1]
            else:
                clv_patient['country_id'].values[i] = None

            if row['category_ids'] != []:
                clv_patient['category_ids'].values[i] = str(row['category_ids'])
                categories = False
                category_ids = row['category_ids']
                for val in category_ids:
                    index = clv_patient_category.id[clv_patient_category.id == val].index.tolist()[0]
                    if categories is False:
                        categories = clv_patient_category.at[index, 'name']
                    else:
                        categories = categories + ';' + clv_patient_category.at[index, 'name']
                clv_patient['categories'].values[i] = categories
            else:
                clv_patient['category_ids'].values[i] = None

            if row['marker_ids'] != []:
                clv_patient['marker_ids'].values[i] = str(row['marker_ids'])
                markers = False
                marker_ids = row['marker_ids']
                for val in marker_ids:
                    index = clv_patient_marker.id[clv_patient_marker.id == val].index.tolist()[0]
                    if markers is False:
                        markers = clv_patient_marker.at[index, 'name']
                    else:
                        markers = markers + ';' + clv_patient_marker.at[index, 'name']
                clv_patient['markers'].values[i] = markers
            else:
                clv_patient['marker_ids'].values[i] = None

            if row['tag_ids'] != []:
                clv_patient['tag_ids'].values[i] = str(row['tag_ids'])
                tags = False
                tag_ids = row['tag_ids']
                for val in tag_ids:
                    index = clv_patient_tag.id[clv_patient_tag.id == val].index.tolist()[0]
                    if tags is False:
                        tags = clv_patient_tag.at[index, 'name']
                    else:
                        tags = tags + ';' + clv_patient_tag.at[index, 'name']
                clv_patient['tags'].values[i] = tags
            else:
                clv_patient['tag_ids'].values[i] = None

        conn = sqlite3.connect(sqlite3_db_name)

        if initialize:

            clv_patient.to_sql('clv_patient', conn, if_exists='replace', index=False)

        else:

            cur = conn.cursor()
            cur.execute('DELETE FROM clv_patient')
            conn.commit()

            clv_patient.to_sql('clv_patient', conn, if_exists='append', index=False)

        sql = '''
            UPDATE clv_patient
            SET district = NULL
            WHERE district = '0';
            '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        sql = '''
            UPDATE clv_patient
            SET mobile = NULL
            WHERE mobile = '0';
            '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        sql = '''
            UPDATE clv_patient
            SET email = NULL
            WHERE email = '0';
            '''
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        conn.close()

    _logger.info(u'%s %s %s %s', '-->', 'Execution time:', secondsToStr(time() - start), '\n')

    return clv_patient
