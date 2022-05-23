from src.services.inventory.interface import DatabaseInterface
from src.database.interface import InventoryModelInterface


class DatabaseHandler(DatabaseInterface):
    def __init__(self, database_model: InventoryModelInterface):
        self.database_model = database_model

    def list_inventories(self, data):
        inventories, paging_data = self.database_model.list_inventories_with_paging(
            page=data["offset"],
            items_per_page=data["no_items"]
        )
        result = list()
        for inventory in inventories:
            result.append(inventory.deserialize())
        return result, paging_data

    def list_deleted_inventories(self, data):
        del_inventories, paging = self.database_model.list_deleted_inventories_with_paging(
            page=data["offset"],
            items_per_page=data["no_items"]
        )
        result = list()
        for inventory in del_inventories:
            result.append(inventory.deserialize())
        return result, paging

    def create_inventory(self, data):
        inventory = self.database_model.create_inventory(data)
        if not inventory:
            return None
        return inventory.deserialize()

    def get_inventory(self, inventory_id):
        data = self.database_model.get_inventory_by_id(inventory_id)
        if data:
            if not data.deleted_at:
                data = data.deserialize()
            else:
                return None
        return data

    def update_inventory(self, inventory_id, data):
        return self.database_model.update_inventory_by_id(inventory_id, data)

    def delete_inventory(self, inventory_id):
        return self.database_model.delete_inventory_by_id(inventory_id)

    def undelete_inventory(self, inventory_id):
        update = {
            "deleted_at": None
        }
        return self.database_model.update_inventory_by_id(inventory_id, update)

    def get_deleted_inventory(self, inventory_id):
        data = self.database_model.get_inventory_by_id(inventory_id)
        if not data:
            return None
        elif not data.deleted_at:
            return None
        return data
