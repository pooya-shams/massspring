"""
networklib.py

this file helps with migrating massspring to a server-client model.
it is just a thin layer over the main massspring file that creates
a server which is connectable through sockets.
the default host is localhost (obviously!) and the default port is
7783, is is the concatination of 77 and 83 which are ascii codes of
'M' and 'S', the first letters of Mass and Spring which are the main
foundations of the whole massspring library.
"""

import socket
import threading
import types
import typing
import sys

ms = "mass"
sp = "spring"
msb = b"mass"
spb = b"spring"
null = b'\0'
default_host = "127.0.0.1"  # localhost
default_port = 7783  # fun fact: ord("M") == 77 && ord("S") == 83; (MassSpring)
buffsize = 255
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def decode_mass_poses(response: bytes) -> list:
    resp = response.decode().rsplit()
    ms_ls = [None]*len(resp)
    for i, line in enumerate(resp):
        ms_ls[i] = list(map(int, map(float, line.split(','))))
    return ms_ls


def encode_mass_poses(mass_lis: list) -> bytes:
    resp = ms + '\n'
    for m in mass_lis:
        resp += ','.join(map(str, (m.x, m.y, m.z))) + '\n'
    return resp.encode()


def encode_spring_poses(spring_lis: list) -> bytes:
    resp = sp+'\n'
    for s in spring_lis:
        resp += ','.join(map(str, (s.m1.x, s.m1.y, s.m1.z))) + \
            ';' + ','.join(map(str, (s.m2.x, s.m2.y, s.m2.z))) + '\n'
    return resp.encode()


def analyse_request(request: bytes, mass_lis: list = None, spring_lis: list = None) -> bytes:
    # just the default request analyser. we wont use this function in
    # this module but it can be used by users and be passed to the
    # handle_client function as a request analyser.
    response: bytes = null
    print("request is: ", request)
    if request == msb:
        response = encode_mass_poses(mass_lis)
    elif request == spb:
        response = encode_spring_poses(spring_lis)
    print("answer is", response)
    return response


def analyse_request_wrapper(mass_lis: list, spring_lis: list):
    def wrapped_request_analyser(request: bytes):
        return analyse_request(request, mass_lis, spring_lis)
    return wrapped_request_analyser


def handle_client(client_socket: socket.socket, request_analyser: typing.Callable) -> None:
    closed = False
    while not closed:
        request = client_socket.recv(buffsize)
        print("[INFO] Received: %s" % request)
        data = request_analyser(request)
        client_socket.send(data)


def handle_client_wrapper(request_analyser: typing.Callable) -> typing.Callable:
    def wrapped_client_handler(client_socket: socket.socket) -> None:
        return handle_client(client_socket, request_analyser)
    return wrapped_client_handler


def start_server_mainloop(
        massspring: types.ModuleType, massspring_mainloop_args: typing.Iterable, massspring_mainloop_kwargs: typing.Mapping[str, typing.Any],
        client_handler: typing.Callable[[socket.socket], None],
        host: str = None, port: int = None):
    # I'm too lazy to write comments. OK?
    if host is None:
        host = default_host
    if port is None:
        port = default_port
    server.bind((host, port))
    server.listen(5)
    massspring_mainloop_thread = threading.Thread(
        target=massspring.mainloop, args=massspring_mainloop_args)
    massspring_mainloop_thread.start()
    thread_list = []
    while massspring_mainloop_thread.is_alive():
        client, addr = server.accept()
        print("[INFO] Accepted connection from: %s:%d" % (addr[0], addr[1]))
        client_handler_thread = threading.Thread(
            target=client_handler, args=(client, ))
        client_handler_thread.daemon = True
        # this thread will die immediately when the program exits
        client_handler_thread.start()
        thread_list.append(client_handler_thread)
    sys.exit(0)
    # exiting and killing all threads, showing no mercy
