#!/usr/bin/env python3
# -- In the name of God --
# Project: massspring (mass+spring)
# File: networklib.py
# Author: Pooya Shams kolahi
# Inspired by Saeed Sarkarati


"""
networklib.py

this file helps with migrating massspring to a server-client model.
it is just a thin layer over the main massspring file that creates
a server which is connectable through sockets.
the default host is localhost (obviously!) and the default port is
7783, is is the concatenation of 77 and 83 which are ascii codes of
'M' and 'S', the first letters of Mass and Spring which are the main
foundations of the whole massspring library.
"""

import socket
import sys
import threading
import types
import typing
import warnings

# Variables

ms = "mass"
sp = "spring"
msb = b"mass"
spb = b"spring"
null = b'\0'
exit_commands = [b'exit', b'quit']
default_host = "127.0.0.1"  # localhost
default_port = 7783  # fun fact: ord("M") == 77 && ord("S") == 83; (MassSpring)
buffsize = 256
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# functions
# encode/decode helper functions

# the encoding tries to send the positions of all possible objects
# that can be shown on the screen to another place, which is the client
# that is receiving them. they will be decoded after being received.
# they try to send as minimum data as possible.
# they work like this:
# the mass encoder/decoder
# the mass encoder will create a "bytes" object and return it.
# this bytes object will contain positions of all masses separated in lines
# each line contains the position of one mass and it is formatted like this:
# x,y,z
# please note that there is no whitespace in the lines (except from newlines
# which are line delimiters) in order to reduce the amount of transferred data
# to the lowest possible.
# the spring encoder/decoder
# on the other hand the spring encoder/decoder will have to send position of
# two masses not one. like the mass encoder it will create a "bytes" object
# with the word "spring" in the first line and return it. but unlike the
# mass encoder it won't send just one position so it will have to separate
# each position being sent. in order to accomplish this the transferred data
#  will be formatted like this:
# x1,y1,z1;x2,y2,z2
# please note that like the mass encoder there are no whitespaces in the lines
# in order to reduce the size of transferred data to the lowest possible.

def encode_mass_poses(mass_lis: list) -> bytes:
    """ gets a list of all positions and returns the "bytes" object """
    resp = ms + '\n'
    for m in mass_lis:
        resp += ','.join(map(str, (m.x, m.y, m.z))) + '\n'
    return resp.encode()


def encode_spring_poses(spring_lis: list) -> bytes:
    """ gets a list of all positions and returns the "bytes" object """
    resp = sp + '\n'
    for s in spring_lis:
        resp += ','.join(map(str, (s.m1.x, s.m1.y, s.m1.z))) + \
            ';' + ','.join(map(str, (s.m2.x, s.m2.y, s.m2.z))) + '\n'
    return resp.encode()


def decode_mass_poses(response: bytes) -> list:
    """
    gets the "bytes" object and returns a list of
    all positions of masses included in it.
    """
    resp = response.decode().rsplit()
    ms_ls = [None] * (len(resp) - 1)
    for i, line in enumerate(resp[1:]):
        ms_ls[i] = list(map(float, line.split(',')))
    return ms_ls


def decode_spring_poses(response: bytes) -> list:
    """
    gets the "bytes" object and returns a list of
    all positions of springs included in it.
    """
    resp = response.decode().rsplit()
    sp_ls = [None] * (len(resp) - 1)
    for i, line in enumerate(resp[1:]):
        m1m, m2m = line.split(';')
        m1 = list(map(float, m1m.split(',')))
        m2 = list(map(float, m2m.split(',')))
        sp_ls[i] = [m1, m2]
    return sp_ls


def decode_mass_spring_poses(response: bytes) -> list:
    """
    gets the "bytes" object and returns results of
    decode_mass_poses and decode_spring_poses.
    it relies on the fact that there is a 'mass' and 'spring'
    in the beginning of the sequence of masses and springs.
    this function will be deprecated after fixing issue #6,
    possibley with the second approach. but if the first approach
    is used then this kind of splitting might become helpful.
    """
    idx1 = response.find(b"mass")
    idx2 = response.find(b"spring")
    if idx1 == -1:
        raise ValueError("No mass found in response")
    if idx2 == -1:
        raise ValueError("No spring found in response")
    mass_resp: bytes
    spring_resp: bytes
    if idx1 < idx2:
        mass_resp = response[idx1:idx2]
        spring_resp = response[idx2:]
    else:
        spring_resp = response[idx1:idx2]
        mass_resp = response[idx2:]
    mass_lis = decode_mass_poses(mass_resp)
    spring_lis = decode_spring_poses(spring_resp)
    return mass_lis, spring_lis


