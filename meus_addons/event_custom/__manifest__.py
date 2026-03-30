{
    'name': 'Customização de Eventos - Grupos',
    'version': '1.0.1',
    'category': 'Marketing',
    'depends': ['event'],  # Importante: depende do módulo oficial de eventos
    'data': [
        'views/event_event_views.xml',
        'views/event_templates.xml', 
            ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}