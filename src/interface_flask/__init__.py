import os
import socket
import threading
from werkzeug.serving import make_server
from flask import Flask
import interface_flask.server

from settings import current

# server_thread = None


# address = 'localhost'
address = current['interface']['flask-address']

used_ports = []

def find_free_port(starting_port=10000, add_to_used = True):
    # global port, starting_port
    # global starting_port, used_ports
    global used_ports

    """
    Check if default debug port 8228 is available,
    increment it by 1 until a port is available.
    :return: port: str
    """
    port_available = False
    search_port = starting_port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while not port_available:
        if search_port in used_ports:
            search_port += 1
            continue

        try:
            sock.bind(('localhost', search_port))
            # sock.bind((address, port))
            port_available = True
        except:
            port_available = False
            # logger.warning('Port %s is in use' % port)
            search_port += 1
            # continue
        finally:
            sock.close()

    if add_to_used:
        used_ports.append(search_port)

    print(f" Found Free Port @: {search_port}")
    return search_port


def get_blank_addr():
    return f"http://{address}:{port}/blank"
    # return f"http://{address}:{port}/blank"

def get_launch_settings_addr():
    return f"http://{address}:{port}/launch_settings"
    # return f"http://{address}:{port}/blank"

def get_startup_addr():
    return f"http://{address}:{port}/startup"
    # return f"http://{address}:{port}/blank"

def get_main_addr():
    return f"http://{address}:{port}/"
    # return f"http://{address}:{port}/blank"


port = find_free_port(current['interface']['flask-port'])

class ServerThread(threading.Thread):

    def __init__(self, app):
        global address, port
        threading.Thread.__init__(self)
        self.srv = make_server(address, port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        # log.info('starting server')
        self.srv.serve_forever()
        # print("server online")

    def shutdown(self):
        print("TRYING TO SHUTDOWN...")
        # sys.exit(0)
        self.srv.shutdown()

server_thread = ServerThread(interface_flask.server.app)

def start_server():
    global server_thread

    server_thread.start()
    # print('server started')

def stop_server():
    global server_thread
    server_thread.shutdown()