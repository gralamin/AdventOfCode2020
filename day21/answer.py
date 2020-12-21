import time


class Food:
    def __init__(self, input_str):
        ingredient_str, allergen_str = input_str.split("(contains")
        allergen_str = allergen_str.strip()[:-1]
        self.allergens = set(allergen_str.split(", "))
        self.ingredients = set(ingredient_str.strip().split(" "))

    def has_allergen(self, allergen):
        return allergen in self.allergens

    def get_ingredients_not_in(self, remove):
        return self.ingredients.difference(remove)

    def __repr__(self):
        return f"Food({self.allergens}, {self.ingredients})"


def get_input():
    with open("input", "r") as f:
        i = 0
        for x in f:
            i += 1
            if not x.strip():
                continue
            yield Food(x)


def get_potential_allergiens(foods):
    allergens = set()
    for food in foods:
        allergens = allergens.union(food.allergens)

    allergen_to_potential_ingredient = {}
    for allergen in allergens:
        potential_ingredients = set()
        for food in foods:
            if not food.has_allergen(allergen):
                continue
            if len(potential_ingredients) == 0:
                potential_ingredients = potential_ingredients.union(food.ingredients)
                continue
            potential_ingredients = potential_ingredients.intersection(food.ingredients)
        allergen_to_potential_ingredient[allergen] = potential_ingredients
    return allergen_to_potential_ingredient


def part1(foods):
    allergen_to_potential_ingredient = get_potential_allergiens(foods)
    all_potential_allergen = set()
    for possible_foods in allergen_to_potential_ingredient.values():
        all_potential_allergen = all_potential_allergen.union(possible_foods)
    unique_ingredients = []
    for food in foods:
        for x in food.get_ingredients_not_in(all_potential_allergen):
            unique_ingredients.append(x)
    return len(unique_ingredients)


if __name__ == "__main__":
    foods = list(get_input())
    start = time.perf_counter()
    print("Part1:", part1(foods))
    end = time.perf_counter()
    print("Completed in {}ms.".format((end - start) * 1000))
    print("\n")
