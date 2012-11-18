import os
from pip.exceptions import DistributionNotFound
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.view import view_config
from utils import cached_graphs, generete_graph

@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    main_template = get_renderer('templates/main_template.pt').implementation()
    popular_searches = [os.path.splitext(i)[0] for i in cached_graphs()]
    return {'main_template': main_template,
            'popular_searches': set(popular_searches[:10]),
            }

@view_config(route_name='graph', renderer='templates/graph.pt')
def graph(request):
    main_template = get_renderer('templates/main_template.pt').implementation()
    package = request.params.get('package')
    package_filename = '.'.join((package, 'png'))
    cached = cached_graphs()
    if not package_filename in cached:
        try:
            generete_graph(package)
        except DistributionNotFound:
            raise HTTPFound(location='/package_not_found?package=%s' % package)
    popular_searches = [os.path.splitext(i)[0] for i in cached]
    template_vars = {'graph_path': '/graphs/%s' % package_filename,}
    template_vars.update(home(request))
    return template_vars

@view_config(route_name='package_not_found', renderer='templates/package_not_found.pt')
def package_not_found(request):
    """
    """
    package = request.params.get('package')
    template_vars = {'package': package,}
    template_vars.update(home(request))
    return template_vars
