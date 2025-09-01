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
from go2_interfaces.srv import Mode
import rclpy


class ServiceVerb(VerbExtension):
    """Service handler."""

    def add_arguments(self, parser, cli_name):
        add_arguments(parser)
        choices = [
            'damp', 'balance_stand', 'stop_move', 'stand_up', 'stand_down', 'sit', 'rise_sit', 
            'hello', 'stretch', 'wallow', 'scrape', 'front_flip', 'front_jump', 'front_pounce',
            'dance1', 'dance2', 'finger_heart', 'dance3', 'dance4', 'hop_spin_left', 'hop_spin_right', 
            'left_flip', 'back_flip', 'free_walk', 'free_bound', 'free_jump', 'free_avoid', 
            'walk_stair', 'walk_up_right', 'cross_step', 'walk_up_left', 'walk_down_right', 'walk_down_left',
            'walk_up', 'walk_down', 'walk_left', 'walk_right', 'walk_forward', 'walk_backward', 'walk_stop',
        ]
        parser.add_argument(
            'NAME',
            help='Name of the service.',
        ).completer = ChoicesCompleter(choices)

    def main(self, *, args):
        with NodeStrategy(args) as node:
            client = node.create_client(Mode, 'mode')
            client.wait_for_service()
            request = Mode.Request()
            request.mode = args.NAME
            future = client.call_async(request)
            rclpy.spin_until_future_complete(node, future)
            response = future.result()
            if response.success:
                print(response.message)
            else:
                print('\033[31m' + response.message + '\033[0m')

        return 0
