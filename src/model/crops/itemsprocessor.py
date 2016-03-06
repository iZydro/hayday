from model.database import *
from model.crops.storage import *


class ItemsProcessorManager:

    items = None
    database = None
    storage = None

    def __init__(self, database_ref: Database, storage_ref: Storage):
        self.items = []
        self.database = database_ref
        self.storage = storage_ref
        pass

    def nice_number(self, time_left):
        time_total_sec = int(time_left / 1000)
        time_min = int(time_total_sec / 60)
        time_sec = time_total_sec - time_min * 60
        return str(time_min) + " min, " + str(time_sec) + " sec"

    def get_free(self, id):
        for item in self.items:
            if item.id == id and item.name == None:
                return item
        return None

    def get_total(self, id):
        # Returns a list of all free slots of a given type
        frees = []
        for item in self.items:
            if item.id == id:
                frees.append(item)
        return frees

    def get_frees(self, id):
        # Returns a list of all free slots of a given type
        frees = []
        for item in self.items:
            if item.id == id and item.name == None:
                frees.append(item)
        return frees

    def add(self, id, data=None, animal=False, tree=False, simulator=None, ts=None):

        if animal:
            data, name = self.database.items.search(id, self.database.generators)

        if tree:
            data, name = self.database.items.search(id, self.database.generators)
            print(data)

        _item = ItemsProcessor(self, id, data)
        self.items.append(_item)

        # Trees autogrow fruit!
        if tree:
            self.initiate_tree(_item, data, ts)

        return _item

    def initiate_tree(self, _item, data, ts):
        fruit_name = "Invalid!"
        if "Tree" in data["data"]["Name"]:
            fruit_name = data["data"]["Name"].split("Tree")[0]
        if "Bush" in data["data"]["Name"]:
            fruit_name = data["data"]["Name"].split("Bush")[0]
            if fruit_name == "Blueberry":
                fruit_name = "Blackberry"
        if "BeeHive" in data["data"]["Name"]:
            fruit_name = "Honeycomb"
        _item.bear_fruit(fruit_name, ts)


    def find(self, name):
        for item in self.items:
            if item.id == name:
                return item
        return None

    def update(self, time, verbose):
        if verbose:
            print("Update ts: " + self.nice_number(time))
        for item in self.items:
            item.update(time)

    def show(self, timestamp):
        print("==========Showing: " + self.nice_number(timestamp) + "=============")
        for item in self.items:
            item.show(timestamp)
        print("=====================================")

    def harvest(self, simulator, verbose=True):
        if verbose:
            print("========== Harvesting =============")
        result = []
        experience = 0
        for item in self.items:
            harvested = item.harvest()
            if harvested:
                result.append(harvested)
                simulator.storage.add(harvested)

                crop_data, crop_name = self.database.items.search(harvested, self.database.generators)
                if crop_data["Mill"] == "Vegetables":
                    simulator.storage.add(harvested)
                if "ExpCollect" in crop_data["data"] or True:
                    experience += int(crop_data["data"]["ExpCollect"])
        if verbose:
            print("Harvested: " + str(result))
            print("===================================")
        return experience


class ItemsProcessor:

    name = None
    data = None
    ts = None
    parent = None
    id = None
    status = "Empty"

    def __init__(self, parent_ref : ItemsProcessorManager, id_ref, animal_data_ref=None):
        self.parent = parent_ref
        self.id = id_ref
        self.animal_data = animal_data_ref
        pass

    def info(self):
        print(self.animal_data)

    def find(self, crop_name):

        self.parent.database.items.search(crop_name, self.parent.database.generators)

        pass

    def plant(self, crop_name_ref, simulator, timestamp):

        crop_data, crop_name = self.parent.database.items.search(crop_name_ref, self.parent.database.generators)
        #print(crop_name, crop_data)

        requirements = []

        if crop_data["Mill"] == self.id:
            requirements.append(crop_name_ref)
        else:
            if crop_data["data"]["ProcessingBuilding"] == self.id:
                # If it is a Mill, check requirements
                requirements = []
                if "Requirements" in crop_data["data"]:
                    for req in crop_data["data"]["Requirements"]:
                        for num in range(int(crop_data["data"]["Requirements"][req])):
                            requirements.append(req)
                else:
                    #requirements.append("caca")
                    pass

        do_it = True
        #print(crop_data, crop_name, requirements)
        #print(requirements)

        # Create a copy of the requirements to check if all are in the storage
        requirements_copy = requirements.copy()

        if len(requirements):
            for item in self.parent.storage.items:
                for req in requirements_copy:
                    if item == req:
                        requirements_copy.remove(req)
                        break
        if len(requirements_copy) != 0:
            # Could not find all requirements
            #print("Could not find all requirements for", crop_name_ref, requirements, requirements_copy)
            do_it = False

        if do_it:
            if len(requirements):
                for req in requirements:
                    self.parent.storage.delete(req)

            self.name = crop_name
            self.data = crop_data["data"]
            self.ts = int(timestamp)
            self.status = "Planted"

            return True

        return False

    def bear_fruit(self, fruit, timestamp):
        self.status = "Bearing"
        self.name = fruit
        self.ts = timestamp
        self.data = self.animal_data["data"]

    def food_needed(self):
        #print(self.animal_data["data"])
        if "Feed" in self.animal_data["data"]:
            return self.animal_data["data"]["Feed"]
        return None

    def good_created(self):
        #print(self.animal_data["data"])
        if "Good" in self.animal_data["data"]:
            return self.animal_data["data"]["Good"]
        return None

    def harvest(self):
        name = self.name
        if self.status == "Ready":
            self.name = None
            self.data = None
            self.ts = None
            self.status = "Empty"
            #print("Harvested: " + name)
            return name
        else:
            #print("Cannot harvest " + str(name))
            return None

    def time_left(self, timestamp):
        if timestamp == None:
            return None
        if not self.name:
            return None

        if self.id == "Field" or self.id == "Cow" or True:
            time_left = int(self.data["TimeMin"])*60*1000 - (timestamp - self.ts)
            if time_left <= 0:
                return "Ready"
            else:
                return self.parent.nice_number(time_left)

    def show(self, timestamp=None):
        print(self.id, "creating", self.name, "with data", self.data, "Status:", self.status, "Time Left:", self.time_left(timestamp))

    def update(self, timestamp):
        if self.name:
            if timestamp - self.ts >= int(self.data["TimeMin"])*60*1000:
                self.status = "Ready"

