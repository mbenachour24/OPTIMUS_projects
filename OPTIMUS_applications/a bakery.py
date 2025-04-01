import time

class Inventory:
    def __init__(self):
        # Initialize stock of raw materials and products
        self.raw_materials = {"flour": 100, "sugar": 50, "eggs": 30}
        self.baked_goods = {"bread": 0, "cake": 0}

    def check_stock(self, item):
        return self.raw_materials.get(item, 0)

    def use_material(self, item, quantity):
        if self.raw_materials.get(item, 0) >= quantity:
            self.raw_materials[item] -= quantity
            return True
        return False

    def add_product(self, product, quantity):
        self.baked_goods[product] += quantity

    def remove_product(self, product, quantity):
        if self.baked_goods.get(product, 0) >= quantity:
            self.baked_goods[product] -= quantity
            return True
        return False

class Bakery:
    def __init__(self, inventory):
        self.inventory = inventory

    def bake(self, product, recipe):
        # Check if enough raw materials are available to bake
        for ingredient, quantity in recipe.items():
            if not self.inventory.use_material(ingredient, quantity):
                print(f"Not enough {ingredient} to bake {product}.")
                return False
        self.inventory.add_product(product, 1)
        print(f"Baked 1 {product}.")
        return True

class Sales:
    def __init__(self, inventory):
        self.inventory = inventory
        self.sales = 0

    def sell(self, product):
        if self.inventory.remove_product(product, 1):
            self.sales += 1
            print(f"Sold 1 {product}.")
            return True
        else:
            print(f"Out of stock for {product}.")
            return False

class BakeryOrchestrator:
    def __init__(self):
        self.inventory = Inventory()
        self.bakery = Bakery(self.inventory)
        self.sales = Sales(self.inventory)

    def run_iteration(self):
        # Bakery bakes bread and cake if enough materials
        print("\nChecking inventory and baking goods...")
        self.bakery.bake("bread", {"flour": 2, "water": 1, "eggs": 1})
        self.bakery.bake("cake", {"flour": 1, "sugar": 2, "eggs": 2})

        # Simulate some sales
        print("\nProcessing sales...")
        self.sales.sell("bread")
        self.sales.sell("cake")

        # Display current inventory
        print("\nCurrent Inventory Status:")
        print(f"Raw materials: {self.inventory.raw_materials}")
        print(f"Baked goods: {self.inventory.baked_goods}")

def main():
    bakery_system = BakeryOrchestrator()
    
    # Simulate iterations of the bakery process
    for i in range(200):  # Simulate 3 iterations (can be extended)
        print(f"\n--- Iteration {i+1} ---")
        bakery_system.run_iteration()
        time.sleep(1)  # Simulate time passing between iterations

if __name__ == "__main__":
    main()
