from src.database import models
from src import utils


class DatabaseHandler:
    @classmethod
    def list_inventories(cls, data):
        paging_data, inventories = models.Inventory.list_inventories_with_paging(
            page=data["offset"],
            items_per_page=data["no_items"]
        )
        result = list()
        for inventory in inventories:
            result.append(utils.serialize_inventory(inventory))
        paging = {
            "items_per_page": paging_data.per_page,
            "page": paging_data.page,
            "total": paging_data.pages
        }
        return result, paging

    @classmethod
    def list_deleted_inventories(cls, data):
        paging_data, del_inventories = models.Inventory.list_deleted_inventories_with_paging(
            page=data["offset"],
            items_per_page=data["no_items"]
        )
        result = list()
        for inventory in del_inventories:
            result.append(utils.serialize_inventory(inventory))
        paging = {
            "items_per_page": paging_data.per_page,
            "page": paging_data.page,
            "total": paging_data.pages
        }
        return result, paging

    @classmethod
    def create_inventory(cls, data):
        inventory = models.Inventory(data["name"], data["amount"])
        return inventory.create_inventory()

    @classmethod
    def get_inventory(cls, inventory_id):
        data = models.Inventory.get_inventory_by_id(inventory_id)
        if data:
            if not data.deleted_at:
                data = utils.serialize_inventory(data)
            else:
                return None
        return data

    @classmethod
    def update_inventory(cls, inventory_id, data):
        return models.Inventory.update_inventory_by_id(inventory_id, data)

    @classmethod
    def delete_inventory(cls, inventory_id):
        return models.Inventory.delete_inventory_by_id(inventory_id)

    @classmethod
    def undelete_inventory(cls, inventory_id):
        update = {
            "deleted_at": None
        }
        return models.Inventory.update_inventory_by_id(inventory_id, update)

    @classmethod
    def get_deleted_inventory(cls, inventory_id):
        data = models.Inventory.get_inventory_by_id(inventory_id)
        if not data:
            return None
        elif not data.deleted_at:
            return None
        return data
