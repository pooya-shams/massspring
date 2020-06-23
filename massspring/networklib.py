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
import threading
import types
import typing
import sys


# Variables

ms = "mass"
sp = "spring"
msb = b"mass"
spb = b"spring"
null = b'\0'
default_host = "127.0.0.1"  # localhost
default_port = 7783  # fun fact: ord("M") == 77 && ord("S") == 83; (MassSpring)
buffsize = 255
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

def decode_mass_poses(response: bytes) -> list:
    """ gets the "bytes" object and returns a list of all positions """
    resp = response.decode().rsplit()
    ms_ls = [None]*len(resp)
    for i, line in enumerate(resp):
        ms_ls[i] = list(map(int, map(float, line.split(','))))
    return ms_ls


def encode_mass_poses(mass_lis: list) -> bytes:
    """ gets a list of all positions and returns the "bytes" object """
    resp = ms + '\n'
    for m in mass_lis:
        resp += ','.join(map(str, (m.x, m.y, m.z))) + '\n'
    return resp.encode()


def encode_spring_poses(spring_lis: list) -> bytes:
    """ gets a list of all positions and returns the "bytes" object """
    resp = sp+'\n'
    for s in spring_lis:
        resp += ','.join(map(str, (s.m1.x, s.m1.y, s.m1.z))) + \
            ';' + ','.join(map(str, (s.m2.x, s.m2.y, s.m2.z))) + '\n'
    return resp.encode()


def analyse_request(request: bytes, mass_lis: list = None, spring_lis: list = None) -> bytes:
    """
    receives the request as a "bytes" object and
    decides which encoder will be used to send data
    """
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
    """
    a wrapper for the analyse_request function mentioned earlier which
    will return a function that just gets the request as an argument.
    """
    def wrapped_request_analyser(request: bytes):
        return analyse_request(request, mass_lis, spring_lis)
    return wrapped_request_analyser


def handle_client(client_socket: socket.socket, request_analyser: typing.Callable) -> None:
    """
    handles the client socket by receiving it's query
    and returning what it asked for in return.
    """
    closed = False
    while not closed:
        request = client_socket.recv(buffsize)
        print("[INFO] Received: %s" % request)
        data = request_analyser(request)
        client_socket.send(data)


def handle_client_wrapper(request_analyser: typing.Callable) -> typing.Callable:
    """
    a wrapper for the handle_client function mentioned earlier which will
    return a function that just gets the client_socket as an argument.
    """
    def wrapped_client_handler(client_socket: socket.socket) -> None:
        return handle_client(client_socket, request_analyser)
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
    massspring_mainloop_thread = threading.Thread(
        target=massspring.mainloop, args=massspring_mainloop_args)
    massspring_mainloop_thread.start()
    # the list containing all threads created when answering clients
    thread_list = []
    # the mainloop of handling clients
    while massspring_mainloop_thread.is_alive():
        client, addr = server.accept()  # accepting the connection
        print("[INFO] Accepted connection from: %s:%d" % (addr[0], addr[1]))
        # setting up the client handling thread
        client_handler_thread = threading.Thread(
            target=client_handler, args=(client, ))
        client_handler_thread.daemon = True
        # this thread will die immediately when the program exits
        client_handler_thread.start()
        # adding it to the threads list
        thread_list.append(client_handler_thread)
    sys.exit(0)
    # exiting and killing all threads, showing no mercy
