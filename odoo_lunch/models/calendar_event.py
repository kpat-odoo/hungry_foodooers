from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import timedelta

class MyCalendarEvent(models.Model):
    _inherit = 'calendar.event'

    def change_attendee_status(self, status, recurrence_update_setting):
        config = self.env['ir.config_parameter'].sudo()
        lockout_days_str = config.get_param('rsvp_lockout_days')
        
        try:
            lockout_days = int(lockout_days_str)
        except ValueError:
            lockout_days = 7

        for event in self:
            if (
                lockout_days > 0
                and event.start
                and event.start <= fields.Datetime.now() + timedelta(days=lockout_days)
            ):
                raise ValidationError(
                    f"The last day to change your RSVP status for this lunch has passed! "
                    f"Please contact KEHU directly to change your status."
                )

        return super().change_attendee_status(status, recurrence_update_setting)

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    rsvp_lockout_days = fields.Integer(
        string="RSVP Lock-Out Period (Days)",
        config_parameter='rsvp_lockout_days',
        help="Number of days before the event when attendees can no longer change their RSVP status. Leave blank or 0 to disable lock-out."
    )