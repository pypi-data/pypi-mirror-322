"""module containing a rewrite of the botocore Crendetial class for
streamlining libraries"""

from __future__ import annotations


class Credentials:
    """A rewrite of the botocore credential class.

    attributes:
        access_key(str): the access key for aws
        secret_key(str): the secret key for aws
        token(str, optional): the temporary session token. Defaults to
            None if connecting with user and not role
    """

    def __init__(
        self,
        access_key: str,
        secret_key: str,
        token: str | None = None,
    ) -> None:

        self.access_key = access_key
        self.secret_key = secret_key
        self.token = token
