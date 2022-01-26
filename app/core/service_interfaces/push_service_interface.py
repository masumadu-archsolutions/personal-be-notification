import abc


class PushServiceInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, "send")) and callable(subclass.send)

    @abc.abstractmethod
    def send(self, subscription_info, message):
        """

        :param subscription_info: receiving device id
        :param message: title of the message
        # :param body: body of the message
        :return:
        """
        raise NotImplementedError
