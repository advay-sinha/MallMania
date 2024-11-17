npc_dialogues = {
    "Food Court": "Welcome to the Food Court! Try our special burger.",
    "Clothing Store": "Looking for a T-shirt? It's on the rack!",
    "Electronics Store": "We have the latest phones in stock.",
    "Entrance": None
}

def talk_to_npc(location):
    return npc_dialogues.get(location)
