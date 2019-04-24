# #!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime
import logging
from subprocess import Popen
from sys import stdout

import click
from colorama import Fore, Style
from pathlib2 import Path

from spacetimegis import (
    app
)

config = app.config

@app.cli.command()
def init():
    """Inits the spacetimegis application"""
    # utils.get_or_create_main_db()
    pass

def create_app(script_info=None):
    return app


def debug_run(app, port):
    return app.run(
        host='0.0.0.0',
        port=int(port),
        threaded=True,
        debug=True)


def console_log_run(app, port):
    from console_log import ConsoleLog
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    app.wsgi_app = ConsoleLog(app.wsgi_app, app.logger)

    def run():
        server = pywsgi.WSGIServer(
            ('0.0.0.0', int(port)),
            app,
            handler_class=WebSocketHandler)
        server.serve_forever()

    run()


@app.cli.command()
@click.option('--debug', '-d', is_flag=True, help='Start the web server in debug mode')
@click.option('--console-log', is_flag=True,
              help='Create logger that logs to the browser console (implies -d)')
@click.option('--address', '-a', default=config.get('WEBSERVER_ADDRESS', '0.0.0.0'),
              help='Specify the address to which to bind the web server')
@click.option('--port', '-p', default=config.get('WEBSERVER_PORT', 9000),
              help='Specify the port on which to run the web server')
@click.option('--workers', '-w', default=config.get('WORKERS', 1),
              help='Number of gunicorn web server workers to fire up [DEPRECATED]')
@click.option('--timeout', '-t', default=config.get('WEBSERVER_TIMEOUT', 100),
              help='Specify the timeout (seconds) for the '
                   'gunicorn web server [DEPRECATED]')
@click.option('--socket', '-s', default=config.get('WEBSERVER_SOCKET'),
              help='Path to a UNIX socket as an alternative to address:port, e.g. '
                   '/var/run/spacetimegis.sock. '
                   'Will override the address and port values. [DEPRECATED]')
def runserver(debug, console_log, address, port, timeout, workers, socket):
    """Starts a spacetimegis web server."""
    debug = debug or config.get('DEBUG') or console_log
    if debug:
        print(Fore.BLUE + '-=' * 20)
        print(
            Fore.YELLOW + 'Starting spacetimegis server in ' +
            Fore.RED + 'DEBUG' +
            Fore.YELLOW + ' mode')
        print(Fore.BLUE + '-=' * 20)
        print(Style.RESET_ALL)
        if console_log:
            console_log_run(app, port)
        else:
            debug_run(app, port)
    else:
        logging.info(
            "The Gunicorn 'spacetimegis runserver' command is deprecated. Please "
            "use the 'gunicorn' command instead.")
        addr_str = ' unix:{socket} ' if socket else' {address}:{port} '
        cmd = (
            'gunicorn '
            '-w {workers} '
            '--timeout {timeout} '
            '-b ' + addr_str +
            '--limit-request-line 0 '
            '--limit-request-field_size 0 '
            'spacetimegis:app').format(**locals())
        print(Fore.GREEN + 'Starting server with command: ')
        print(Fore.YELLOW + cmd)
        print(Style.RESET_ALL)
        Popen(cmd, shell=True).wait()


@app.cli.command()
@click.option('--verbose', '-v', is_flag=True, help='Show extra information')
def version(verbose):
    """Prints the current version number"""
    print(Fore.BLUE + '-=' * 15)
    print(Fore.YELLOW + 'spatiotemporaldata ' + Fore.CYAN + '{version}'.format(
        version=config.get('VERSION_STRING')))
    print(Fore.BLUE + '-=' * 15)
    if verbose:
        print('[DB] : ' + '{}'.format(db.engine))
    print(Style.RESET_ALL)

