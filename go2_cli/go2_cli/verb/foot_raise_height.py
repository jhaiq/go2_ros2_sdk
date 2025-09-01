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
from go2_interfaces.srv import FootRaiseHeight, GetFootRaiseHeight
import rclpy


class FootRaiseHeightVerb(VerbExtension):
    """Foot Raise Height."""

    def add_arguments(self, parser, cli_name):
        add_arguments(parser)
        choices = [
            'set',
            'get',
        ]
        parser.add_argument(
            'NAME',
            choices=choices,
            help='Name of the service.',
        ).completer = ChoicesCompleter(choices)
        parser.add_argument(
            'VALUE',
            nargs='?',
            help='Height of the foot.',
            type=float,
        )

    def main(self, *, args):
        with NodeStrategy(args) as node:
            if (args.NAME == 'set'):
                client = node.create_client(FootRaiseHeight, 'foot_raise_height')
                client.wait_for_service()
                request = FootRaiseHeight.Request()
                request.height = args.VALUE
                future = client.call_async(request)
                rclpy.spin_until_future_complete(node, future)
                response = future.result()
                if response.success:
                    print(response.message)
                else:
                    print('\033[31m' + response.message + '\033[0m')
            elif (args.NAME == 'get'):
                client = node.create_client(GetFootRaiseHeight, 'get_foot_raise_height')
                client.wait_for_service()
                request = GetFootRaiseHeight.Request()
                future = client.call_async(request)
                rclpy.spin_until_future_complete(node, future)
                response = future.result()
                if response.success:
                    print('Foot raise height: ', response.height)
                else:
                    print('\033[31m' + response.message + '\033[0m')

        return 0
