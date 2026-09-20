def cakes(recipe, available):
    pasteles = []
    if not recipe or not available:
        return 0
    for ingredient in recipe:
        if ingredient not in available:
            return 0
        else:
            pasteles.append(available[ingredient] // recipe[ingredient])
    return min(pasteles)

print(cakes({'flour': 500, 'sugar': 200, 'eggs': 1}, {'flour': 1200, 'sugar': 1200, 'eggs': 5, 'milk': 200}))