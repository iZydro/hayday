from model.database import *
from model.crops.itemsprocessor import *
from model.crops.storage import *
import json


class Simulator:

    database = None
    storage = None
    manager = None
    experience = None

    crops_cnt = None

    list_of_unlocked_buildings = None

    def __init__(self):
        self.database = Database()
        self.database.init_data()
        self.experience = 0
        self.crops_cnt = {}

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

        if not food_found:
            return None
        #print("Food found: " + food_found)

        self.storage.delete(food_found)

        good = animal.good_created()
        #print("Good name: " + good)
        animal.plant(good, self, time)

    def create_product(self, product_ref, timestamp):
        product, product_name = database.items.search(product_ref, database.generators)
        #print(product_name, product)

        all_found = True
        for required in product["data"]["Requirements"]:
            num_required = int(product["data"]["Requirements"][required])
            #print("Requires: " + required + " (" + str(num_required) + ")")
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

        # First, add all new items to the manager

        self.level = int(self.database.get_level(self.experience))
        self.list_of_unlocked_buildings, total_recipes = self.get_all_products(self.level)

        # Add new buildings if they do not exist
        for pb in self.list_of_unlocked_buildings["CraftedProducts"]:
            if self.manager.find(pb):
                # Ya existe
                pass
            else:
                #print("Adding: " + pb)
                self.manager.add(pb)

        self.manager.update(time)
        exp = self.manager.harvest(self)
        self.experience += exp
        self.plant_feed_animal(self, time)
        exp = self.manager.harvest(self)
        self.experience += exp
        #self.manager.show(time)
        self.storage.list()
        print("Level: " + str(self.level) + " - Experience: " + str(self.experience))

    def rolling_plant(self, slot, crops, simulator, time):

        # Create sequence pointer for this slot if it does not exist
        if slot not in self.crops_cnt:
            self.crops_cnt[slot] = 0

        frees = self.manager.get_frees(slot)
        for free in frees:
            #print("Try plant", str(crops[simulator.crops_cnt[slot]]))
            if free.plant(crops[self.crops_cnt[slot]], simulator, time):
                #print("Planted", str(crops[simulator.crops_cnt[slot]]))
                self.crops_cnt[slot] += 1
                if self.crops_cnt[slot] >= len(crops):
                    self.crops_cnt[slot] = 0

    def plant_feed_animal(self, simulator, time):

        #for item_name, item_data in simulator.database.items.iterate():
        #    if int(item_data["unlock"]) <= simulator.level:
        #        #print(item_name)
        #        pass

        self.rolling_plant("Vegetables", ["Wheat", "Corn", "Soybean", "Sugarcane", "Carrot"], simulator, time)

        # Create crafted items in available mills

        for pb in self.list_of_unlocked_buildings["CraftedProducts"]:
            recipes = []
            for recipe in self.list_of_unlocked_buildings["CraftedProducts"][pb]:
                for key in recipe:
                    recipes.append(key)
            #print("Rolling plant", pb, recipes)
            self.rolling_plant(pb, recipes, simulator, time)

        #self.rolling_plant("Hammermill", ["Chicken Food", "Cow Food"], simulator)
        #self.rolling_plant("Bakery", ["Bread", "Corn Bread"], simulator)

        frees = self.manager.get_frees("Cow")
        for free in frees:
            self.feed_animal("Cow", time)

        frees = self.manager.get_frees("Chicken")
        for free in frees:
            self.feed_animal("Chicken", time)

        frees = self.manager.get_frees("Pig")
        for free in frees:
            #print(free.show())
            self.feed_animal("Pig", time)

    def get_all_products(self, level):
        recipes = 0
        mills = {}
        for item_name, item_data in self.database.items.iterate():
            if int(item_data["unlock"]) <= level:

                mill = item_data["Mill"]
                if mill not in mills:
                    mills[mill] = {}
                if "ProcessingBuilding" in item_data["data"]:
                    pb = item_data["data"]["ProcessingBuilding"]
                else:
                    pb = mill # "(primary)"
                if pb not in mills[mill]:
                    mills[mill][pb] = [] # 0
                time = "0"
                if "TimeMin" in item_data["data"]:
                    time = item_data["data"]["TimeMin"]
                mills[mill][pb].append({item_name: time}) # += 1

                #simulator.database.items.show_one(item_name, item_data)
                recipes += 1

        return mills, recipes

if __name__ == "__main__":

    simulator = Simulator()
    database = Database()
    database.init_data()

    simulator.storage = Storage(database)
    simulator.manager = ItemsProcessorManager(database, simulator.storage)
    #simulator.crops_cnt = {}

    #database.fruits.show()
    #database.fruit_trees.show()
    #exit(1)

#    mills, total_recipes = simulator.get_all_products(28)
#    print("Total recipes: " + str(total_recipes))
#    print(json.dumps(mills, indent=4))

#    for mill in mills:
#        print(mill, len(mills[mill]))
#        items = ""
#        for item in mills[mill]:
#            items += " - " + item + "(" + str(len(mills[mill][item])) + ")"
#        print(items)

    #req, item = database.items.search("Sweater", database.generators)
    #print(item, req)


    print("Fielding")

    time = 0

    simulator.storage.add("Corn")
    simulator.storage.add("Corn")
    simulator.storage.add("Corn")
    simulator.storage.add("Wheat")
    simulator.storage.add("Wheat")
    simulator.storage.add("Wheat")
    simulator.storage.add("Soybean")
    simulator.storage.add("Soybean")
    simulator.storage.add("Soybean")
    simulator.storage.add("Sugarcane")
    simulator.storage.add("Sugarcane")
    simulator.storage.add("Sugarcane")
    simulator.storage.add("Carrot")
    simulator.storage.add("Carrot")
    simulator.storage.add("Carrot")

    #simulator.storage.add("Chicken Food")
    #simulator.storage.add("Cow Food")

    simulator.manager.add("Hammermill")
    simulator.manager.add("Hammermill")
    simulator.manager.add("Hammermill")
    simulator.manager.add("Hammermill")
    simulator.manager.add("Hammermill")
    simulator.manager.add("Hammermill")

    #simulator.manager.add("Bakery")

    for counter in range(1, 32):
        simulator.manager.add("Vegetables")

    for counter in range(1, 10):
        simulator.manager.add("Cow", animal=True)
    for counter in range(1, 15):
        simulator.manager.add("Chicken", animal=True)
    for counter in range(1, 10):
        simulator.manager.add("Pig", animal=True)

    for iterations in range(1, 500):
        time += 1000*10*60
        simulator.update_harvest_show_list(time)

    #for item in database.items.items:
    #    print(database.items.items[item])

    exit(1)

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

    time += 1000*62*60
    simulator.update_harvest_show_list(time)
    time += 1000*62*60
    simulator.update_harvest_show_list(time)
    time += 1000*62*60
    simulator.update_harvest_show_list(time)
    time += 1000*62*60
    simulator.update_harvest_show_list(time)
    time += 1000*62*60
    simulator.update_harvest_show_list(time)
    time += 1000*62*60
    simulator.update_harvest_show_list(time)
    time += 1000*62*60
    simulator.update_harvest_show_list(time)

    for iterations in range(1, 100):
        time += 1000*12*60
        simulator.update_harvest_show_list(time)
