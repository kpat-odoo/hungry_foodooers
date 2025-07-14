from odoo import http
from odoo.http import route, request

import qrcode
import io
import base64
from datetime import date, datetime


class LunchKioskController(http.Controller):
    @route("/lunch_kiosk", type="http", auth="public")
    def lunch_kiosk(self):
        today = date.today()
        lunch_menu = request.env['lunch.menu'].sudo().search([
            ('date', '>=', datetime.combine(today, datetime.min.time())),
            ('date', '<=', datetime.combine(today, datetime.max.time())),
        ], limit=1)
        target_url = f"{request.httprequest.host_url}lunch_kiosk/check_in/{lunch_menu.id}"

        qr = qrcode.QRCode(box_size=10, border=4)
        qr.add_data(target_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buffer = io.BytesIO()
        img.save(buffer, bitmap_format="png")
        img_str = base64.b64encode(buffer.getvalue()).decode()

        return request.render(
            "odoo_lunch.lunch_kiosk_layout",
            {
                "qr_code": img_str,
            },
        )

    @route('/lunch_kiosk/check_in/<int:menu_id>', type='http', auth='user')
    def lunch_check_in(self, menu_id, **kwargs):
        username = request.env.user.name

        user_partner = request.env.user.partner_id

        menu = request.env['lunch.menu'].sudo().browse(menu_id)
        event = menu.event
        attendee = event.attendee_ids.filtered(lambda a: a.partner_id == user_partner)
        if not attendee or attendee.state != 'accepted':
            return request.render('odoo_lunch.lunch_checkin_error', {
                'username': username,
            })

        # TODO set the user as checked-in in the backend

        return request.render('odoo_lunch.lunch_checked_in', {
            'username': username,
            'menu_name': menu.name,
            'allergy_info': menu.allergy_info,
        })
