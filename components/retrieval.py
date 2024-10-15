import json

def load_components():
    with open('data/components_data.json', 'r') as f:
        data = json.load(f)
    return data

def get_affordable_components(budget, preferences=None):
    data = load_components()
    affordable_components = {}

    # Initialize remaining budget
    remaining_budget = budget

    # Define the order of component selection (you can adjust this)
    component_types = ['cpus', 'motherboards', 'gpus', 'rams', 'storage', 'power_supplies', 'cases']

    for component_type in component_types:
        components = data.get(component_type, [])
        # Apply preferences if any
        if preferences and 'brand' in preferences:
            components = [c for c in components if c.get('brand', '').lower() == preferences['brand'].lower()]
        # Sort components by price (ascending)
        components = sorted(components, key=lambda x: x['price'])
        # Find the most expensive component within the remaining budget
        affordable_component = None
        for component in components:
            if component['price'] <= remaining_budget:
                affordable_component = component
            else:
                break
        if affordable_component:
            affordable_components[component_type] = affordable_component
            remaining_budget -= affordable_component['price']
        else:
            # If no component fits in the budget, skip this component type
            continue

    return affordable_components, remaining_budget
