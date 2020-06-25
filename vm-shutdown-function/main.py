from google.cloud import monitoring_v3
from google.cloud.monitoring_v3 import query
from googleapiclient import discovery
import config
import logging

service = discovery.build('compute', 'v1', cache_discovery=False)

logging.basicConfig(level=logging.DEBUG)


def auto_shutdown(args):
    # notebook_vms = get_notebook_vms()
    instances = monitor_vms()

    for vm in instances:
        logging.debug(f"Checking {vm.metric.labels['instance_name']}")
        # if vm.metric.labels['instance_name'] in notebook_vms:
        points = [x.value.double_value * 100 for x in vm.points]
        if max(points) < config.min_cpu_usage_percent:
            shutdown(vm.metric.labels['instance_name'])


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
