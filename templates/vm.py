
BASE_COMPUTE_URL = 'https://www.googleapis.com/compute/v1'

def BuildGlobalComputeUrl(project, collection, value):
    return ''.join([BASE_COMPUTE_URL, '/projects/', project, '/global/', collection, '/', value])

def BuildZonalComputeUrl(project, zone, collection, value):
    return ''.join([BASE_COMPUTE_URL, '/projects/', project, '/zones/', zone, '/', collection, '/', value])

def GenerateConfig(context):
    
    resources = []
    resources.append({
        'type': 'compute.v1.instance',
        'name': context.env['name'],
        'properties': {
            'zone': context.properties['zone'],
            'machineType': BuildZonalComputeUrl(context.env['project'], context.properties['zone'], 'machineTypes', 'f1-micro'),
            'metadata': {
                'items': [{
                    'key': 'gce-container-declaration',
                    'value': context.imports[context.properties['containerManifest']]
                }]
            },
            'disks': [{
                'deviceName': 'boot',
                'type': 'PERSISTENT',
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': BuildGlobalComputeUrl('cos-cloud', 'images', 'family/cos-stable')
                }
            }],
            'networkInterfaces': [{
                'accessConfigs': [{
                    'name': 'External NAT',
                    'type': 'ONE_TO_ONE_NAT'
                }]
            }],
            'serviceAccounts': [{
                'email': 'default',
                'scopes': [
                    "https://www.googleapis.com/auth/devstorage.read_only",
                    "https://www.googleapis.com/auth/logging.write",
                    "https://www.googleapis.com/auth/monitoring.write",
                    "https://www.googleapis.com/auth/servicecontrol",
                    "https://www.googleapis.com/auth/service.management.readonly",
                    "https://www.googleapis.com/auth/trace.append"
                ]
            }],
            'scheduling': {
                'automaticRestart': False
            },
            'startRestricted': False,
            'tags': {
                'items': ['http-server', 'https-server']
            }
        }
    })

    return {'resources': resources}