# import requests
# from odoo.tests import Form
# import werkzeug.wrappers

# import base64
# from datetime import datetime
# from odoo import http, _, exceptions
# from odoo.http import content_disposition, request
# from operator import itemgetter,methodcaller

# class ApkManagementModule(http.Controller):

#     @http.route(['/api/bpg_get_info_home_screen'], type='json', method='GET', auth='user')
#     def bpg_get_info_home_screen(self, **kw):
#         dict_ptw = {}
#         user = request.env['res.users'].search([('id', '=', kw['id'])])

#         visits = request.env['visit.management'].sudo().search([])

#         findings = request.env['vetting.report.line'].sudo().search([],order='date desc',limit=250)
#         findingItems = request.env['finding.item'].sudo().search([],order='open_date desc')

#         countVetting = 0
#         countKunjungan = 0
#         countFinding = 0
#         countFindingItem = 0
#         countItemClose = 0

#         totalKunjungan =0
#         totalItem = 0

#         persentaseVetting = 0.0
#         persentaseKunjungan = 0.0
#         persentaseFinding = 0.0

#         dict_request2 = {}


#         for v in findingItems:
#             countFindingItem += 1

#         for v in visits:
#             if v.tipe_kunjungan == 'vetting' or v.tipe_kunjungan == 'vettingPlus':
#                 countVetting += 1
#             if v.tipe_kunjungan == 'visit':
#                 countKunjungan += 1
#             totalKunjungan += 1
#             for line in visits.kunjungan_line:
#                 countFinding += 1
#                 if line.item_count:
#                     totalItem += line.item_count
#                 for item in line.list_finding_item:
#                     if item.status == 'close':
#                         countItemClose += 1

#         if totalKunjungan > 0:
#             persentaseVetting = (countVetting / totalKunjungan) * 100
#             persentaseKunjungan = (countKunjungan / totalKunjungan) * 100
#         if totalItem >0:
#             persentaseFinding = (countItemClose / totalItem) * 100

#         for j in user:
#             dict_ptw = {'id': j.id, 'name': j.name, 'job_name': j.job_id.name, 'countVetting': countVetting,
#                         'countProject': countKunjungan, 'countFinding': countFindingItem,
#                         'persentaseVetting':persentaseVetting,'persentaseKunjungan':persentaseKunjungan,
#                         'persentaseFinding':persentaseFinding
#                         }
#         return dict_ptw

#     @http.route(['/api/bpg_get_list_kunjungan_info'], type='json', method='GET', auth='user')
#     def bpg_get_list_kunjungan_info(self, **kw):
#         dict_ptw = {}
#         visits = request.env['visit.management'].sudo().search([])

#         countVetting = 0
#         countVettingPlus = 0
#         countNegative = 0
#         countVisit = 0
#         countPerbaikan = 0
#         countSelfAssesment = 0

#         for v in visits:
#             if v.tipe_kunjungan == 'vetting':
#                 countVetting += 1
#             if v.tipe_kunjungan == 'vettingPlus':
#                 countVettingPlus += 1
#             if v.tipe_kunjungan == 'negativeFeedback':
#                 countNegative += 1
#             if v.tipe_kunjungan == 'visit':
#                 countVisit += 1
#             if v.tipe_kunjungan == 'perbaikan':
#                 countPerbaikan += 1
#             if v.tipe_kunjungan == 'selfAssesment':
#                 countSelfAssesment += 1

#         dict_ptw = {'countVetting': countVetting,'countVettingPlus':countVettingPlus,
#                     'countNegative': countNegative,'countVisit': countVisit, 'countPerbaikan': countPerbaikan,
#                     'countSelfAssesment':countSelfAssesment
#                     }
#         return dict_ptw


#     @http.route(['/api/bpg_get_list_kunjungan'], type='json', method='GET', auth='user')
#     def bpg_get_list_kunjungan(self, **kw):
#         if kw['tipe_kunjungan'] == 'visit':
#             visits = request.env['visit.management'].sudo().search(
#                 [('tipe_kunjungan', '=', 'visit')],
#                 order='date desc',limit=100)
#         elif kw['tipe_kunjungan'] == 'perbaikan':
#             visits = request.env['visit.management'].sudo().search(
#                 [('tipe_kunjungan', '=', 'perbaikan')],order='date desc', limit=100)
#         elif kw['tipe_kunjungan'] == 'negativeFeedback':
#             visits = request.env['visit.management'].sudo().search(
#                 [('tipe_kunjungan', '=', 'negativeFeedback')],
#                 order='date desc',limit=100)
#         elif kw['tipe_kunjungan'] == 'vetting':
#             visits = request.env['visit.management'].sudo().search(
#                 [('tipe_kunjungan', '=', 'vetting')],
#                 order='date desc',limit=100)
#         elif kw['tipe_kunjungan'] == 'vettingPlus':
#             visits = request.env['visit.management'].sudo().search(
#                 [('tipe_kunjungan', '=', 'vettingPlus')],
#                 order='date desc',limit=100)
#         elif kw['tipe_kunjungan'] == 'selfAssesment':
#             visits = request.env['visit.management'].sudo().search(
#                 [('tipe_kunjungan', '=', 'selfAssesment')],
#                 order='date desc',limit=100)
#         dict_request = {}
#         data_request = []

