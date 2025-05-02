# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

import images

from clvsol_odoo_client2.db import *

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


class CLVhealthJCAFB(object):

    def __init__(
        self,

        server='http://localhost:8069',
        super_user_pw='',

        CompanyName='CLVhealth-JCAFB',
        Company_image=images.Company_image,
        website='https://github.com/CLVsol',

        admin_user_pw='admin',
        admin_user_email='admin@clvsol.com',
        Administrator_image=images.Administrator_image,

        data_admin_user_name='Data Administrator',
        data_admin_user='data.admin',
        data_admin_user_pw='data.admin',
        data_admin_user_email='data.admin@clvsol.com',
        DataAdministrator_image=images.DataAdministrator_image,

        dbname='clvhealth_jcafb',

        lang='pt_BR',
        tz='America/Sao_Paulo',
        country='Brazil',

        demo_data=False,
        upgrade_all=False,
        modules_to_upgrade=[],
    ):

        self.server = server
        self.super_user_pw = super_user_pw

        self.CompanyName = CompanyName
        self.Company_image = Company_image
        self.website = website

        self.admin_user_pw = admin_user_pw
        self.admin_user_email = admin_user_email
        self.Administrator_image = Administrator_image

        self.data_admin_user_name = data_admin_user_name
        self.data_admin_user = data_admin_user
        self.data_admin_user_pw = data_admin_user_pw
        self.data_admin_user_email = data_admin_user_email
        self.DataAdministrator_image = DataAdministrator_image

        self.dbname = dbname

        self.lang = lang
        self.tz = tz
        self.country = country

        self.demo_data = demo_data
        self.upgrade_all = upgrade_all
        self.modules_to_upgrade = modules_to_upgrade

        self.db = DB(
            server=self.server,
            super_user_pw=self.super_user_pw,
            admin_user_pw=self.admin_user_pw,
            data_admin_user_pw=self.data_admin_user_pw,
            dbname=self.dbname,
            demo_data=self.demo_data,
            lang=self.lang,
            tz=self.tz,
            country=self.country
        )

    def install_upgrade_module(self, module, upgrade, group_name_list=[]):

        print('\n%s%s' % ('--> ', module))
        if module in self.modules_to_upgrade:
            new_module = self.db.module_install_upgrade(module, True)
        else:
            new_module = self.db.module_install_upgrade(module, upgrade)

        return new_module

    def install(self):

        global upgrade

        print('--> create_database()')
        newDB = self.db.create()
        if newDB:

            print('\n--> newDB: ', newDB)
            print('\n--> my_company_setup()')
            self.db.my_company_setup(self.CompanyName, self.website, self.Company_image)
            print('\n--> Administrator()')
            self.db.administrator_setup(self.admin_user_email, self.Administrator_image)
            print('\n--> data_administrator_user_setup()')
            self.db.data_administrator_user_setup(
                self.data_admin_user_name, self.data_admin_user_email, self.CompanyName,
                self.data_admin_user, self.data_admin_user_pw, self.DataAdministrator_image
            )

        else:

            print('\n--> newDB: ', newDB)
            print('\n--> my_company_setup()')
            self.db.my_company_setup(self.CompanyName, self.website, self.Company_image)
            print('\n--> Administrator()')
            self.db.administrator_setup(self.admin_user_email, self.Administrator_image)
            print('\n--> data_administrator_user_setup()')
            self.db.data_administrator_user_setup(
                self.data_admin_user_name, self.data_admin_user_email, self.CompanyName,
                self.data_admin_user, self.data_admin_user_pw, self.DataAdministrator_image
            )

            print('\n--> newDB: ', newDB)
            client = erppeek.Client(
                server=self.server,
                db=self.dbname,
                user='admin',
                password=self.admin_user_pw
            )
            print('\n--> Update Modules List"')
            IrModuleModule = client.model('ir.module.module')
            IrModuleModule.update_list()

        group_names = []

        # ############################################################################################
        #
        # Odoo Addons
        #
        # ############################################################################################

        self.install_upgrade_module('mail', False, group_names)

        self.install_upgrade_module('hr', False, group_names)

        self.install_upgrade_module('contacts', False, group_names)

        self.install_upgrade_module('base_address_extended', False, group_names)

        self.install_upgrade_module('survey', False, group_names)

        # ############################################################################################
        #
        # CLVsol l10n-brazil
        #
        # ############################################################################################

        self.install_upgrade_module('l10n_br_base', self.upgrade_all, group_names)

        self.install_upgrade_module('l10n_br_zip', self.upgrade_all, group_names)

        # ############################################################################################
        #
        # CLVsol Odoo Addons
        #
        # ############################################################################################

        # group_names = [
        #     'User (Base)',
        #     'Super User (Base)',
        #     'Annotation User (Base)',
        #     'Register User (Base)',
        #     'Log User (Base)',
        #     'Manager (Base)',
        #     'Super Manager (Base)',
        # ]
        self.install_upgrade_module('clv_base', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_phase', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_file_system', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_global_tag', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_set', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_pool', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_employee', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_employee_history', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_survey', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_event', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_document', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_document_survey', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_lab_test', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_lab_test_survey', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_partner_entity', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_residence', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_patient', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_patient_history', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_patient_rec', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_residence_history', self.upgrade_all, group_names)

        # ############################################################################################
        #
        # CLVsol Odoo Addons - JCAFB customizations
        #
        # # ############################################################################################

        self.install_upgrade_module('clv_base_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_employee_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_event_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_document_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_document_pool_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_lab_test_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_lab_test_pool_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_residence_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_residence_pool_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_patient_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_patient_pool_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_patient_rec_jcafb', self.upgrade_all, group_names)

        # ############################################################################################
        #
        # CLVsol Odoo Addons - Log
        #
        # ############################################################################################

        self.install_upgrade_module('clv_global_log', self.upgrade_all, group_names)

        # ############################################################################################
        #
        # CLVsol Odoo Addons - Log - JCAFB customizations
        #
        # ############################################################################################

        self.install_upgrade_module('clv_document_log_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_lab_test_log_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_partner_entity_log_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_residence_log_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_patient_log_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_patient_rec_log_jcafb', self.upgrade_all, group_names)

        # # # self.install_upgrade_module('clv_processing_log_jcafb', self.upgrade_all, group_names)

        # # # self.install_upgrade_module('clv_external_sync_log_jcafb', self.upgrade_all, group_names)

        # ############################################################################################
        #
        # CLVsol Odoo Addons - Summary
        #
        # # ############################################################################################

        self.install_upgrade_module('clv_summary', self.upgrade_all, group_names)

        # ############################################################################################
        #
        # CLVsol Odoo Addons - Summary - JCAFB customizations
        #
        # ############################################################################################

        self.install_upgrade_module('clv_summary_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_employee_summary_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_residence_summary_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_patient_summary_jcafb', self.upgrade_all, group_names)

        # ############################################################################################
        #
        # CLVsol Odoo Addons - Verification
        #
        # ############################################################################################

        self.install_upgrade_module('clv_verification', self.upgrade_all, group_names)

        # ############################################################################################
        #
        # CLVsol Odoo Addons - Verification - JCAFB customizations
        #
        # ############################################################################################

        self.install_upgrade_module('clv_verification_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_verification_log_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_partner_entity_verification_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_patient_rec_verification_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_residence_verification_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_patient_verification_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_lab_test_verification_jcafb', self.upgrade_all, group_names)

        # ############################################################################################
        #
        # CLVsol Odoo Addons - Export
        #
        # ############################################################################################

        self.install_upgrade_module('clv_export', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_document_export', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_lab_test_export', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_patient_export', self.upgrade_all, group_names)

        # ############################################################################################
        #
        # CLVsol Odoo Addons - Export - JCAFB customizations
        #
        # ############################################################################################

        self.install_upgrade_module('clv_export_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_document_export_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_lab_test_export_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_patient_export_jcafb', self.upgrade_all, group_names)

        # ############################################################################################
        #
        # CLVsol Odoo Addons - Process
        #
        # ############################################################################################

        self.install_upgrade_module('clv_processing', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_survey_process', self.upgrade_all, group_names)
        # PyYank installation failure.

        # ############################################################################################
        #
        # CLVsol Odoo Addons - Process - JCAFB customizations
        #
        # ############################################################################################

        self.install_upgrade_module('clv_processing_jcafb', self.upgrade_all, group_names)

        # ############################################################################################
        #
        # CLVsol Odoo Addons - Sync
        #
        # ############################################################################################

        self.install_upgrade_module('clv_external_sync', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_base_sync', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_phase_sync', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_file_system_sync', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_global_tag_sync', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_set_sync', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_employee_sync', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_employee_history_sync', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_survey_sync', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_event_sync', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_document_sync', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_document_survey_sync', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_lab_test_sync', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_lab_test_survey_sync', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_partner_entity_sync', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_residence_sync', self.upgrade_all, group_names)

        # # # self.install_upgrade_module('clv_residence_history_sync', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_patient_sync', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_patient_history_sync', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_patient_rec_sync', self.upgrade_all, group_names)

        # ############################################################################################
        #
        # CLVsol Odoo Addons - Sync - JCAFB customizations
        #
        # ############################################################################################

        self.install_upgrade_module('clv_external_sync_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_employee_sync_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_event_sync_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_document_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_document_log_sync_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_lab_test_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_lab_test_log_sync_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_lab_test_verification_sync_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_residence_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_residence_log_sync_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_residence_verification_sync_jcafb', self.upgrade_all, group_names)

        # # # self.install_upgrade_module('clv_residence_history_sync_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_patient_sync_jcafb', self.upgrade_all, group_names)

        # # self.install_upgrade_module('clv_patient_log_sync_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_patient_verification_sync_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_patient_rec_sync_jcafb', self.upgrade_all, group_names)

        # self.install_upgrade_module('clv_patient_rec_verification_sync_jcafb', self.upgrade_all, group_names)

        self.install_upgrade_module('clv_verification_sync_jcafb', self.upgrade_all, group_names)
