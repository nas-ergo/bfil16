{
    'name' : 'BFIL_MRP_CUSTOMIZATION',
    'version' : '1.0.1',
    'author' : 'rifat',
    'category' : 'Manufacturing',
    'sequence' : 1,
    'summary' : 'BFIL_MRP_CUSTOMIZATION',
    'description' : '',
    'depends' : ['base', 'mrp', 'mrp_workorder'],
    'data' : [
        'security/ir.model.access.csv',
        'data/resume_email_template.xml',
        'data/without_resume_email_template.xml',
        'views/work_center.xml',
        'views/mrp_routing_workcenter_views_inherited.xml',
        'wizard/resume_pop.xml',
    ],
    'demo' : [],
    'installable' : True,
    'application': True,
    'auto_install' : False,
    'asset' : {},
}