#         for v in visits:
#             dict_request = {'id': v.id, 'vessel_name': v.vessel_id.name, 'lokasi': v.lokasi,
#                             'open_date': v.open_date,
#                             'pic': v.pic.name, 'tipe_kunjungan': v.tipe_kunjungan,
#                             'divisi_name': v.divisi_id.name,
#                             'vendor': v.vendor.name, }
#             data_request.append(dict_request)

#         return data_request

#     @http.route(['/api/bpg_get_list_tool_box_meeting'], type='json', method='GET', auth='user')
#     def bpg_get_list_tool_box_meeting(self, **kw):
#         tool_box = request.env['visit.management'].sudo().search(
#             [('tipe_kunjungan', '=', 'toolBoxMeeting')],
#             order='date desc', limit=500)
#         dict_request = {}
#         data_request = []

#         for v in tool_box:
#             dict_request = {'id': v.id, 'name': v.name, 'metode_rapat': v.metode_rapat,
#                             'jenis_rapat': v.jenis_rapat,
#                             'date': v.date, 'count_anggota': v.count_anggota,
#                             'divisi_name': v.divisi_id.name,
#                             'lokasi': v.lokasi, 'pic': v.pic.name,'sisa_waktu': v.sisa_waktu,
#                             'state': v.state,}
#             data_request.append(dict_request)

#         return data_request

#     @http.route(['/api/bpg_show_tool_box_meeting'], type='json', method='GET', auth='user')
#     def bpg_show_tool_box_meeting(self, **kw):
#         tool_box = request.env['visit.management'].sudo().search([('id', '=', kw['id'])])
#         dict_request = {}
#         data_request = []
#         for v in tool_box:
#             dict_line = {}
#             data_line = []
#             dict_line_two = {}
#             data_line_two = []
#             for fi in v.anggota_id:
#                 dict_line = {
#                     'id': fi.id,
#                     'name': fi.name.name,
#                     'jabatan': fi.jabatan,
#                 }
#                 data_line.append(dict_line)
#             for fi in v.meeting_line:
#                 dict_line_two = {
#                     'id': fi.id,
#                     'name_id': fi.name.id,
#                     'name': fi.name.name,
#                     'open_date': fi.open_date,
#                     'close_date': fi.close_date,
#                     'deadline_date': fi.deadline_date,
#                     'percentage': fi.percentage,
#                     'status': fi.status,
#                     'tindak_lanjut': fi.tindak_lanjut,
#                     'divisi': fi.divisi,
#                     'keterangan': fi.keterangan,
#                 }
#                 data_line_two.append(dict_line_two)
#             dict_request = {
#                 'id': v.id,
#                 'name': v.name,
#                 'metode_rapat': v.metode_rapat,
#                 'jenis_rapat': v.jenis_rapat,
#                 'date': v.date,
#                 'count_anggota': v.count_anggota,
#                 'divisi_name': v.divisi_id.name,
#                 'lokasi': v.lokasi,
#                 'pic': v.pic.name,
#                 'sisa_waktu': v.sisa_waktu,
#                 'state': v.state,
#                 'catatan': v.catatan,
#                 'anggota':data_line,
#                 'list_meeting':data_line_two
#             }
#             # data_work_orders.append(dict_work_orders)
#         return dict_request

#     @http.route('/api/bpg_get_list_finding_item', auth='user', type="json", method='GET')
#     def bpg_get_list_finding_item(self, **kw):
#         data = request.env['finding.item'].search([])
#         data_list = []
#         for d in data:
#             data_list.append({
#                 'id': d.id,
#                 'name': d.name
#             })
#         return data_list

#     @http.route(['/api/create_tool_box_meeting'], type='json', auth='user', method='POST', csrf=False,
#                 website=False)
#     def create_tool_box_meeting(self, **kw):
#         dict = {}
#         if kw:
#             record = {
#                 'name': kw.get('name'),
#                 'metode_rapat': kw.get('metode_rapat'),
#                 'jenis_rapat': kw.get('jenis_rapat'),
#                 'date': kw.get('date'),
#                 'open_date': kw.get('open_date'),
#                 'close_date': kw.get('close_date'),
#                 'deadline_date': kw.get('deadline_date'),
#                 'divisi_id': kw.get('divisi_id'),
#                 'lokasi': kw.get('lokasi'),
#                 'pic': kw.get('pic'),
#                 'state': 'open',
#                 'catatan': kw.get('catatan'),
#             }
#             new_request = request.env['visit.management'].sudo().create(record)
#             dict = {'id': new_request.id, }
#             for rec in kw['anggota_id']:
#                 if rec.get('name') != '':
#                     line = {
#                         'request_id': new_request.id,
#                         'name': rec.get('name'),
#                         'jabatan': rec.get('jabatan'),
#                     }
#                     new_line = request.env['anggota.visit'].sudo().create(line)
#             for rec in kw['meeting_line']:
#                 if rec.get('name'):
#                     line = {
#                         'request_id': new_request.id,
#                         'name': rec.get('name'),
#                         'open_date': rec.get('open_date'),
#                         'close_date': rec.get('close_date'),
#                         'deadline_date': rec.get('deadline_date'),
#                         'percentage': rec.get('percentage'),
#                         'status': rec.get('status'),
#                         'tindak_lanjut': rec.get('tindak_lanjut'),
#                         'divisi': rec.get('divisi'),
#                         'keterangan': rec.get('keterangan'),
#                     }
#                     new_line = request.env['meeting.line'].sudo().create(line)
#         return dict

