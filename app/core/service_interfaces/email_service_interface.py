import abc


class EmailServiceInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            (hasattr(subclass, "send"))
            and callable(subclass.send)
            and hasattr(subclass, "client")
        )

    @property
    def client(self):
        raise NotImplementedError

    @abc.abstractmethod
    def send(self, recipients, text_body, html_body):
        """

        :param subject: subject of the email
        :param sender: sender of the email
        :param recipients: recipient of the mail
        :param text_body: body of email in ascii text
        :param html_body: body of email in html format
        :return:
        """
        raise NotImplementedError
