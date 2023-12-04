from odoo import api, fields, models

class IndoorGames(models.Model):
    _name = "indoor.event"
    _inherit = []
    _description = "Indoor Games Management System Event"

    member_name = fields.Char(string="Name") # Many2one with indoor.member
    # member_name = fields.Many2one("indoor.member", string="Name")

    partner_type = fields.Char(string="Membership Type") # onchange: member_type
    # event_game = Many2one with indoor.game
    # event_players = Many2many with indoor.member
    # event_start_time
    # event_end_time
    # event_duration = selection-->1hr, 2hr, 3hr
    # bill = indoor.game-->charge/hour * event_duration + indoor.game-->indoor.partner_type discount percentage + tax
    # payment_status = paid/due-->boolean, checkbox, default-->due
