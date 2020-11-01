import socket
from threading import Thread
from threading import Lock
import sys


class DPServer:

    def __init__(self):
        self._routes = {}
        self._log_lock = Lock()

    def route(self, route_name):
        def decorator(request_handler):
            self._routes[route_name] = request_handler
            return request_handler
        return decorator

    def _serve(self, path, data: bytes):
        view_function = self._routes.get(path)
        if view_function:
            if len(data) == 0:
                return view_function()
            else:
                return view_function(data)
        else:
            raise ValueError('Route "{}" has not been registered'.format(path))

    def _request_handler(self, sock: socket.socket):
        msg = sock.recv(1024)
        msg = msg.decode("utf-8")
        request, size = msg.split(',')
        if request in self._routes:
            sock.send(bytes("ACK", 'ascii'))
            data = sock.recv(int(size))
            return_msg = self._serve(request, data)
            sock.send(bytes(return_msg, "utf-8"))
        else:
            sock.send(bytes("UNK", 'ascii'))
            print("[!] Unknown request '{}'".format(request), file=sys.stderr)

    def run(self, host, port):
        print("[ ] Starting server at " + host + ":" + str(port))
        sock = SocketInit((host, port))
        # Listen for incoming connections
        sock.listen(1)
        threads = []
        while True:
            client_socket, client_addr = sock.accept()
            client_socket.settimeout(20)
            print("[+] New client connected at " + client_addr[0] + ":" + str(client_addr[1]))
            new_thread = ClientThread(self._request_handler, client_socket, self._log_lock)
            new_thread.start()
            threads.append(new_thread)
            for t in threads:
                if not (t.is_alive()):
                    t.join()
                    threads.remove(t)


class ClientThread(Thread):

    def __init__(self, app_handler, client_socket: socket.socket, print_lock: Lock):
        Thread.__init__(self)
        self.app_handler = app_handler
        self.client_socket = client_socket
        self.client_addr = client_socket.getpeername()
        self.log_lock = print_lock

    def run(self):
        self.app_handler(self.client_socket)
        self.client_socket.close()
        self.log_lock.acquire()
        print("[-] Client " + self.client_addr[0] + ":" + str(self.client_addr[1]) + " disconnected")
        self.log_lock.release()


def SocketInit(addr):
    # Create a TCP/IP socket
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the port
    my_socket.bind(addr)
    return my_socket
