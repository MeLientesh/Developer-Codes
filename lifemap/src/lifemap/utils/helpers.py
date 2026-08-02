def validate_input(data):
    # Validate that the input data is not empty
    if not data:
        raise ValueError("Input data cannot be empty.")
    return True

def format_node_data(node_data):
    # Format the node data for consistency
    return {
        "id": node_data.get("id"),
        "label": node_data.get("label"),
        "type": node_data.get("type", "generic")
    }

def format_relationship_data(relationship_data):
    # Format the relationship data for consistency
    return {
        "source_node": relationship_data.get("source_node"),
        "target_node": relationship_data.get("target_node"),
        "strength": relationship_data.get("strength", 1)
    }

def generate_unique_id(existing_ids):
    # Generate a unique ID for new nodes or relationships
    new_id = 1
    while new_id in existing_ids:
        new_id += 1
    return new_id