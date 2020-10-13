"""
NDU-Gate

connector ayar dosyası : etc/thingsboard-gateway/config/camera.json
"""

import time
from threading import Thread
from random import choice
from string import ascii_lowercase
import datetime
import serial
from datetime import datetime, date
from datetime import timezone, timedelta
import requests
import json
import re
import subprocess
from os import path
import zmq

# Import base class for connector and logger
from thingsboard_gateway.connectors.connector import Connector, log
from thingsboard_gateway.tb_utility.tb_utility import TBUtility
# Import base class for connector and logger

# Define a connector class, it should inherit from "Connector" class.
import sys

HOSTNAME = "127.0.0.1"
PORT = "60600"

class NDUGateCameraConnector(Thread, Connector):
    def __init__(self, gateway, config, connector_type):
        super().__init__()    # Initialize parents classes
        self.statistics = {'MessagesReceived': 0, 'MessagesSent': 0}    # Dictionary, will save information about count received and sent messages.
        self.__config = config
        log.debug("NDU - config %s", config)
        self.__gateway = gateway
        # get from the configuration or create name for logs.
        self.setName(self.__config.get("name", "Custom %s connector " % self.get_name() + ''.join(choice(ascii_lowercase) for _ in range(5))))
        log.info("Starting Custom %s connector", self.get_name())
        self.daemon = True    # Set self thread as daemon
        self.stopped = True    # Service variable for check state
        self.__connected = False    # Service variable for check connection to device
        # Dictionary with devices, will contain devices configurations, converters for devices and serial port objects
        self.__devices = {}
        self.__masterCameraName = self.__config.get("devices")[0].get("name")
        # Call function to load converters and save it into devices dictionary
        self.lastConnectionCheck = 0
        # first interval(seconds) to reconnect device
        self.__connect_to_devices()    # Call function for connect to devices
        self.__waitSession = False
        self.deviceLastAttributes = {}
        self.__setAttributeQuery = {}
        for device in config.get("devices"):
            self.deviceLastAttributes[device.get("name")] = {}
            self.__setAttributeQuery[device.get("name")] = [""]

        log.info('Custom connector %s initialization success.',
                 self.get_name())    # Message to logger
        log.info("Devices in configuration file found: %s ", '\n'.join(
            device for device in self.__devices))    # Message to logger

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
    
    # Function for opening connection and connecting to devices
    def __connect_to_devices(self):
        # @warn camera must open there
        device_config = self.__devices[self.__masterCameraName]['device_config']
        self.__gateway.add_device(device_config["name"], {"connector": self}, device_type=device_config["type"])
        self.__connected = True
        self.lastConnectionCheck = time.time()

    def open(self):    # Function called by gateway on start
        self.stopped = False
        self.socket.bind("tcp://{}:{}".format(HOSTNAME, PORT))
        self.start()

    def get_name(self):    # Function used for logging, sending data and statistic
        return self.name

    def is_connected(self):    # Function for checking connection state
        return self.__connected

    def run(self):    # Main loop of thread
        currentConfig = self.__devices[self.__masterCameraName]['device_config']
        deviceName =  currentConfig.get('name', 'CustomSerialDevice')
        deviceType =  currentConfig.get('deviceType', 'default')
        
        result_dict = {
            'deviceName': deviceName,
            'deviceType': deviceType,
            'attributes': [],
            'telemetry': [],
        }

        try:
            while True:
                data_part = self.socket.recv_string()
                if not data_part:
                    continue

                json_string = data_part.split(' ', 1)[1]
                if json_string is None or json_string is str(""):
                    continue

                data = json.loads(json_string)

                result_dict['telemetry'] = []
                result_dict['telemetry'] = []

                if data is None:
                    continue

                for key in data:
                    item = {}
                    item[key] = data[key]
                    result_dict['telemetry'].append(item)

                self.__gateway.send_to_storage(self.get_name(), result_dict)
                time.sleep(0.1)
        except Exception as e:
            self.log_exception(e)

    def log_exception(self, e):
        if hasattr(e, 'message'):
            log.error(e.message)
        else:
            log.exception(e)

    def close(self):    # Close connect function, usually used if exception handled in gateway main loop or in connector main loop
        self.context.destroy()
        self.stopped = True
        self.__gateway.del_device(self.__devices[self.__masterCameraName])

    # Function used for processing attribute update requests from ThingsBoard
    def on_attributes_update(self, content):
        device_name = content["device"]
        log.debug("NDU - on_attributes_update device : %s , content : %s", content, device_name)
        pass

    def server_side_rpc_handler(self, content):
        log.debug("NDU - server_side_rpc_handler content : %s", content)
        pass
