from odoo import http
from odoo.http import route, request

import qrcode
import io
import base64
from datetime import date

class LunchKioskController(http.Controller):
    @route('/lunch_kiosk', type='http', auth='public')
    def lunch_kiosk(self):
        # Get current date in yyyy-mm-dd format
        current_date_str = date.today().strftime('%Y-%m-%d')

        # Build target URL
        target_url = f"{request.httprequest.host_url}lunch_kiosk/check_in/{current_date_str}"
        
        # Generate QR code that points to "/test"
        qr = qrcode.QRCode(box_size=10, border=4)
        qr.add_data(target_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Convert QR image to base64
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()

        return request.render('odoo_lunch.lunch_kiosk_layout', {
            'qr_code': img_str,
        })

    @route('/lunch_kiosk/check_in/<string:check_in_date>', type='http', auth='user')
    def lunch_check_in(self, check_in_date, **kwargs):
        username = request.env.user.name

        # TODO set the user as checked-in in the backend

        return request.render('odoo_lunch.lunch_checked_in', {
            'username': username,
            'check_in_date': check_in_date,
        })
