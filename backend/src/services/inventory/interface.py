from src import utils
from abc import ABC, abstractmethod


class DatabaseInterface(ABC):
    @abstractmethod
    def list_inventories(self, request):
        pass

    @abstractmethod
    def list_deleted_inventories(self, data):
        pass

    @abstractmethod
    def get_inventory(self, inventory_id):
        pass

    @abstractmethod
    def create_inventory(self, data):
        pass

    @abstractmethod
    def update_inventory(self, inventory_id, data):
        pass

    @abstractmethod
    def delete_inventory(self, inventory_id):
        pass

    @abstractmethod
    def get_deleted_inventory(self, inventory_id):
        pass

    @abstractmethod
    def undelete_inventory(self, inventory_id):
        pass


class LogicInterface(ABC):
    @abstractmethod
    def list_inventories(self, request) -> utils.Response:
        pass

    @abstractmethod
    def list_deleted_inventories(self, request) -> utils.Response:
        pass

    @abstractmethod
    def get_inventory(self, request) -> utils.Response:
        pass

    @abstractmethod
    def create_inventory(self, request) -> utils.Response:
        pass

    @abstractmethod
    def update_inventory(self, request) -> utils.Response:
        pass

    @abstractmethod
    def delete_inventory(self, request) -> utils.Response:
        pass

    @abstractmethod
    def upload_image_inventory(self, request) -> utils.Response:
        pass

    @abstractmethod
    def undelete_inventory(self, request) -> utils.Response:
        pass

    def get_image_inventory(self, request) -> str:
        pass

