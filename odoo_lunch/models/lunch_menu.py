from odoo import fields, models, api
<<<<<<< Updated upstream

from datetime import datetime, time

=======
from dateutil.relativedelta import relativedelta
 
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
    event = fields.Many2one('calendar.event', string='Calendar Event')


    @api.model
    def create(self, vals):
        lunch_menu = super().create(vals)

        if lunch_menu.date:
            lunch_menu._create_calendar_event()

        return lunch_menu

    def write(self, vals):
        res = super().write(vals)

        for record in self:
            if 'date' in vals or 'name' in vals:
                record._create_calendar_event()
        return res

    def _create_calendar_event(self):
        """Creates or updates a calendar event for this lunch menu and invites all partners."""
        if not self.date:
            return

        start_dt = datetime.combine(self.date, time(9, 0))
        end_dt = datetime.combine(self.date, time(17, 0))

        all_partners = self.env['res.partner'].search([])

        event_vals = {
            'name': f"Lunch: {self.name}",
            'start': start_dt,
            'stop': end_dt,
            'allday': False,
            'partner_ids': [(6, 0, all_partners.ids)],
        }

        if self.event:
            self.event.write(event_vals)
        else:
            event = self.env['calendar.event'].create(event_vals)
            self.event = event.id

=======
    is_all_week = fields.Boolean(string="For All Week", default=False)
    date_end = fields.Date(string="End Date", compute="_compute_end_date")

    @api.depends("is_all_week")
    def _compute_end_date(self):
        for menu in self:
            menu.date_end = menu.date + relativedelta(days=(4 - menu.date.weekday())) if menu.is_all_week else menu.date
>>>>>>> Stashed changes
