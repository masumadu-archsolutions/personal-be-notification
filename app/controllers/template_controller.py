from app.definitions.result import Result
from app.definitions.service_result import ServiceResult
from app.repositories import NotificationTemplateRepository


class TemplateController:
    def __init__(self, notification_template_repository: NotificationTemplateRepository):
        self.repository = notification_template_repository

    def index(self):
        templates = self.repository.index()
        return ServiceResult(Result(templates, 200))

    def show(self, template_id):
        template = self.repository.find_by_id(template_id)
        return ServiceResult(Result(template, 200))

    def create(self, data):
        template = self.repository.create(data)
        return ServiceResult(Result(template, 201))

    def update(self, template_id, data):
        template = self.repository.update_by_id(template_id, data)
        return ServiceResult(Result(template, 200))

    def delete(self, template_id):
        self.repository.delete(template_id)
        ServiceResult(Result({}, 204))
