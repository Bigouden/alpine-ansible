#!/usr/bin/env python3
#coding: utf-8

'''Ansible Exporter'''

import json
import logging
import os
import sys
import time
from datetime import datetime
from io import StringIO
import ansible.cli.galaxy
import pytz
from ansible import context as ansible_context
from ansible import __version__ as ansible_core_version
from ansiblelint import __version__ as ansible_lint_version
from prometheus_client.core import REGISTRY, Metric
from prometheus_client import start_http_server, PROCESS_COLLECTOR, PLATFORM_COLLECTOR

ANSIBLE_EXPORTER_NAME = os.environ.get('ANSIBLE_EXPORTER_NAME',
                                       'ansible-exporter')
ANSIBLE_EXPORTER_LOGLEVEL = os.environ.get('ANSIBLE_EXPORTER_LOGLEVEL',
                                           'INFO').upper()
ANSIBLE_EXPORTER_TZ = os.environ.get('TZ', 'Europe/Paris')

# Logging Configuration
try:
    pytz.timezone(ANSIBLE_EXPORTER_TZ)
    logging.Formatter.converter = lambda *args: \
                                  datetime.now(tz=pytz.timezone(ANSIBLE_EXPORTER_TZ)).timetuple()
    logging.basicConfig(stream=sys.stdout,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S',
                        level=ANSIBLE_EXPORTER_LOGLEVEL)
except pytz.exceptions.UnknownTimeZoneError:
    logging.Formatter.converter = lambda *args: \
                                  datetime.now(tz=pytz.timezone('Europe/Paris')).timetuple()
    logging.basicConfig(stream=sys.stdout,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S',
                        level='INFO')
    logging.error("TZ invalid : %s !", ANSIBLE_EXPORTER_TZ )
    os._exit(1)
except ValueError:
    logging.basicConfig(stream=sys.stdout,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%d/%m/%Y %H:%M:%S',
                        level='INFO')
    logging.error("ANSIBLE_EXPORTER_LOGLEVEL invalid !")
    os._exit(1)

# Check ANSIBLE_EXPORTER_PORT
try:
    ANSIBLE_EXPORTER_PORT = int(os.environ.get('ANSIBLE_EXPORTER_PORT', '8123'))
except ValueError:
    logging.error("ANSIBLE_EXPORTER_PORT must be int !")
    os._exit(1)

ANSIBLE_COLLECTIONS_PATHS = os.environ.get('ANSIBLE_COLLECTIONS_PATHS',
                                           '/usr/share/ansible/collections')

METRICS = [
    {'name': 'ansible_core',
     'description': 'Ansible Core Information',
     'type': 'gauge'},
    {'name': 'ansible_lint',
     'description': 'Ansible Lint Information',
     'type': 'gauge'},
    {'name': 'ansible_collection',
     'description': 'Ansible Collection Information',
     'type': 'gauge'}
]

# REGISTRY Configuration
REGISTRY.unregister(PROCESS_COLLECTOR)
REGISTRY.unregister(PLATFORM_COLLECTOR)
REGISTRY.unregister(REGISTRY._names_to_collectors['python_gc_objects_collected_total'])

ARGS = ('collection', 'list',)
CLIARGS = {'version': None,
           'verbosity': 0,
           'type': ARGS[0],
           'action': ARGS[1],
           'api_server': None,
           'api_key': None,
           'ignore_certs': None,
           'timeout': None,
           'collections_path': (ANSIBLE_COLLECTIONS_PATHS,),
           'collection': None,
           'output_format': 'json',
           'validate_certs': None
          }

class AnsibleCollector():
    '''Ansible Collector Class'''
    def __init__(self):
        self.metrics = []
        self.metrics.append({'name': 'ansible_core',
                             'labels': {'version': ansible_core_version}} | METRICS[0])
        self.metrics.append({'name': 'ansible_lint',
                             'labels': {'version': ansible_lint_version}} | METRICS[1])
        self.metrics.extend(self.get_ansible_collections())

    def get_ansible_collections(self):
        '''Retrieve Ansible Collections Informations'''
        collections = []
        ansible_galaxy = ansible.cli.galaxy.GalaxyCLI(ARGS)
        ansible_context.CLIARGS = CLIARGS
        ansible_buffer = StringIO()
        sys.stdout = ansible_buffer
        ansible_galaxy.execute_list()
        res = json.loads(ansible_buffer.getvalue())
        sys.stdout = sys.__stdout__
        for name, version in res[f"{ANSIBLE_COLLECTIONS_PATHS}/ansible_collections"].items():
            collections.append({'name': 'ansible_collection',
                                'labels': {'name': name,
                                           'version': version['version']}
                               } | METRICS[2])
        return collections

    def collect(self):
        '''Collect Prometheus Metrics'''
        labels = {'job': ANSIBLE_EXPORTER_NAME}
        for metric in self.metrics:
            labels |= metric['labels']
            prometheus_metric = Metric(metric['name'], metric['description'], metric['type'])
            prometheus_metric.add_sample(metric['name'],
                                         value=1,
                                         labels=labels)
            yield prometheus_metric

def main():
    '''Main Function'''
    logging.info("Starting Ansible Exporter on port %s.", ANSIBLE_EXPORTER_PORT)
    logging.debug("ANSIBLE_EXPORTER_PORT: %s.", ANSIBLE_EXPORTER_PORT)
    logging.debug("ANSIBLE_EXPORTER_NAME: %s.", ANSIBLE_EXPORTER_NAME)
    AnsibleCollector()
    # Start Prometheus HTTP Server
    start_http_server(ANSIBLE_EXPORTER_PORT)
    # Init AnsibleCollector
    REGISTRY.register(AnsibleCollector())
    # Infinite Loop
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
