from odoo import fields, models


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
    lunch_item_ids = fields.One2many(comodel_name="lunch.item", inverse_name="lunch_menu_id", string="Lunch Items")
