from app.api.api_v1.endpoints.sms_view import sms


def init_app(app):
    """
    Register app blueprints over here
    # eg: # app.register_blueprint(user, url_prefix="/api/users")
    :param app:
    :return:
    """
    app.register_blueprint(sms, url_prefix="/api/sms")
