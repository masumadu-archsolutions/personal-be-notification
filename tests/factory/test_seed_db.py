import pytest

from app.models import EmailModel, NotificationTemplateModel, SMSModel
from tests import BaseTestCase


class TestSeedDB(BaseTestCase):
    @pytest.mark.model
    def test_seed_db(self):
        runner = self.app.test_cli_runner()
        self.assertEqual(NotificationTemplateModel.query.count(), 2)
        command = self.app.cli.commands
        result = runner.invoke(command["db_seed"])
        self.assertFalse(result.exception)
        self.assertIn("migrating models", result.output)
        self.assertIn("Seeding complete", result.output)

    @pytest.mark.model
    def test_seed_sms_model(self):
        runner = self.app.test_cli_runner()
        self.assertEqual(SMSModel.query.count(), 1)
        command = self.app.cli.commands
        result = runner.invoke(command["db_seed"], args=["-m", "smsmodel"])
        self.assertFalse(result.exception)
        self.assertIn("migrating models", result.output)
        self.assertIn("Seeding complete", result.output)
        self.assertEqual(SMSModel.query.count(), 2)
        cmd_result = runner.invoke(
            command["db_seed"], args=["-c", "3", "-m", "smsmodel"]
        )
        self.assertFalse(cmd_result.exception)
        self.assertIn("migrating models", cmd_result.output)
        self.assertIn("Seeding complete", cmd_result.output)
        self.assertEqual(SMSModel.query.count(), 5)

    @pytest.mark.model
    def test_seed_notification_template_model(self):
        runner = self.app.test_cli_runner()
        self.assertEqual(NotificationTemplateModel.query.count(), 2)
        command = self.app.cli.commands
        result = runner.invoke(
            command["db_seed"], args=["-m", "notificationtemplatemodel"]
        )
        self.assertFalse(result.exception)
        self.assertIn("migrating models", result.output)
        self.assertIn("Seeding complete", result.output)

    @pytest.mark.model
    def test_seed_email_model(self):
        runner = self.app.test_cli_runner()
        self.assertEqual(EmailModel.query.count(), 1)
        command = self.app.cli.commands
        result = runner.invoke(command["db_seed"], args=["-m", "emailmodel"])
        self.assertFalse(result.exception)
        self.assertIn("migrating models", result.output)
        self.assertIn("Seeding complete", result.output)
        self.assertEqual(EmailModel.query.count(), 2)
        cmd_result = runner.invoke(
            command["db_seed"], args=["-c", "3", "-m", "emailmodel"]
        )
        self.assertFalse(cmd_result.exception)
        self.assertIn("migrating models", cmd_result.output)
        self.assertIn("Seeding complete", cmd_result.output)
        self.assertEqual(EmailModel.query.count(), 5)
