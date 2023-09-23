import os
import socket
from threading import Thread

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

class ChatReaderThread(Thread):
    def __init__(self, conn, addr):
        """Инициализация потока"""
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr

    def run(self):
        with self.conn:
            while True:
                data = self.conn.recv(1024)
                if not data or data == "goodbye":
                    break
                print(data)

class ChatWriterThread(Thread):
    def __init__(self, conn, addr):
        """Инициализация потока"""
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr

    def run(self):
        with self.conn:
            while True:
                data = input()
                if data == "goodbye":
                    break
                self.conn.sendall(data)

def main(urls):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        crt = ChatReaderThread(conn, addr)
        cwt = ChatWriterThread(conn, addr)
        crt.start()
        cwt.start()
        crt.join()
        cwt.join()


if __name__ == "__main__":
    main()