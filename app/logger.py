import logging
import json_logging
import sys
import time
from datetime import datetime
import json
from json_logging import DefaultRequestResponseDTO
from opentelemetry import trace

# Init logger
logger = logging.getLogger("test-logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

JSON_SERIALIZER = lambda log: json.dumps(log, ensure_ascii=False)

class JSONRequestLogFormatter(logging.Formatter):
    """
       Formatter for HTTP request instrumentation logging
    """

    def format(self, record):
        """
            Format the specified record as text. Overriding default python logging implementation
        """
        log_object = self._format_log_object(record, request_util=json_logging._request_util)
        return JSON_SERIALIZER(log_object)

    def _format_log_object(self, record, request_util):
        json_log_object = {}

        request_adapter = request_util.request_adapter
        response_adapter = request_util.response_adapter

        request = record.request_response_data._request
        response = record.request_response_data._response

        length = request_adapter.get_content_length(request)

        json_log_object.update({
            "type": "request",
            "path": request_adapter.get_path(request),
            "action": request.endpoint,
            "controller": "Main",
            "http_agent": request_adapter.get_http_header(request, 'user-agent', ""),
            "http_referer": request_adapter.get_http_header(request, 'referer', ""),
            "x_forwarded_for": request_adapter.get_http_header(request, 'x-forwarded-for', ""),
            "protocol": request_adapter.get_protocol(request),
            "method": request_adapter.get_method(request),
            "remote_ip": request_adapter.get_remote_ip(request),
            "request_size": json_logging.util.parse_int(length, -1),
            "host": request_adapter.get_remote_ip(request),
            "remote_port": request_adapter.get_remote_port(request),
            "status": response_adapter.get_status_code(response),
            "response_size": response_adapter.get_response_size(response),
            "response_content_type": response_adapter.get_content_type(response),
            "trace_id": trace.get_current_span().get_span_context().trace_id
        })

        json_log_object.update(record.request_response_data)

        return json_log_object


class RequestResponseDTO(DefaultRequestResponseDTO):
    def __init__(self, request, **kwargs):
        super(RequestResponseDTO, self).__init__(request, **kwargs)
        self._request_start = datetime.now()
        self["timestamp"] = time.time()

    # noinspection PyAttributeOutsideInit
    def on_request_complete(self, response):
        super(RequestResponseDTO, self).on_request_complete(response)
        time_delta = datetime.now() - self._request_start
        self["duration"] = int(time_delta.total_seconds()) * 1000 + int(time_delta.microseconds / 1000)