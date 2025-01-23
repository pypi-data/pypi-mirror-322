"""Top-level package for NetBox cesnet_services Plugin."""

__author__ = """Jan Krupa"""
__email__ = "jan.krupa@cesnet.cz"
__version__ = "0.0.1"


from netbox.plugins import PluginConfig
#from middleware import PrdaLoggingMiddleware, DynamicBasePathMiddleware


class PrdaMiddlewareConfig(PluginConfig):
    name = "prda_middleware"
    verbose_name = "Prda Middleware"
    description = ""
    version = __version__
    base_url = "prda-middleware"
    middleware = ["prda_middleware.middleware.PrdaLoggingMiddleware", "prda_middleware.middleware.DynamicBasePathMiddleware"]


config = PrdaMiddlewareConfig
