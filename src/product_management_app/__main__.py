from typing import Any, Dict

import rich
from pymongo.database import Database
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from product_management_app.mongo import MongoDbController


class DatabaseSecrets:
    collection_name: str = "products"


def main():
    uri = input("Introduce the uri for connection: ")
    # Create a new client and connect to the server.
    client: MongoClient[Dict[str, Any]] = MongoClient(uri, server_api=ServerApi("1"))

    # Test connectivity.
    controller = MongoDbController(client)
    controller.ping_server()

    # Ask for database name to connect.
    database_name = str(input("Introduce the database name:"))
    database = client[database_name]

    # If test_collection doesn't exists app will create it.
    test_collection = database.test_collection

    # Initialize test date to be created.
    test_data = {"_id": 1, "name": "test", "release_date": "10/01/2024"}

    # We use this to test connectivity with collection.
    test_response = controller.insert_test_data(test_collection, test_data)
    print(f"Added test document with id {test_response}")
    print()

    # Then remove the created test data.
    controller.delete_data(test_collection, data=test_data)
    print(f"Removed test document")

    show_menu(controller, database)


def show_menu(controller: MongoDbController, database: Database):
    """Shows a menu with valid options and do something."""
    options = [
        "Show all products",
        "Show a single product",
        "Store a new product",
        "Update a product",
        "Remove a product",
        "Exit",
    ]
    tree = Tree("Menu", guide_style="bold red")
    for key, option in enumerate(options):
        tree.add(f"{Text(str(key+1))} {option}")
    rich.print(tree)

    selected_option = int(input(f"Select an option (1-{len(options)}): "))
    collection = database[DatabaseSecrets.collection_name]
    if selected_option == 1:
        table = Table(header_style="bold red")
        table.add_column("ID", style="dim", width=12)
        table.add_column("NAME")
        table.add_column("Release Date", justify="right")
        for entry in controller.show_all_products(collection):
            if entry is None:
                continue
            table.add_row(
                str(entry["_id"]), str(entry["name"]), str(entry["release_date"])
            )
        rich.print(table)
    elif selected_option == 2:
        entry = controller.show_single_product(collection)
        if entry is None:
            print()
            show_menu(controller, database)
        table = Table(header_style="bold red")
        table.add_column("ID", style="dim", width=12)
        table.add_column("NAME")
        table.add_column("Release Date", justify="right")
        table.add_row(str(entry["_id"]), str(entry["name"]), str(entry["release_date"]))
        rich.print(table)
    elif selected_option == 3:
        controller.store_new_product(collection)
    elif selected_option == 4:
        controller.update_a_product(collection)
    elif selected_option == 5:
        controller.remove_a_product(collection)
    elif selected_option == 6:
        raise SystemExit(0)
    else:
        print()
        show_menu(controller, database)
    print()
    show_menu(controller, database)


if __name__ == "__main__":
    main()
