"""module for global exceptions used in vcapi"""


class TypeErrorOL(TypeError):
    """TypeError exception with premade error message"""

    def __init__(self, expected: type, actual: type):
        super().__init__(
            f"Expected '{str(expected)}', received '{str(actual)}'"
        )
