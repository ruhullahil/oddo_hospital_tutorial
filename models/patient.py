from odoo import api, fields, models, _, tools
from datetime import date
from odoo.exceptions import ValidationError


class salesUser(models.Model):
    _inherit = "sale.order"
    name_of_salers = fields.Char(string="sealer name")
    this_is_for_test = fields.Char(string=" this is test purpose")

    def just_use_for_test(self):
        print('just use for test work from order')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    company_type = fields.Selection(selection_add=[('om', 'Odoo Mates'), ('odoodev', 'Odoo Dev')])


class HospitalPatient(models.Model):

    def name_get(self):
        # name get function for the model executes automatically
        res = []
        for rec in self:
            res.append((rec.id, '%s - %s' % (rec.name, rec.p_id)))
        return res

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        domain = args + ['|', ('p_id', operator, name), ('name', operator, name)]
        return super(HospitalPatient, self).search(domain, limit=limit).name_get()

    def _cron_start(self):
        print("corn work")

    @api.constrains('date_of_bath')
    def age_validate(self):

        for single in self:
            birthDate = single.date_of_bath
            today = date.today()
            age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
            if age <= 1:
                raise ValidationError(_("enter correct date of bath"))

    @api.onchange('doctor_id')
    def set_doctor_gender(self):
        for single in self:
            single.doctor_gender = single.doctor_id.gender

    def send_patient_mail(self):
        print('send mail')
        template_id = self.env.ref('hospital.patient_card_email_send').id
        template = self.env['mail.template'].browse(template_id)
        lang = self.env.context.get('lang')
        # template.send_mail(self.id, force_send=True)
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "mail.mail_notification_paynow",
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            # 'model_description': self.with_context(lang=lang).type_name,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def action_code_call_patient(self):
        print('come action_code_call_patient ---->')
        return {
            'name': _('patient'),
            'domain': [],
            "view_mode": 'tree,form',
            'res_model': 'hospital.patient',
            'type': 'ir.actions.act_window',
            'view_id': False,

        }

    _name = 'hospital.patient'
    _description = ' ith sis for testing amad model name is hostipat patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string=' Name', required=True)
    date_of_bath = fields.Date(string='Date', required=True, index=False, readonly=False,
                               states={'draft': [('readonly', False)]},
                               default=fields.Date.context_today)
    address = fields.Char(string="Address ")
    email = fields.Char(string="Email")
    image = fields.Binary(string="Image", attachment=True)
    p_id = fields.Char(string='Patient Reference', required=True, copy=False, readonly=False,
                       states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female')], default='male', string="Gender")
    active = fields.Boolean("Active", default=True)
    users_id = fields.Many2one('res.users', string="PRO")
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")
    doctor_gender = fields.Selection([('male', 'Male'),
                                      ('female', 'Female')], default='male', string=" Doctor Gender")
    record_create_date = fields.Date(string="Record Create Date", required=True, default=fields.Date.context_today)

    def print_from_object(self):
        return self.env.ref('hospital.record_id').report_action(self)

    def print_excel_from_object(self):
        return self.env.ref('hospital.report_patient_card_xlsx').report_action(self)

    @api.depends('date_of_bath')
    def compute_age(self):

        for single in self:
            birthDate = single.date_of_bath
            today = date.today()
            age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
            if age >= 18:
                single.age_group = 'adult'

            else:
                single.age_group = 'not_adult'

    @api.depends('name')
    def compute_appointment(self):
        self.appointment_count = self.env['hospital.appintment'].search_count([('patient_name', '=', self.name)])

    age_group = fields.Selection([('adult', 'Adult'), ('not_adult', 'Not Adult')], string="age_group",
                                 compute=compute_age)
    appointment_count = fields.Integer(string="Appointment count", compute=compute_appointment)

    def open_pation_appointment(self):
        return {
            'name': _('Product Margins'),
            'domain': [('patient_name', '=', self.name)],
            "view_mode": 'tree,form',
            'res_model': 'hospital.appintment',
            'type': 'ir.actions.act_window',
            'view_id': False,

        }

    @api.model
    def create(self, vals):
        print("------------ : create called")
        if vals.get('p_id', _('New')) == _('New'):
            vals['p_id'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        result = super(HospitalPatient, self).create(vals)
        print(result)
        return result
