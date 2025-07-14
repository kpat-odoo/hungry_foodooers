from odoo import api, fields, models
from datetime import datetime, time

from dateutil.relativedelta import relativedelta
 

class LunchMenu(models.Model):
    _name = "lunch.menu"
    _description = "Lunch Menu"

    name = fields.Char(string="Menu Name", required=True)
    date = fields.Date(string="Menu Date", required=True)
    stage = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        string="Menu Stage",
        default="draft",
        required=True,
    )
    ingredients = fields.Text(string="Ingredient")
    allergy_info = fields.Char(string="Allergy Information")
    category = fields.Selection(
        selection=[
            ("main_course", "Main Course"),
            ("side_dish", "Side Dish"),
            ("alternative", "Alternative"),
        ],
        default="main_course",
    )

    image = fields.Binary(string="Meal")

    event = fields.Many2one("calendar.event", string="Calendar Event")

    accepted_count = fields.Integer(related="event.accepted_count", store=True)
    declined_count = fields.Integer(related="event.declined_count", store=True)
    awaiting_count = fields.Integer(related="event.awaiting_count", store=True)
    tentative_count = fields.Integer(related="event.tentative_count", store=True)

    is_all_week = fields.Boolean(string="For All Week", default=False)
    date_end = fields.Date(string="End Date", compute="_compute_end_date")

    @api.model_create_multi
    def create(self, vals_list):
        lunch_menu = super().create(vals_list)

        if lunch_menu.date:
            lunch_menu._create_calendar_event()

        return lunch_menu

    def write(self, vals):
        res = super().write(vals)

        for record in self:
            if "stage" in vals or "date" in vals or "name" in vals:
                record._create_calendar_event()
        return res

    def _create_calendar_event(self):
        """Creates or updates a calendar event for this lunch menu and invites all partners."""
        if self.stage == "draft" or not self.date:
            return

        start_dt = datetime.combine(self.date, time(9, 0))
        end_dt = datetime.combine(self.date_end, time(17, 0))

        all_partners = self.env["res.partner"].search([])

        event_vals = {
            "name": f"Lunch: {self.name}",
            "start": start_dt,
            "stop": end_dt,
            "allday": True,
            "partner_ids": [(6, 0, all_partners.ids)],
        }

        if self.event:
            self.event.write(event_vals)
        else:
            event = self.env["calendar.event"].create(event_vals)
            self.event = event.id

    @api.depends("is_all_week")
    def _compute_end_date(self):
        for menu in self:
            menu.date_end = menu.date + relativedelta(days=(4 - menu.date.weekday())) if menu.is_all_week else menu.date
