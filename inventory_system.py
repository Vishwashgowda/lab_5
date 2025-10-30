"""
Inventory System Module
Provides basic inventory management functions like adding, removing, saving,
and loading stock data from a JSON file.
"""

import json
import logging
from datetime import datetime
import ast

# Configure logging
logging.basicConfig(
    filename='inventory.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def add_item(stock_data, item="default", qty=0, logs=None):
    """Add a given quantity of an item to stock."""
    if logs is None:
        logs = []

    if not isinstance(item, str) or not isinstance(qty, int):
        logging.warning("Invalid types: item=%s, qty=%s", type(item), type(qty))
        return stock_data

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")
    logging.info("Added %d of %s", qty, item)
    return stock_data


def remove_item(stock_data, item, qty):
    """Remove a given quantity of an item from stock."""
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        logging.error("Tried to remove non-existent item: %s", item)
    except TypeError:
        logging.error("Invalid quantity type for removal: %s", qty)
    return stock_data


def get_qty(stock_data, item):
    """Return the current quantity of an item."""
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """Load inventory data from a JSON file."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.warning("File %s not found. Starting with empty data.", file)
        return {}
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON from %s", file)
        return {}


def save_data(stock_data, file="inventory.json"):
    """Save current stock data to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(stock_data, f, indent=4)
    logging.info("Data saved successfully to %s", file)


def print_data(stock_data):
    """Print all items and their quantities."""
    print("Items Report")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")


def check_low_items(stock_data, threshold=5):
    """Return list of items below a certain threshold."""
    return [i for i, q in stock_data.items() if q < threshold]


def main():
    """Main function to test inventory operations."""
    stock_data = {}

    stock_data = add_item(stock_data, "apple", 10)
    stock_data = add_item(stock_data, "banana", 2)
    stock_data = remove_item(stock_data, "apple", 3)
    stock_data = remove_item(stock_data, "orange", 1)

    print(f"Apple stock: {get_qty(stock_data, 'apple')}")
    print(f"Low items: {check_low_items(stock_data)}")

    save_data(stock_data)
    stock_data = load_data()

    print_data(stock_data)

    # Example of safe evaluation using ast.literal_eval
    safe_eval = ast.literal_eval("['eval', 'safe']")
    print("Safe eval result:", safe_eval)


if __name__ == "__main__":
    main()