def analyse_request(request: bytes, information: typing.Mapping[bytes, typing.Callable], delimiter: bytes = b'|'):
    """
    analyse_request is just the default request analyser. we wont use this function in
    this module but it can be used by users and be passed to the handle_client function
    as a request analyser.
    receives the request as a "bytes" object, extracts all requests from it and
    decides which analyser function provided in information dictionary will be
    used to process it.
    yields bytes objects.
    """
    assert type(delimiter) == bytes and len(delimiter) == 1, ValueError("'delimiter' must be bytes object of length 1")
    reqlist = request.split(delimiter)
    for req in reqlist:
        if req in exit_commands:
            yield req
            # this will later cause handle_client to exit
        elif req in information:
            func = information[req]
            assert callable(func), TypeError("'information' values should be callable.")
            ans: bytes = func()
            assert type(ans) == bytes, ValueError("'information' values should return bytes object.")
            ans = ans.strip()
            yield ans
        else:
            warnings.warn(Warning("the request %s is not in the 'information' dictionary" % req))


def analyse_request_wrapper(mass_lis: list, spring_lis: list):
    """
    a wrapper for the analyse_request function mentioned earlier which
    will return a function that just gets the request as an argument.
    """
    def wrapped_request_analyser(request: bytes):
        return analyse_request(request, mass_lis, spring_lis)
    return wrapped_request_analyser


def send(soc: socket.socket, data: bytes):
    """ sends data properly and safely """
    assert type(soc) == socket.socket, TypeError("'soc' should be socket.socket")
    assert type(data) == bytes, TypeError("'data' should be bytes")
    length = str(len(data)).encode()
    soc.send(length)
    return soc.send(data)


def recv(soc: socket.socket):
    """ receives data properly and safely """
    length = int(soc.recv(buffsize).decode())
    return soc.recv(length)


def handle_client(client_socket: socket.socket, addr: typing.Iterable, request_analyser: typing.Callable) -> None:
    """
    handles the client socket by receiving it's query
    and returning what it asked for in return.
    it runs in an infinite loop and receives the request and sends TWO respones to them:
    - the first one is the length of the actual response returned from
    request_analyser with a newline character at the end of it
    - the second one is the actual respone itself.
    as far as I know they won't get mixed together so that the client can do a socket.recv
    with 256 as buffersize and use the length to do another recv.
    """
    try:
        while True:
            # receiving the request asked by the client maxlength should be specified
            # by client in a message with maxlength 256.
            request = recv(client_socket)
            # processing the received request
            data = request_analyser(request)
            for resp in data:
                # checking if we should exit
                if resp in exit_commands:
                    return
                # sending the received data
                send(client_socket, resp)
    except BrokenPipeError:
        # client closed the connection after receiving the whole response
        print(f"[ERROR] connection with {addr[0]}:{addr[1]} closed unexpectedly: Broken Pipe.")


def handle_client_wrapper(request_analyser: typing.Callable) -> typing.Callable:
    """
    a wrapper for the handle_client function mentioned earlier which will
    return a function that just gets the client_socket as an argument.
    """
    def wrapped_client_handler(client_socket: socket.socket, addr: typing.Iterable) -> None:
        return handle_client(client_socket, addr, request_analyser)
    return wrapped_client_handler


def start_server_mainloop(
        massspring: types.ModuleType, massspring_mainloop_args: typing.Iterable, massspring_mainloop_kwargs: typing.Mapping[str, typing.Any],
        client_handler: typing.Callable[[socket.socket], None],
        host: str = None, port: int = None):
    # I'm too lazy to write comments. OK?
    # checking the values to be valid or reflecting default values
    if host is None:
        host = default_host
    if port is None:
        port = default_port
    # setting up the server
    server.bind((host, port))
    server.listen(5)
    # setting up the main program thread. if this thread finishes,
    # all of the other threads will be killed or forced to stop.
    # TODO: implement this line ( ^ ) properly.
    massspring_mainloop_thread = threading.Thread(
        target=massspring.mainloop, args=massspring_mainloop_args, kwargs=massspring_mainloop_kwargs)
    massspring_mainloop_thread.start()
    # the list containing all threads created when answering clients
    thread_list = []
    # the mainloop of handling clients
    while massspring_mainloop_thread.is_alive():
        client, addr = server.accept()  # accepting the connection
        print("[INFO] Accepted connection from: %s:%d" % (addr[0], addr[1]))
        # setting up the client handling thread
        client_handler_thread = threading.Thread(
            target=client_handler, args=(client, addr))
        client_handler_thread.daemon = True
        # this thread will die immediately when the program exits
        client_handler_thread.start()
        # adding it to the threads list
        thread_list.append(client_handler_thread)
    sys.exit(0)
    # exiting and killing all threads, showing no mercy
