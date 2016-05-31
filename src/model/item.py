from model import *


class Item:

    items = None

    def __init__(self):

        self.items = {}

    def add(self, name, pb, data=None, unlock=None):

        if unlock == None:
            if "UnlockLevel" in data:
                unlock = data["UnlockLevel"]
            else:
                unlock = 0

        self.items[name] = {"Mill": pb, "data": data, "unlock": unlock}

    def show_one(self, item_name, item):
        pb = "(primary)"
        ul = str(item["unlock"])
        name = "noName"
        time = "noTime"
        if "data" in item and item["data"]:
            if "ProcessingBuilding" in item["data"]:
                pb = item["data"]["ProcessingBuilding"]
            #if "UnlockLevel" in item["data"]:
            #    ul = item["data"]["UnlockLevel"]
            if "Name" in item["data"]:
                name = item["data"]["Name"]
            if "TimeMin" in item["data"]:
                time = item["data"]["TimeMin"]
        print(str(name) + " => " + item["Mill"] + " => " + pb + " => Level: " + ul + " => Time: " + time)

    def iterate(self):
        for item in self.items:
            yield item, self.items[item]

    def show(self):

        for item in self.items:
            self.show_one(item, self.items[item])

        return

    def search(self, search_item, generators):

        primary_buildings = globalNames.all_type_products

        #print("Searching: " + str(search_item))
        for item in self.items:
            if item == search_item:

                # Get the building where the item is created
                building = self.items[item]["Mill"]
                #print("Found in building: " + building)

                if building in primary_buildings:
                    return generators[building].search(item)
                else:
                    caca
                    return generators["ProcessingBuildings"].search(item)

        return None
