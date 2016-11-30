__author__ = 'LamQT lamqt@hanelsoft.vn'
from openerp import models, fields, api
from openerp.osv import osv
import base64
import time

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
            
        return res 
        