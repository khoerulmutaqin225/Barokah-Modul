from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from datetime import datetime
from datetime import timedelta
import base64
import io
from PIL import Image

from odoo.http import content_disposition, request

_STATES = [
    ("open", "Open"),
    ("on_progress", "On Progress"),
    ("close", "Close")
]
class VisitManagement(models.Model):
    _name = "visit.management"
    _inherit = 'mail.thread'

    def button_open(self):
        return self.write({"state": "open"})

    def button_on_progress(self):
        return self.write({"state": "on_progress"})
    def button_close(self):
        return self.write({"state": "close"})

    name = fields.Char(
        string='Name',
        required=True,
    )

    state = fields.Selection(
        selection=_STATES,
        string="Status",
        index=True,
        track_visibility="onchange",
        required=True,
        copy=False,
        default="open",
    )

    @api.depends('image_1920')
    def _compute_image_64(self):
        for template in self:
            if template.image_1920:
                template.image_1920 = self._compress_image(template.image_1920)

    def _set_image_64(self):
        for template in self:
            if template.image_1920:
                template.image_1920 = self._compress_image(template.image_1920)

    def _compress_image(self, image_data):
        # Decode the image data from base64
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))

        # Compress the image
        compressed_image = io.BytesIO()
        image.save(compressed_image, format='JPEG', optimize=True, quality=60)

        # Encode the compressed image data to base64
        return base64.b64encode(compressed_image.getvalue())

    image_1920 = fields.Binary("Image", compute='_compute_image_64', inverse='_set_image_64', store=True)

    document = fields.Binary(string="Document")

    vendor = fields.Many2one(
        'bpg.additional.vendor',
        string='Vendor',
        required=False)

    date = fields.Date(
        string='Release Date',
        required=True,
    )

    lokasi = fields.Char(
        string='Lokasi',
        required=False,
    )

    latitude = fields.Char(
        'Latitude',
        required=False)

    longitude = fields.Char(
        'Longitude',
        required=False,
    )

    vessel_id = fields.Many2one('shipping.vessel', string='Kapal', required=False)

    type_vessel = fields.Many2one(string="Type Vessel", readonly=True, related="vessel_id.type_id", store=True, )

    fleet = fields.Selection(
        string='Fleet',
        selection=[('fleet1', 'Fleet 1'), ('fleet2', 'Fleet 2'), ('fleet3', 'Fleet 3'),
                   ('fleet4', 'Fleet 4'), ('fleet5', 'Fleet 5'), ('fleet6', 'Fleet 6'), ('fleet7', 'Fleet 7')],
        readonly=True,
        # related="vessel_id.fleet",
        store=True,
    )
    


    open_date = fields.Datetime(
        string='Open Date',
        default=False,
    )

    close_date = fields.Datetime(
        string='Close Date',
        default=False,
    )

    deadline_date = fields.Datetime(
        string='Deadline Date',
        default=False,
    )

    @api.depends('open_date','deadline_date')
    def _compute_date_difference(self):
        difference = 0
        for record in self:
            if record.open_date and record.deadline_date:
                dt_1 = fields.Datetime.from_string(record.open_date)
                dt_2 = fields.Datetime.from_string(record.deadline_date)
                difference = (dt_2 - dt_1).days
                record.update({'sisa_waktu':difference})
            else:
                record.update({'sisa_waktu':difference})

    sisa_waktu = fields.Integer(
        compute='_compute_date_difference',
        string='Sisa Waktu',
        store=True,
    )

    pic = fields.Many2one(
        'bpg.additional.pic',
        string='PIC',
        required=False)

    tipe_kunjungan = fields.Selection(
        string='Tipe Kunjungan',
        selection=[
            ('visit', 'Visit'),
            ('perbaikan', 'Perbaikan Kapal'),
            ('vetting', 'Vetting'),
            ('vettingPlus', 'Vetting Plus'),
            ('negativeFeedback', 'Negative Feedback'),
            ('selfAssesment', 'Self Assesment'),
            ('toolBoxMeeting', 'Tool Box Meeting'),
        ],
        default='visit'
    )

    metode_rapat = fields.Selection(
        string='Metode Rapat',
        selection=[
            ('offline', 'Offline'),
            ('online', 'Online'),
        ],
        default='offline'
    )

    jenis_rapat = fields.Selection(
        string='Jenis Rapat',
        selection=[
            ('internal', 'Internal'),
            ('eksternal', 'Eksternal'),
        ],
        default='internal'
    )

    divisi_id = fields.Many2one(
        'hr.department',
        string='Divisi',
        track_visibility='onchange'
    )

    catatan = fields.Text(
        'catatan',
        required=False,
        track_visibility='onchange'
    )

    anggota_id = fields.One2many(
        'anggota.visit', 'group_anggota_visit_id',
        string="Group Stock Cargo Report",
        required=False,
    )

    count_anggota = fields.Integer(
        compute='_compute_count_anggota',
        string='Jumlah Anggota',
        store=True,
    )

    @api.depends('anggota_id')
    def _compute_count_anggota(self):
        for record in self:
            if not record.anggota_id:
                record.count_anggota = 0
            else:
                record.count_anggota = len(record.anggota_id)


    kunjungan_line = fields.One2many(
        'vetting.report.line', 'group_visit_id',
        string="Group Visit Report",
        required=False,
    )

    meeting_line = fields.One2many(
        'meeting.line', 'group_visit_id',
        string="Group Visit Report",
        required=False,
    )

class AnggotaVisitManagement(models.Model):
    _name = "anggota.visit"

    name = fields.Many2one(
        'bpg.additional.pic',
        string='Nama',
        required=False)

    jabatan = fields.Char(
        string='Jabatan',
        required=False)

    group_anggota_visit_id = fields.Many2one(
        'visit.management',
        string='Group Anggota Visit',
        readonly=True,
        index=True,
        auto_join=True,
    )