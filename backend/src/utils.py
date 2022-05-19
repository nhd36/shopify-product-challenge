import uuid
from typing import Tuple

from PIL import Image
from io import BytesIO
from src.config.config import Config


def generate_random_id() -> str:
    return uuid.uuid4().hex


class Serializer:
    @classmethod
    def serialize_inventory(cls):
        pass

    @classmethod
    def serialize_location(cls):
        pass


class Response:
    def __init__(self, data, message: str, status_code):
        self.data = data
        self.message = message
        self.status_code = status_code

    def format(self) -> dict:
        return {
            "data": self.data,
            "message": self.message,
            "status_code": self.status_code
        }


def validate_coordinates_str(coordinates: str):
    coordinates_list = coordinates.split(",")
    if len(coordinates_list) != 2:
        return False

    lat = coordinates_list[0].strip()
    long = coordinates_list[1].strip()

    if lat.isnumeric() and long.isnumeric():
        return True
    return False


def serialize_inventory(inventory) -> dict:
    data = dict()
    data["name"] = inventory.name
    data["amount"] = inventory.amount
    data["created_at"] = inventory.created_at
    data["id"] = inventory.id
    data["has_image"] = inventory.has_image
    data["deleted_at"] = inventory.deleted_at
    return data


def is_image_type(image_name):
    if image_name == "":
        return None
    image_types = ["png", "jpeg", "jpg"]
    image_type = image_name.split(".")[-1]
    if image_type not in image_types:
        return None
    return image_type


def resize_image(file):
    in_mem_file = BytesIO(file.read())
    image = Image.open(in_mem_file)
    image.thumbnail((500, 500))
    return image


def save_image(image, inventory_id: str) -> str:
    file_name = f"{inventory_id}.png"
    file_url = f"{Config.static_folder}/{file_name}"
    image.save(file_url, "PNG")
    return file_name


def check_fields_in_body(fields: list, data: dict) -> Tuple[bool, str]:
    for field in fields:
        field_name = field[0]
        field_type = field[1]
        if field_name not in data:
            return False, f"missing {field}"
        if type(data[field_name]) != field_type:
            return False, f"invalid type: '{field_name}' is {field_type}"
        if field_type == "str" and data[field_name].strip() == "":
            return False, f"'{field_name}' is blank"
    return True, ""
