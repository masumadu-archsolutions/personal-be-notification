import abc


class SMSServiceInterface(metaclass=abc.ABCMeta):
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
    def send(self, sender, receiver, message):
        """

        :param sender: sender of the message
        :param receiver: the data of that should be saved
        :param message: expiration of the data in seconds
        :return:
        """
        raise NotImplementedError
