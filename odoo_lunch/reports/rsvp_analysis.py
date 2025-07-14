from odoo import fields, models


class LunchMenuRSVPReport(models.Model):
    _name = 'lunch.menu.rsvp.report'
    _auto = False  # SQL view

    menu_id = fields.Many2one('lunch.menu', string="Menu")
    response_status = fields.Selection([
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('awaiting', 'Awaiting'),
        ('tentative', 'Tentative'),
    ], string="RSVP Status")
    count = fields.Integer()
