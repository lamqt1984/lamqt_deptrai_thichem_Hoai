{
    'name': 'Pdf Report auto attachment',
    'summary': 'Automatically attach PDF file when you download PDF Reports on odoo system. If you can not find the old reports, you can download again',
    'version': '1.0',
    'category': '',
    'description': """
		All pdf reports on odoo use
			+ Qweb report
			+ Jasper report
			+ Webkit report
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
