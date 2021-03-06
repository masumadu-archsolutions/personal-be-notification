import inspect
import os
from functools import wraps

import jwt
from flask import request
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, PyJWTError

from app.core.exceptions import AppException


def auth_required(other_roles=None):
    def authorize_user(func):
        """
        A wrapper to authorize an action using
        :param func: {function} the function to wrap around
        :return:
        """

        @wraps(func)
        def view_wrapper(*args, **kwargs):
            authorization_header = request.headers.get("Authorization")
            if not authorization_header:
                raise AppException.ValidationException("Missing authentication token")

            token = authorization_header.split()[1]
            try:
                key = os.getenv("JWT_PUBLIC_KEY")  # noqa E501
                payload = jwt.decode(
                    token,
                    key=key,
                    algorithms=["HS256", "RS256"],
                    audience="account",
                    issuer=os.getenv("JWT_ISSUER"),
                )  # noqa E501
                # Get realm roles from payload
                available_roles = payload.get("realm_access").get("roles")

                # Append service name to function name to form role
                # e.g customer_update_user
                service_name = os.getenv("SERVICE_NAME")
                generated_role = service_name + "_" + func.__name__

                authorized_roles = []

                if other_roles:
                    authorized_roles = other_roles.split("|")

                authorized_roles.append(generated_role)

                if is_authorized(authorized_roles, available_roles):
                    if "user_id" in inspect.getfullargspec(func).args:
                        kwargs["user_id"] = payload.get(
                            "preferred_username"
                        )  # noqa E501
                    return func(*args, **kwargs)
            except ExpiredSignatureError:
                raise AppException.ExpiredTokenException("Token Expired")
            except InvalidTokenError:
                raise AppException.OperationError("Invalid Token")
            except PyJWTError:
                raise AppException.OperationError("Error decoding token")
            raise AppException.Unauthorized()

        return view_wrapper

    return authorize_user


def is_authorized(access_roles, available_roles):
    for role in access_roles:
        if role in available_roles:
            return True

    return False
