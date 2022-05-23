import copy
import math

from src.database.interface import InventoryModelInterface
from src import utils
from datetime import datetime
import heapq


class InventoryModelTest(InventoryModelInterface):
    mock_database = list()
    heapq.heapify(mock_database)

    def __init__(self, name: str, amount: int):
        self.id = utils.generate_random_id()
        self.name = name
        self.amount = amount
        self.created_at = datetime.now()
        self.deleted_at = None
        self.has_image = False

    @classmethod
    def create_inventory(cls, data):
        inventory_test = InventoryModelTest(data["name"], data["amount"])
        current_time = datetime.utcnow().timestamp()
        heapq.heappush(cls.mock_database, (current_time, inventory_test))
        return inventory_test

    @classmethod
    def get_inventory_by_id(cls, inventory_id: str):
        for wrapper in cls.mock_database:
            if wrapper[1].id == inventory_id:
                return wrapper[1]
        return None

    @classmethod
    def __get_inventories(cls, deleted=False):
        inventories = copy.deepcopy(cls.mock_database)
        copy_inventories = list()
        while len(inventories) > 0:
            inventory = heapq.heappop(inventories)[1]
            if not deleted and inventory.deleted_at is None:
                copy_inventories.append(inventory)
            elif deleted and inventory.deleted_at is not None:
                copy_inventories.append(inventory)
        return copy_inventories

    @classmethod
    def paging_inventories(cls, database: list, page: int, items_per_page: int):
        prev_page = page - 1
        index_start = prev_page * items_per_page
        index_end = index_start + items_per_page
        print(index_end, len(database))
        if index_start > len(database) - 1:
            return []
        if index_end > len(database) - 1:
            return database[index_start:]
        return database[index_start:index_end]

    @classmethod
    def list_inventories_with_paging(cls, page, items_per_page):
        paging_data = {
            "items_per_page": items_per_page,
            "page": page,
            "total": math.ceil(len(cls.mock_database) / items_per_page)
        }
        database = cls.__get_inventories()
        return cls.paging_inventories(database, page, items_per_page), paging_data

    @classmethod
    def list_deleted_inventories_with_paging(cls, page, items_per_page):
        database = cls.__get_inventories(True)
        return cls.paging_inventories(database, page, items_per_page)

    @classmethod
    def update_inventory_by_id(cls, inventory_id: str, update: dict):
        for index in range(len(cls.mock_database)):
            if cls.mock_database[index][1].id == inventory_id:
                if "amount" in update:
                    cls.mock_database[index][1].amount = update["amount"]
                if "name" in update:
                    cls.mock_database[index][1].name = update["name"]
        return True

    @classmethod
    def delete_inventory_by_id(cls, inventory_id: str):
        database = list()
        while len(cls.mock_database) > 0:
            inventory = heapq.heappop(cls.mock_database)
            if inventory[1].id == inventory_id:
                continue
            database.append(inventory)
        cls.mock_database = database
        return True

    def deserialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "amount": self.amount,
            "created_at": self.created_at,
            "deleted_at": self.deleted_at,
            "has_image": self.has_image
        }

