from odoo import api, fields, models

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
    member_type = fields.Char(string='Member Type', default="None", readonly=1)
    # member_type = fields.Char(string='Member Type', default="None", readonly=1, compute="_get_mem_status")

    parent_o2m_players = fields.Many2one("indoor.event", string="Parent m2m players")

    def _get_mem_status(self):
        pass