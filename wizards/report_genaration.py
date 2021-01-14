from odoo import models, fields, _


class ReportGenaration(models.TransientModel):
    _name = 'hospital.generate.report'

    def print_patient_names(self):
        list_num = self.env['hospital.patient'].search(
            [('record_create_date', '>=', self.start_date), ('record_create_date', '<=', self.end_date)])
        print(list_num)
        id_list = []
        for single in list_num:
            print(single.id)
            id_list.append(single.id)
        print(id_list)
        return self.env.ref('hospital.generate_report_all').with_context(landscape=True).report_action(id_list)

    start_date = fields.Date(string='Start Date', required=True, default=fields.Date.context_today)
    end_date = fields.Date(string='End Date', required=True, default=fields.Date.context_today)
