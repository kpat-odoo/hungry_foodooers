from odoo import http
from odoo.http import route, request


class LunchKioskController(http.Controller):
    @route('/lunch_kiosk', auth='user')
    def lunch_kiosk(self):
        return request.render('odoo_lunch.lunch_kiosk_layout')
