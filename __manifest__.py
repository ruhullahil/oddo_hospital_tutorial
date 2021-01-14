# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'hospital',
    'version' : '1.0',
    'summary': 'hospitqal apps',
    'sequence': 10,
    'description': """test --- """,
    'category': 'others',
    'website': 'https://www.odoo.com/',
    'depends': ['mail','sale','website','board'],
    'data': ['security/security.xml',
             'security/ir.model.access.csv',
             'views/apointment_action.xml',
             'views/appointment.xml',
             'views/sale_order.xml',
             'views/template.xml',
             'report/report.xml',
             'report/genarate_report.xml',
             'wizards/create_appointment.xml',
             'wizards/report_genaration.xml',
             'data/patient_seq.xml',
             'report/patient_card.xml',
             'views/wbsite_template.xml',
             'views/settings.xml',
             'views/patient.xml',
             'views/doctor.xml',
             'views/dashboard.xml',
             'views/server_actions.xml',
             'views/menu.xml',
             'data/sequence.xml',
             'data/mail_template.xml',
             'data/corn.xml',
             'data/data.xml',






             ],


    'installable': True,
    'application': True,
    'auto_install': False,

}

