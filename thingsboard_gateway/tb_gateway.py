#     Copyright 2020. ThingsBoard
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

import getopt
from os import path, listdir, mkdir, curdir
import sys
import time
import traceback
from sys import platform
from thingsboard_gateway.gateway.tb_gateway_service import TBGatewayService

DEFAULT_TB_GATEWAY_CONF = "/etc/ndu-gateway/config/tb_gateway.yaml"
DEFAULT_TB_GATEWAY_CONF_WIN = "C:/ndu-gateway/config/tb_gateway.yaml"

def _get_config():
    print(sys.argv)
    ndu_gateway_config_file = None

    if len(sys.argv) > 1:
        try:
            opts, _ = getopt.getopt(sys.argv[1:], "c:", ["config="])
            for opt, arg in opts:
                if opt in ['-c', '--config']:
                    ndu_gateway_config_file = arg
        except getopt.GetoptError:
            print('tb_gateway.py -c <config_file_path>')

    config_file_name = "ndu_gate.yaml"
    if ndu_gateway_config_file is None:
        config_file_name = "tb_gateway.yaml"

        config_file = path.dirname(path.abspath(__file__)) + '/config/'.replace('/', path.sep) + config_file_name
        if path.isfile(config_file):
            ndu_gateway_config_file = config_file

    if ndu_gateway_config_file is None:
        print("Config file not specified, going to use default")
        if platform == "win32":
            ndu_gateway_config_file = DEFAULT_TB_GATEWAY_CONF.replace('/', path.sep)
        else:
            ndu_gateway_config_file = DEFAULT_TB_GATEWAY_CONF_WIN.replace('/', path.sep)

    print("Config file is {}".format(ndu_gateway_config_file))

    return ndu_gateway_config_file



def main():
    if "logs" not in listdir(curdir):
        mkdir("logs")
    TBGatewayService(_get_config())


def daemon():
    TBGatewayService(_get_config())


if __name__ == '__main__':
    main()
