""" tcp receiver - thread based """

import socket
import threading
import time

TIMEOUT = 1.0

class ThreadedReceiver(threading.Thread):
    """Threaded tcp receiver that receives the data and stores it key value based"""
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self._ip_port = (ip, port)
        self._running = False
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._d_lock = threading.Lock()
        self._datastore = {}
    def _go_server(self):
        self._running = True
        self._socket.bind(self._ip_port)
        self._socket.listen(0)
        self._socket.settimeout(TIMEOUT)

        while self._running:
            try:
                conn, _ = self._socket.accept()
            except socket.timeout:
                continue
            conn.settimeout(TIMEOUT)
            try:
                data = conn.recv(1024)
            except socket.timeout:
                conn.close()
                continue
            if not data:
                break
            if data.strip()[:2] == "::":
                conn.send(self._handle_cmd(data))
            else:
                self._handle_data(data)
            conn.close()
        self._socket.close()

    def stop_receiver(self):
        """ Stop the thread and join it """
        self._running = False
        self.join()

    def _handle_data(self,data):
        spl = data.strip()
        if spl.count(" ") > 0:
            key = spl[:spl.find(" ")]
            val = spl[spl.find(" ")+1:]
            try:
                value = float(val)
            except ValueError:
                value = val
            self.set_value(key, value)
    def _handle_cmd(self, data):
        cmd = data.strip()
        if cmd == "::quit":
            self._running = False
            return "OK"
        elif cmd == "::dumpdata":
            res = "All data:\n"
            for key in self._datastore.keys():
                res += str(key) + ": "+str(self._datastore[key])+"\n"
            return res
        return "Unknown command"

    def run(self):
        self._go_server()
    def get_value(self, key):
        self._d_lock.acquire()
        if key in self._datastore:
            ret = self._datastore[key]
        else:
            ret = 0
        self._d_lock.release()
        return ret

    def set_value(self, key, value):
        self._d_lock.acquire()
        self._datastore[key] = value
        self._d_lock.release()



def test_main():
    """ test the class """
    trsrv = ThreadedReceiver('127.0.0.1', 9530)
    trsrv.start()

    while trsrv._running:
        time.sleep(1)
        print trsrv._datastore

    trsrv.stop_receiver()

if __name__ == "__main__":
    test_main()
