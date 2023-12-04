from odoo import api, fields, models
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

class IndoorGames(models.Model):
    _name = "indoor.event"
    _inherit = []
    _description = "Indoor Games Management System Event"
    _rec_name = "member_name"

    # member_name = fields.Char(string="Name") # Many2one with indoor.member
    member_name = fields.Many2one("indoor.member", string="Event Master")

    # partner_type = fields.Char(string="Membership Type") # onchange: member_name
    # partner_type = fields.Char(string="Membership Type", compute="_get_type") # skipped for now --> sol--> onchange not method
    

    # event_game = Many2one with indoor.game
    event_game = fields.Many2one("indoor.game", string="Event Game")

    # event_players = Many2many with indoor.member
    event_players = fields.One2many("indoor.member", "parent_o2m_players", string="Players")

    event_start_time = fields.Datetime(string="Start Time")
    # event_end_time = fields.Datetime(string="End Time")
    # event_duration = selection-->1hr, 2hr, 3hr
    event_duration = fields.Selection([('1', "1 Hour"), ('2', '2 Hour'), ('3', "3 Hour")], string="Duration")
    
    # event_satus = in hh hours, mm minutes-->Running-->Closed
    # event_status = fields.Boolean(string="Event Status", compute="_get_status")

    delay_hour = fields.Integer(string="Delay Hour", default=0)
    # bill = indoor.game-->charge/hour * event_duration + indoor.game-->indoor.partner_type discount percentage + tax
    subtotal = fields.Integer(string="Subtotal", default=0, readonly=1)
    discount = fields.Integer(string="Discount", default=0, readonly=1)
    delay_charge = fields.Integer(string="Delay Charge", default=0, readonly=1)
    tax = fields.Integer(string="Tax", default=0, readonly=1)
    bill = fields.Integer(string="Bill", compute="_get_bill")

    # payment_status = paid/due-->boolean, checkbox, default-->due
    payment_status = fields.Boolean(string="Payment Status")

    # @api.depends('partner_type', 'membership_duration')
    # def _get_type(self):
    #     for item in self:
    #         item.partner_type = item.member_name.partner_type

    @api.depends('event_game', 'event_duration')
    def _get_bill(self):
        for item in self:
            # item.bill = int(item.event_game.charge_per_hour) * int(item.event_duration)
            # item.bill = 100
            
            # show discount --> onchange: -->
            # discount = (int(item.event_game.charge_per_hour) * item.event_game.basic_partner_discount_percentage/100)

            item.subtotal = (int(item.event_game.charge_per_hour) * int(item.event_duration))
            if item.member_name.member_type == "None":
                item.discount = 0
            elif item.member_name.member_type == "Basic":
                item.discount = (int(item.event_game.charge_per_hour) * item.event_game.basic_partner_discount_percentage/100)   
            elif item.member_name.member_type == "Silver":
                item.discount = (int(item.event_game.charge_per_hour) * item.event_game.silver_partner_discount_percentage/100)  
            elif item.member_name.member_type == "Gold":
                item.discount = (int(item.event_game.charge_per_hour) * item.event_game.gold_partner_discount_percentage/100)
            # item.subtotal = (int(item.event_game.charge_per_hour) * int(item.event_duration)) - item.discount
            item.delay_charge = item.event_game.delay_charge * item.delay_hour
            item.tax = item.subtotal * 2/100
            item.bill = item.subtotal - item.discount + item.delay_charge + item.tax
             
            print("discount.............", item.discount)
            print("bill.............", (int(item.event_game.charge_per_hour) - item.discount) * int(item.event_duration) )




    # @api.depends('membership_end_time')
    # def _get_status(self):
    #     datetimeStart = self.membership_end_time +  " 12:00:00"
    #     datetime1 = datetime.strptime(datetimeStart, "%Y-%m-%d %H:%M:%S")
    #     now = datetime.now()
    #     current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

    #     if current_datetime > datetime1:
    #         self.membership_status = False
    #         self.member_name.member_type = None
    #     else:
    #         self.membership_status = True



# event close hole game ta available hobe
# membership expire hole member er type = None hobe