#     @http.route(['/api/edit_one_list_meeting'], type='json', auth='user', method='POST', csrf=False, website=False)
#     def edit_one_list_meeting(self, **kw):
#         data = request.env['meeting.line'].sudo().search([('id', '=', kw['id'])])
#         data.write({'name': kw['name'],
#                           'open_date': kw['open_date'],
#                           'close_date': kw['close_date'],
#                           'deadline_date': kw['deadline_date'],
#                           'percentage': kw['percentage'],
#                           'status': kw['status'],
#                           'tindak_lanjut': kw['tindak_lanjut'],
#                             'divisi': kw['divisi'],
#                           'keterangan': kw['keterangan']
#                           })
#         return kw

#     @http.route(['/api/bpg_show_finding'], type='json', method='GET', auth='user')
#     def bpg_show_finding(self, **kw):
#         finding = request.env['vetting.report.line'].sudo().search([('id', '=', kw['id'])])
#         dict_finding = {}
#         data_finding = []
#         for wo in finding:
#             dict_line = {}
#             data_line = []
#             for fi in wo.list_finding_item:
#                 image = False
#                 if fi.image_1920:
#                     image_base_url = 'http://202.74.236.120:8069'
#                     # image_base_url = 'http://localhost:8069/'
#                     image = image_base_url + '/web/image?model=finding.item' + '&field=image_1920' + '&id=' + str(
#                         fi.id)
#                 dict_line = {
#                     'id': fi.id,
#                     'name': fi.name,
#                     'remark': fi.remark,
#                     'image_1920': image,
#                     'target_date': fi.target_date,
#                     'open_date': fi.open_date,
#                     'close_date': fi.close_date,
#                     'percentage': fi.percentage,
#                     'nama_pic': fi.penanggung_jawab.name,
#                     'nama_pic_id': fi.penanggung_jawab.id,
#                     'status': fi.status,
#                     'group_vetting_report_line_id': fi.group_vetting_report_line_id,
#                     'act': 'normal'
#                 }
#                 data_line.append(dict_line)
#             dict_finding = {
#                 'id': wo.id,
#                 'date': wo.date,
#                 'item_count': wo.item_count,
#                 'lokasi': wo.lokasi,
#                 'status': wo.status,
#                 'tipe_kunjungan': wo.tipe_kunjungan,
#                 'name': wo.name.name,
#                 'name_id': wo.name.id,
#                 'type_vessel': wo.type_vessel.name,
#                 'jenis_inspeksi_id': wo.jenis_inspeksi_id.id,
#                 'jenis_inspeksi_id_name': wo.jenis_inspeksi_id.name,
#                 'list_finding_item':data_line
#             }
#             # data_work_orders.append(dict_work_orders)
#         return dict_finding

#     @http.route(['/api/bpg_get_list_finding_info'], type='json', method='GET', auth='user')
#     def bpg_get_list_finding_info(self, **kw):
#         dict_ptw = {}
#         finding = request.env['vetting.report.line'].sudo().search([])

#         countItemOpen = 0
#         countItemClose = 0
#         countItemOnProgress = 0

#         for v in finding:
#             if v.status == 'open':
#                 countItemOpen += 1
#             if v.status == 'close':
#                 countItemClose += 1
#             if v.status == 'on_progress':
#                 countItemOnProgress += 1

#         dict_ptw = {'countItemOpen': countItemOpen, 'countItemClose': countItemClose,
#                     'countItemOnProgress': countItemOnProgress,
#                     }
#         return dict_ptw


#     @http.route(['/api/bpg_get_list_finding'], type='json', method='GET', auth='user')
#     def bpg_get_list_finding(self, **kw):
#         if kw['status'] == 'all':
#             finding = request.env['vetting.report.line'].sudo().search([],order='date desc',
#                 limit=250)
#         elif kw['status'] == 'open':
#             finding = request.env['vetting.report.line'].sudo().search(
#                 [('status', '=', 'open')],order='date desc', limit=100)
#         elif kw['status'] == 'close':
#             finding = request.env['vetting.report.line'].sudo().search(
#                 [('status', '=', 'close')],
#                 order='date desc',limit=100)
#         elif kw['status'] == 'on_progress':
#             finding = request.env['vetting.report.line'].sudo().search(
#                 [('status', '=', 'on_progress')],
#                 order='date desc',limit=100)
#         dict_request = {}
#         data_request = []

#         for v in finding:
#             countItemOpen=0
#             countItemClose=0
#             countItemOnProgress=0
#             for line in v.list_finding_item:
#                 if line.status == 'open':
#                     countItemOpen += 1
#                 if line.status == 'close':
#                     countItemClose += 1
#                 if line.status == 'on_progress':
#                     countItemOnProgress += 1

