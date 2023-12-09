from odoo import api, fields, models
from datetime import date
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


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
    # event_game = fields.Many2one("indoor.game", string="Event Game", domain=[('indoor_membership.partner_type', '=', 'Basic')])
    event_game = fields.Many2one("indoor.game", string="Event Game")

    # event_players = Many2many with indoor.member
    event_players = fields.One2many("indoor.member", "parent_o2m_players", string="Players")

    event_start_time = fields.Datetime(string="Start Time")
    # event_duration = selection-->1hr, 2hr, 3hr
    event_duration = fields.Selection([('1', "1 Hour"), ('2', '2 Hour'), ('3', "3 Hour")], string="Duration")


    # @api.depends('event_start_time', 'event_duration')
    # def _get_end_date(self):
        # for item in self:
            # item.event_end_time = item.event_start_time + timedelta(hours=int(item.event_duration))
    event_end_time = fields.Datetime(string="End Time")
    # event_end_time = fields.Datetime(string="End Time", compute="_get_end_date")

    
    # event_satus = in hh hours, mm minutes-->Running-->Closed
    # event_status = fields.Boolean(string="Event Status", compute="_get_status")

    delay_hour = fields.Integer(string="Delay Hour", default=0)
    # bill = indoor.game-->charge/hour * event_duration + indoor.game-->indoor.partner_type discount percentage + tax
    subtotal = fields.Integer(string="Subtotal", default=0, readonly=1)
    discount = fields.Integer(string="Discount", default=0, readonly=1)
    delay_charge = fields.Integer(string="Delay Charge", default=0, readonly=1)
    tax = fields.Integer(string="Tax", default=0, readonly=1)
    bill = fields.Integer(string="Bill", compute="_get_bill")

    payment_method = fields.Selection([('cash', "Cash"), ('bkash', "bKash")], string="Payment Method")
    # payment_status = paid/due-->boolean, checkbox, default-->due
    payment_status = fields.Boolean(string="Payment Status")

    # @api.depends('partner_type', 'membership_duration')
    # def _get_type(self):
    #     for item in self:
    #         item.partner_type = item.member_name.partner_type


    def search_games(self):
        # search_game_ids = self.env['indoor.event'].search([('event_game', '=', self.event_game.name)])
        # for item in search_game_ids:
            # if (item.event_start_time < self.event_start_time < item.event_end_time) or (item.event_start_time < self.event_end_time < item.event_end_time):
            #     raise UserError("The game is not availabe")
            # print("Name: ", item.member_name.name, "        Type: ", item.event_game.name)
            # print("Event Start: ", item.event_start_time, "        Event End: ", item.event_end_time)
        # print("Start Time: ", self.event_start_time, "        End Time: ", self.event_end_time)
        print(type(self.event_start_time))
    @api.onchange('event_start_time','event_duration')
    def onchange_event_start_duration(self,):
        for item in self:
            print("type of event_start_time", type(item.event_start_time))
            print("event_start_time", item.event_start_time)
            print("event_duration", item.event_duration)


            if item.event_start_time == False or item.event_duration == False: # not None
                item.event_end_time = False # not None
            else:
                item.event_end_time = item.event_start_time + timedelta(hours=int(item.event_duration))
            print("Type of timedelta: ", type(timedelta(hours=int(item.event_duration))))


            print("Event Start Time", item.event_start_time)
            print("Event End Time", item.event_end_time)
            if item.event_start_time != False and item.event_end_time != False:
                search_game_ids = item.env['indoor.event'].search([('event_game', '=', item.event_game.name)])
                cnt = 0
                for rec in search_game_ids:
                    print("cnt-->", cnt, "Event Member Name-->", rec.member_name.name)
                    cnt += 1
                    print("Final-->", item.event_start_time)
                    print("Final-->", item.event_end_time)
                    print("Final-->", rec.event_start_time)
                    print("Final-->", rec.event_end_time)

                    # if (type(item.event_start_time) != type(True)) and (type(item.event_end_time) != type(True) ) and ((rec.event_start_time < item.event_start_time < rec.event_end_time) or (rec.event_start_time < item.event_end_time < rec.event_end_time)):
                        # raise UserError("The game is not availabe")
                    if (rec.event_start_time < item.event_start_time < rec.event_end_time) or (rec.event_start_time < item.event_end_time < rec.event_end_time):
                        raise UserError("The game is not availabe")
            else:
                print("Datetime True/False")
            


    @api.depends('event_game', 'event_duration')
    def _get_bill(self):
        cnt = 0
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
            
            
            print("cnt-->", cnt, "Event Master-->", item.member_name.name, "Event Game-->", item.event_game.name)
            print("Duration-->", item.event_duration, "Bill-->", item.bill)
            cnt += 1
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




# event create hole select kora game er status unavailable hobe. event close hole game ta available hobe. ekhane start_time
  # end_time both indoor.game model e set korte hobe.
  # button click korle function call korbe and oi function e custom sql query lekha thakbe jar maddhome indoor.membership model e
    # ei start_time and end_time e ei game available or not find out korbe.
    # button click er age event_game, start_time, end_time choose korte hobe.

# membership expire hole member er type = None hobe --> done
# at a time multiple membership e thaka jabe na --> member_name select korar pore onchange e available or not dekhabe-no-->domain-->done
  # onchange e field e availabe ashle then etar onchange e baki field gulo show korbe age hidden thakbe.
# not only the type of variable but also the end time will be passed to the indoor.member --> done
# cancel membership
# event calculate korar age check expirity of membership
# event e all game dekhacche. but member je game e membership niyeche check kore only segulor upor discount calculate hobe.
  # er jonne membership create korar smy select kora game gulu o indoor.member model e pathate hobe.
  # or membership theke game selection bad dibo.
# membership neyar smy check prev membership expired or not(membership_status == False, member_type==None)
# indoor.member e parent m2m players --> force show --> form view id same with indoor.member --> done
# indoor.member e notebook e membership history, event history, players/participation history, transaction history
# game quantity, purchase--> vendor
# settings --> inherite tree view
# create new type of membership

# static --> onno obj change korle sobar jonne change hoye jabe so not possible
