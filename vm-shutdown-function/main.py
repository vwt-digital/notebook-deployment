import googleapiclient.http
from google.cloud import monitoring_v3
from google.cloud.monitoring_v3 import query
from googleapiclient import discovery
import config
import logging
from datetime import datetime

service = discovery.build('compute', 'v1', cache_discovery=False)

logging.basicConfig(level=logging.DEBUG)


def auto_shutdown(args):
    # notebook_vms = get_notebook_vms()
    instances = monitor_vms()
    logging.info(f"Found {instances} to shutdown")

    for vm in instances:
        logging.debug(f"Checking {vm.metric.labels['instance_name']}")
        # if vm.metric.labels['instance_name'] in notebook_vms:
        points = [x.value.double_value * 100 for x in vm.points]
        if max(points) < config.min_cpu_usage_percent:
            instance_name = vm.metric.labels['instance_name']
            shutdown(instance_name)
            set_last_active(instance_name)


def set_last_active(instance_name):
    instance = service.instances().get(project=config.project,
                                       zone=config.zone,
                                       instance=instance_name).execute()

    meta_data_body = {
        'fingerprint': instance['metadata']['fingerprint'],
        'items': [
            x for x in instance['metadata']['items'] if x['key'] != "last-active"
        ],
        'kind': 'compute#metadata'

    }
    meta_data_body['items'].append({"key": "last-active", "value": datetime.today().strftime('%Y-%m-%d')})
    result: googleapiclient.http.HttpRequest = service.instances().setMetadata(project=config.project,
                                                                               zone=config.zone,
                                                                               instance=instance_name,
                                                                               body=meta_data_body)

    logging.info("Added last active date")

    logging.info(f"{result.body}")


def shutdown(instance):
    logging.info(f"Shutting down {instance}...")
    request = service.instances().stop(project=config.project, zone=config.zone, instance=instance)
    request.execute()
    logging.info(f"{instance} shut down.")


def monitor_vms():
    client = monitoring_v3.MetricServiceClient()
    cpu_query = query.Query(client,
                            project=config.project,
                            metric_type='compute.googleapis.com/instance/cpu/utilization',
                            minutes=config.inactive_time_minutes)
    return cpu_query


def get_notebook_vms():
    """Returns a list of instance-ids that are a notebook.
    An instance is a notebook when it has the tag 'deeplearning-vm'"""
    notebook_vms = []

    request = service.instances().list(project=config.project, zone=config.zone)
    while request is not None:
        response = request.execute()

        for instance in response['items']:
            if instance['tags']['items'] and 'deeplearning-vm' in instance['tags']['items']:
                notebook_vms.append(instance['name'])

        request = service.instances().list_next(previous_request=request, previous_response=response)

    return notebook_vms