#             dict_request = {'id': v.id, 'vessel_name': v.name.name, 'lokasi': v.lokasi,'status':v.status,
#                             'date': v.date,'tipe_kunjungan': v.tipe_kunjungan, 'countTemuan':v.item_count,
#                             'countItemOpen':countItemOpen,'countItemClose':countItemClose,'countItemOnProgress':countItemOnProgress }
#             data_request.append(dict_request)

#         return data_request

#     @http.route(['/api/bpg_get_list_vetting'], type='json', method='GET', auth='user')
#     def bpg_get_list_vetting(self, **kw):
#         finding = request.env['vetting.report.line'].sudo().search(
#             [('tipe_kunjungan', '=', 'vetting')],order='date desc', limit=100)
#         dict_request = {}
#         data_request = []

#         for v in finding:
#             countItemOpen = 0
#             countItemClose = 0
#             countItemOnProgress = 0
#             for line in finding.list_finding_item:
#                 if line.status == 'open':
#                     countItemOpen += 1
#                 if line.status == 'close':
#                     countItemClose += 1
#                 if line.status == 'on_progress':
#                     countItemOnProgress += 1

#             dict_request = {'id': v.id, 'vessel_name': v.name.name, 'lokasi': v.lokasi,
#                             'date': v.date, 'countTemuan': v.item_count,
#                             'countItemOpen': countItemOpen, 'countItemClose': countItemClose,
#                             'countItemOnProgress': countItemOnProgress}
#             data_request.append(dict_request)

#         return data_request

#     @http.route(['/api/bpg_get_list_item_info'], type='json', method='GET', auth='user')
#     def bpg_get_list_item_info(self, **kw):
#         dict_ptw = {}
#         finding = request.env['finding.item'].sudo().search([])

#         countItemOpen = 0
#         countItemClose = 0
#         countItemOnProgress = 0

#         for v in finding:
#             if v.status == 'open':
#                 countItemOpen += 1
#             if v.status == 'close':
#                 countItemClose += 1
#             if v.status == 'on_progress':
#                 countItemOnProgress += 1

#         dict_ptw = {'countItemOpen': countItemOpen, 'countItemClose': countItemClose,
#                     'countItemOnProgress': countItemOnProgress,
#                     }
#         return dict_ptw

#     @http.route(['/api/bpg_get_list_item'], type='json', method='GET', auth='user')
#     def bpg_get_list_item(self, **kw):
#         if kw['status'] == 'all':
#             finding = request.env['finding.item'].sudo().search([],order='open_date desc',limit=500)
#         elif kw['status'] == 'open':
#             finding = request.env['finding.item'].sudo().search(
#                 [('status', '=', 'open')],order='open_date desc', limit=250)
#         elif kw['status'] == 'close':
#             finding = request.env['finding.item'].sudo().search(
#                 [('status', '=', 'close')],
#                 order='open_date desc',limit=250)
#         elif kw['status'] == 'on_progress':
#             finding = request.env['finding.item'].sudo().search(
#                 [('status', '=', 'on_progress')],
#                 order='open_date desc',limit=250)
#         dict_request = {}
#         data_request = []

#         for v in finding:
#             countItemOpen = 0
#             countItemClose = 0
#             countItemOnProgress = 0
#             for line in v.action_item_ids:
#                 if line.status == 'open':
#                     countItemOpen += 1
#                 if line.status == 'close':
#                     countItemClose += 1
#                 if line.status == 'on_progress':
#                     countItemOnProgress += 1

#             dict_request = {'id': v.id, 'name': v.name, 'remark': v.remark, 'status': v.status,
#                             'target_date': v.target_date, 'open_date': v.open_date, 'close_date': v.close_date,
#                             'percentage': v.percentage,'penanggung_jawab': v.penanggung_jawab.name,
#                             'countItemOpen': countItemOpen, 'countItemClose': countItemClose,
#                             'countItemOnProgress': countItemOnProgress}
#             data_request.append(dict_request)

#         return data_request

#     @http.route(['/api/bpg_edit_finding_item'], type='json', method='POST', auth='user')
#     def bpg_edit_finding_item(self, **kw):
#         data = {}
#         if kw:
#             for rec in kw['action_item_ids']:
#                 if rec.get('name') != '':
#                     line = {
#                         'title': rec.get('title'),
#                         'deskripsi': rec.get('deskripsi'),
#                         'target_date': rec.get('target_date'),
#                         'open_date': rec.get('open_date'),
#                         'close_date': rec.get('close_date'),
#                         'status': rec.get('status'),
#                         'Action_id': kw['id'],
#                     }
#                     request.env['action.item'].sudo().create(line)
#         return kw

#     @http.route(['/api/edit_finding_item'], type='json', auth='user', method='POST', csrf=False, website=False)
#     def edit_finding_item(self, **kw):
#         data = request.env['finding.item'].sudo().search([('id', '=', kw['id'])])
#         data.write({
#             'name': kw.get('name'),
#             'open_date': kw.get('open_date'),
#             'close_date': kw.get('close_date'),
#             'target_date': kw.get('target_date'),
#             'percentage': kw.get('percentage'),
#             'penanggung_jawab': kw.get('penanggung_jawab'),
#             'status': kw.get('status'),
#         })
#         return kw

