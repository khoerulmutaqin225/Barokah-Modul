
from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _update_picking_from_group_key(self, key):
        """The picking is updated with data from the grouping key.
        This method is designed for extensibility, so that other modules
        can store more data based on new keys."""
        super(StockPicking, self)._update_picking_from_group_key(key)
        for rec in self:
            for key_element in key:
                if (
                    "location_dest_id" in key_element.keys()
                    and key_element["location_dest_id"]
                ):
                    rec.location_dest_id = key_element["location_dest_id"]
        return False
