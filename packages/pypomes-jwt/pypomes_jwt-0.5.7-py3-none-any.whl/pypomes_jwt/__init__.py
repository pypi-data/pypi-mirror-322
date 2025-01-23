from .jwt_data import (
    jwt_request_token, jwt_validate_token
)
from .jwt_pomes import (
    JWT_ENDPOINT_URL,
    JWT_ACCESS_MAX_AGE, JWT_REFRESH_MAX_AGE,
    JWT_HS_SECRET_KEY, JWT_RSA_PRIVATE_KEY, JWT_RSA_PUBLIC_KEY,
    jwt_needed, jwt_verify_request,
    jwt_get_claims, jwt_get_token, jwt_get_token_data,
    jwt_service, jwt_set_service_access, jwt_remove_service_access
)

__all__ = [
    # jwt_data
    "jwt_request_token", "jwt_validate_token",
    # jwt_pomes
    "JWT_ENDPOINT_URL",
    "JWT_ACCESS_MAX_AGE", "JWT_REFRESH_MAX_AGE",
    "JWT_HS_SECRET_KEY", "JWT_RSA_PRIVATE_KEY", "JWT_RSA_PUBLIC_KEY",
    "jwt_needed", "jwt_verify_request",
    "jwt_get_claims", "jwt_get_token", "jwt_get_token_data",
    "jwt_service", "jwt_set_service_access", "jwt_remove_service_access"
]

from importlib.metadata import version
__version__ = version("pypomes_jwt")
__version_info__ = tuple(int(i) for i in __version__.split(".") if i.isdigit())
