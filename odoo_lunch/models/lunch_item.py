from odoo import fields, models


class LunchItem(models.Model):
    _name = "lunch.item"
    _description = "Lunch Item"

    ingredients = fields.Char(string="Ingredient")
    allergy_info = fields.Char(string="Allergy Information")
    category = fields.Selection(
        selection=[
            ("main_course", "Main Course"),
            ("side_dish", "Side Dish"),
            ("alternative", "Alternative"),
        ],
        default="main_course",
    )
    lunch_menu_id = fields.Many2one(
        comodel_name="lunch.menu",
        string="Lunch Menu",
        required=True,
        ondelete="cascade",
    )
