import http

from flask import Blueprint, request, send_file
from flask_cors import cross_origin
from src.config.config import Config
from src.database import models
from src.services.inventory.database_handler import DatabaseHandler

from .logic_handler import LogicHandler

inventory_service = Blueprint("inventory_blueprint", __name__, url_prefix="/inventory")
database_handler = DatabaseHandler(models.Inventory)
logic_handler = LogicHandler(database_handler)


@inventory_service.route("", methods=["GET", "POST"])
@cross_origin(headers=["Content-Type", "Authorization"])
def list_create_inventories():
    if request.method == "GET":
        response = logic_handler.list_inventories(request)
        return response.format(), response.status_code

    if request.method == "POST":
        response = logic_handler.create_inventory(request)
        return response.format(), response.status_code


@inventory_service.route("/<inventory_id>", methods=["GET", "PUT", "DELETE"])
@cross_origin(headers=["Content-Type", "Authorization"])
def rud_inventory(inventory_id):
    if request.method == "GET":
        response = logic_handler.get_inventory(request)
        return response.format(), response.status_code

    if request.method == "PUT":
        response = logic_handler.update_inventory(request)
        return response.format(), response.status_code

    if request.method == "DELETE":
        response = logic_handler.delete_inventory(request)
        return response.format(), response.status_code


@inventory_service.route("/image/<inventory_id>", methods=["GET", "PUT"])
@cross_origin(headers=["Content-Type", "Authorization"])
def handle_image(inventory_id):
    if request.method == "GET":
        data = logic_handler.get_image_inventory(request)
        if data:
            return send_file(f"{Config.static_folder}/{data}.png"), http.HTTPStatus.OK.real
        return "No image exists", http.HTTPStatus.NOT_FOUND.real
    if request.method == "PUT":
        response = logic_handler.upload_image_inventory(request)
        return response.format(), response.status_code


@inventory_service.route("/delete", methods=["GET"])
@cross_origin(headers=["Content-Type", "Authorization"])
def list_deleted_inventories():
    if request.method == "GET":
        response = logic_handler.list_deleted_inventories(request)
        return response.format(), response.status_code


@inventory_service.route("/undelete/<inventory_id>", methods=["PUT"])
@cross_origin(headers=["Content-Type", "Authorization"])
def undelete_inventory(inventory_id):
    if request.method == "PUT":
        response = logic_handler.undelete_inventory(request)
        return response.format(), response.status_code
