"""class responsible for the sigv4 signature in http request"""

from __future__ import annotations

from urllib.parse import quote as uri_encode
from hashlib import sha256
import hmac
import datetime as dt
import logging

import requests
from requests.auth import AuthBase

from aws_sig._credentials import Credentials
from aws_sig._utils import sorted_dictionary, url_parse
from aws_sig.exceptions import TypeErrorOL as TypeError

TIMESTAMP_FORMAT = "%Y%m%dT%H%M%SZ"
DATE_FORMAT = "%Y%m%d"

LOGGER = logging.getLogger(__name__)


class SigV4(AuthBase):
    """SigV4 based authorizer"""

    _credentials: Credentials
    _service: str
    _region: str

    CONTENT_HEADER = "X-Amz-Content-SHA256"

    def __init__(
        self,
        aws_access_key: str,
        aws_secret_key: str,
        region: str,
        service: str,
        aws_session_token: str | None = None,
    ):

        self._credentials = Credentials(
            aws_access_key,
            aws_secret_key,
            aws_session_token
        )

        self._service = service.lower()
        self._region = region.lower()

    def __call__(
            self,
            request: requests.PreparedRequest
    ) -> requests.PreparedRequest:
        """used for authentication in API requests

        Args:
            request (requests.Request): the request making an
                authentication request
            time (dt.datetime): an override to the current time for
                testing purposes
        """

        time = dt.datetime.utcnow()

        url = url_parse(request.url)
        query = url["query"]

        # get base headers
        headers = request.headers if request.headers is not None else {}

        aws_headers = {
            "Host": url["netloc"],
            "X-Amz-Date": time.strftime(TIMESTAMP_FORMAT)
        }

        if self._credentials.token is not None:
            aws_headers["X-Amz-Security-Token"] = self._credentials.token

        if self.CONTENT_HEADER in headers:
            aws_headers[self.CONTENT_HEADER] = headers[self.CONTENT_HEADER]

        # encode the body if needed
        body = request.body

        if isinstance(body, bytes):
            body = body.decode()

        # get canonical request
        canonical_request = self._get_canonical_request(
            method=request.method,
            host=url["netloc"],
            ressource=url["path"],
            query=query,
            headers=aws_headers,
            payload=body,
            time=time
        )

        # get string to sign
        string_to_sign = self._get_string_to_sign(
            time=time,
            canonical_request=canonical_request,
        )

        # get signature
        signature = self._get_signature(string_to_sign, time)

        request.headers = self._get_authorization_headers(
            {x.lower(): y for x, y in aws_headers.items()},
            signature,
        )

        for key, val in headers.items():
            if key not in request.headers:
                request.headers[key] = val

        return request

    def _get_authorization_headers(
            self,
            headers: dict[str, str],
            signature: str,
    ) -> str:
        """return the final authorization headers formatted and ordered

        Args:
            headers (dict[str, str]): the headers to include with the
                signature
            signature (str): the signature

        Returns:
            str: the full authroization header
        """

        # sort the headers alphabetically and raise if not a dictionnary
        headers = sorted_dictionary(headers)

        # raise if signature not a string
        if not isinstance(signature, str):
            raise TypeError(str, type(signature))

        # get date stamp and signed headers for final authorization
        # header
        datestamp = headers["x-amz-date"][:8]
        signed_headers = ';'.join(headers.keys())

        # buld the final header
        headers["Authorization"] = (
            "AWS4-HMAC-SHA256 "
            f"Credential={self._credentials.access_key}/{datestamp}/"
            f"{self._region}/{self._service}/aws4_request,"
            f"SignedHeaders={signed_headers},"
            f"Signature={signature}"
        )

        return headers

    def _get_signature(
        self,
        string_to_sign: str,
        time: dt.datetime,
    ) -> str:

        # check that time is a datetime object
        try:
            datestamp = time.strftime(DATE_FORMAT)
        except AttributeError as exc:
            raise TypeError from exc

        # calculate signature
        date_key = self.sign(
            f"AWS4{self._credentials.secret_key}",
            datestamp
        )

        region_key = self.sign(date_key, self._region)
        service_key = self.sign(region_key, self._service)
        signing_key = self.sign(service_key, "aws4_request")

        return self.sign(signing_key, string_to_sign, True)

    @staticmethod
    def sign(
        key: bytes,
        message: bytes,
        return_hex: bool = False
    ) -> bytes | str:
        """signs a message with the key provided and returns the byte or
        hex digest based on what is requested

        Args:
            key (bytes): the key to encrypt the message
            message (bytes): the message to encrypt
            hex (bool, optional): Returns the hex digest if True.
                Defaults to False.

        Returns:
            bytes|str: the byte or hex digest
        """

        # convert key and message to bytes if not already
        if isinstance(key, str):
            key = key.encode()

        if isinstance(message, str):
            message = message.encode()

        # make the encryption object
        encrypted = hmac.new(key, message, sha256)

        # convert to str or bytes based on request from user
        if return_hex:
            return encrypted.hexdigest()

        return encrypted.digest()

    def _get_string_to_sign(
        self,
        time: dt.datetime,
        canonical_request: str,
    ) -> str:
        """prepares the string to -sign based on the calculated
        canonical request

        Args:
            time (dt.datetime): the timestamp to use in the signature
            canonical_request (str): the cannonical request calculated

        Returns:
            str: the string to sign formatted
        """

        # check for any attribution error and raise type error if found
        try:
            timestamp = time.strftime(TIMESTAMP_FORMAT)
            datestamp = time.strftime(DATE_FORMAT)
            hashed_request = sha256(canonical_request.encode()).hexdigest()
        except AttributeError as exc:
            raise TypeError from exc

        return (
            "AWS4-HMAC-SHA256\n"
            f"{timestamp}\n"
            f"{datestamp}/{self._region}/{self._service}/aws4_request\n"
            f"{hashed_request}"
        )

    def _get_canonical_request(
        self,
        method: str,
        host: str,
        ressource: str,
        *,
        query: dict[str, str],
        headers: dict[str, str],
        time: dt.datetime,
        payload: str = None,
    ) -> str:
        """calculates the canonical request for AWS auth

        Args:
            method (str): the rest API method being used
            ressource (str): the ressource called on the API endpoint
            query (dict): the query in a dictionary format
            headers (dict): the headers in a dictionary format
            payload (str, optional): the payload for the request

        Returns:
            str: the formatted canonical request
        """

        # hash the payload
        payload = "" if payload == [] or payload is None else payload

        try:
            hashed_payload = sha256(payload.encode()).hexdigest()
        except AttributeError as exc:
            raise TypeError from exc

        # replace empty ressource with forward slash
        ressource = "/" if ressource == "" or ressource is None else ressource

        # prepare headers
        try:
            canonical_headers = sorted_dictionary(
                {
                    x.lower(): y.strip()
                    for x, y in headers.items()
                }
            )

            del headers

            # ensure query is alhabetically sorted for hashing
            query = sorted_dictionary(query)

        except (AttributeError, TypeError) as exc:
            raise TypeError from exc

        # add host, content hash and timestamp to headers
        if isinstance(host, str):
            canonical_headers["host"] = host
        else:
            raise TypeError(str, type(host))

        # make sure time object is a datetime object
        try:
            canonical_headers["x-amz-date"] = time.strftime(TIMESTAMP_FORMAT)
        except AttributeError as exc:
            raise TypeError from exc

        # sort the headers by keys
        canonical_headers = {
            x: canonical_headers[x]
            for x in sorted(canonical_headers.keys())
        }

        # prepare payload

        # ensure http_verb is upper case
        try:
            http_verb = method.upper()
        except AttributeError as exc:
            raise TypeError from exc

        # encode the ressource to url_encoding standard
        canonical_uri = uri_encode(ressource)

        canonical_query_str = '&'.join(
            [
                f"{uri_encode(x)}={uri_encode(str(y)).replace('/', '%2F')}"
                for x, y in query.items()
            ]
        )

        # create the canonical header string by providing one line per
        # header. The key is changed to lower case and the value is
        # strip of trailling spaces
        canonical_header_str = '\n'.join(
            [f"{x.lower()}:{y.strip()}" for x, y in canonical_headers.items()]
        ) + '\n'

        # create the signed headers by providing an alphabetically
        # ordered list of the keys in the headers
        signed_headers = ';'.join(
            [x.lower() for x in canonical_headers.keys()]
        )

        return (
            f"{http_verb}\n"
            f"{canonical_uri}\n"
            f"{canonical_query_str}\n"
            f"{canonical_header_str}\n"
            f"{signed_headers}\n"
            f"{hashed_payload}"
        )
