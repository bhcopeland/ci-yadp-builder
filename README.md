Yet Another Docker Plugin config builder
=======

Yet Another Docker Plugib (yadp) is extremely hard to manage, when running multiple slaves with multiple images. Due to the way Jenkins displays the configuration page. YADP provides a [groovy script](https://github.com/KostyaSha/yet-another-docker-plugin/blob/master/docs/script-console-scripts/configure-yadocker-cloud.groovy) which builds a json array to populate the config in Jenkins.

This script uses yaml and jinja2 to generate a java jsonarray to build the configuration, using a !include constructor in the yaml file, allowing the ability to template up docker_images, since many of our slaves run the same image, it lessens repetition.

Usage
=======

####hosts.yml
List your jenkin_slaves here
```
- host1:
  cloud_name: host1.example.org
  docker-url: tcp://0.0.0.0:2375
  docker_templates: !include external_template_file.yml

- host2:
  cloud_name: host2
  docker-url: tcp://0.0.0.1:2375
  docker_templates:
    - xenial-amd64:
      docker_image_name: 'ubuntu:latest'
      max_instances: '1'
      labels: 'docker-ubuntu'
```
