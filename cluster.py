import os
import os.path as path
import logging
import json
import requests
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

LOG = logging.getLogger(__name__)

PEERS_FILE = os.getenv('PEERS_FILE', '/etc/sysconfig/etcd-peers')
CLIENT_SCHEME = os.getenv('CLIENT_SCHEME', 'http')
PEER_SCHEME = os.getenv('PEER_SCHEME', 'http')
CLIENT_PORT = int(os.getenv('CLIENT_PORT', 2379))
PEER_PORT = int(os.getenv('PEER_PORT', 2380))
MAX_RETRIES = int(os.getenv('MAX_RETRIES', 10))

credentials = GoogleCredentials.get_application_default()
service = discovery.build('compute', 'v1', credentials=credentials)

class Instance:
    """
    Get the details of the current instance from metadata.
    """
    def __init__(self):
        def request_metadata(path):
            response = requests.get('http://metadata.google.internal{}'.format(path), headers={'Metadata-Flavor': 'Google'}).text
            response.strip()
            return response

        def get_instance():
            LOG.debug("Fetching instance metadata")
            project_id = request_metadata('/0.1/meta-data/project-id')
            zone = request_metadata('/computeMetadata/v1/instance/zone')
            name = request_metadata('/computeMetadata/v1/instance/name')
            LOG.debug("Fetching instance")
            request = service.instances().get(project=project, zone=zone, instance=name)
            return json.loads(request.execute())

        self.instance = get_instance()

        LOG.info('This instance is [name: %s, id: %s, ip: %s, zone: %s, project_id: %s]', self.name, self.id, self.ip, self.zone, self.project_id)
        LOG.debug("Done fetching instance metadata")

    @property
    def instance_group():
        self.instance["meta-data"]

    def get_instance_group_peers():
        request = service.instanceGroups().listInstances(project=project, zone=zone, instanceGroup=instanceGroup, body={})
        return json.loads(request.execute())


class InstanceGroupManager:
    """docstring for InstanceGroupPeers"""
    def __init__(self, name):


class InstanceGroupMembers:
    """docstring for InstanceGroupPeers"""
    def __init__(self, ):


# class EtcdNode(object):
#     """docstring for EtcdNode"""
#     def __init__(self, arg):
#         super(EtcdNode, self).__init__()
#         self.arg = arg



# class EtcdCluster(object):
#     """docstring for EtcdCluster"""
#     def __init__(self, arg):
#         super(EtcdCluster, self).__init__()
#         self.arg = arg


def main():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)s - %(message)s')
    ch.setFormatter(formatter)
    LOG.addHandler(ch)
    LOG.propagate = False

    LOG.info('starting etcd cluster search')

    if path.isfile(PEERS_FILE):
        LOG.info('Peers file %s already exists', PEERS_FILE)
        return

    instance = Instance()
    instance_group = InstanceGroupPeers(instance_id=instance.id)


    # group = LocalGroup(metadata.instance_id)
    # cluster = EtcdCluster(group.peer_nodes(), metadata.instance_id, metadata.instance_ip)
    # if cluster.existing_cluster:
    #     cluster.eject_orphans()
    #     cluster.join()
    # else:
    #      cluster.create()

    # with open(PEERS_FILE, 'w') as peers_file:
    #     cluster.write_cluster_variables(peers_file)

    LOG.info('Done')

if __name__ == '__main__':
    main()
