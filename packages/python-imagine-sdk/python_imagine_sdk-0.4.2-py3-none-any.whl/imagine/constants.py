from http import HTTPStatus


RETRY_STATUS_CODES = {
    # 500: Internal Server Error
    HTTPStatus.INTERNAL_SERVER_ERROR,
    # 502: Bad Gateway
    HTTPStatus.BAD_GATEWAY,
    # 503: Service Unavailable
    HTTPStatus.SERVICE_UNAVAILABLE,
    # 504: Gateway Timeout
    HTTPStatus.GATEWAY_TIMEOUT,
}

TIMEOUT = 30

USER_AGENT_NAME = "python-imagine-sdk"