#     @http.route(['/api/get_one_finding_item'], type='json', auth='user', method='GET', csrf=False, website=False)
#     def get_one_finding_item(self, **kw):
#         finding = request.env['finding.item'].sudo().search([('id', '=', kw['id'])])
#         dict_p = {}
#         data_p = []
#         for p in finding:
#             dict_p_line = {}
#             data_p_line = []
#             imageItem=False
#             if p.image_1920:
#                 image_base_url = 'http://202.74.236.120:8069'
#                 # image_base_url = 'http://localhost:8069/'
#                 imageItem = image_base_url + '/web/image?model=finding.item' + '&field=image_1920' + '&id=' + str(
#                     p.id)
#             for line in p.action_item_ids:
#                 dict_p_line = {'id': line.id, 'title': line.title, 'deskripsi': line.deskripsi,
#                                'target_date': line.target_date, 'open_date': line.open_date,
#                                'close_date': line.close_date,
#                                'status': line.status,'statusAct': False, 'act': 'normal'}
#                 data_p_line.append(dict_p_line)
#             dict_p = {'id': p.id, 'name': p.name, 'remark': p.remark,
#                                'image_1920': imageItem, 'target_date': p.target_date,
#                                'open_date': p.open_date,
#                                'close_date': p.close_date, 'percentage': p.percentage,
#                                'penanggung_jawab': p.penanggung_jawab.name, 'status': p.status,
#                                'line_ids': data_p_line,}
#             # data_work_orders.append(dict_work_orders)
#         return dict_p

#     @http.route(['/api/bpg_get_list_negative'], type='json', method='GET', auth='user')
#     def bpg_get_list_negative(self, **kw):
#         finding = request.env['vetting.report.line'].sudo().search(
#             [('tipe_kunjungan', '=', 'negativeFeedback')],order='date desc', limit=100)
#         dict_request = {}
#         data_request = []

#         for v in finding:
#             countItemOpen = 0
#             countItemClose = 0
#             countItemOnProgress = 0
#             for line in finding.list_finding_item:
#                 if line.status == 'open':
#                     countItemOpen += 1
#                 if line.status == 'close':
#                     countItemClose += 1
#                 if line.status == 'on_progress':
#                     countItemOnProgress += 1

#             dict_request = {'id': v.id, 'vessel_name': v.name.name, 'lokasi': v.lokasi,
#                             'date': v.date, 'countTemuan': v.item_count,
#                             'countItemOpen': countItemOpen, 'countItemClose': countItemClose,
#                             'countItemOnProgress': countItemOnProgress}
#             data_request.append(dict_request)

#         return data_request

#     @http.route(['/api/bpg_get_list_vetting_plus'], type='json', method='GET', auth='user')
#     def bpg_get_list_vetting_plus(self, **kw):
#         finding = request.env['vetting.report.line'].sudo().search(
#             [('tipe_kunjungan', '=', 'vettingPlus')],order='date desc', limit=100)
#         dict_request = {}
#         data_request = []

#         for v in finding:
#             countItemOpen = 0
#             countItemClose = 0
#             countItemOnProgress = 0
#             for line in finding.list_finding_item:
#                 if line.status == 'open':
#                     countItemOpen += 1
#                 if line.status == 'close':
#                     countItemClose += 1
#                 if line.status == 'on_progress':
#                     countItemOnProgress += 1

#             dict_request = {'id': v.id, 'vessel_name': v.name.name, 'lokasi': v.lokasi,
#                             'date': v.date, 'countTemuan': v.item_count,
#                             'countItemOpen': countItemOpen, 'countItemClose': countItemClose,
#                             'countItemOnProgress': countItemOnProgress}
#             data_request.append(dict_request)

#         return data_request

#     @http.route(['/api/bpg_get_info_account_screen'], type='json', method='GET', auth='user')
#     def bpg_get_info_account_screen(self, **kw):
#         dict_account = {}
#         user = request.env['res.users'].search([('id', '=', kw['id'])])
#         visits = request.env['visit.management'].sudo().search([])
#         countVetting = 0
#         countKunjungan = 0
#         countPerbaikan = 0
#         countSelfAssesment = 0
#         for no in visits:
#             if no.tipe_kunjungan == 'visit':
#                 countKunjungan += 1
#             if no.tipe_kunjungan == 'perbaikan':
#                 countPerbaikan += 1
#             if no.tipe_kunjungan == 'vetting' or no.tipe_kunjungan == 'vettingPlus':
#                 countVetting += 1
#             if no.tipe_kunjungan == 'selfAssesment':
#                 countSelfAssesment += 1
#         for j in user:
#             dict_account = {'id': j.id, 'name': j.name, 'job_name': j.job_id.name, 'countVetting': countVetting,
#                             'countKunjungan': countKunjungan,'countPerbaikan': countPerbaikan,'countSelfAssesment': countSelfAssesment}
#         return dict_account

#     @http.route('/api/bpg_get_additional_lokasi', auth='user', type="json", method='GET')
#     def bpg_get_additional_lokasi(self, **kw):
#         data = request.env['bpg.additional.lokasi'].search([('active', '=', True)])
#         data_list = []
#         for d in data:
#             data_list.append({
#                 'id': d.id,
#                 'name': d.name
#             })
#         return data_list

