{
        "name" : "marsans",
        "version" : "0.1",
        "author" : "Castillo",
        "website" : "http://openerp.com",
        "category" : "Tools",
        "description": """ With this module you can manage hotels, cities and routes. 
It also offers a calendar and a tool for finding hotels or scales too expensive.  """,
        "depends" : ['base','report_webkit','product','sale'],
        "init_xml" : [ ],
        "demo_xml" : [ ],
        "update_xml" : ['marsans_view.xml', 'marsans_report.xml', 'report/header_marsans.xml'],
        "installable": True
}
