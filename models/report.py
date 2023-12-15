from odoo import api, fields, models
from datetime import date
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class IndoorGames(models.TransientModel):
    _name = "indoor.report"
    _description = "Indoor Games Management System Report"

    start_time = fields.Datetime(string="Start Time")
    end_time = fields.Datetime(string="End Time")

    def action_search(self):
        search_event_ids = self.env['indoor.event'].search([('event_start_time', '>', self.start_time), ('event_end_time', '<', self.end_time)])
        print("Search Event IDs: ", search_event_ids)



        return self.env.ref("indoor.action_report_event_summary").report_action(search_event_ids)



    def action_search_with_data(self):
        search_event_ids = self.env['indoor.event'].search([('event_start_time', '>', self.start_time), ('event_end_time', '<', self.end_time)])
        
        data_line = list()
        for item in search_event_ids:
            data_line.append((item.event_game.name,item.member_name.name,item.event_start_time))

        datas = {
            'start_date': self.start_time,
            'end_date': self.end_time,
            'data_line': data_line,
        }

        return self.env.ref("indoor.action_report_event_summary_with_data").report_action([], data=datas)


        # {
        #     'data_line': [(game, master, date),(game, master, date)],
        # }

        # {
        #     'data_line': [
        #                     {
        #                         'game': game,
        #                         'master': master,
        #                         'date': date
        #                     },
        #                     {
        #                         'game': game,
        #                         'master': master,
        #                         'date': date
        #                     },
        #                 ]
        # }