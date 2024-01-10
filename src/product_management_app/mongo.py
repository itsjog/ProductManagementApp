import pprint

from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from product_management_app.datatypes import DefaultData


class MongoDbController:
    def __init__(self, client) -> None:
        self.client = client

    def delete_data(self, collection: Collection[DefaultData], data: DefaultData):
        print(f"Removing test document with following data:")
        pprint.pprint(data, indent=4, width=100)
        return collection.delete_one(data).deleted_count

    def insert_test_data(
        self, collection: Collection[DefaultData], test_data: DefaultData
    ) -> int:
        print(f"Adding test document with data: ")
        pprint.pprint(test_data, indent=4, width=100)
        return collection.insert_one(test_data).inserted_id

    def ping_server(self) -> None:
        # Send a ping to confirm a successful connection
        try:
            self.client.admin.command("ping")
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def show_all_products(self, collection: Collection[DefaultData]):
        return collection.find()

    def remove_a_product(self, collection: Collection[DefaultData]):
        entry_id = int(input("Select an ID to remove: "))
        return collection.delete_one(
            {
                "_id": entry_id,
            },
        ).deleted_count

    def show_single_product(self, collection: Collection[DefaultData]):
        entry_id = int(input("Select an ID to look for: "))
        return collection.find_one(
            {"_id": entry_id},
        )

    def store_new_product(self, collection: Collection[DefaultData]):
        new_entry_id = int(input("Select an ID to store: "))
        new_name = input("Introduce a name: ")
        new_release_date = input("Introduce product's release date:")
        try:
            return collection.insert_one(
                {
                    "_id": new_entry_id,
                    "name": new_name,
                    "release_date": new_release_date,
                }
            )
        except DuplicateKeyError:
            print("ID already in use")
            return self.store_new_product(collection)

    def update_a_product(self, collection: Collection[DefaultData]):
        entry_id = int(input("Select an ID to update: "))

        update_name = input("Introduce a name: ")
        update_release_date = input("Introduce product's release date:")
        return collection.update_one(
            {
                "_id": entry_id,
            },
            {
                "$set": {
                    "name": update_name,
                    "release_date": update_release_date,
                },
            },
        ).modified_count
