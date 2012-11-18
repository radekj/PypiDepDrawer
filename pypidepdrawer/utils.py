import os
from pyramid.config import Configurator
from gluttony import gluttony
import pygraphviz as pgv

def get_graphs_path():
    config = Configurator()
    path = os.path.join(config.package.__path__[0], 'graphs')
    return path

def cached_graphs():
    """
    """
    path = get_graphs_path()
    return os.listdir(path)

def generete_dot_file(package):
    """
    """
    dot_filename = '.'.join((package, 'dot'))
    graphs_path = get_graphs_path()
    dot_file_path = os.path.join(graphs_path, dot_filename)
    args = [package, '--pydot', dot_file_path]
    gluttony_command = gluttony.Command()
    gluttony_command.main(args)
    return dot_file_path

def generete_graph(package):
    """
    """
    dot_file_path = generete_dot_file(package)
    G = pgv.AGraph(dot_file_path)

    png_filename = '.'.join((package, 'png'))
    graphs_path = get_graphs_path()
    png_file_path = os.path.join(graphs_path, png_filename)
    G.draw(os.path.join(graphs_path, png_file_path), prog='dot')
