# my_plugin/middleware.py
import logging

logger = logging.getLogger(__name__)

class PrdaLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        logger.info(f"Request received: {request.method} {request.path}")

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        logger.info(f"Response sent: {response.status_code}")

        return response
    

#class DynamicBasePathMiddleware:
#    def __init__(self, get_response):
#        self.get_response = get_response
#
#    def __call__(self, request):
#        logging.error("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
#        custom_path = request.META.get("HTTP_X_CUSTOM_PATH", "")
#        logging.error(f"AAAAAAAAAAAAAAA:   {custom_path}")
#        if custom_path:
#            logging.error("Jsem v IF")
#            request.META["CUSTOM_PATH"] = custom_path
#            request.path_info = request.path_info[len(custom_path):]
#        return self.get_response(request)

class DynamicBasePathMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Získání custom_path z hlavičky (např. HTTP_X_CUSTOM_PATH)
        custom_path = request.META.get("HTTP_X_CUSTOM_PATH", "")
        logging.error(f"Custom path: {custom_path}")

        # Pokud custom_path existuje a path_info začíná custom_path
        if custom_path and request.path_info.startswith(custom_path):
            # Uložení původní cesty pro pozdější použití (pokud je potřeba)
            request.META["ORIGINAL_PATH_INFO"] = request.path_info
            logging.error(f"Original path info: {request.path_info}")

            # Upravení path_info (odstranění custom_path)
            request.path_info = request.path_info[len(custom_path):]
            logging.error(f"New path info: {request.path_info}")

            # Upravení path (odstranění custom_path)
            request.path = request.path[len(custom_path):]
            logging.error(f"New path: {request.path}")

        # Pokračování v zpracování požadavku
        response = self.get_response(request)

        return response