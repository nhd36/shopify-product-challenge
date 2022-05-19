import datetime
from flask_sqlalchemy import SQLAlchemy
from src import utils

db = SQLAlchemy()


class Inventory(db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.String, primary_key=True, index=True)
    name = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Integer, default=0)
    created_at = db.Column(db.Float, default=datetime.datetime.utcnow().timestamp())
    deleted_at = db.Column(db.Float, default=None)
    has_image = db.Column(db.Boolean, default=False)

    # Many-To-Many relationship since 1 item can be at multiple locations, and 1 location can have multiple items
    locations = db.relationship("LocationInventory", back_populates="inventory")

    def __init__(self, name: str, amount: int) -> None:
        self.id = utils.generate_random_id()
        self.name = name
        self.amount = amount

    def create_inventory(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as ex:
            print(ex)
            return False
        return True

    @classmethod
    def get_inventory_by_id(cls, inventory_id: str):
        data = cls.query.filter_by(
            id=inventory_id
        ).first()
        return data

    @classmethod
    def get_inventories(cls):
        data = cls.query.filter_by(
            deleted_at=None
        ).all()

        return data

    @classmethod
    def list_condition_inventories_with_paging(cls, page=1, items_per_page=10, deleted=False):
        if not deleted:
            data = cls.query.filter_by(
                deleted_at=None
            )
        else:
            data = cls.query.filter(
                cls.deleted_at.isnot(None)
            )
        paging_data = data.paginate(
            page,
            items_per_page,
            False
        )
        return paging_data, paging_data.items

    @classmethod
    def list_inventories_with_paging(cls, page=1, items_per_page=10):
        return cls.list_condition_inventories_with_paging(page, items_per_page, deleted=False)

    @classmethod
    def list_deleted_inventories_with_paging(cls, page=1, items_per_page=10):
        return cls.list_condition_inventories_with_paging(page, items_per_page, deleted=True)

    @classmethod
    def update_inventory_by_id(cls, inventory_id: str, update: dict):
        data = cls.query.filter_by(
            id=inventory_id
        )
        try:
            data.update(update)
            db.session.commit()
        except Exception as ex:
            print(ex)
            return False
        return True

    @classmethod
    def delete_inventory_by_id(cls, inventory_id: str):
        delete = {
            "deleted_at": datetime.datetime.utcnow().timestamp()
        }
        return cls.update_inventory_by_id(inventory_id, delete)


class Location(db.Model):
    __tablename__ = "location"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.String(5), nullable=False, index=True)
    coordinates = db.Column(db.String(20))
    created_at = db.Column(db.Float, default=datetime.datetime.utcnow().timestamp())
    deleted_at = db.Column(db.Float, default=None)

    # Many-To-Many relationships, explained in the Inventory
    inventories = db.relationship("LocationInventory", back_populates="location")

    def __init__(self, name, address, zip_code, coordinates):
        self.name = name
        self.address = address
        self.zip_code = zip_code
        self.coordinates = coordinates

    @classmethod
    def list_locations_with_paging(cls, page=1, items_per_page=10):
        data = cls.query.filter_by(
            deleted_at=None
        ).order_by(
            cls.created_at.desc()
        ).paginate(
            page,
            items_per_page,
            False
        ).items
        return data

    @classmethod
    def get_location_by_id(cls, location_id):
        data = cls.query.filter_by(
            id=location_id
        ).first()
        return data

    @classmethod
    def get_location_by_zip_code(cls, zip_code):
        data = cls.query.filter_by(
            zip_code=zip_code
        ).all()
        return data


# Associate table, mapping 2 tables
class LocationInventory(db.Model):
    __tablename__ = "location_inventory"

    inventory_id = db.Column(db.ForeignKey("inventory.id"), primary_key=True)
    location_id = db.Column(db.ForeignKey("location.id"), primary_key=True)
    created_at = db.Column(db.Float, default=datetime.datetime.utcnow().timestamp())
    deleted_at = db.Column(db.Float, default=None)

    inventory = db.relationship(Inventory, back_populates="locations")
    location = db.relationship(Location, back_populates="inventories")
