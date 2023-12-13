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
        for item in self:
            search_event_ids = item.env['indoor.event'].search([('event_start_time', '>', item.start_time), ('event_end_time', '<', item.end_time)])
            print("Search Event IDs: ", search_event_ids)

