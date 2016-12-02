__author__ = 'LamQT lamqt@hanelsoft.vn'
from openerp import models, fields, api
from openerp.osv import osv
import base64
import time
import logging
import threading
import openerp.report


class PdfAttachment(models.Model):
    _name = 'pdf.attachment'
    
    name = fields.Char(string='Report Name')
    date = fields.Datetime(string='Date Download')
    model_name = fields.Char(string='Model Name')
    id_obj = fields.Char(string='IDs')
    attachment_ids = fields.Many2many('ir.attachment', 'pdf_attachment_relation', 'pdf_template_id', 'attachment_id', string= 'Attachments')
    user_id = fields.Many2one('res.users', string='User')

class PdfReport(osv.Model):
    _inherit = "report"
    
    @api.v7
    def get_pdf(self, cr, uid, ids, report_name, html=None, data=None, context=None):
        res = super(PdfReport, self).get_pdf(cr, uid, ids, report_name, html=html, data=data, context=context)
        if ids:
            report_xml = self.pool.get('ir.actions.report.xml')
            ir_attachment = self.pool.get('ir.attachment')
            report_xml_obj = report_xml.search(cr, uid, [('report_name','=',report_name)])
            report_xml_model = report_xml.browse(cr, uid, report_xml_obj[0]).model
            file_pdf = base64.encodestring(res)
            attachment_data = {
                           'name': report_name + '.pdf',
                           'datas_fname': report_name.replace(':', '_') + '.pdf',
                           'datas': file_pdf,
                           'type': 'binary',
                           }
            fields_obj = ir_attachment.create(cr, uid, attachment_data, context=context)
            mang_id = []
            mang_id.append(fields_obj)
            date = time.strftime("%Y-%m-%d %H:%M:%S")
            pdf_attachment = self.pool.get('pdf.attachment')
            vals = {
                    'name': report_name + '.pdf',
                    'date': date,
                    'model_name': report_xml_model,
                    'id_obj': str(sorted(ids)).replace('[', '').replace(']', ''),
                    'user_id': uid,
                    'attachment_ids': [(6, 0, mang_id)],
                    }
            pdf_attachment.create(cr, uid, vals, context=context)
        else:
            ir_attachment = self.pool.get('ir.attachment')
            file_pdf = base64.encodestring(res)
            attachment_data = {
                           'name': report_name + '.pdf',
                           'datas_fname': report_name.replace(':', '_') + '.pdf',
                           'datas': file_pdf,
                           'type': 'binary',
                           }
            fields_obj = ir_attachment.create(cr, uid, attachment_data, context=context)
            mang_id = []
            mang_id.append(fields_obj)
            date = time.strftime("%Y-%m-%d %H:%M:%S")
            pdf_attachment = self.pool.get('pdf.attachment')
            vals = {
                    'name': report_name + '.pdf',
                    'date': date,
                    'model_name': '',
                    'id_obj': '',
                    'user_id': uid,
                    'attachment_ids': [(6, 0, mang_id)],
                    }
            pdf_attachment.create(cr, uid, vals, context=context)
            
        return res 

_logger = logging.getLogger(__name__)

self_reports = {}
self_id = 0
self_id_protect = threading.Semaphore()

original_exp_report_new = openerp.service.report.exp_report

def exp_report(db, uid, object, ids, datas=None, context=None):
    cr = openerp.registry(db).cursor()
    result, format = openerp.report.render_report(cr, uid, ids, object, datas, context)
    if result and format == 'pdf' and len(ids) == 1:
        from openerp.api import Environment 
        env = Environment(cr, uid, context)
        ir_attachment = env['ir.attachment']
        ir_xml_obj = env['ir.actions.report.xml']
        ir_result = ir_xml_obj.search([('report_name', '=', object)])
        abc = False
        if ir_result:
            abc = ir_result.name
        active_model = context.get('active_model', False)
        id_report = context.get('active_ids', False)
        p_obj = env[active_model].browse(id_report[0])
        if active_model == 'account.invoice':
            report_name = p_obj.internal_number or abc or '_'
        elif active_model in ['sale.oder', 'stock.picking', 'purchase.order']:
            report_name = p_obj.name or abc or '_' 
        else:
            report_name = abc or p_obj.name or '_' 
        file_pdf = base64.encodestring(result)
        
        attachment_data = {
                           'name': (abc or report_name) + '.pdf',
                           'datas_fname': report_name.replace(':', '_') + '.pdf',
                           'datas': file_pdf,
                           'type': 'binary',
                           }
        fields_obj = ir_attachment.create(attachment_data)
        mang_id = []
        for i in fields_obj:
            mang_id.append(i.id)
        
        date = time.strftime("%Y-%m-%d %H:%M:%S")
        pdf_attachment = env['pdf.attachment']
        vals = {
                'name': report_name + '.pdf',
                'date': date,
                'model_name': active_model,
                'id_obj': id_report,
                'user_id': uid,
                'attachment_ids': [(6, 0, mang_id)],
                }
        id_att = pdf_attachment.create(vals)
            
        cr.commit()
        if id_att.id > 1:
            check = id_att.id-1
            check_obj = pdf_attachment.search([('id', '=', check)])
            if check_obj:
                id_check = pdf_attachment.browse(check)
                if id_att.name == id_check.name and id_att.model_name == id_check.model_name and id_att.id_obj == id_check.id_obj:
                    id_att.unlink()
                    cr.commit()
    return original_exp_report_new(db, uid, object, ids, datas, context)
    
openerp.service.report.exp_report = exp_report
