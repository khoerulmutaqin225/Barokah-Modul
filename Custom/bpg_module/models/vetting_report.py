
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from datetime import datetime
from datetime import timedelta
import base64
import io
from PIL import Image



class VettingReport(models.Model):
    _name = 'vetting.report'
    _inherit = 'mail.thread'

    name = fields.Char(
        string='Judul report',
        required=True,
    )

    date = fields.Date(
        string='Tanggal',
        default=fields.Date.context_today,
    )

    year_id = fields.Many2one(comodel_name='bpg.tahun.baru', string="Year")

    vos = fields.Char(
        string='VOS',
        required=False,
    )   

    vessel_id = fields.Char(string='Kapal')

    type_vessel = fields.Char(string="Type Vessel")

    fleet = fields.Char(string='Fleet')

    # vessel_id = fields.Many2one('shipping.vessel',
    #                                string='Kapal',
    #                                required=False)

    # type_vessel = fields.Many2one(string="Type Vessel", readonly=True, related="vessel_id.type_id",
    #                              store=True, )

    # fleet = fields.Selection(
    #     string='Fleet',
    #     selection=[('fleet1', 'Fleet 1'), ('fleet2', 'Fleet 2'), ('fleet3', 'Fleet 3'),
    #                ('fleet4', 'Fleet 4'), ('fleet5', 'Fleet 5'), ('fleet6', 'Fleet 6'), ('fleet7', 'Fleet 7')],
    #     readonly=True,
    #     related="vessel_id.fleet",
    #     store=True,
    # )

    expired_psa_date = fields.Date(
        string='Expired PSA Date',
        default=False,
    )

    preventing_plan_date = fields.Date(
        string='Preventing Plan Date',
        default=False,
    )

    preventing_act_date = fields.Date(
        string='Preventing Actual Date',
        default=False,
    )

    preventing_lokasi = fields.Many2one(
        'bpg.additional.lokasi',
        string='Preventing Lokasi',
        required=False)

    preventing_pic = fields.Many2one(
        'bpg.additional.pic',
        string='Preventing PIC',
        required=False)

    pengajuan_vos_plan_date = fields.Date(
        string='Pengajuan VOS Plan Date',
        default=False,
    )

    pengajuan_vos_act_date = fields.Date(
        string='Pengajuan VOS Actual Date',
        default=False,
    )

    pengajuan_vos_lokasi = fields.Many2one(
        'bpg.additional.lokasi',
        string='Pengajuan VOS Lokasi',
        required=False)

    pengajuan_vos_pic = fields.Many2one(
        'bpg.additional.pic',
        string='Pengajuan VOS PIC',
        required=False)

    vetting_plan_date = fields.Date(
        string='Vetting Plan Date',
        default=False,
    )

    vetting_online_date = fields.Date(
        string='Vetting Online Date',
        default=False,
    )

    vetting_act_date = fields.Date(
        string='Vetting Actual Date',
        default=False,
    )

    vetting_lokasi = fields.Many2one(
        'bpg.additional.lokasi',
        string='Vetting Lokasi',
        required=False)

    inspektor = fields.Many2one(
        'bpg.additional.pic',
        string='Inspektor',
        required=False)

    esscort = fields.Many2one(
        'bpg.additional.pic',
        string='Esscort',
        required=False)

    status = fields.Many2one(
        'bpg.status.vetting',
        string='Status',
        required=False)

    # vetting_report_line = fields.One2many(
    #     'vetting.report.line', 'group_vetting_report_id',
    #     string="Group Vetting Report",
    #     required=False,
    # )

