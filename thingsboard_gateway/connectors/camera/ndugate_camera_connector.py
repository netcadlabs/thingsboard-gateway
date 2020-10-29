"""
NDU-Gate

connector ayar dosyası : etc/thingsboard-gateway/config/camera.json
"""

import time
from threading import Thread
from random import choice
from string import ascii_lowercase
import json
import zmq

from thingsboard_gateway.connectors.connector import Connector, log

# TODO - use config
HOSTNAME = "127.0.0.1"
PORT = "60600"


def log_exception(e):
    if hasattr(e, 'message'):
        log.error(e.message)
    else:
        log.exception(e)


class NDUGateCameraConnector(Thread, Connector):
    def __init__(self, gateway, config, connector_type):
        super().__init__()
        self.statistics = {'MessagesReceived': 0, 'MessagesSent': 0}
        self.__config = config
        log.info("NDU - config %s", config)
        self.__gateway = gateway
        # get from the configuration or create name for logs.
        self.setName(self.__config.get("name", "Custom %s connector " % self.get_name() + ''.join(choice(ascii_lowercase) for _ in range(5))))
        log.info("Starting Custom %s connector", self.get_name())

        self.daemon = True  # Set self thread as daemon
        self.stopped = True  # Service variable for check state
        self.__connected = False  # Service variable for check connection to device
        self.__devices = {}
        self.__masterCameraName = self.__config.get("devices")[0].get("name")

        self.__load_device_configs(connector_type)
        self.lastConnectionCheck = 0
        self.__connect_to_devices()

        self.deviceLastAttributes = {}
        self.__setAttributeQuery = {}
        for device in config.get("devices"):
            self.deviceLastAttributes[device.get("name")] = {}
            self.__setAttributeQuery[device.get("name")] = [""]

        log.info('Custom connector %s initialization success.', self.get_name())
        log.info("Devices in configuration file found: %s ", '\n'.join(device for device in self.__devices))

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)

    def __connect_to_devices(self):
        device_config = self.__devices[self.__masterCameraName]['device_config']
        self.__gateway.add_device(device_config["name"], {"connector": self}, device_type=device_config["type"])
        self.__connected = True
        self.lastConnectionCheck = time.time()

    def __load_device_configs(self, connector_type):
        devices_config = self.__config.get('devices')
        try:
            if devices_config is not None:
                for device_config in devices_config:
                    self.__devices[device_config['name']] = {'device_config': device_config}
            else:
                log.error('"devices" section not found in conf. connector %s has being stopped.', self.get_name())
                self.close()
        except Exception as e:
            log.exception(e)

    def open(self):
        log.info('%s connecting %s:%s', self.get_name(), HOSTNAME, PORT)
        self.stopped = False
        self.socket.connect("tcp://{}:{}".format(HOSTNAME, PORT))
        topic = self.__config.get("topic", "ndugate")
        self.socket.subscribe(topic)
        self.start()

    def get_name(self):
        return self.name

    def is_connected(self):
        return self.__connected

    def run(self):  # Main loop of thread
        log.info('%s started.', self.get_name())
        current_config = self.__devices[self.__masterCameraName]['device_config']
        device_name = current_config.get('name', 'NDUGateCamera')
        device_type = current_config.get('deviceType', 'default')

        result_dict = {
            'deviceName': device_name,
            'deviceType': device_type,
            'attributes': [],
            'telemetry': [],
        }

        try:
            while True:
                try:
                    data_part = self.socket.recv_string()
                    log.info('%s got data %s', self.get_name(), data_part)
                    if not data_part:
                        continue

                    json_string = data_part.split(' ', 1)[1]
                    if json_string is None or json_string is str(""):
                        continue

                    data = json.loads(json_string)

                    result_dict['telemetry'] = []
                    result_dict['attributes'] = []

                    if data is None:
                        continue

                    if data.get("telem") is not None:
                        telem_data = data.get("telem")
                        for key in data.get("telem"):
                            item = {}
                            item[key] = telem_data[key]
                            result_dict['telemetry'].append(item)

                    if data.get("attr") is not None:
                        attr_data = data.get("attr")
                        # for key in attr_data:
                        #     item = {}
                        #     item[key] = attr_data[key]
                        result_dict['attributes'].append(attr_data)

                    log.info("Data %s", result_dict)
                    self.__gateway.send_to_storage(self.get_name(), result_dict)
                    time.sleep(0.1)
                except Exception as e:
                    log_exception(e)
                    time.sleep(5)  # socket hatası olursa daha uzun süre uyu
        except Exception as e:
            log_exception(e)

    def close(self):
        if self.context:
            self.context.destroy()
        self.stopped = True
        # self.__gateway.del_device(self.__devices[self.__masterCameraName])

    def on_attributes_update(self, content):
        device_name = content["device"]
        log.debug("NDU - on_attributes_update device : %s , content : %s", content, device_name)
        pass

    def server_side_rpc_handler(self, content):
        log.debug("NDU - server_side_rpc_handler content : %s", content)
        pass
