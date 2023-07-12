import abc


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, model):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, model):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, id):
        raise NotImplementedError

    @abc.abstractmethod
    def list(self, filters=None, order_by=None, limit=None, offset=None):
        raise NotImplementedError
