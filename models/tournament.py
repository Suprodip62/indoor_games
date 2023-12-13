from odoo import api, fields, models
from datetime import date
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class IndoorGames(models.Model):
    _name = "indoor.tournament"
    _inherit = []
    _description = "Indoor Games Management System Tournament"
    _rec_name = "member_name"

    member_name = fields.Many2one("indoor.member", string="Event Master")    
    tournament_start_time = fields.Datetime(string="Start Time")
    tournament_duration = fields.Selection([('1', "1 Hour"), ('2', '2 Hour'), ('3', "3 Hour")], string="Duration")
    state = fields.Selection([('draft',"Draft"),('confirm',"Confirm"),('cancel',"Cancel")], string="Status")

    tournament_end_time = fields.Datetime(string="End Time")
    # state = fields.Selection([('draft',"Draft"),('confirm',"Confirm"),('cancel',"Cancel")], string="Status")

    record_line_ids = fields.One2many("indoor.event", "tournament_id", string="Tournament")
    subtotal = fields.Integer(string="Subtotal", compute="_get_subtotal")
    discount = fields.Integer(string="Discount", compute="_get_discount")
    participation_discount = fields.Integer(string="Discount", compute="_get_participation_discount")
    tax = fields.Integer(string="Discount", compute="_get_tax")
    bill = fields.Integer(string="Bill", compute="_get_bill")

    # tournament_paid_amount = fields.Integer(string="Paid", compute="_get_tournament_paid_amount")
    # tournament_due_amount = fields.Integer(string="Due", compute="_get_tournament_due_amount")

    def _get_subtotal(self):
        for rec in self:
            sum = 0
            for item in rec.record_line_ids:
                sum += item.subtotal
            rec.subtotal = sum
    def _get_discount(self):
        for item in self:
            item.discount = 0
    def _get_participation_discount(self):
        for item in self:
            item.participation_discount = 0
    def _get_tax(self):
        for item in self:
            item.tax = 0
    def _get_bill(self):
        for item in self:
            item.bill = item.subtotal - item.discount - item.participation_discount + item.tax
    def button_confirm(self):
        self.write({
           'state': "confirm"
        })
        print("......id.....", self.id)
        return {'name' : 'Transaction',
            'type' : 'ir.actions.act_window',
            'res_model' : 'indoor.transaction',
            'view_mode' : 'form',
            'target' : 'new',
            # 'target' : 'current',
            # 'target' : 'main',
            'context' : {'member_name' : self.member_name.name, 
                         'event_id' : "tournament-"+str(self.id),
                        #  'event_game' : self.event_game.name, 
                        #  'event_game_id' : self.event_game_id,
                         'event_start_time' : self.tournament_start_time,
                         'event_duration' : self.tournament_duration,
                         'event_end_time' : self.tournament_end_time,
                         'subtotal' : self.subtotal,
                         'discount' : self.discount,
                         'participation_discount' : self.participation_discount,
                         'tax' : self.tax,
                         'bill' : self.bill
                        }
            # 'domain' : [('patient_id', '=', self.id)]
        }
    def button_cancel(self):
        pass
    