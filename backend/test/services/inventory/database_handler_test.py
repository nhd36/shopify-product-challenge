from test.services.inventory import InventoryModelTest
from src.services.inventory.database_handler import DatabaseHandler
import unittest

database_handler_mock = DatabaseHandler(InventoryModelTest)


class DatabaseHandlerTest(unittest.TestCase):
    __paging_data = {
        "offset": 1,
        "no_items": 1
    }
    __mock_inventory_data = {
        "name": "Nam Dao",
        "amount": 1000
    }

    def test_initially_empty_database(self):
        inventories, paging_data = database_handler_mock.list_inventories(self.__paging_data)
        self.assertEqual(len(inventories), 0)

    def test_create_new_inventory(self):
        inventory = database_handler_mock.create_inventory(self.__mock_inventory_data)
        inventories, paging_data = database_handler_mock.list_inventories(self.__paging_data)
        self.assertEqual(inventory["name"], self.__mock_inventory_data["name"])
        self.assertEqual(inventory["amount"], self.__mock_inventory_data["amount"])
        self.assertEqual(1, len(inventories))

    def test_get_inventory_by_id(self):
        inventory = database_handler_mock.create_inventory(self.__mock_inventory_data)
        inventoryRetrieve = database_handler_mock.get_inventory(inventory["id"])
        self.assertIsNotNone(inventoryRetrieve)
        self.assertEqual(inventory["id"], inventoryRetrieve["id"])

    def test_create_two_inventories_inorder(self):
        inventory = database_handler_mock.create_inventory(self.__mock_inventory_data)
        inventory2 = database_handler_mock.create_inventory({
            "name": "Nam Dao 1",
            "amount": 10000
        })
        inventories, paging_data = database_handler_mock.list_inventories({
            "offset": 1,
            "no_items": 10
        })
        self.assertEqual(len(inventories), 2)
        self.assertEqual(inventories[0]["id"], inventory["id"])
        self.assertEqual(inventories[1]["id"], inventory2["id"])

    def test_update_inventory(self):
        update_data = {
            "name": "Nam Dao 1",
            "amount": 2000
        }
        inventory = database_handler_mock.create_inventory(self.__mock_inventory_data)
        database_handler_mock.update_inventory(inventory["id"], update_data)
        inventoryUpdated = database_handler_mock.get_inventory(inventory["id"])
        self.assertEqual(inventoryUpdated["id"], inventory["id"])
        self.assertEqual(inventoryUpdated["name"], update_data["name"])
        self.assertEqual(inventoryUpdated["amount"], update_data["amount"])

    def test_delete_inventory(self):
        inventory = database_handler_mock.create_inventory(self.__mock_inventory_data)
        database_handler_mock.delete_inventory(inventory["id"])
        inventories, paging_data = database_handler_mock.list_inventories(self.__paging_data)
        self.assertEqual(len(inventories), 0)


