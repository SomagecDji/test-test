{
    'name': "Documents custom",

    'summary': "Document management",

    'description': """
        App to upload and manage your documents.
    """,

    'author': "Odoo",
    'category': 'Operations/Documents',
    'version': '1.0',
    'application': True,
    'website': 'https://www.odoo.com/page/documents',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'portal', 'web', 'attachment_indexation','documents'],

    # always loaded
    'data': [
        'views/templates.xml',
        'views/inherit_project_workspace_view.xml',
        'views/inherit_project_workspace_country_view.xml'
    ],

}
