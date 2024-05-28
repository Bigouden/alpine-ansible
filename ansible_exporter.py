#!/usr/bin/env python3
# coding: utf-8
# pyright: reportMissingImports=false

"""Ansible Exporter"""

import json
import logging
import os
import sys
import threading
import time
import warnings
from datetime import datetime
from io import StringIO
from typing import Callable
from wsgiref.simple_server import make_server

import ansible.cli.galaxy
import pytz
from ansible import __version__ as ansible_core_version
from ansible import context as ansible_context
from ansible.plugins.loader import init_plugin_loader
from ansiblelint import __version__ as ansible_lint_version
from prometheus_client import PLATFORM_COLLECTOR, PROCESS_COLLECTOR
from prometheus_client.core import REGISTRY, CollectorRegistry, Metric
from prometheus_client.exposition import _bake_output, _SilentHandler, parse_qs

LOGFMT = "%(asctime)s - %(levelname)s - %(message)s"
DATEFMT = "%d/%m/%Y %H:%M:%S"

# Ignore Ansible Warning
warnings.filterwarnings("ignore")

ANSIBLE_EXPORTER_NAME = os.environ.get("ANSIBLE_EXPORTER_NAME", "ansible-exporter")
ANSIBLE_EXPORTER_LOGLEVEL = os.environ.get("ANSIBLE_EXPORTER_LOGLEVEL", "INFO").upper()
ANSIBLE_EXPORTER_TZ = os.environ.get("TZ", "Europe/Paris")


def make_wsgi_app(
    registry: CollectorRegistry = REGISTRY, disable_compression: bool = False
) -> Callable:
    """Create a WSGI app which serves the metrics from a registry."""

    def prometheus_app(environ, start_response):
        # Prepare parameters
        accept_header = environ.get("HTTP_ACCEPT")
        accept_encoding_header = environ.get("HTTP_ACCEPT_ENCODING")
        params = parse_qs(environ.get("QUERY_STRING", ""))
        headers = [
            ("Server", ""),
            ("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0"),
            ("Pragma", "no-cache"),
            ("Expires", "0"),
            ("X-Content-Type-Options", "nosniff"),
        ]
        if environ["PATH_INFO"] == "/":
            status = "301 Moved Permanently"
            headers.append(("Location", "/metrics"))
            output = b""
        elif environ["PATH_INFO"] == "/favicon.ico":
            status = "200 OK"
            output = b""
        elif environ["PATH_INFO"] == "/metrics":
            status, tmp_headers, output = _bake_output(
                registry,
                accept_header,
                accept_encoding_header,
                params,
                disable_compression,
            )
            headers += tmp_headers
        else:
            status = "404 Not Found"
            output = b""
        start_response(status, headers)
        return [output]

    return prometheus_app


def start_wsgi_server(
    port: int,
    addr: str = "0.0.0.0",  # nosec B104
    registry: CollectorRegistry = REGISTRY,
) -> None:
    """Starts a WSGI server for prometheus metrics as a daemon thread."""
    app = make_wsgi_app(registry)
    httpd = make_server(addr, port, app, handler_class=_SilentHandler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()


start_http_server = start_wsgi_server

# Logging Configuration
try:
    pytz.timezone(ANSIBLE_EXPORTER_TZ)
    logging.Formatter.converter = lambda *args: datetime.now(
        tz=pytz.timezone(ANSIBLE_EXPORTER_TZ)
    ).timetuple()
    logging.basicConfig(
        stream=sys.stdout,
        format=LOGFMT,
        datefmt=DATEFMT,
        level=ANSIBLE_EXPORTER_LOGLEVEL,
    )
except pytz.exceptions.UnknownTimeZoneError:
    logging.Formatter.converter = lambda *args: datetime.now(
        tz=pytz.timezone("Europe/Paris")
    ).timetuple()
    logging.basicConfig(
        stream=sys.stdout,
        format=LOGFMT,
        datefmt=DATEFMT,
        level="INFO",
    )
    logging.error("TZ invalid : %s !", ANSIBLE_EXPORTER_TZ)
    os._exit(1)
except ValueError:
    logging.basicConfig(
        stream=sys.stdout,
        format=LOGFMT,
        datefmt=DATEFMT,
        level="INFO",
    )
    logging.error("ANSIBLE_EXPORTER_LOGLEVEL invalid !")
    os._exit(1)

# Check ANSIBLE_EXPORTER_PORT
try:
    ANSIBLE_EXPORTER_PORT = int(os.environ.get("ANSIBLE_EXPORTER_PORT", "8123"))
except ValueError:
    logging.error("ANSIBLE_EXPORTER_PORT must be int !")
    os._exit(1)

ANSIBLE_COLLECTIONS_PATHS = os.environ.get(
    "ANSIBLE_COLLECTIONS_PATHS", "/usr/share/ansible/collections"
)

METRICS = [
    {
        "name": "ansible_core",
        "description": "Ansible Core Information",
        "type": "gauge",
    },
    {
        "name": "ansible_lint",
        "description": "Ansible Lint Information",
        "type": "gauge",
    },
    {
        "name": "ansible_collection",
        "description": "Ansible Collection Information",
        "type": "gauge",
    },
]

# REGISTRY Configuration
REGISTRY.unregister(PROCESS_COLLECTOR)
REGISTRY.unregister(PLATFORM_COLLECTOR)
REGISTRY.unregister(REGISTRY._names_to_collectors["python_gc_objects_collected_total"])

ARGS = (
    "collection",
    "list",
)
CLIARGS = {
    "version": None,
    "verbosity": 0,
    "type": ARGS[0],
    "action": ARGS[1],
    "api_server": None,
    "api_key": None,
    "ignore_certs": None,
    "timeout": None,
    "collections_path": None,
    "collection": None,
    "output_format": "json",
    "resolved_validate_certs": None,
}


class AnsibleCollector:
    """Ansible Collector Class"""

    def __init__(self):
        self.metrics = []
        self.metrics.append(
            {"name": "ansible_core", "labels": {"version": ansible_core_version}}
            | METRICS[0]
        )
        self.metrics.append(
            {"name": "ansible_lint", "labels": {"version": ansible_lint_version}}
            | METRICS[1]
        )
        self.metrics.extend(self.get_ansible_collections())

    def get_ansible_collections(self):
        """Retrieve Ansible Collections Informations"""
        collections = []
        init_plugin_loader()
        ansible_galaxy = ansible.cli.galaxy.GalaxyCLI(ARGS)
        ansible_context.CLIARGS = CLIARGS
        ansible_buffer = StringIO()
        sys.stdout = ansible_buffer
        ansible_galaxy.execute_list()
        res = json.loads(ansible_buffer.getvalue())
        sys.stdout = sys.__stdout__
        for name, version in res[
            f"{ANSIBLE_COLLECTIONS_PATHS}/ansible_collections"
        ].items():
            collections.append(
                {
                    "name": "ansible_collection",
                    "labels": {"name": name, "version": version["version"]},
                }
                | METRICS[2]
            )
        return collections

    def collect(self):
        """Collect Prometheus Metrics"""
        for metric in self.metrics:
            labels = {"job": ANSIBLE_EXPORTER_NAME}
            labels |= metric["labels"]
            prometheus_metric = Metric(
                metric["name"], metric["description"], metric["type"]
            )
            prometheus_metric.add_sample(metric["name"], value=1, labels=labels)
            yield prometheus_metric


def main():
    """Main Function"""
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


if __name__ == "__main__":
    main()
