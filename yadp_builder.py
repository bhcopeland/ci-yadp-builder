import argparse
import yaml
import os.path
from jinja2 import FileSystemLoader, Environment
import jenkins
import logging

logging.basicConfig(level=logging.INFO)

class LoaderMeta(type):

    def __new__(metacls, __name__, __bases__, __dict__):
        """Add include constructer to class."""

        # register the include constructor on the class
        cls = super().__new__(metacls, __name__, __bases__, __dict__)
        cls.add_constructor('!include', cls.construct_include)

        return cls


class Loader(yaml.Loader, metaclass=LoaderMeta):
    """YAML Loader with `!include` constructor."""

    def __init__(self, stream):
        """Initialise Loader."""

        try:
            self._root = os.path.split(stream.name)[0]
        except AttributeError:
            self._root = os.path.curdir

        super().__init__(stream)

    def construct_include(self, node):
        """Include file referenced at node."""

        filename = os.path.abspath(os.path.join(
            self._root, self.construct_scalar(node)
        ))
        extension = os.path.splitext(filename)[1].lstrip('.')

        with open(filename, 'r') as f:
            if extension in ('yaml', 'yml'):
                return yaml.load(f, Loader)
            else:
                return ''.join(f.readlines())

def jinja2_from_template(directory, template_name, data):
    loader = FileSystemLoader(directory)
    env = Environment(loader=loader)
    template = env.get_template(template_name)
    return template.render(hosts=data)

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', type=str, required=True, help='Username for Jenkins server')
    parser.add_argument('-p', '--password', type=str, required=True, help='Password for Jenkins server')
    parser.add_argument('-i', '--inventory', type=str, required=True, default='hosts.yml', help='specify inventory host path')
    return parser

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    with open(args.inventory, 'r') as f:
        data = yaml.load(f, Loader)
    template_output = jinja2_from_template('./templates', 'configure-yadocker-cloud.groovy.j2', data)
    server = jenkins.Jenkins('http://localhost:8080', username=args.username, password=args.password)
    info = server.run_script(template_output)
    logging.info(info)

