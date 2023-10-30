from odoo import fields, models

class ActionItem(models.Model):
    _name = 'action.item'

    title = fields.Char('Title')
    deskripsi = fields.Char(string='Deskripsi')
    target_date = fields.Date(
        string='Deadline Date',
        default=False,
    )

    open_date = fields.Date(
        string='Open Date',
        default=False,
    )

    close_date = fields.Date(
        string='Close Date',
        default=False,
    )
    status = fields.Selection(
        string='Tipe',
        selection=[
            ('open', 'Open'),
            ('on_progress', 'On Progress'),
            ('close', 'Close'),
        ],
        default='open'
    )

    Action_id = fields.Many2one(
        string='Action Id',
        comodel_name='finding.item'
    )