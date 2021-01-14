from odoo import models, api


class GenarateAllReport(models.AbstractModel):
    _name = 'report.hospital.generate_all_paint_report'
    _description = 'this is used for model extend patient_card'

    @api.model
    def _get_report_values(self, docids, data=None):
        print('docids __: ', docids)

        report = self.env['hospital.patient'].browse(docids)
        print('did : ', docids)

        return {

            'doc_model': 'hospital.patient',
            'docs': report,

        }
