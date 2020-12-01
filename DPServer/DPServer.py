import socket
from threading import Thread
from threading import Lock
import sys


class DPServer:
    """
    Application Protocol:
    Client sends: {request name},{argument size}
    Server sends: ACK/UNK/ERR
    (ACK: server correctly received request name and argument size. UNK: unknown request name. ERR: error occurred.)
    Connection will be terminated if UNK or ERR occurred.
    Client sends: argument in bytes array (if the argument size is 0, this step will be skipped.)
    Server sends: return message in bytes array
    end of connection
    """

    def __init__(self):
        self._routes = {}
        self._log_lock = Lock()

    def route(self, route_name: str):
        """
        Decorator factory. Adding route name to the app dictionary along with the function that is map to.
        @param route_name: name of the route
        @return: function cross bounding to the route
        """
        def decorator(request_handler):
            self._routes[route_name] = request_handler
            return request_handler
        return decorator

    def _serve(self, path, arg: bytes):
        """
        Execute a view function
        @param path: route name
        @param arg: argument
        @return: return message, sending back to client, in bytes array.
        """
        view_function = self._routes.get(path)
        if view_function:
            if len(arg) == 0:
                return view_function()
            else:
                return view_function(arg)
        else:
            raise ValueError('Route "{}" has not been registered'.format(path))

    def _request_handler(self, sock: socket.socket):
        """
        TCP server singer request handler. The request handler followers the
        application protocol described above.
        @param sock: socket created for communicating with the client
        """
        msg = sock.recv(1024)
        msg = msg.decode("utf-8")
        request, size = msg.split(',')
        # validation
        if not (request in self._routes):
            sock.send(bytes("UNK", 'ascii'))
            print("[!] Unknown request '{}'".format(request), file=sys.stderr)
            return
        try:
            arg_size = int(size)
        except RuntimeError:
            sock.send(bytes("ERR", 'ascii'))
            print("[!] Invalid argument size'{}'".format(size), file=sys.stderr)
            return

        sock.send(bytes("ACK", 'ascii'))
        if arg_size == 0:
            data = bytearray()
        else:
            data = sock.recv(arg_size)
        return_msg = self._serve(request, data)
        sock.send(return_msg)

    def run(self, host, port):
        print("[ ] Start server at " + host + ":" + str(port))
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
