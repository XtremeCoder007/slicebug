import struct
import subprocess


class BasePlugin:
    def __init__(self, path):
        self._path = path
        self._process = subprocess.Popen(
            self._path,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self._process.terminate()

    def send_bytes(self, message):
        message_len = struct.pack("<i", len(message))
        self._process.stdin.write(message_len)
        self._process.stdin.write(message)
        self._process.stdin.flush()

    def recv_bytes(self):
        message_len_encoded = self._process.stdout.read(4)
        (message_len,) = struct.unpack("<i", message_len_encoded)
        message = self._process.stdout.read(message_len)
        return message
