from app.api.api_v1.endpoints.sms_view import sms
from app.api.api_v1.endpoints.template_view import template


def init_app(app):
    """
    Register app blueprints over here
    # eg: # app.register_blueprint(user, url_prefix="/api/users")
    :param app:
    :return:
    """
    app.register_blueprint(sms, url_prefix="/api/v1/sms")
    app.register_blueprint(template, url_prefix="/api/v1/templates")