#     @http.route('/api/bpg_create_additional_lokasi', auth='user', type="json", method='GET')
#     def bpg_create_additional_lokasi(self, **kw):
#         dict = {}
#         if kw:
#             record = {
#                 'name': kw.get('name'),
#                 'active': True,
#             }
#             new = request.env['bpg.additional.lokasi'].sudo().create(record)
#             dict = {'id': new.id, 'name': kw.get('name')}
#         return dict

#     @http.route('/api/bpg_get_additional_pic', auth='user', type="json", method='GET')
#     def bpg_get_additional_pic(self, **kw):
#         data = request.env['bpg.additional.pic'].search([('active', '=', True)])
#         data_list = []
#         for d in data:
#             data_list.append({
#                 'id': d.id,
#                 'name': d.name
#             })
#         return data_list

#     @http.route('/api/bpg_create_additional_pic', auth='user', type="json", method='GET')
#     def bpg_create_additional_pic(self, **kw):
#         dict = {}
#         if kw:
#             record = {
#                 'name': kw.get('name'),
#                 'active': True,
#             }
#             new = request.env['bpg.additional.pic'].sudo().create(record)
#             dict = {'id': new.id, 'name': kw.get('name')}
#         return dict

#     @http.route('/api/bpg_get_additional_vendor', auth='user', type="json", method='GET')
#     def bpg_get_additional_vendor(self, **kw):
#         data = request.env['bpg.additional.vendor'].search([('active', '=', True)])
#         data_list = []
#         for d in data:
#             data_list.append({
#                 'id': d.id,
#                 'name': d.name
#             })
#         return data_list

#     @http.route('/api/bpg_create_additional_vendor', auth='user', type="json", method='GET')
#     def bpg_create_additional_vendor(self, **kw):
#         dict = {}
#         if kw:
#             record = {
#                 'name': kw.get('name'),
#                 'active': True,
#             }
#             new = request.env['bpg.additional.vendor'].sudo().create(record)
#             dict = {'id': new.id, 'name': kw.get('name')}
#         return dict

#     @http.route('/api/bpg_create_additional_inspeksi', auth='user', type="json", method='GET')
#     def bpg_create_additional_inspeksi(self, **kw):
#         dict = {}
#         if kw:
#             record = {
#                 'name': kw.get('name'),
#                 'active': True,
#             }
#             new = request.env['bpg.jenis.inspeksi'].sudo().create(record)
#             dict = {'id': new.id, 'name': kw.get('name')}
#         return dict

#     @http.route('/api/bpg_get_additional_inspeksi', auth='user', type="json", method='GET')
#     def bpg_get_additional_inspeksi(self, **kw):
#         data = request.env['bpg.jenis.inspeksi'].search([('active', '=', True)])
#         data_list = []
#         for d in data:
#             data_list.append({
#                 'id': d.id,
#                 'name': d.name
#             })
#         return data_list

#     @http.route('/api/bpg_get_kapal', auth='user', type="json", method='GET')
#     def bpg_get_kapal(self, **kw):
#         data = request.env['shipping.vessel'].search(
#             [('fleet', '!=', False), ('valid', '=', True)])
#         data_list = []
#         for usr in data:
#             data_list.append({
#                 'code_vessel': usr.code_vessel,
#                 'name': usr.name,
#                 'id': usr.id,
#             })
#         return data_list

#     @http.route(['/bpg_download_report_kunjungan/<int:id>'], type='http', auth='public')
#     def bpg_download_report_kunjungan(self, id, **kw):
#         data = request.env['visit.management'].sudo().browse(id)
#         if data:
#             document = base64.b64decode(data.document)
#             headers = [
#                 ('Content-Type', 'application/octet-stream'),
#                 ('Content-Disposition', f'attachment; filename="{data.name}.pdf"')
#             ]
#             return request.make_response(document, headers)
#         else:
#             return request.not_found()

#     @http.route(['/api/bpg_edit_kunjungan_line'], type='json', method='POST', auth='user')
#     def edit_kunjungan_line(self, **kw):
#         kunjungan = request.env['visit.management'].sudo().search([('id', '=', kw['id'])])
#         for p in kunjungan:
#             for rec in kw['anggota']:
#                 if rec.get('status') == False:
#                     if rec.get('act') == 'update':
#                         line_search = p.anggota_id.search([('id', '=', rec.get('id'))])
#                         line_search.write({
#                             'name': rec.get('name'),
#                             'jabatan': rec.get('jabatan'),
#                         })
#                     elif rec.get('act') == 'delete':
#                         line_search = p.anggota_id.search([('id', '=', rec.get('id'))])
#                         line_search.unlink()

#                 elif rec.get('status') == True:
#                     if rec.get('name') != '':
#                         record = {
#                             'name': rec.get('name'),
#                             'jabatan': rec.get('jabatan'),
#                             'group_anggota_visit_id': p.id,
#                         }
#                         request.env['anggota.visit'].sudo().create(record)

