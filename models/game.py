from odoo import api, fields, models

class IndoorGames(models.Model):
    _name = "indoor.game"
    _inherit = []
    _description = "Indoor Games Management System Games"

    name = fields.Char(string="Name")
    image = fields.Image(string="Image")
    charge_per_hour = fields.Char(string="Charge/hour")
    basic_partner_discount_percentage = fields.Char(string="Basic Partner Discount Percentage")
    gold_partner_discount_percentage = fields.Char(string="Gold Partner Discount Percentage")
    silver_partner_discount_percentage = fields.Char(string="Silver Partner Discount Percentage")
    delay_charge = fields.Char(string="Delay Charge")
    available = fields.Boolean(string="Available", default=True)
    