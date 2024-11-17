# Map layout and item locations
mall_layout = {
    "Entrance": {"neighbors": ["Food Court", "Clothing Store"], "item": None},
    "Food Court": {"neighbors": ["Entrance", "Electronics Store"], "item": "Burger"},
    "Clothing Store": {"neighbors": ["Entrance"], "item": "T-shirt"},
    "Electronics Store": {"neighbors": ["Food Court"], "item": "Phone"}
}

def get_neighbors(location):
    return mall_layout.get(location, {}).get("neighbors", [])

def get_item(location):
    item = mall_layout.get(location, {}).get("item")
    if item:
        mall_layout[location]["item"] = None  # Remove item after collection
    return item
