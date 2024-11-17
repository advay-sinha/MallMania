def add_item(inventory, item):
    if item not in inventory:
        inventory.append(item)
        return True
    return False

def show_inventory(inventory):
    return inventory if inventory else ["Empty"]
