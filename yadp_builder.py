import yaml
import os.path
import jinja2

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

if __name__ == '__main__':
    with open('hosts.yml', 'r') as f:
        data = yaml.load(f, Loader)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader('./'))
    template_output = env.get_template('docker-hosts.groovy.tmpl').render(hosts=data)
    print(template_output)
    with open('configure-yadocker-cloud.groovy', 'w') as fw:
       fw.write(template_output)
