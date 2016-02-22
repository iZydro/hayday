from model import *


class Item:

    items = None

    def __init__(self):

        self.items = {}

    def add(self, name, pb, data=None):

        self.items[name] = {"Mill": pb, "data": data}

    def show(self):

        for item in self.items:
            pb = "(primary)"
            if "data" in self.items[item] and self.items[item]["data"]:
                if "ProcessingBuilding" in self.items[item]["data"]:
                    pb = self.items[item]["data"]["ProcessingBuilding"]
            print(item + " => " + self.items[item]["Mill"] + " => " + pb)

    def search(self, search_item, generators):

        primary_buildings = {
            "Fishing", "Vegetables", "Trees", "Animals", "AnimalProducts", "Fruits", "Mills"
        }

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
