import json

from slicebug.cricut.base_plugin import BasePlugin
from slicebug.cricut.protobufs.CriGeo_pb2 import Command, CommandResponse
from slicebug.exceptions import UserError, ProtocolError


class PathUtilPlugin(BasePlugin):
    def send(self, message):
        self.send_bytes(message.SerializeToString())

    def recv(self):
        return CommandResponse.FromString(self.recv_bytes())

    def svg_to_canvas(self, svg):
        command = Command()
        command.svgConvertCanvas.svg = svg
        self.send(command)

        response = self.recv()

        match type_ := response.WhichOneof("type"):
            case "errorResponse":
                raise UserError(
                    f"SVG parser returned error: {response.errorResponse.detail}",
                )
            case "svgConvertCanvasResponse":
                return json.loads(response.svgConvertCanvasResponse.canvas)
            case _:
                raise ProtocolError(f"unexpected response type: {type_}")
