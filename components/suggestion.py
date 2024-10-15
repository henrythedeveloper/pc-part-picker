from .data_loader import load_components

def suggest_build(budget, preferences=None):
    data = load_components()
    build = {}
    remaining_budget = budget

    # Prioritize components (adjust as needed)
    component_order = ['cpus', 'motherboards', 'gpus', 'rams', 'storage', 'power_supplies', 'cases']

    for comp_type in component_order:
        components = data[comp_type]
        # Apply preferences
        if preferences and 'brand' in preferences:
            components = [comp for comp in components if comp.get('brand', '').lower() == preferences['brand'].lower()]
        # Sort by price descending to get the best within budget
        components = sorted(components, key=lambda x: x['price'], reverse=True)
        for comp in components:
            if comp['price'] <= remaining_budget:
                build[comp_type[:-1].capitalize()] = comp
                remaining_budget -= comp['price']
                break  # Move to next component

    return build, remaining_budget
