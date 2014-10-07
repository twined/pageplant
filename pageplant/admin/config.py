from django.core.urlresolvers import reverse_lazy


APP_ADMIN_URLS = {
    'url_base': 'pageplant',
    'namespace': 'pageplant',
}

APP_ADMIN_MENU = {
    # for the posts section
    'Sider': {
        'anchor': 'pages',
        'bgcolor': '#65BD77',
        'icon': 'fa fa-file-text icon',

        'menu': {
            'Oversikt': {
                'url': reverse_lazy('admin:pageplant:list'),
                'icon': 'glyphicon glyphicon-th-list',
                'order': 0,
            },
            'Ny side': {
                'url': reverse_lazy('admin:pageplant:create'),
                'icon': 'glyphicon glyphicon-plus-sign',
                'order': 1,
            },
            'Sidebilder': {
                'url': reverse_lazy('admin:pageplant:pageimage-list'),
                'icon': 'glyphicon glyphicon-th-list',
                'order': 2,
            },
            'Last opp sidebilder': {
                'url': reverse_lazy('admin:pageplant:pageimage-create'),
                'icon': 'glyphicon glyphicon-picture',
                'order': 3,
            },
        }
    }
}
