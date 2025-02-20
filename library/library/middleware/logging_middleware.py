import logging
import time

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """Middleware to log request details and response status codes."""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        # Process request
        response = self.get_response(request)

        # Log detailed request & response info
        self.log_request_response(request, response, start_time)

        return response

    def log_request_response(self, request, response, start_time):
        """Logs detailed info about each request and response."""
        execution_time = round((time.time() - start_time) * 1000, 2)  # in ms
        log_message = (
            f"[{request.method}] {request.path} - Status {response.status_code} "
            f"- Time: {execution_time}ms"
        )

        # Log extra data for debugging
        extra_data = {
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "execution_time": execution_time,
        }

        if response.status_code >= 400:
            logger.error(log_message, extra=extra_data)
        else:
            logger.info(log_message, extra=extra_data)