class MeetingLine(models.Model):
    _name = "meeting.line"

    name = fields.Many2one(
        comodel_name='finding.item',
        string='Name',
        required=True,
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

    percentage = fields.Float(
        string='Persentase',
        required=False)

    status = fields.Selection(
        string='Tipe',
        selection=[
            ('open', 'Open'),
            ('on_progress', 'On Progress'),
            ('close', 'Close'),
        ],
        default='open'
    )

    tindak_lanjut = fields.Char(
        string='Tindak Lanjut',
        required=False,
    )

    divisi = fields.Char(
        string='Koordinasi Lintas Divisi',
        required=False,
    )

    keterangan = fields.Char(
        string='Lokasi',
        required=False,
    )

    group_visit_id = fields.Many2one(
        'visit.management',
        string='Group Visit Report',
        readonly=True,
        index=True,
        auto_join=True,
    )


class VettingReportLine(models.Model):
    _name = "vetting.report.line"

    # def action_openListItemTreeView(self):
    #     print(self.id)
    #     return {
    #         'name': _('List Item'),
    #         "type": "ir.actions.act_window",
    #         "res_model": 'vetting.report.line',
    #         "res_id":self.id,
    #         "view_mode": "form",
    #         "view_id":self.env.ref('bpg_module.vetting_report_line_form').id
    #     }

    # def _compute_items(self):
    #     record_data = self.env['finding.item'].read_group(
    #         [('group_vetting_report_line_id', 'in', self.ids)],
    #         ['group_vetting_report_line_id'], ['group_vetting_report_line_id'])
    #     result = dict((data['group_vetting_report_line_id'][0], data['group_vetting_report_line_id_count']) for data in record_data)
    #     for record in self:
    #         record.item_count = result.get(record.id, 0)

    item_count = fields.Integer(string="Item Count")
    # item_count = fields.Integer(compute='_compute_items', string="Item Count")

    date = fields.Date(
        string='Release Date',
        required=False,
    )

    lokasi = fields.Char(
        string='Lokasi',
        required=False,
    )

    # group_vetting_report_id = fields.Many2one(
    #     'vetting.report',
    #     string='Group Vetting Report',
    #     readonly=True,
    #     index=True,
    #     auto_join=True,
    # )

    status = fields.Selection(
        string='Tipe',
        selection=[
            ('open', 'Open'),
            ('on_progress', 'On Progress'),
            ('close', 'Close'),
        ],
        default='open'
    )

    group_visit_id = fields.Many2one(
        'visit.management',
        string='Group Visit Report',
        readonly=True,
        index=True,
        auto_join=True,
    )

    tipe_kunjungan = fields.Selection(
        string='Tipe Kunjungan',
        selection=[
            ('visit', 'Visit'),
            ('perbaikan', 'Perbaikan Kapal'),
            ('vetting', 'Vetting'),
            ('vettingPlus', 'Vetting Plus'),
            ('negativeFeedback', 'Negative Feedback'),
            ('selfAssesment', 'Self Assesment'),
        ],
        readonly=True, related="group_visit_id.tipe_kunjungan",
        store=True,
    )

    # name = fields.Many2one(string='Kapal'

    name = fields.Many2one('shipping.vessel',
                                string='Kapal',
                                readonly=True, related="group_visit_id.vessel_id",
                                store=True,)

    type_vessel = fields.Many2one(string="Type Vessel", readonly=True, related="group_visit_id.type_vessel",
                                store=True, )

    # type_vessel = fields.Char(string="Type Vessel")   

    jenis_inspeksi_id = fields.Many2one(
        'bpg.jenis.inspeksi',
        string='Jenis Inspeksi',
        required=False)

    list_finding_item = fields.One2many(
        'finding.item', 'group_vetting_report_line_id',
        string="Group Vetting Report",
        required=False,
    )

class FindingItem(models.Model):
    _name = "finding.item"
    _inherit = 'mail.thread'

    name = fields.Char(string='Uraian', )

    remark = fields.Text(
        'Remark',
        required=False,
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

    penanggung_jawab = fields.Many2one(
        'bpg.additional.pic',
        string='Penanggung jawab',
        required=False)

    percentage = fields.Float(
        string='Persentase',
        required=False)

    status = fields.Selection(
        string='Tipe',
        selection=[
            ('open', 'Open'),
            ('on_progress', 'On Progress'),
            ('close', 'Close'),
        ],
        default='open'
    )

    action_item_ids = fields.One2many(
        string='Action',
        comodel_name='action.item',
        inverse_name='Action_id',
    )

    group_vetting_report_line_id = fields.Many2one(
        'vetting.report.line',
        string='Group Vetting Report Line',
        readonly=True,
        index=True,
        auto_join=True,
    )

class BPGTahunBaru(models.Model):
    _name = "bpg.tahun.baru"

    name = fields.Char(ondelete="cascade", string='Year', )

    active = fields.Boolean(
        string='Active',
        default=True,
        required=False)


class BPGAdditionalLokasi(models.Model):
    _name = "bpg.additional.lokasi"

    name = fields.Char(
        string='Name',
        required=False)

    active = fields.Boolean(
        string='Active',
        default=True,
        required=False)

class BPGAdditionalPIC(models.Model):
    _name = "bpg.additional.pic"

    name = fields.Char(
        string='Name',
        required=False)

    active = fields.Boolean(
        string='Active',
        default=True,
        required=False)

class BPGAdditionalVendor(models.Model):
    _name = "bpg.additional.vendor"

    name = fields.Char(
        string='Name',
        required=False)

    active = fields.Boolean(
        string='Active',
        default=True,
        required=False)


class BPGStatusVetting(models.Model):
    _name = "bpg.status.vetting"

    name = fields.Char(
        string='Name',
        required=False)

    active = fields.Boolean(
        string='Active',
        default=True,
        required=False)


class BPGJenisInspeksi(models.Model):
    _name = "bpg.jenis.inspeksi"

    name = fields.Char(
        string='Name',
        required=False)

    active = fields.Boolean(
        string='Active',
        default=True,
        required=False)