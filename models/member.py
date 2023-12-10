from odoo import api, fields, models
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta


class IndoorGames(models.Model):
    _name = "indoor.member"
    _inherit = []
    _description = "Indoor Games Management System Members"

    name = fields.Char(string='Name')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Char(string='Address')
    image = fields.Image(string="Image")
    website = fields.Char(string='Website')
    occupation = fields.Char(string='Occupation')
    language = fields.Char(string='Language')
    gender = fields.Selection([('male', "Male"), ('female', 'Female')], string='Gender')
    dob = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age")
    height = fields.Float(string="Height")
    weight = fields.Float(string="Weight")
    member_type = fields.Char(string='Member Type', default="None", readonly=1)
    membership_end_time = fields.Char(string="Membership Expirity Time", default="None", readonly=1)
    membership_status = fields.Boolean(string="Membership Status", compute="_get_status")
    # member_type = fields.Char(string='Member Type', default="None", readonly=1, compute="_get_mem_status")

    parent_o2m_players = fields.Many2one("indoor.event", string="Parent m2m players", invisible=1)

    def _get_mem_status(self):
        pass

    @api.depends('membership_end_time')
    def _get_status(self):
        if self.membership_end_time == "None":
            self.membership_status = False
        else:
            datetimeStart = self.membership_end_time +  " 12:00:00"
            datetime1 = datetime.strptime(datetimeStart, "%Y-%m-%d %H:%M:%S")
            today = date.today()

            if today > datetime1.date():
                self.membership_status = False
                self.member_name.member_type = "None"
            else:
                self.membership_status = True