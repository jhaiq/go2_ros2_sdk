# Copyright 2025 Juan Carlos Manzanares Serrano
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ros2cli.verb import VerbExtension
from ros2cli.node.strategy import NodeStrategy
from ros2cli.node.strategy import add_arguments
from argcomplete.completers import ChoicesCompleter
from go2_interfaces.srv import SetSwitchObstaclesAvoidance, GetSwitchObstaclesAvoidance
import rclpy


class SwitchObstaclesAvoidanceVerb(VerbExtension):
    """SwitchObstaclesAvoidance."""

    def add_arguments(self, parser, cli_name):
        add_arguments(parser)
        choices = [
            'start',
            'stop',
            'get',
        ]
        parser.add_argument(
            'NAME',
            choices=choices,
            help='Name of the service.',
        ).completer = ChoicesCompleter(choices)

    def main(self, *, args):
        with NodeStrategy(args) as node:
            if (args.NAME == 'start' or args.NAME == 'stop'):
                client = node.create_client(SetSwitchObstaclesAvoidance, 'set_obstacles_avoidance')
                client.wait_for_service(1)
                request = SetSwitchObstaclesAvoidance.Request()
                request.enable = (args.NAME == 'start')
                future = client.call_async(request)
                rclpy.spin_until_future_complete(node, future, timeout_sec=1)
                response = future.result()
                if response is None:
                    print('\033[31mTimeout Error\033[0m')
                else:
                    print(response.message)
                    
            elif (args.NAME == 'get'):
                client = node.create_client(GetSwitchObstaclesAvoidance, 'get_obstacles_avoidance')
                client.wait_for_service(1)
                request = GetSwitchObstaclesAvoidance.Request()
                future = client.call_async(request)
                rclpy.spin_until_future_complete(node, future, timeout_sec=1)
                response = future.result()
                if response is None:
                    print('\033[31mTimeout Error\033[0m')
                    return 0

                if response.enable:
                    print(response.message + '. Obstacles avoidance is enabled')
                else:
                    print(response.message + '. Obstacles avoidance is disabled')

        return 0