#             for rec in kw['list_finding']:
#                 if rec.get('status') == False:
#                     if rec.get('act') == 'update':
#                         line_search = p.kunjungan_line.search([('id', '=', rec.get('id'))])
#                         line_search.write({
#                             'tipe_kunjungan': rec.get('tipe_kunjungan'),
#                             'jenis_inspeksi_id': rec.get('jenis_inspeksi_id'),
#                             'date': rec.get('date'),
#                             'lokasi': rec.get('lokasi'),
#                             'item_count': rec.get('item_count')
#                         })
#                     elif rec.get('act') == 'delete':
#                         line_search = p.kunjungan_line.search([('id', '=', rec.get('id'))])
#                         line_search.unlink()

#                 elif rec.get('status') == True:
#                     if rec.get('name') != '':
#                         record = {
#                             'tipe_kunjungan': rec.get('tipe_kunjungan'),
#                             'jenis_inspeksi_id': rec.get('jenis_inspeksi_id'),
#                             'date': rec.get('date'),
#                             'lokasi': rec.get('lokasi'),
#                             'item_count': rec.get('item_count'),
#                             'group_visit_id': p.id,
#                         }
#                         request.env['vetting.report.line'].sudo().create(record)
#         return kw

#     @http.route(['/api/bpg_show_kunjungan'], type='json', method='GET', auth='user')
#     def show_kunjungan(self, **kw):
#         kunjungan = request.env['visit.management'].sudo().search([('id', '=', kw['id'])])
#         dict_kunjungan = {}
#         data_kunjungan = []
#         for wo in kunjungan:
#             dict_anggota_line = {}
#             data_anggota_line = []
#             dict_kunjungan_line = {}
#             data_kunjungan_line = []
#             dict_anggota_line = {}
#             data_anggota_line = []
#             imageVisit=False
#             if wo.image_1920:
#                 image_base_url = 'http://202.74.236.120:8069'
#                 # image_base_url = 'http://localhost:8069/'
#                 imageVisit = image_base_url + '/web/image?model=visit.management' + '&field=image_1920' + '&id=' + str(
#                     wo.id)

#             for ao in wo.anggota_id:
#                 dict_anggota_line = {
#                     'id': ao.id,
#                     'name': ao.name,
#                     'jabatan': ao.jabatan,
#                 }
#                 data_anggota_line.append(dict_anggota_line)

#             for line in wo.kunjungan_line:
#                 dict_finding = {}
#                 data_finding = []
#                 for fi in line.list_finding_item:
#                     image = False
#                     if fi.image_1920:
#                         image_base_url = 'http://202.74.236.120:8069'
#                         # image_base_url = 'http://localhost:8069/'
#                         image = image_base_url + '/web/image?model=finding.item' + '&field=image_1920' + '&id=' + str(
#                             fi.id)
#                     dict_finding = {
#                         'id': fi.id,
#                         'name': fi.name,
#                         'remark': fi.remark,
#                         'image_1920': image,
#                         'target_date': fi.target_date,
#                         'open_date': fi.open_date,
#                         'close_date': fi.close_date,
#                         'percentage': fi.percentage,
#                         'nama_pic': fi.penanggung_jawab.name,
#                         'nama_pic_id': fi.penanggung_jawab.id,
#                         'status': fi.status,
#                         'group_vetting_report_line_id': fi.group_vetting_report_line_id.id,
#                         'act': 'normal'
#                     }
#                     data_finding.append(dict_finding)

#                 dict_kunjungan_line = {
#                     'id': line.id,
#                     'name': line.name,
#                     'type_vessel': line.type_vessel,
#                     'tipe_kunjungan': line.tipe_kunjungan,
#                     'date': line.date,
#                     'lokasi': line.lokasi,
#                     'jenis_inspeksi_id': line.jenis_inspeksi_id,
#                     'group_visit_id': line.group_visit_id,
#                     'status': False,
#                     'item_count': line.item_count,
#                     'list_finding_item': data_finding,
#                     'act': 'normal'
#                 }
#                 data_kunjungan_line.append(dict_kunjungan_line)

#             dict_kunjungan = {
#                 'id': wo.id,
#                 'name': wo.name,
#                 'tipe_kunjungan': wo.tipe_kunjungan,
#                 'vessel_id': wo.vessel_id,
#                 'type_vessel': wo.type_vessel,
#                 'date': wo.date,
#                 'pic': wo.pic,
#                 'vendor': wo.vendor,
#                 'lokasi': wo.lokasi,
#                 'latitude': wo.latitude,
#                 'longitude': wo.longitude,
#                 'open_date': wo.open_date,
#                 'close_date': wo.close_date,
#                 'deadline_date': wo.deadline_date,
#                 'document': wo.document,
#                 'count_anggota': wo.count_anggota,
#                 'sisa_waktu': wo.sisa_waktu,
#                 'catatan': wo.catatan,
#                 'image_1920': imageVisit,
#                 'anggota_id': data_anggota_line,
#                 'kunjungan_line': data_kunjungan_line
#             }
#             # data_work_orders.append(dict_work_orders)
#         return dict_kunjungan

#     @http.route(['/api/bpg_show_detail_kunjungan'], type='json', method='GET', auth='user')
#     def show_detail_kunjungan(self, **kw):
#         detail_kunjungan = request.env['visit.management'].sudo().search([('id', '=', kw['id'])])
#         dict_kunjungan = {}
#         data_kunjungan = []
#         for wo in detail_kunjungan:
#             dict_kunjungan_line = {}
#             data_kunjungan_line = []

