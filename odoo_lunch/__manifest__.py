{
    "name": "Buffalo Lunch App",
    "description": """
    This module implements changes as specified below.
        * 
    - Developer: Thy (natl), Junqi (juwu), Keya Patel (kpat)
    """,
    "category": "Custom Development",
    "version": "1.1.0",
    "author": "Odoo Development Services",
    "maintainer": "Odoo Development Services",
    "website": "https://www.odoo.com",
    "license": "OPL-1",
    "depends": ["website", "calendar", "event", "base"],
    "data": [
        "security/odoo_lunch_security.xml",
        "security/ir.model.access.csv",
        "views/odoo_lunch_menus.xml",
        "views/lunch_menu_views.xml",
        "views/lunch_week_views.xml",
    ],
    "application": True,
    "installable": True,
}
