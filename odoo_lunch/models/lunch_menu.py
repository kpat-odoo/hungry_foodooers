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
