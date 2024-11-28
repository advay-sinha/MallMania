import random
import mall_map

npc_riddles = {
    "Food Court": "I am round and cheesy, a favorite of many. What am I?",  # Answer: Pizza
    "Clothing Store": "I keep you warm in the winter, what am I?",  # Answer: Jacket
    "Electronics Store": "I help you talk to someone far away. What am I?",  # Answer: Phone
    "Entrance": None
}

npc_rewards_given = set()  # Track locations where rewards have been collected

def talk_to_npc(location):
    return npc_riddles.get(location)

# Define rewards for different locations
rewards = {
    "Food Court": "Pizza Slice",
    "Clothing Store": "Cool Jacket",
    "Electronics Store": "Smartphone",
    "Entrance": "Keychain",
}

def give_item(location):
    """
    Returns a reward item based on the current location.

    Args:
        location (str): The current location.

    Returns:
        str: The reward item.
    """
    return rewards.get(location, None)

