from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/index.mak')
def on_page_load(request):
    return {'project': 'checksftp'}

@view_config(route_name='runthecheck', renderer='json')
def on_run_check(request):
    return {'message': 'Testing 123...'}
