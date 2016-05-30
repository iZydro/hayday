from model import *
#from model.processing_building import *
from model.item import *
import json


class Base:

    valid_items = ["Name", "UnlockLevel", "TimeMin", "TimeSec", "FruitCount", "IsFruit", "Price", "ProcessingBuilding",
                   "Good", "Feed", "ExpCollect"]
    level_items = ["Level", "ExpToNextLevel", "MaxFields",
                   "MaxChickenHabitats", "MaxCowHabitats", "MaxSheepHabitats", "MaxPigHabitats", "MaxGoatHabitats"]

    generators = None

    def __init__(self):
        self.generators = {}
        self.items = {}

    def read(self, base_name, names=valid_items):

        name = base_name + ".csv.txt"

        with open(globalNames.folder + name, "r") as infile:
            data = infile.read()

        data = data.replace('"', '')

        #print(data)

        lines = data.splitlines()
        num_lines = len(lines)

        fields = {}
        headers = lines[0].split(",")
        hcnt = 0
        for header in headers:
            fields[header] = hcnt
            hcnt += 1

#        for field in fields:
#            print(field, fields[field])

        current_line = 2 # Skip headers

        current_item = None
        while current_line < num_lines:
            line = lines[current_line]

            #print(line)

            words = line.split(",")
            id_product = words[fields[names[0]]]
            if id_product != "":
                # New item
                self.items[words[fields[names[0]]]] = {}
                current_item = self.items[words[fields[names[0]]]]

                for field in fields:
                    if field in names:
                        if words[fields[field]] != "":
                            current_item[field] = words[fields[field]]

                #current_item["items"] = {}

            if "Requirement" in fields:
                if "Requirements" not in current_item:
                    current_item["Requirements"] = {}
                current_item["Requirements"][words[fields["Requirement"]]] = words[fields["RequirementAmount"]]

            current_line += 1

        #print(json.dumps(self.items, indent=4))

    def _search(self, item):

        for building in self.items:
            print(building)

        return None

    def add(self, item):
        self.items[item] = {}

    def recursive_search(self, product, generators, items):

        print("================Recursively searching onto these requirements : " + str(product))

        for required in product["data"]["Requirements"]:
            print(required + " is required")

            required_data = items.search(required, generators)
            print("Required data: " + str(required_data))
            if required_data and "Requirements" in required_data:
                self.recursive_search(required_data, generators, items)
            else:
                if required_data and "ProcessingBuilding" in required_data:
                    print("*************Found primary: " + required + " from " + required_data["ProcessingBuilding"])
                else:
                    print("*************Found primary: " + required + " - data: " + str(required_data))

