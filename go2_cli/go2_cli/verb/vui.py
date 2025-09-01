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
from go2_interfaces.srv import SetBrightness, GetBrightness, SetVolume, GetVolume
import rclpy


class VUIVerb(VerbExtension):
    """VUI Interfaces."""

    def add_arguments(self, parser, cli_name):
        add_arguments(parser)
        choices = [
            'set_brightness',
            'get_brightness',
            'set_volume',
            'get_volume',
        ]
        parser.add_argument(
            'NAME',
            choices=choices,
            help='Name of the vui service.',
        ).completer = ChoicesCompleter(choices)
        parser.add_argument(
            'VALUE',
            help='Value of the brightness or volume.',
            type=int,
            nargs='?',
        )

    def main(self, *, args):
        with NodeStrategy(args) as node:
            if args.NAME == 'set_brightness':
                client = node.create_client(SetBrightness, 'set_brightness')
                client.wait_for_service(1)
                request = SetBrightness.Request()
                request.brightness = args.VALUE
                future = client.call_async(request)
                rclpy.spin_until_future_complete(node, future, timeout_sec=1)
                response = future.result()
                
                if response is None:
                    print('\033[31mTimeout Error\033[0m')
                else:
                    print(response.message)
            elif args.NAME == 'get_brightness':
                client = node.create_client(GetBrightness, 'get_brightness')
                client.wait_for_service(1)
                request = GetBrightness.Request()
                future = client.call_async(request)
                rclpy.spin_until_future_complete(node, future, timeout_sec=1)
                response = future.result()

                if response is None:
                    print('\033[31mTimeout Error\033[0m')
                else:
                    print('The brightness is:', response.brightness)
            elif args.NAME == 'set_volume':
                client = node.create_client(SetVolume, 'set_volume')
                client.wait_for_service(1)
                request = SetVolume.Request()
                request.volume = args.VALUE
                future = client.call_async(request)
                rclpy.spin_until_future_complete(node, future, timeout_sec=1)
                response = future.result()
                
                if response is None:
                    print('\033[31mTimeout Error\033[0m')
                else:
                    print(response.message)
            elif args.NAME == 'get_volume':
                client = node.create_client(GetVolume, 'get_volume')
                client.wait_for_service(1)
                request = GetVolume.Request()
                future = client.call_async(request)
                rclpy.spin_until_future_complete(node, future, timeout_sec=1)
                response = future.result()
                
                if response is None:
                    print('\033[31mTimeout Error\033[0m')
                else:
                    print('The volume is:', response.volume)

        return 0
