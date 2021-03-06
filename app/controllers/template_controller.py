from app.core.result import Result
from app.repositories import NotificationTemplateRepository


class NotificationTemplateController:
    def __init__(self, notification_template_repository: NotificationTemplateRepository):
        self.repository = notification_template_repository

    def index(self):
        templates = self.repository.index()
        return Result(templates, 200)

    def show(self, template_id):
        template = self.repository.find_by_id(template_id)
        return Result(template, 200)

    def create(self, data):
        template = self.repository.create(data)
        return Result(template, 201)

    def update(self, template_id, data):
        template = self.repository.update_by_id(template_id, data)
        return Result(template, 200)

    def delete(self, template_id):
        self.repository.delete(template_id)
        return Result({}, 204)
        # TODO: delete template file when template is deleted