#             for line in wo.kunjungan_line:
#                 dict_finding = {}
#                 data_finding = []
#                 for fi in line.list_finding_item:
#                     dict_finding = {
#                         'id': fi.id,
#                         'name': fi.name,
#                         'remark': fi.remark,
#                         'target_date': fi.target_date,
#                         'open_date': fi.open_date,
#                         'close_date': fi.close_date,
#                         'percentage': fi.percentage,
#                         'nama_pic': fi.penanggung_jawab.name,
#                         'nama_pic_id': fi.penanggung_jawab.id,
#                         'status': fi.status,
#                         'group_vetting_report_line_id': fi.group_vetting_report_line_id,
#                         'act': 'normal'
#                     }
#                     data_finding.append(dict_finding)

#                 dict_kunjungan_line = {
#                     'id': line.id,
#                     'name': line.name,
#                     'type_vessel': line.type_vessel,
#                     'tipe_kunjungan': line.tipe_kunjungan,
#                     'date': line.date,
#                     'lokasi': line.lokasi,
#                     'jenis_inspeksi_id': line.jenis_inspeksi_id,
#                     'group_visit_id': line.group_visit_id,
#                     'status': line.status,
#                     'item_count': line.item_count,
#                     'list_finding_item': data_finding,
#                     'act': 'normal'
#                 }
#                 data_kunjungan_line.append(dict_kunjungan_line)

#             dict_kunjungan = {
#                 'id': wo.id,
#                 'name': wo.name,
#                 'tipe_kunjungan': wo.tipe_kunjungan,
#                 'vessel_id': wo.vessel_id,
#                 'type_vessel': wo.type_vessel,
#                 'date': wo.date,
#                 'pic': wo.pic,
#                 'vendor': wo.vendor,
#                 'deadline_date': wo.deadline_date,
#                 'sisa_waktu': wo.sisa_waktu,
#                 'catatan': wo.catatan,
#                 'kunjungan_line': data_kunjungan_line
#             }
#             # data_work_orders.append(dict_work_orders)
#         return dict_kunjungan

#     @http.route(['/api/bpg_create_kunjungan/'], type='json', method='POST', auth='user')
#     def create_kunjungan(self, **kw):
#         data = {}
#         if kw:
#             record = {
#                 'name': kw.get('name'),
#                 'tipe_kunjungan': kw.get('tipe_kunjungan'),
#                 'vessel_id': kw.get('vessel_id'),
#                 'type_vessel': kw.get('type_vessel'),
#                 'date': kw.get('date'),
#                 'pic': kw.get('pic'),
#                 'vendor': kw.get('vendor'),
#                 'lokasi': kw.get('lokasi'),
#                 'latitude': kw.get('latitude'),
#                 'longitude': kw.get('longitude'),
#                 'open_date': kw.get('open_date'),
#                 'close_date': kw.get('close_date'),
#                 'deadline_date': kw.get('deadline_date'),
#                 'document': kw.get('document'),
#                 'count_anggota': kw.get('count_anggota'),
#                 'sisa_waktu': kw.get('sisa_waktu'),
#                 'catatan': kw.get('catatan'),
#                 'image_1920': kw.get('image_1920'),
#             }
#             new = request.env['visit.management'].sudo().create(record)

#             for rec in kw['anggota_line']:
#                 if rec.get('name') != '':
#                     line = {
#                         'name': rec.get('name'),
#                         'jabatan': rec.get('jabatan'),
#                         'group_anggota_visit_id': new.id,
#                     }
#                     request.env['anggota.visit'].sudo().create(line)

#             for rec in kw['finding_line']:
#                 if rec.get('name') != '':
#                     line = {
#                         'tipe_kunjungan': rec.get('tipe_kunjungan'),
#                         'name': rec.get('name'),
#                         'jenis_inspeksi_id': rec.get('jenis_inspeksi_id'),
#                         'date': rec.get('date'),
#                         'lokasi': rec.get('lokasi'),
#                         'item_count': rec.get('item_count'),
#                         'status': rec.get('status'),
#                         'list_finding_item': rec.get('list_finding_item'),
#                         'group_visit_id': new.id,
#                     }
#                     request.env['vetting.report.line'].sudo().create(line)
#             data = {
#                 'id': new.id,
#                 'name': kw.get('name'),
#                 'tipe_kunjungan': kw.get('tipe_kunjungan'),
#                 'vessel_id': kw.get('vessel_id'),
#                 'type_vessel': kw.get('type_vessel'),
#                 'date': kw.get('date'),
#                 'pic': kw.get('pic'),
#                 'vendor': kw.get('vendor'),
#                 'lokasi': kw.get('lokasi'),
#                 'latitude': kw.get('latitude'),
#                 'longitude': kw.get('longitude'),
#                 'open_date': kw.get('open_date'),
#                 'close_date': kw.get('close_date'),
#                 'deadline_date': kw.get('deadline_date'),
#                 'document': kw.get('document'),
#                 'count_anggota': kw.get('count_anggota'),
#                 'sisa_waktu': kw.get('sisa_waktu'),
#                 'catatan': kw.get('catatan'),
#                 'image_1920': kw.get('image_1920'),
#             }
#         return data