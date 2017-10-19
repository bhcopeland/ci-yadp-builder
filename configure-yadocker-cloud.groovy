JSONArray clouds_yadocker = [ 
  [
    cloud_name: 'x86_64-07',
    docker_url: 'tcp://0.0.0.0:2375',
    max_containers: '1',
    docker_templates: [
      // List item of templates 
      [
         docker_image_name: 'linaro/xenial',
         max_instances: '1',
         labels: 'docker-xenial docker-xenial-amd64 docker-xenial-amd64-08',
      ],

      [
         docker_image_name: 'linaro/utopic',
         max_instances: '10',
         labels: 'docker-utopic docker-utopic-amd64 docker-utopic-amd64-08',
      ],

      ],
    ],

  [
    cloud_name: 'lhg-01',
    docker_url: '',
    max_containers: '',
    docker_templates: [
      // List item of templates 
      [
         docker_image_name: 'linaro/xenial',
         max_instances: '1',
         labels: 'docker-xenial-lhg',
      ],

      ],
    ],

  ] as JSONArray