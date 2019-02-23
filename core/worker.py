#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import queue
import socket
import requests
import threading
import logging as log
from .plugins.IPlugin import connection_type

QUIT = 0xDEADBEEF


class Worker(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.shutdown_flag = threading.Event()
        self.q = queue

    def http_connection(self, addr, plugin):
        res = None
        try:
            url = 'http://{}:{}{}'.format(addr[0],
                                          addr[1], plugin.relative_url)
            res = requests.get(url, allow_redirects=True,
                               verify=False, timeout=plugin.timeout)
        except requests.exceptions.SSLError:
            log.debug('SSLError from {}:{}'.format(addr[0], addr[1]))
        except requests.exceptions.ReadTimeout:
            log.debug('timeout from {}:{}'.format(addr[0], addr[1]))
        except Exception as e:
            log.debug('Error {}:{} -> {}'.format(addr[0], addr[1], e))
        finally:
            return res
        return None

    def raw_connection(self, addr):
        sock = socket.socket()
        sock.settimeout(1)
        try:
            sock.connect((addr[0], addr[1]))
        except socket.timeout:
            log.debug("Socket timeout from {}:{}".format(addr[0], addr[1]))
            return None
        except socket.error:
            log.debug("Socket connect error {}:{}".format(addr[0], addr[1]))
            return None
        return sock

    def connect(self, addr, plugin):
        if plugin.connection_type is connection_type.WEB:
            log.debug("Creating websocket for {}:{}".format(addr[0], addr[1]))
            return self.http_connection(addr, plugin)
        elif plugin.connection_type is connection_type.RAW:
            log.debug("Creating TCP socket for {}:{}".format(addr[0], addr[1]))
            return self.raw_connection(addr)
        return None

    def run(self):
        log.debug("Starting new thread")
        while not self.shutdown_flag.is_set():
            addr = self.q.get()
            if addr is QUIT:
                log.info("error=Thread stopping by QUIT")
                return
            for port, _, plugin in PLUGINS:
                if port == addr[1]:
                    conn = self.connect(addr, plugin)
                    if conn:
                        plugin.exec(conn)
            self.q.task_done()
        log.info("error=Thread stopping by SHUTDOWN_FLAG")


class Queue():
    def __init__(self):
        self.max_workers = None
        self.q = queue.Queue()
        self.threads = []

    def init(self, plugin, threads):
        global PLUGINS
        PLUGINS = plugin
        self.max_workers = threads
        for i in range(self.max_workers):
            t = Worker(self.q)
            t.start()
            self.threads.append(t)

    def push(self, data):
        res = data.split()
        log.info(
            "New_job={}:{} queue_size={}".format(
                res[0],
                res[1],
                self.q.qsize()))
        try:
            self.q.put((res[0], int(res[1])))
        except Exception as e:
            log.error('Error Q PUT {} -> {}'.format(data))

    def stop(self):
        for i in range(self.max_workers):
            self.q.put(QUIT)
        for t in self.threads:
            t.shutdown_flag.set()
        for w in self.threads:
            w.join()


if __name__ == '__main__':
    pass
