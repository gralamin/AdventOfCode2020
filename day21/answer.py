import time


class Food:
    def __init__(self, input_str, allergens=None, ingredients=None):
        if allergens is None or ingredients is None:
            ingredient_str, allergen_str = input_str.split("(contains")
            allergen_str = allergen_str.strip()[:-1]
            self.allergens = set(allergen_str.split(", "))
            self.ingredients = set(ingredient_str.strip().split(" "))
        else:
            self.allergens = allergens
            self.ingredients = ingredients

    def has_allergen(self, allergen):
        return allergen in self.allergens

    def get_ingredients_not_in(self, remove):
        return self.ingredients.difference(remove)

    def create_food_without(self, remove_ingredients, remove_allergens):
        return Food(
            None,
            self.allergens.difference(remove_allergens),
            self.ingredients.difference(remove_ingredients),
        )

    @property
    def not_empty(self):
        return len(self.allergens) > 0 and len(self.ingredients) > 0

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


def simplify_food(foods):
    # Basically sudoku solve: We know a bunch have to be things
    # So take those out of the others, and solve 1 by 1 until we have all of
    # them as unique.
    uniques = {}
    all_allergen_to_potential_ingredient = get_potential_allergiens(foods)

    while len(uniques) != len(all_allergen_to_potential_ingredient.keys()):
        # print("")
        # print(len(uniques), len(all_allergen_to_potential_ingredient.keys()))
        # print(foods)
        allergen_dict = get_potential_allergiens(foods)

        all_potential_allergen = set()
        for possible_foods in allergen_dict.values():
            all_potential_allergen = all_potential_allergen.union(possible_foods)

        # print(allergen_dict)
        if not allergen_dict:
            raise ValueError("Should have ended")
        known_not_allergens = []
        for food in foods:
            for x in food.get_ingredients_not_in(all_potential_allergen):
                known_not_allergens.append(x)
        # print(known_not_allergens)

        for key, values in allergen_dict.items():
            if len(values) == 1:
                # print(f"adding unique {key}")
                uniques[key] = values.pop()

        unique_allergens = set(uniques.keys())
        unique_ingredients = set(uniques.values())
        unique_ingredients = unique_ingredients.union(known_not_allergens)
        # print(unique_allergens)
        # print(unique_ingredients)
        foods = [
            f.create_food_without(unique_ingredients, unique_allergens) for f in foods
        ]
        foods = [f for f in foods if f.not_empty]
    return uniques


def part2(foods):
    csv = []
    uniques = simplify_food(foods)
    for key in sorted(uniques.keys()):
        csv.append(uniques[key])
    return ",".join(csv)


if __name__ == "__main__":
    foods = list(get_input())
    start = time.perf_counter()
    print("Part1:", part1(foods))
    end = time.perf_counter()
    print("Completed in {}ms.".format((end - start) * 1000))
    print("\n")

    start = time.perf_counter()
    print("Part2:", part2(foods))
    end = time.perf_counter()
    print("Completed in {}ms.".format((end - start) * 1000))
    print("\n")
