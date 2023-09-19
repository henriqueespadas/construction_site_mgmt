{
    'name': 'Construction Site Management',
    'version': '14.0.1.0.0',
    'category': 'Operations/Construction',
    'license': 'AGPL-3',
    'summary': 'Advanced management features for construction sites',
    'author': 'Espadas',
    'depends': [
        'hr',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/actions.xml',
        'views/menus.xml',
        'views/construction_shifit_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
