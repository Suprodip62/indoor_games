from odoo import api, fields, models

class IndoorGames(models.Model):
    _name = "indoor.membership"
    _inherit = []
    _description = "Indoor Games Management System Membership"

    member_name = fields.Char(string="Name") # Many2one with indoor.member
    partner_type = fields.Selection([('basic', "Basic"), ('silver', 'Silver'), ('gold', "Gold")], string="Membership Type")
    membership_fees = fields.Integer(string="Fees", readonly=1) # onchange: basic-->100, silver-->200, gold-->300 times(*) 1 for 1 month, 2 for 2 month
    # membership_products = fields.One2many()
    membership_duration = fields.Selection([('1', "1 Month"), ('2', '2 Month'), ('3', "3 Month")], string="Duration")
    # membership_start_time = fields.Date(string="Start Time") --> cancel
    membership_end_time = fields.Date(string="End Time") # onchange: auto calculate from duration
