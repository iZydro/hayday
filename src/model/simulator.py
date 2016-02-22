from model.main import *
from model.crops.field import *
from model.crops.storage import *


class Simulator:

    database = None
    storage = None
    manager = None
    experience = None

    def __init__(self):
        self.database = Main()
        self.database.init_data()
        self.experience = 0

    def harvest(self, item):
        harvested = item.harvest()
        if harvested:
            # Store item
            self.storage.add(harvested)

            # If vegetable, harvest two elements
            self.storage.add(harvested)

    def feed_animal(self, animal_ref, time):
        #print("Feed Animal")

        animal = self.manager.get_free(animal_ref)
        food_needed = animal.food_needed()
        #print("Food for animal: " + food_needed)

        food_found = self.storage.get_one(food_needed)
        #print("Food found: " + food_found)

        self.storage.delete(food_found)

        good = animal.good_created()
        #print("Good name: " + good)
        animal.plant(good, time)

    def create_product(self, product_ref, timestamp):
        product, product_name = database.items.search(product_ref, database.generators)
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
            #print("Cannot create")
            pass
        else:
            #print("Can create!")
            # Remove items from storage
            for required in product["data"]["Requirements"]:
                num_required = int(product["data"]["Requirements"][required])
                self.storage.delete(required)

            pb = product["data"]["ProcessingBuilding"]
            #print("pb:" + pb)
            pb_ref = self.manager.find(pb)
            #print("pbref:" + str(pb_ref))
            pb_ref.plant(product_name, timestamp)

    def update_harvest_show_list(self, time):
        self.manager.update(time)
        exp = self.manager.harvest(simulator)
        self.experience += exp
        self.plant_feed_animal(time)
        self.manager.show(time)
        self.storage.list()
        print("Experience: " + str(self.experience))

    def plant_feed_animal(self, time):
        crops = [ "Wheat", "Corn" ]
        crop_cnt = 0
        free = simulator.manager.get_free("Vegetables")
        while free:
            free.plant(crops[crop_cnt], time)
            crop_cnt += 1
            if crop_cnt >= len(crops):
                crop_cnt = 0
            free = simulator.manager.get_free("Vegetables")

        free = simulator.manager.get_free("Hammermill")
        while free:
            free.plant("Chicken Food", time)
            free = simulator.manager.get_free("Hammermill")

if __name__ == "__main__":

    simulator = Simulator()
    database = Main()
    database.init_data()

    simulator.manager = FieldManager(database)
    simulator.storage = Storage(database)

    print("Fielding")

    time = 0

    simulator.storage.add("Corn")
    simulator.storage.add("Wheat")
    simulator.storage.add("Wheat")
    simulator.storage.add("Wheat")

    simulator.storage.add("Chicken Food")
    simulator.storage.add("Cow Food")

    simulator.manager.add("Hammermill")
    simulator.manager.add("Bakery")

    for counter in range(1, 10):
        simulator.manager.add("Vegetables")

    simulator.manager.get_free("Vegetables").plant("Wheat", time)
    simulator.manager.get_free("Vegetables").plant("Wheat", time)
    simulator.manager.get_free("Vegetables").plant("Wheat", time)
    simulator.manager.get_free("Vegetables").plant("Corn", time)
    simulator.manager.get_free("Vegetables").plant("Corn", time)
    simulator.manager.get_free("Vegetables").plant("Corn", time)

    simulator.manager.add("Cow")
    simulator.manager.add("Chicken")

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
    simulator.manager.get_free("Vegetables").plant("Wheat", time)
    simulator.update_harvest_show_list(time)

    simulator.manager.show(time)
    simulator.storage.list()

    time += 1000*50*60
    simulator.update_harvest_show_list(time)

    simulator.create_product("Chicken Food", time)
    simulator.create_product("Bread", time)

    simulator.manager.show(time)
    simulator.storage.list()

    time += 1000*50*60
    simulator.update_harvest_show_list(time)

    time += 1000*5*60
    simulator.update_harvest_show_list(time)
    time += 1000*5*60
    simulator.update_harvest_show_list(time)
    time += 1000*5*60
    simulator.update_harvest_show_list(time)
