"""module for global exceptions used in vcapi"""


class TypeErrorOL(TypeError):

    def __init__(self, expected: type, actual: type):
        super().__init__(
            f"Expected '{str(expected)}', received '{str(actual)}'"
        )
