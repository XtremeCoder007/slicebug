from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import ECB

from slicebug.cricut.base_plugin import BasePlugin
from slicebug.cricut.protobufs.Bridge_pb2 import PBCommonBridge
from slicebug.exceptions import ProtocolError


class DevicePlugin(BasePlugin):
    def __init__(self, path, request_key):
        super().__init__(path)
        self._request_key = request_key

    def _encrypt_request(self, message):
        cipher = Cipher(AES(self._request_key), ECB())
        encryptor = cipher.encryptor()
        padder = PKCS7(128).padder()
        padded = padder.update(message.SerializeToString()) + padder.finalize()
        return encryptor.update(padded) + encryptor.finalize()

    def send(self, message):
        self.send_bytes(self._encrypt_request(message))

    def _recv(self):
        return PBCommonBridge.FromString(self.recv_bytes())

    def recv(self, expect=None):
        message = self._recv()

        if (expect is not None) and (message.status != expect):
            raise ProtocolError(
                f"incorrect message status: expected {expect}, got {message.status}"
            )

        return message
