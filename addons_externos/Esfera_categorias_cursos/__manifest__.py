{
    'name': 'Esfera inscripciones a cursos',
    'version': '1.0',
    'category': 'Ventas',
    'summary': 'Gestión de Inscripciones a cursos',
    'depends': ['base', 'sale', 'website_sale', 'product', 'account'],
    'data': [
        'views/slide_channel_inscripciones_views.xml',
        'views/product_template_views.xml',
        'views/slide_channel_tags_views.xml',
        'data/cron_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}