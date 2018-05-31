def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('authenticate', '/authenticate')
    config.add_route('create_view', '/create')
    config.add_route('create_secret', '/create/{username}')

