import http

from src import utils
from src.services.inventory.interface import DatabaseInterface, LogicInterface


class LogicHandler(LogicInterface):
    def __init__(self, database: DatabaseInterface):
        self.database = database

    def list_inventories(self, request):
        offset = request.args.get("page", 1, type=int)
        no_items = request.args.get("items", 10, type=int)

        filtered_data = {
            "offset": offset,
            "no_items": no_items
        }
        inventories, paging_data = self.database.list_inventories(filtered_data)
        data = {
            "inventory": inventories,
            "paging_data": paging_data
        }
        return utils.Response(data, "success query", http.HTTPStatus.OK.real)

    def list_deleted_inventories(self, request):
        offset = request.args.get("page", 1, type=int)
        no_items = request.args.get("items", 10, type=int)

        filtered_data = {
            "offset": offset,
            "no_items": no_items
        }
        del_inventories, paging_data = self.database.list_deleted_inventories(filtered_data)
        data = {
            "inventory": del_inventories,
            "paging_data": paging_data
        }
        return utils.Response(data, "success query", http.HTTPStatus.OK.real)

    def get_inventory(self, request) -> utils.Response:
        inventory_id = request.view_args["inventory_id"]
        data = self.database.get_inventory(inventory_id)
        if not data:
            return utils.Response(None, "data not exists", http.HTTPStatus.NOT_FOUND.real)
        return utils.Response(data, "success query data", http.HTTPStatus.OK.real)

    def create_inventory(self, request) -> utils.Response:
        filtered_data = dict()
        if not request.json:
            return utils.Response(None, "missing body", http.HTTPStatus.BAD_REQUEST.real)

        data = request.json
        fields = [("name", str), ("amount", int)]
        valid, message = utils.check_fields_in_body(fields, data)
        if not valid:
            return utils.Response(None, message, http.HTTPStatus.BAD_REQUEST.real)

        filtered_data["name"] = data["name"].strip()
        filtered_data["amount"] = data["amount"]

        inventory = self.database.create_inventory(filtered_data)
        if inventory is None:
            return utils.Response(None, "fail to create data", http.HTTPStatus.INTERNAL_SERVER_ERROR.real)
        return utils.Response(inventory, "success insert data", http.HTTPStatus.OK.real)

    def update_inventory(self, request):
        data = request.json
        filtered_data = dict()
        if "name" in data and data["name"].strip() != "":
            filtered_data["name"] = data["name"].strip()

        if "amount" in data and type(data["amount"]) == int:
            filtered_data["amount"] = data["amount"]

        if len(filtered_data) == 0:
            return utils.Response(None, "nothing to update", http.HTTPStatus.BAD_REQUEST.real)
        inventory_id = request.view_args["inventory_id"]

        # Check if inventory exists
        data = self.database.get_inventory(inventory_id)
        if not data:
            return utils.Response(None, "data not found", http.HTTPStatus.OK.real)

        # Update the inventory
        inventory = self.database.update_inventory(inventory_id, filtered_data)
        if not inventory:
            return utils.Response(None, "fail to update", http.HTTPStatus.INTERNAL_SERVER_ERROR.real)
        return utils.Response(None, "success update", http.HTTPStatus.OK.real)

    def delete_inventory(self, request):
        inventory_id = request.view_args["inventory_id"]

        # Check if inventory exists
        data = self.database.get_inventory(inventory_id)
        if not data:
            return utils.Response(None, "data not found", http.HTTPStatus.OK.real)

        if not self.database.delete_inventory(inventory_id):
            return utils.Response(None, "data not found", http.HTTPStatus.NOT_FOUND.real)
        return utils.Response(None, "success delete", http.HTTPStatus.OK.real)

    def upload_image_inventory(self, request):
        inventory_id = request.view_args["inventory_id"]
        if "image" not in request.files:
            return utils.Response(None, "no file found", http.HTTPStatus.BAD_REQUEST.real)
        image = request.files["image"]
        image_type = utils.is_image_type(image.filename)
        if not image_type:
            return utils.Response(None, "image invalid type", http.HTTPStatus.BAD_REQUEST.real)

        data = self.database.get_inventory(inventory_id)
        if not data:
            return utils.Response(None, "data not found", http.HTTPStatus.NOT_FOUND.real)

        image_resize = utils.resize_image(image)
        utils.save_image(image_resize, inventory_id)
        update_data = {
            "has_image": True
        }

        if not self.database.update_inventory(inventory_id, update_data):
            return utils.Response(None, "fail to upload image", http.HTTPStatus.INTERNAL_SERVER_ERROR.real)
        return utils.Response(None, "success upload", http.HTTPStatus.OK.real)

    def undelete_inventory(self, request):
        inventory_id = request.view_args["inventory_id"]
        # Check if inventory exists
        data = self.database.get_deleted_inventory(inventory_id)
        if not data:
            return utils.Response(None, "data not found", http.HTTPStatus.BAD_REQUEST.real)

        if not self.database.undelete_inventory(inventory_id):
            return utils.Response(None, "fail to undelete data", http.HTTPStatus.INTERNAL_SERVER_ERROR.real)
        return utils.Response(None, "success undelete data", http.HTTPStatus.OK.real)

    def get_image_inventory(self, request):
        inventory_id = request.view_args["inventory_id"]
        # Check if inventory exists
        data = self.database.get_inventory(inventory_id)
        if not data:
            return None
        elif not data["has_image"]:
            return None
        return inventory_id
