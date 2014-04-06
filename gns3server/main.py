#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import datetime
import sys
import multiprocessing
import tornado.options
from gns3server.server import Server
from gns3server.version import __version__

# command line options
from tornado.options import define
define("host", default="0.0.0.0", help="run on the given host/IP address", type=str)
define("port", default=8000, help="run on the given port", type=int)
define("ipc", default=False, help="use IPC for module communication", type=bool)


def main():
    """
    Entry point for GNS3 server
    """

    if sys.platform.startswith("win"):
        # necessary on Windows to use freezing software
        multiprocessing.freeze_support()

    current_year = datetime.date.today().year
    print("GNS3 server version {}".format(__version__))
    print("Copyright (c) 2007-{} GNS3 Technologies Inc.".format(current_year))

    # we only support Python 3 version >= 3.3
    if sys.version_info < (3, 3):
        raise RuntimeError("Python 3.3 or higher is required")

    print("Running with Python {major}.{minor}.{micro} and has PID {pid}".format(major=sys.version_info[0],
                                                                                 minor=sys.version_info[1],
                                                                                 micro=sys.version_info[2],
                                                                                 pid=os.getpid()))

    try:
        tornado.options.parse_command_line()
    except (tornado.options.Error, ValueError):
        tornado.options.print_help()
        raise SystemExit

    from tornado.options import options
    server = Server(options.host,
                    options.port,
                    ipc=options.ipc)
    server.load_modules()
    server.run()

if __name__ == '__main__':
    main()
