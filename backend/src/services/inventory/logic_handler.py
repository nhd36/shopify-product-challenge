import http

from src import utils
from .database_handler import DatabaseHandler


class LogicHandler:
    @classmethod
    def list_inventories(cls, request):
        offset = request.args.get("page", 1, type=int)
        no_items = request.args.get("items", 10, type=int)

        filtered_data = {
            "offset": offset,
            "no_items": no_items
        }
        inventories, paging_data = DatabaseHandler.list_inventories(filtered_data)
        data = {
            "inventory": inventories,
            "paging_data": paging_data
        }
        return utils.Response(data, "success query", http.HTTPStatus.OK.real)

    @classmethod
    def list_deleted_inventories(cls, request):
        offset = request.args.get("page", 1, type=int)
        no_items = request.args.get("items", 10, type=int)

        filtered_data = {
            "offset": offset,
            "no_items": no_items
        }
        del_inventories, paging_data = DatabaseHandler.list_deleted_inventories(filtered_data)
        data = {
            "inventory": del_inventories,
            "paging_data": paging_data
        }
        return utils.Response(data, "success query", http.HTTPStatus.OK.real)

    @classmethod
    def get_inventory(cls, request) -> utils.Response:
        inventory_id = request.view_args["inventory_id"]
        data = DatabaseHandler.get_inventory(inventory_id)
        if not data:
            return utils.Response(None, "data not exists", http.HTTPStatus.NOT_FOUND.real)
        return utils.Response(data, "success query data", http.HTTPStatus.OK.real)

    @classmethod
    def create_inventory(cls, request) -> utils.Response:
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

        if not DatabaseHandler.create_inventory(filtered_data):
            return utils.Response(None, "fail to create data", http.HTTPStatus.INTERNAL_SERVER_ERROR.real)
        return utils.Response(None, "success insert data", http.HTTPStatus.OK.real)

    @classmethod
    def update_inventory(cls, request):
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
        data = DatabaseHandler.get_inventory(inventory_id)
        if not data:
            return utils.Response(None, "data not found", http.HTTPStatus.OK.real)

        # Update the inventory
        if not DatabaseHandler.update_inventory(inventory_id, filtered_data):
            return utils.Response(None, "fail to update", http.HTTPStatus.INTERNAL_SERVER_ERROR.real)
        return utils.Response(None, "success update", http.HTTPStatus.OK.real)

    @classmethod
    def delete_inventory(cls, request):
        inventory_id = request.view_args["inventory_id"]

        # Check if inventory exists
        data = DatabaseHandler.get_inventory(inventory_id)
        if not data:
            return utils.Response(None, "data not found", http.HTTPStatus.OK.real)

        if not DatabaseHandler.delete_inventory(inventory_id):
            return utils.Response(None, "data not found", http.HTTPStatus.NOT_FOUND.real)
        return utils.Response(None, "success delete", http.HTTPStatus.OK.real)

    @classmethod
    def upload_image_inventory(cls, request):
        inventory_id = request.view_args["inventory_id"]
        print(request.files)
        if "image" not in request.files:
            return utils.Response(None, "no file found", http.HTTPStatus.BAD_REQUEST.real)
        image = request.files["image"]
        image_type = utils.is_image_type(image.filename)
        if not image_type:
            return utils.Response(None, "image invalid type", http.HTTPStatus.BAD_REQUEST.real)

        data = DatabaseHandler.get_inventory(inventory_id)
        if not data:
            return utils.Response(None, "data not found", http.HTTPStatus.NOT_FOUND.real)

        image_resize = utils.resize_image(image)
        utils.save_image(image_resize, inventory_id)
        update_data = {
            "has_image": True
        }

        if not DatabaseHandler.update_inventory(inventory_id, update_data):
            return utils.Response(None, "fail to upload image", http.HTTPStatus.INTERNAL_SERVER_ERROR.real)
        return utils.Response(None, "success upload", http.HTTPStatus.OK.real)

    @classmethod
    def undelete_inventory(cls, request):
        inventory_id = request.view_args["inventory_id"]
        # Check if inventory exists
        data = DatabaseHandler.get_deleted_inventory(inventory_id)
        if not data:
            return utils.Response(None, "data not found", http.HTTPStatus.BAD_REQUEST.real)

        if not DatabaseHandler.undelete_inventory(inventory_id):
            return utils.Response(None, "fail to undelete data", http.HTTPStatus.INTERNAL_SERVER_ERROR.real)
        return utils.Response(None, "success undelete data", http.HTTPStatus.OK.real)

    @classmethod
    def get_image_inventory(cls, request):
        inventory_id = request.view_args["inventory_id"]
        # Check if inventory exists
        data = DatabaseHandler.get_inventory(inventory_id)
        if not data:
            return None
        elif not data["has_image"]:
            return None
        return inventory_id
