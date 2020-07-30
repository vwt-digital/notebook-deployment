from googleapiclient import discovery
import config
import logging
from datetime import datetime

service = discovery.build('compute', 'v1', cache_discovery=False)

logging.basicConfig(level=logging.DEBUG)


def auto_remove(args):
    request = service.instances().list(project=config.project, zone=config.zone)
    while request is not None:
        response = request.execute()

        for instance in response['items']:
            print(instance['name'])
            print(instance['status'])
            d = {x['key']: x['value'] for x in instance['metadata']['items']}
            date_str = d.get("last-active")
            if date_str:
                date_object = datetime.strptime(date_str, '%Y-%m-%d').date()
                print(date_object)
                days_since_last_active = (datetime.now().date() - date_object).days
                if days_since_last_active > config.turned_off_days:
                    delete_request = service.instances().delete(project=config.project,
                                                                zone=config.zone,
                                                                instance=instance['name'])
                    delete_request.execute()
        request = service.instances().list_next(previous_request=request, previous_response=response)
