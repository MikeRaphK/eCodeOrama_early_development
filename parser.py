def get_parent_event(block_id : str, blocks : list):
    if not blocks[block_id]["parent"]:
        return blocks[block_id]["opcode"]
    return get_parent_event(blocks[block_id]["parent"], blocks)


def parse_json(project_json : dict) -> dict:
    """
    Parses the given JSON's block sequences per sprite.

    Args:
        project_json (dict): The loaded JSON content from a Scratch project's project.json file.

    Returns:
        dict: A dictionary where each key is a sprite's name (unique). The value is a dictionary which contains the following items:
                - 'events': A list of event names which trigger the sprite. Each event is represented as a tuple,
                where the first item is the event name and the rest of the items are event parameters (if they exist)
                - 'broadcasts_sent': A list of broadcasts which the sprite sends. Each broadcast is represented as a tuple,
                where the first item is the broadcast name and the second item is the event that caused this broadcast
                - 'costume': The id of a costume that will be used for codeOrama
    """
    sprite_communication = {}
    sprite_list = project_json["targets"]

    # Go over each sprite
    for sprite in sprite_list:
        name = sprite["name"]
        blocks = sprite["blocks"]
        events = []
        broadcasts_sent = []

        # Go over all of its blocks
        for block_id, block_data in blocks.items():
            opcode = block_data["opcode"]

            # Events
            if opcode == "event_whenflagclicked" or opcode == "event_whenthisspriteclicked":
                events.append((opcode,))
            elif opcode == "event_whenkeypressed":
                key = block_data["fields"]["KEY_OPTION"][0]
                events.append((opcode, key))
            elif opcode == "event_whenbackdropswitchesto":
                backdrop = block_data["fields"]["BACKDROP"][0]
                events.append((opcode, backdrop))
            elif opcode == "event_whengreaterthan":
                metric = block_data["fields"]["WHENGREATERTHANMENU"][0]
                value = block_data["inputs"]["VALUE"][1][1]
                events.append((opcode, metric, value))
            elif opcode == "event_whenbroadcastreceived":
                message = block_data["fields"]["BROADCAST_OPTION"][0]
                events.append((opcode, message))
            # Broadcast sent
            elif opcode == "event_broadcast":
                message = block_data["inputs"]["BROADCAST_INPUT"][1][1]
                parent = get_parent_event(block_id, blocks)
                broadcasts_sent.append((message, parent))

        sprite_communication[name] = {"events" : events, "broadcasts_sent" : broadcasts_sent, "costume" : sprite["costumes"][0]["assetId"]}

    return sprite_communication