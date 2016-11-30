{
    'name': 'Pdf Report auto attachment',
    'summary': 'Automatically attach PDF file when you download PDF Reports on odoo system. You can not find the old reports, you can go menu "Auto Attached PDF Report" to download again',
    'version': '1.0',
    'category': '',
    'description': """
            All pdf reports on odoo use qweb report. If you use Jasper Report, we can send to you additional package for auto attach with this for FREE
    """,
    'author': "HanelSoft",
    'website': 'http://www.hanelsoft.vn/',
    'depends': ['sale', 'stock', 'account', 'purchase'],
    'data': ['attached_pdf_report.xml'],
    'js': [],
    'installable': True,
    'auto_install': False,
    'application': False,
    'currency': 'EUR',
    'price': 399
}
