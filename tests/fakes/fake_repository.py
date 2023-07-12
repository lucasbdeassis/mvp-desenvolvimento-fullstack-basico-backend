from src.adapters.abc_repository import AbstractRepository


class FakeRepository(AbstractRepository):
    data = {}

    def create(self, model):
        self.data[model.id] = model

    def get(self, id):
        return self.data[id]

    def update(self, model):
        self.data[model.id] = model

    def delete(self, id):
        del self.data[id]

    def list(self, filters=None, order_by=None, limit=None, offset=None):
        return self.data.values()
