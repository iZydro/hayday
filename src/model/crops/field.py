from model.main import *


class FieldManager:

    items = None
    database = None

    def __init__(self, database_ref: Main):
        self.items = []
        self.database = database_ref
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

    def add(self, id, data=None):

        if id == "Cow" or id == "Chicken":
            data, name = self.database.items.search(id, self.database.generators)
            print(data)

        _item = Field(self, id, data)
        self.items.append(_item)
        return _item

    def find(self, name):
        for item in self.items:
            if item.id == name:
                return item
        pass

    def update(self, time):
        print("Update ts: " + self.nice_number(time))
        for item in self.items:
            item.update(time)

    def show(self, timestamp):
        print("==========Showing: " + self.nice_number(timestamp) + "=============")
        for item in self.items:
            item.show(timestamp)
        print("=====================================")

    def harvest(self, simulator):
        print("========== Harvesting =============")
        result = []
        for item in self.items:
            harvested = item.harvest()
            if harvested:
                result.append(harvested)
                simulator.storage.add(harvested)
        print("Harvested: " + str(result))
        print("===================================")


class Field:

    name = None
    data = None
    ts = None
    parent = None
    id = None
    status = "Empty"

    def __init__(self, parent_ref, id_ref, animal_data_ref=None):
        self.parent = parent_ref
        self.id = id_ref
        self.animal_data = animal_data_ref
        pass

    def info(self):
        print(self.animal_data)

    def find(self, crop_name):

        self.parent.database.items.search(crop_name)

        pass

    def plant(self, crop_name_ref, timestamp):

        crop_data, crop_name = self.parent.database.items.search(crop_name_ref, self.parent.database.generators)

        #print(crop_data, crop_name)
        if crop_data["Mill"] == self.id:
            #print("Valid")
            pass
        else:
            if crop_data["data"]["ProcessingBuilding"] == self.id:
                #print("Valid")
                pass
            else:
                return

        self.name = crop_name
        self.data = crop_data["data"]
        self.ts = int(timestamp)
        self.status = "Planted"
        pass

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
            if timestamp - self.ts > int(self.data["TimeMin"])*60*1000:
                self.status = "Ready"
