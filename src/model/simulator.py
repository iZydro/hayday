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

    def update_harvest_show_list(self, time, verbose=True):

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

        self.manager.update(time, verbose)
        exp = self.manager.harvest(self, verbose)
        self.experience += exp

        # Try to plant and feed eveything!
        self.plant_feed_animal(self, time)

        if verbose:
            self.storage.list()
            print("Level: " + str(self.level) + " - Experience: " + str(self.experience))

    def fill_crops(self, simulator, time):

        # Create a list of unlocked crops
        unlocked_crops = []
        planted_crops = {}
        for crop in self.database.fields.items:
            crop_data, crop_name = self.database.items.search(crop, self.database.generators)
            if int(crop_data["data"]["UnlockLevel"]) <= self.level:
                unlocked_crops.append(crop_name)
                planted_crops[crop_name] = 0

        total_fields = self.manager.get_total("Vegetables")
        crops_per_field = int(len(total_fields) / len(unlocked_crops))

        for field in total_fields:
            if field.name in unlocked_crops:
                planted_crops[field.name] += 1

        # Plant the fields until reaching the desired number of each crop
        for crop_name in unlocked_crops:
            crops_in_storage = self.storage.how_many(crop_name)

            # Only plant is there are few stored
            if crops_in_storage < 10:

                # Check how many crops of each class are planted
                crops_to_plant = crops_per_field - planted_crops[crop_name]
                for crop in range(0, crops_to_plant):
                    free = self.manager.get_free("Vegetables")
                    if free:
                        free.plant(crop_name, simulator, time)


    def rolling_plant(self, slot, crops, simulator, time):

        # Create sequence pointer for this slot if it does not exist
        if slot not in self.crops_cnt:
            self.crops_cnt[slot] = 0

        unlocked = False
        unlock_level = 0
        # Ensure that crops_cnt points to an unlocked recipe!
        while not unlocked:
            crop_name_ref = str(crops[simulator.crops_cnt[slot]])

            for item_name, item_data in self.database.items.iterate():
    #            print(item_name, item_data["Mill"], item_data["data"])
                if item_data["data"]["Name"] == crop_name_ref:
                    unlock_level = int(item_data["unlock"])
            if unlock_level <= int(self.level):
                unlocked = True
            else:
                self.crops_cnt[slot] += 1
                if self.crops_cnt[slot] >= len(crops):
                    self.crops_cnt[slot] = 0

        frees = self.manager.get_frees(slot)
        for free in frees:
            if free.plant(crops[self.crops_cnt[slot]], simulator, time):
                self.crops_cnt[slot] += 1
                if self.crops_cnt[slot] >= len(crops):
                    self.crops_cnt[slot] = 0
            else:
                #print("Could not plant:", crops[self.crops_cnt[slot]])
                pass

    def add_if_less_than_minimum(self, items_to_add):
        # Add an item from the listo to the storage if there are less than 10 items in the storage
        # That would simulate ores, fishes, etc
        for item_to_add in items_to_add:
            if self.storage.how_many(item_to_add) < 10:
                self.storage.add(item_to_add)

    def plant_feed_animal(self, simulator, time):

        # Check if we run out of crops and add one for free if needed
        for crop in self.database.fields.items:
            found = False
            if self.storage.find(crop):
                found = True
            veggies = self.manager.get_total("Vegetables")
            for veggie in veggies:
                if veggie.name == crop:
                    found = True
                    break

            if not found:
                self.storage.add(crop)

        # Add fishes and ores for free...
        self.add_if_less_than_minimum(["Fish Meat", "Lobster Meat", "Duck Down", "SilverOre", "GoldOre", "PlatinumOre", "CoalOre", "IronOre"])

        '''
        self.storage.add("Fish Meat")
        self.storage.add("Lobster Meat")
        self.storage.add("Duck Down")

        self.storage.add("SilverOre")
        self.storage.add("GoldOre")
        self.storage.add("PlatinumOre")
        self.storage.add("CoalOre")
        self.storage.add("IronOre")
'''
        #for item_name, item_data in simulator.database.items.iterate():
        #    if int(item_data["unlock"]) <= simulator.level:
        #        #print(item_name)
        #        pass

        # Plant basic crops
        self.fill_crops(simulator, time)
        #self.rolling_plant("Vegetables", ["Wheat", "Corn", "Soybean", "Sugarcane", "Carrot", "Pumpkin", "Potato"], simulator, time)

        # Create crafted items in available mills

        for pb in self.list_of_unlocked_buildings["CraftedProducts"]:
            recipes = []
            for recipe in self.list_of_unlocked_buildings["CraftedProducts"][pb]:
                for key in recipe:
                    # Append to list only if it has been unlocked!
                    recipe_data, recipe_name = self.database.processing_buildings.search(key)
                    if "UnlockLevel" not in recipe_data["data"] or int(recipe_data["data"]["UnlockLevel"]) <= self.level:
                        recipes.append(key)
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

        frees = self.manager.get_frees("Sheep")
        for free in frees:
            #print(free.show())
            self.feed_animal("Sheep", time)

        frees = self.manager.get_frees("Goat")
        for free in frees:
            #print(free.show())
            self.feed_animal("Goat", time)

        # Revive trees
        for tree in self.database.fruit_trees.items:
            for tree_element in self.manager.get_frees(tree):
                self.manager.initiate_tree(tree_element, tree_element.animal_data, time)



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

    database.fishes.show()

    exit(1)

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

    for counter in range(1, 15):
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
