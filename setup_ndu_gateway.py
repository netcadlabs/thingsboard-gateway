# -*- coding: utf-8 -*-

#     Copyright 2019. ThingsBoard
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README_NDU_GATEWAY.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSION = "2.6.6"

setup(
    version=VERSION,
    name="ndu-gateway",
    author="Thingsboard & Netcad Innovation Labs",
    author_email="netcadinnovationlabs@gmail.com",
    license="Apache Software License (Apache Software License 2.0)",
    description="Thingsboard Gateway for IoT devices. Modified By Netcad for NDU",
    url="https://github.com/netcadlabs/ndu-gateway",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    python_requires=">=3.5",
    packages=['ndu_gateway', 'ndu_gateway.gateway', 'ndu_gateway.storage',
              'ndu_gateway.tb_client', 'ndu_gateway.connectors', 'ndu_gateway.connectors.ble',
              'ndu_gateway.connectors.mqtt', 'ndu_gateway.connectors.opcua', 'ndu_gateway.connectors.request',
              'ndu_gateway.connectors.modbus', 'ndu_gateway.connectors.can', 'ndu_gateway.connectors.bacnet',
              'ndu_gateway.connectors.bacnet.bacnet_utilities', 'ndu_gateway.connectors.odbc',
              'ndu_gateway.connectors.rest', 'ndu_gateway.connectors.snmp',
              'ndu_gateway.connectors.camera',
              'ndu_gateway.tb_utility', 'ndu_gateway.extensions',
              'ndu_gateway.extensions.mqtt', 'ndu_gateway.extensions.modbus', 'ndu_gateway.extensions.opcua',
              'ndu_gateway.extensions.ble', 'ndu_gateway.extensions.serial', 'ndu_gateway.extensions.request',
              'ndu_gateway.extensions.can', 'ndu_gateway.extensions.bacnet', 'ndu_gateway.extensions.odbc',
              'ndu_gateway.extensions.rest',  'ndu_gateway.extensions.snmp'
              ],
    install_requires=[
        'jsonpath-rw',
        'regex',
        'pip',
        'paho-mqtt',
        'PyYAML',
        'simplejson',
        'requests',
        'zmq'
    ],
    download_url='https://github.com/netcadlabs/ndu-gateway/archive/%s.tar.gz' % VERSION,
    entry_points={
        'console_scripts': [
            'ndu-gateway = ndu_gateway.tb_gateway:daemon'
        ]},
    package_data={
        "*": ["config/*"]
    })



