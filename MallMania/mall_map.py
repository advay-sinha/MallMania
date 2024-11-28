# Map layout and item locations
mall_layout = {
    "Entrance": {"neighbors": ["Food Court", "Clothing Store"], "item": None},
    "Food Court": {"neighbors": ["Entrance", "Electronics Store"], "item": ["Pizza"]},
    "Clothing Store": {"neighbors": ["Entrance"], "item": ["Jacket"]},
    "Electronics Store": {"neighbors": ["Food Court"], "item": ["Laptop"]}
}

def get_neighbors(location):
    # Get neighbors for a given location
    if location in mall_layout:
        return mall_layout[location]["neighbors"]
    return []


def change_location(new_location):
    global current_location
    if new_location in get_neighbors(current_location):
        current_location = new_location
        print(f"Moved to {current_location}")
    else:
        print("You can't go there!")


def get_item(location):
    item = mall_layout.get(location, {}).get("item")
    if item:
        mall_layout[location]["item"] = None  # Remove item after collection
    return item