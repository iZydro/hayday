from model.main import *
from model.crops.field import *
from model.crops.storage import *

class Simulator:

    main = None
    storage = None
    manager = None

    def __init__(self):
        self.main = Main()
        self.main.init_data()

    def harvest(self, item):
        harvested = item.harvest()
        if harvested:
            # Store item
            self.storage.add(harvested)

            # If vegetable, harvest two elements
            self.storage.add(harvested)

    def feed_animal(self, animal_ref, time):
        print("Feed Animal")

        animal = self.manager.get_free(animal_ref)
        food_needed = animal.food_needed()
        print("Food for animal: " + food_needed)

        food_found = self.storage.get_one(food_needed)
        print("Food found: " + food_found)

        self.storage.delete(food_found)

        good = animal.good_created()
        egg, egg_name = main.items.search(good, main.generators)

        print("Egg name: " + egg_name)

        animal.plant(egg_name, egg, time)

    def create_product(self, product_ref, timestamp):
        product, product_name = main.items.search(product_ref, main.generators)
        print(product_name, product)

        all_found = True
        for required in product["data"]["Requirements"]:
            num_required = int(product["data"]["Requirements"][required])
            print("Requires: " + required + " (" + str(num_required) + ")")
            if self.storage.find(required, num_required):
                # Found
                pass
            else:
                all_found = False

        if not all_found:
            print("Cannot create")
        else:
            print("Can create!")
            # Remove items from storage
            for required in product["data"]["Requirements"]:
                num_required = int(product["data"]["Requirements"][required])
                self.storage.delete(required)

            pb = product["data"]["ProcessingBuilding"]
            print("pb:" + pb)
            pb_ref = self.manager.find(pb)
            print("pbref:" + str(pb_ref))
            pb_ref.plant(product_name, product, timestamp)


if __name__ == "__main__":

    simulator = Simulator()
    main = Main()
    main.init_data()

    simulator.manager = FieldManager(main)
    simulator.storage = Storage(main)

    print("Fielding")

    time = 0

    carrot, carrot_name = main.items.search("Carrot", main.generators)
    wheat, wheat_name = main.items.search("Wheat", main.generators)
    indigo, indigo_name = main.items.search("Corn", main.generators)

    cow, cow_name = main.items.search("Cow", main.generators)
    chicken, chicken_name = main.items.search("Chicken", main.generators)

    milk, milk_name = main.items.search("Milk", main.generators)
    egg, egg_name = main.items.search("Egg", main.generators)

    simulator.storage.add("Corn")
    simulator.storage.add("Wheat")
    simulator.storage.add("Wheat")
    simulator.storage.add("Wheat")

    simulator.storage.add("Chicken Food")
    simulator.storage.add("Cow Food")

    simulator.manager.add("Hammermill")

    simulator.manager.add("Vegetables")
    simulator.manager.add("Vegetables")
    simulator.manager.add("Vegetables")

    simulator.manager.get_free("Vegetables").plant(wheat_name, wheat, time)
    simulator.manager.get_free("Vegetables").plant(carrot_name, carrot, time)
    simulator.manager.get_free("Vegetables").plant(indigo_name, indigo, time)

    simulator.manager.add("Cow", cow)
    simulator.manager.add("Chicken", chicken)

    simulator.create_product("Chicken Food", time)
    simulator.manager.show(time)
    simulator.storage.list()

    simulator.feed_animal("Chicken", time)
    simulator.feed_animal("Cow", time)
    simulator.manager.show(time)
    simulator.storage.list()

    time += 1000*5*60
    simulator.manager.update(time)
    simulator.manager.show(time)
    simulator.storage.list()

    simulator.manager.harvest(simulator)

    time += 1000*7*60
    simulator.manager.update(time)

    simulator.manager.show(time)
    simulator.storage.list()

    simulator.manager.harvest(simulator)

    simulator.manager.show(time)
    simulator.storage.list()

    time += 1000*50*60
    simulator.manager.update(time)
    simulator.manager.show(time)
    simulator.storage.list()

    simulator.manager.harvest(simulator)

    simulator.create_product("Chicken Food", time)

    simulator.manager.show(time)
    simulator.storage.list()
