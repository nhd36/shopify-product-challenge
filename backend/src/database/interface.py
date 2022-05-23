from abc import ABC, abstractmethod


class InventoryModelInterface(ABC):
    @abstractmethod
    def create_inventory(self, data):
        pass

    @abstractmethod
    def get_inventory_by_id(self, inventory_id: str):
        pass

    @abstractmethod
    def list_inventories_with_paging(self, page, items_per_page):
        pass

    @abstractmethod
    def list_deleted_inventories_with_paging(self, page, items_per_page):
        pass

    @abstractmethod
    def update_inventory_by_id(self, inventory_id: str, update: dict):
        pass

    @abstractmethod
    def delete_inventory_by_id(self, inventory_id: str):
        pass

    @abstractmethod
    def deserialize(self):
        pass
