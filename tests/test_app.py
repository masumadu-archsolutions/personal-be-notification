import pytest

from tests import BaseTestCase


class TestAppConfig(BaseTestCase):
    @pytest.mark.app
    def test_app_config(self):
        self.assertTrue(self.app.config["DEBUG"])
        self.assertTrue(self.app.config["TESTING"])
        self.assertTrue(self.app.config["DEVELOPMENT"])
        self.assertIsNotNone(self.app.config["SECRET_KEY"])
