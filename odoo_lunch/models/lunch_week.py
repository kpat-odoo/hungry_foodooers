from odoo import fields, models


class LunchWeek(models.Model):
    _name = "lunch.week"
    _description = "Holds menus for each week"

    name = fields.Char(string="Name", required=True)
    date_start = fields.Date(string="Week start date")
    date_end = fields.Date(string="Week end date")
    stage = fields.Selection(
        selection=[("draft", "Draft"), ("confirmed", "Confirmed"), ("posted", "Posted"), ("cancel", "Cancelled")],
        default="draft",
        string="Stage",
    )
    menu_ids = fields.Many2many(string="Menus", comodel_name="lunch.menu")

    def action_send_rsvp_email(self):
        template_id = self.env.ref('odoo_lunch.rsvp_reminder', raise_if_not_found=False)
        for record in self:
            template_id.send_mail(record.id, force_send=True)
