import argparse
import yaml
import os.path
from jinja2 import FileSystemLoader, Environment
import jenkins
import logging


class Loader(yaml.Loader):

    def __init__(self, *args, **kwargs):
        super(Loader, self).__init__(*args, **kwargs)
        self.add_constructor('!include', type(self).construct_include)
        try:
            self._root = os.path.split(self)[0]
        except AttributeError:
            self._root = os.path.curdir

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
    parser.add_argument('-u', '--username', type=str, required=True,
                        help='Username for Jenkins server')
    parser.add_argument('-p', '--password', type=str, required=True,
                        help='Password for Jenkins server')
    parser.add_argument('-s', '--server', type=str,
                        default='http://localhost:8080',
                        help='Jenkins server URL. e.g. http://localhost:8080')
    parser.add_argument('-i', '--inventory', type=str, default='hosts.yml',
                        help='specify inventory host path')
    parser.add_argument('-l', '--loglevel', default='INFO',
                        help="Setting logging level, default: %(default)s")
    parser.add_argument('--dryrun', action='store_true',
                        help='Do not publish to Jenkins')
    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    with open(args.inventory, 'r') as f:
        data = yaml.load(f, Loader)
    logging.debug(data)
    template_output = jinja2_from_template(
                      './templates',
                      'configure-yadocker-cloud.groovy.j2', data)
    server = jenkins.Jenkins(args.server, username=args.username,
                             password=args.password)
    if args.dryrun:
        with open('/tmp/configure-yadocker-cloud.groovy', 'w') as fw:
            fw.write(template_output)
        template_output = jinja2_from_template(
                          './templates',
                          'configure-yadocker-cloud.groovy-dryrun.j2', data)

        publishdry = server.run_script(template_output)
        if 'error' in publishdry:
            logging.info(publishdry)
            exit(1)
        logging.info(publishdry)
    else:
        publish = server.run_script(template_output)
        logging.info(publish)
