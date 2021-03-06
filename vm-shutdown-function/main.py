import time

from google.cloud import monitoring_v3
from google.cloud.monitoring_v3 import query
from googleapiclient import discovery
import config
import logging
from datetime import datetime

service = discovery.build('compute', 'v1', cache_discovery=False)

logging.basicConfig(level=logging.DEBUG)


def auto_shutdown(args):
    try:
        # notebook_vms = get_notebook_vms()
        instances = monitor_vms()
        logging.info(f"Checking {len(list(instances))} instances for activity.")

        for vm in instances:
            logging.info(f"Checking {vm.metric.labels['instance_name']}")
            # if vm.metric.labels['instance_name'] in notebook_vms:
            points = [x.value.double_value * 100 for x in vm.points]
            if max(points) < config.min_cpu_usage_percent:
                logging.info(f"{vm.metric.labels['instance_name']} was not recently active.")

                instance_name = vm.metric.labels['instance_name']
                set_last_active(instance_name)
                shutdown(instance_name)
            else:
                logging.info(f"{vm.metric.labels['instance_name']} was recently active: {max(points)}%")
    except Exception as e:
        logging.error(e, exc_info=True)
        time.sleep(5)


def set_last_active(instance_name):
    logging.info(f"setting last active date for {instance_name}")
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
    result = service.instances().setMetadata(project=config.project,
                                             zone=config.zone,
                                             instance=instance_name,
                                             body=meta_data_body).execute()

    logging.info("Added last active date")

    logging.info(f"{result}")


def shutdown(instance):
    logging.info(f"Shutting down {instance}...")
    request = service.instances().stop(project=config.project, zone=config.zone, instance=instance)
    request.execute()
    logging.info(f"{instance} shut down.")


def monitor_vms():
    logging.info("Checking active time of the vms")
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
