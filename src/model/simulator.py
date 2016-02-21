from model.main import *
from model.crops.field import *
from model.crops.storage import *

class Simulator:

    main = None
    storage = None

    def __init__(self):
        self.main = Main()
        self.main.init_data()

    def harvest(self, item):
        harvested = item.harvest()
        if harvested:
            # Store item
            self.storage.add(harvested)

            # If vegetable, harvest two elements
            if item.id == "Vegetables":
                self.storage.add(harvested)

    def feed_animal(self, animal):
        food_needed = manager.get_free(animal).food_needed()
        print("Food for animal: " + food_needed)
        manager.get_free(animal).plant(milk_name, milk, time)

if __name__ == "__main__":

    simulator = Simulator()
    main = Main()
    main.init_data()

    manager = FieldManager(main)
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

    simulator.storage.add("Chicken Food")

    manager.add("Hammermill")

    manager.add("Vegetables")
    manager.add("Vegetables")
    manager.add("Vegetables")

    manager.get_free("Vegetables").plant(wheat_name, wheat, time)
    manager.get_free("Vegetables").plant(carrot_name, carrot, time)
    manager.get_free("Vegetables").plant(indigo_name, indigo, time)

    manager.add("Cow", cow)
    manager.add("Chicken")

    manager.get_free("Cow").info()
    simulator.feed_animal("Cow")

    manager.get_free("Chicken").plant(egg_name, egg, time)

    manager.show(time)

    time += 1000*5*60
    manager.update(time)
    manager.show(time)

    for item in manager.items:
        simulator.harvest(item)
    simulator.storage.list()

    time += 1000*7*60
    manager.update(time)
    manager.show(time)

    for item in manager.items:
        simulator.harvest(item)

    manager.show(time)

    simulator.storage.list()

    time += 1000*10*60
    manager.update(time)
    manager.show(time)

    for item in manager.items:
        simulator.harvest(item)

    manager.show(time)

    simulator.storage.list()
