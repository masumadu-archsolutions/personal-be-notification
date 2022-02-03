import pytest

from tests import BaseTestCase

MIGRATING_MODELS = "migrating models"
SEEDING_COMPLETE = "Seeding complete"


class TestSeedDB(BaseTestCase):
    @pytest.mark.model
    def test_seed_db(self):
        runner = self.app.test_cli_runner()
        command = self.app.cli.commands
        result = runner.invoke(command["db_seed"])
        self.assertFalse(result.exception)
        self.assertIn(MIGRATING_MODELS, result.output)
        self.assertIn(SEEDING_COMPLETE, result.output)

    @pytest.mark.model
    def test_seed_sms_model(self):
        runner = self.app.test_cli_runner()
        command = self.app.cli.commands
        result = runner.invoke(command["db_seed"], args=["-m", "smsmodel"])
        self.assertFalse(result.exception)
        self.assertIn(MIGRATING_MODELS, result.output)
        self.assertIn(SEEDING_COMPLETE, result.output)

    @pytest.mark.model
    def test_seed_notification_template_model(self):
        runner = self.app.test_cli_runner()
        command = self.app.cli.commands
        result = runner.invoke(
            command["db_seed"], args=["-m", "notificationtemplatemodel"]
        )
        self.assertFalse(result.exception)
        self.assertIn(MIGRATING_MODELS, result.output)
        self.assertIn(SEEDING_COMPLETE, result.output)

    @pytest.mark.model
    def test_seed_email_model(self):
        runner = self.app.test_cli_runner()
        command = self.app.cli.commands
        result = runner.invoke(command["db_seed"], args=["-m", "emailmodel"])
        self.assertFalse(result.exception)
        self.assertIn(MIGRATING_MODELS, result.output)
        self.assertIn(SEEDING_COMPLETE, result.output)

    @pytest.mark.model
    def test_seed_push_message_model(self):
        runner = self.app.test_cli_runner()
        command = self.app.cli.commands
        result = runner.invoke(command["db_seed"], args=["-m", "pushmessagemodel"])
        self.assertFalse(result.exception)
        self.assertIn(MIGRATING_MODELS, result.output)
        self.assertIn(SEEDING_COMPLETE, result.output)

    @pytest.mark.model
    def test_seed_push_subscription_model(self):
        runner = self.app.test_cli_runner()
        command = self.app.cli.commands
        result = runner.invoke(command["db_seed"], args=["-m", "pushsubscriptionmodel"])
        self.assertFalse(result.exception)
        self.assertIn(MIGRATING_MODELS, result.output)
        self.assertIn(SEEDING_COMPLETE, result.output)
