import json
import os
import typing

import httpx
import urllib3


class ResponseStream(httpx.SyncByteStream):
    CHUNK_SIZE = 1024

    def __init__(self, urllib3_stream: typing.Any) -> None:
        self._urllib3_stream = urllib3_stream

    def __iter__(self) -> typing.Iterator[bytes]:
        for chunk in self._urllib3_stream.stream(self.CHUNK_SIZE, decode_content=False):
            yield chunk

    def close(self) -> None:
        self._urllib3_stream.release_conn()


class URLLib3Transport(httpx.BaseTransport):
    def __init__(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.pool = urllib3.PoolManager(cert_reqs="CERT_NONE")

    def handle_request(self, request: httpx.Request):
        payload = json.loads(request.content.decode("utf-8").replace("'", '"'))
        encoded_data = json.dumps(payload).encode("utf-8")

        is_stream = payload.get("stream", True)

        response = self.pool.request(
            request.method,
            str(request.url),
            headers=request.headers,
            body=encoded_data,
            preload_content=not is_stream,
            timeout=30,
        )  # Convert httpx.URL to string

        if not is_stream:
            return httpx.Response(
                response.status,
                headers=httpx.Headers(
                    [(name, value) for name, value in response.headers.iteritems()]
                ),
                content=response.data,
            )
        else:
            return httpx.Response(
                status_code=response.status,
                headers=httpx.Headers(
                    [(name, value) for name, value in response.headers.iteritems()]
                ),
                content=ResponseStream(response),
                extensions={"urllib3_response": response},
            )


def env_var_to_bool(env_var_name: str) -> bool:
    return os.getenv(env_var_name, "false").lower() in {"true", "1", "t", "y", "yes"}
