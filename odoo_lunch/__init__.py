from . import models
from . import reports
from . import controllers
from odoo import api, SUPERUSER_ID


def create_rsvp_report_view(cr, registry):
    cr.execute("""
        CREATE OR REPLACE VIEW lunch_menu_rsvp_report AS (
            SELECT id as menu_id, 'accepted' as response_status, accepted_count as count FROM lunch_menu
            UNION ALL
            SELECT id, 'declined', declined_count FROM lunch_menu
            UNION ALL
            SELECT id, 'awaiting', awaiting_count FROM lunch_menu
            UNION ALL
            SELECT id, 'tentative', tentative_count FROM lunch_menu
        );
    """)
