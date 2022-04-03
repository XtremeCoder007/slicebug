class UserError(Exception):
    """Raised when we'd like to ask the user to do something differently."""

    def __init__(self, message, resolution=None):
        super().__init__(message, resolution)


class ProtocolError(Exception):
    """Raised when Cricut software did something unexpected."""
