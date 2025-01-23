# This file is part of Octopus Sensing <https://octopus-sensing.nastaran-saffar.me/>
# Copyright © Nastaran Saffaryazdi 2021
#
# Octopus Sensing Visualizer is a free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
#  either version 3 of the License, or (at your option) any later version.
#
# Octopus Sensing Visualizer is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Octopus Sensing Visualizer.
# If not, see <https://www.gnu.org/licenses/>.

import os
import sys
import cherrypy
import configparser
from octopus_sensing_visualizer.end_point import *

CONFIG_FILE_PATH="./octopus_sensing_visualizer_config.conf"

def main():
    ui_build_path = os.path.join(os.path.dirname(
        os.path.abspath(sys.modules[__name__].__file__)), 'ui_build')

    if not os.path.isfile(CONFIG_FILE_PATH):
        raise Exception("I need a config file called octopus_sensing_visualizer_config.conf")

    # Load the configuration file
    config = configparser.RawConfigParser(allow_no_value=True)
    config.read(CONFIG_FILE_PATH)

    port = 8080
    if config.has_option('SERVER', 'port'):
        port = int(config.get('SERVER', 'port'))

    cherrypy.tree.mount(RootHandler(), '/', config={
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': ui_build_path,
            'tools.staticdir.index': 'index.html',
        },
    })
    end_point = EndPoint(config)
    cherrypy.tree.mount(end_point, '/api')

    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.server.socket_port = port
    cherrypy.engine.autoreload.on = False
    cherrypy.engine.start()
    cherrypy.engine.block()
